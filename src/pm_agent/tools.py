"""Agent tools. Read tools run normally; action tools and submit_decision never run
their bodies: before_tool_callback answers every gated call with the action
gateway's result (ADR 0002)."""

import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from pydantic import BaseModel
from pypdf import PdfReader
from pypdf.errors import PyPdfError

from .case import CaseView, Event
from .gateway import ActionGateway

MAX_TOOL_CALLS = 30
NATIVE_MEDIA = {"application/pdf", "image/png", "image/jpeg", "image/gif", "image/webp"}


class ToolCallLimitExceeded(RuntimeError):
    pass


@dataclass
class CaseRun:
    """Everything one case's tools need, keyed by the ADK session that runs it."""

    case_view: CaseView
    gateway: ActionGateway
    tool_calls: int = 0


CASE_RUNS: dict[str, CaseRun] = {}


def case_run(tool_context: ToolContext) -> CaseRun:
    return CASE_RUNS[tool_context.session.id]


def before_tool_callback(tool: BaseTool, args: dict, tool_context: ToolContext):
    """Enforce the tool-call limit and send every gated call through the gateway."""
    run = case_run(tool_context)
    run.tool_calls += 1
    if run.tool_calls > MAX_TOOL_CALLS:
        run.gateway.ledger.append(
            tool=tool.name,
            args=args,
            status="blocked",
            would_status="blocked",
            rule="LIMIT",
            reason=f"More than {MAX_TOOL_CALLS} tool calls.",
            mode=run.gateway.mode,
        )
        raise ToolCallLimitExceeded(f"more than {MAX_TOOL_CALLS} tool calls")
    if tool.name not in GATED:
        return None
    result = run.gateway.review(tool.name, args)
    if tool.name == "submit_decision" and result["status"] == "recorded":
        tool_context.actions.skip_summarization = True
    return result


# Read tools


def get_case_overview(tool_context: ToolContext) -> dict:
    """Case details, initial request, the question asked (if any), how many events
    are visible, and the attachments and files you may read. Call this first."""
    view = case_run(tool_context).case_view
    overview = {
        "case_id": view.case_id,
        "details": view.details,
        "initial_request": view.initial_request,
        "question": view.question,
        "event_count": len(view.events),
        "attachments": view.attachments,
        "other_sections": view.sections,
    }
    if view.raw:
        overview["files"] = view.files
        overview["note"] = (
            "This case is not in the usual layout. Use list_files and read_file."
        )
    return overview


def get_events(first: int, last: int, tool_context: ToolContext) -> dict:
    """Events numbered first..last inclusive (numbers start at 1)."""
    view = case_run(tool_context).case_view
    return {"events": [_event(e) for e in view.events if first <= e.number <= last]}


def search_events(text: str, tool_context: ToolContext) -> dict:
    """Events whose body, sender or recipient contains the text (case-insensitive)."""
    view = case_run(tool_context).case_view
    needle = text.lower()
    return {
        "events": [
            _event(e)
            for e in view.events
            if needle in f"{e.body}\n{e.sender}\n{e.recipient}".lower()
        ]
    }


def read_attachment(name: str, tool_context: ToolContext) -> dict:
    """Read one attachment listed in the case overview, e.g. an invoice PDF."""
    view = case_run(tool_context).case_view
    if name not in view.attachments:
        return {"error": f"No attachment {name!r}. Available: {view.attachments}"}
    return _read(view.path / "attachments" / name)


def list_files(tool_context: ToolContext) -> dict:
    """Every file in a case folder that is not in the usual layout."""
    return {"files": case_run(tool_context).case_view.files}


def read_file(name: str, tool_context: ToolContext) -> dict:
    """Read one file returned by list_files."""
    view = case_run(tool_context).case_view
    if name not in view.files:
        return {"error": f"No file {name!r}. Available: {view.files}"}
    return _read(view.path / name)


def _event(event: Event) -> dict:
    return {
        "number": event.number,
        "timestamp": event.timestamp,
        "channel": event.channel,
        "from": event.sender,
        "to": event.recipient,
        "body": event.body,
        "attachments": event.attachment_files,
    }


def _read(path: Path) -> dict:
    """PDFs and images go to Claude natively; anything else is read as text."""
    mime_type = mimetypes.guess_type(path.name)[0]
    if mime_type not in NATIVE_MEDIA:
        return {"name": path.name, "text": path.read_text(errors="replace")}
    if mime_type == "application/pdf":
        try:
            PdfReader(path).pages[0]
        except (PyPdfError, OSError, ValueError, IndexError):
            return {"name": path.name, "error": "The PDF is unreadable or empty."}
    return {
        "name": path.name,
        "document": types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type),
    }


# Action tools (answered by the gateway)


def send_message(
    to: Literal["tenant", "landlord", "contractor"],
    subject: str,
    body: str,
    purpose: Literal["request", "instruct", "update"],
) -> dict:
    """Draft a message to one party. purpose: request = ask for information, a quote
    or a decision, including chasing and asking a contractor for a quote, a date or
    progress on a job it already has; instruct = commit a contractor to attend or do
    work the landlord has approved, or forward an invoice to the landlord for
    payment; update = inform only. Messages to the landlord or contractor must
    include the case property address with its postcode."""


def book_contractor(
    contractor: str,
    work: str,
    slot: str,
    approved_amount_gbp: float,
    approval_event: int,
) -> dict:
    """Book a contractor. approval_event is the visible event number that records
    the landlord's approval to spend."""


def approve_invoice(
    contractor: str,
    invoice_amount_gbp: float,
    approved_quote_gbp: float,
    quote_evidence: str,
    invoice_evidence: str,
) -> dict:
    """Approve a contractor's invoice for payment. Each evidence is an event number
    or attachment file name in which that exact amount appears."""


def charge_tenant(amount_gbp: float, reason: str, evidence: str) -> dict:
    """Propose charging the tenant. Always held for property manager approval."""


def schedule_followup(due_date: str, reason: str) -> dict:
    """Schedule a dated follow-up (YYYY-MM-DD) with the reason for waiting."""


def close_case(reason: str) -> dict:
    """Close the case after the final checks."""


class HandoverNote(BaseModel):
    known: str
    conflicts: str
    done: str
    needed: str


def escalate(reason: str, handover_note: HandoverNote) -> dict:
    """Hand the case to the property manager. The handover note says what is known,
    what conflicts, what was done and what decision or action is needed."""


def submit_decision(
    next_move: Literal["act", "ask", "wait", "escalate"],
    summary: str,
    answer_to_question: str | None,
    facts: list[str],
    conflicts: list[str],
    missing: list[str],
    options_rejected: list[str],
    uncertainty: str,
) -> dict:
    """Submit the next move, exactly once, after recording its actions. Facts cite
    event numbers or attachment names. answer_to_question answers the case's
    question if it has one, otherwise null."""


READ_TOOLS = [
    get_case_overview,
    get_events,
    search_events,
    read_attachment,
    list_files,
    read_file,
]
GATED_TOOLS = [
    send_message,
    book_contractor,
    approve_invoice,
    charge_tenant,
    schedule_followup,
    close_case,
    escalate,
    submit_decision,
]
GATED = {f.__name__ for f in GATED_TOOLS}
