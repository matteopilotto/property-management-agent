"""Action gateway: agency policy checked in code on every action (spec §7, ADR 0002)."""

import json
import logging
import re
from dataclasses import dataclass
from typing import Literal

from pypdf import PdfReader
from pypdf.errors import PyPdfError

from .case import CaseView
from .ledger import Ledger

log = logging.getLogger(__name__)

GatewayMode = Literal["enforce", "observe"]

APPROVAL = re.compile(r"(?i)\b(approv\w*|go ahead|proceed|happy for|authori[sz]\w*)\b")
POSTCODE = re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b")
AMOUNT = re.compile(r"\d[\d,]*(?:\.\d+)?")
EVENT_NUMBER = re.compile(r"(?i)^\s*(?:event\s*)?#?\s*(\d+)\s*$")
HAZARD = re.compile(
    r"(?i)\b("
    r"gas|carbon monoxide|spark\w*|shock\w*|exposed wir\w*|"
    r"water (?:near|in|into|on|behind|over) (?:the )?(?:electric\w*|socket\w*|fuse\w*|"
    r"light\w*|wiring|switch\w*)|"
    r"(?:broken|shatter\w*|smashed) (?:glass|window\w*|pane\w*)|"
    r"glass (?:is )?(?:broken|shatter\w*|smashed)|"
    r"flood\w*|ceiling (?:has )?collaps\w*|collaps\w* ceiling|"
    r"no heating|no hot water|(?:smoke|co|carbon monoxide) alarm\w*|fire"
    r")\b"
)
RECORDED = ("approved", "held")


@dataclass
class Verdict:
    status: Literal["approved", "held", "blocked", "duplicate"]
    rule: str | None = None
    reason: str | None = None
    how_to_fix: str | None = None


APPROVED = Verdict("approved")


class ActionGateway:
    """Approves, holds, blocks or drops each action and writes it to the ledger."""

    def __init__(
        self, case_view: CaseView, ledger: Ledger, mode: GatewayMode = "enforce"
    ):
        self.case_view = case_view
        self.ledger = ledger
        self.mode = mode
        self._events = {e.number: e for e in case_view.events}
        postcodes = POSTCODE.findall(case_view.details.get("Property", ""))
        self._postcode = _postcode(postcodes[-1]) if postcodes else None
        self._recorded: set[str] = set()
        self._pdf_text: dict[str, str] = {}

    def review(self, tool: str, args: dict) -> dict:
        """Judge one action, record it, and return what the agent sees as the result."""
        verdict = self._judge(tool, args)
        status = "approved" if self.mode == "observe" else verdict.status
        self.ledger.append(
            tool=tool,
            args=args,
            status=status,
            would_status=verdict.status,
            rule=verdict.rule,
            reason=verdict.reason,
            mode=self.mode,
        )
        return tool_result(status, verdict)

    def _judge(self, tool: str, args: dict) -> Verdict:
        key = json.dumps([tool, _normalise(args)], sort_keys=True, default=str)
        if key in self._recorded:
            return Verdict("duplicate", "R6", "The same action is already recorded.")
        rule = {
            "book_contractor": self._approval_before_spend,
            "charge_tenant": self._tenant_charge,
            "approve_invoice": self._invoice_within_quote,
            "send_message": self._right_property,
            "submit_decision": self._no_waiting_on_hazards,
        }.get(tool)
        verdict = rule(args) if rule else APPROVED
        if verdict.status in RECORDED:
            self._recorded.add(key)
        return verdict

    def _approval_before_spend(self, args: dict) -> Verdict:
        cited = args.get("approval_event")
        match = EVENT_NUMBER.match(str(cited))
        event = self._events.get(int(match.group(1))) if match else None
        if event and (
            "landlord" in event.sender.lower() or APPROVAL.search(event.body)
        ):
            return APPROVED
        return Verdict(
            "held",
            "R1",
            f"approval_event {cited!r} is not a visible event from the Landlord or "
            "one that records approval to proceed.",
        )

    def _tenant_charge(self, args: dict) -> Verdict:
        return Verdict("held", "R2", "Charges to the Tenant always need approval.")

    def _invoice_within_quote(self, args: dict) -> Verdict:
        amounts = {}
        for label, amount_key, evidence_key in (
            ("quote", "approved_quote_gbp", "quote_evidence"),
            ("invoice", "invoice_amount_gbp", "invoice_evidence"),
        ):
            amount = _amount(args.get(amount_key))
            evidence = args.get(evidence_key)
            text = self._evidence_text(evidence)
            if amount is None or text is None or not _mentions(text, amount):
                return Verdict(
                    "held",
                    "R3",
                    f"The {label} amount {args.get(amount_key)!r} was not found in "
                    f"the cited evidence {evidence!r}.",
                )
            amounts[label] = amount
        if amounts["invoice"] > amounts["quote"] + 0.005:
            return Verdict(
                "held",
                "R3",
                f"Invoice £{amounts['invoice']:.2f} exceeds the approved quote "
                f"£{amounts['quote']:.2f}.",
            )
        return APPROVED

    def _right_property(self, args: dict) -> Verdict:
        if not self._postcode:
            log.warning(
                "R4 inactive for case %s: no known property", self.case_view.case_id
            )
            return Verdict("approved", None, "R4 inactive: no known property postcode.")
        text = f"{args.get('subject', '')}\n{args.get('body', '')}"
        named = {_postcode(p) for p in POSTCODE.findall(text)}
        property_ = self.case_view.details["Property"]
        others = sorted(named - {self._postcode})
        if others:
            return Verdict(
                "blocked",
                "R4",
                f"The message names postcode(s) {', '.join(others)}, but the case "
                f"property is {property_}.",
                f"Remove the other addresses and refer only to {property_}.",
            )
        if args.get("to") in ("landlord", "contractor") and self._postcode not in named:
            return Verdict(
                "blocked",
                "R4",
                "Messages to the Landlord or Contractor must name the case property.",
                f"Include the property address {property_} in the message.",
            )
        return APPROVED

    def _no_waiting_on_hazards(self, args: dict) -> Verdict:
        if args.get("next_move") != "wait":
            return APPROVED
        sources = [("initial request", self.case_view.initial_request)] + [
            (f"event {e.number}", e.body) for e in self.case_view.events
        ]
        hits = [
            f"{name} ({', '.join(sorted({m.lower() for m in HAZARD.findall(text)}))})"
            for name, text in sources
            if HAZARD.search(text)
        ]
        if not hits:
            return APPROVED
        return Verdict(
            "blocked",
            "R5",
            f"Possible safety hazard in {'; '.join(hits)}.",
            "Do not wait on a possible hazard: act, ask or escalate instead.",
        )

    def _evidence_text(self, evidence) -> str | None:
        name = str(evidence).strip()
        if name in self.case_view.attachments:
            if name not in self._pdf_text:
                self._pdf_text[name] = pdf_text(
                    self.case_view.path / "attachments" / name
                )
            return self._pdf_text[name]
        match = EVENT_NUMBER.match(name)
        event = self._events.get(int(match.group(1))) if match else None
        return event.body if event else None


def tool_result(status: str, verdict: Verdict) -> dict:
    if status == "approved":
        return {"status": "recorded"}
    if status == "held":
        return {"status": "held_for_property_manager", "reason": verdict.reason}
    if status == "blocked":
        return {
            "status": "blocked",
            "reason": verdict.reason,
            "how_to_fix": verdict.how_to_fix,
        }
    return {"status": "duplicate"}


def pdf_text(path) -> str:
    try:
        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    except (PyPdfError, OSError, ValueError):
        return ""


def _postcode(text: str) -> str:
    return text.replace(" ", "").upper()


def _amount(value) -> float | None:
    try:
        return float(str(value).replace("£", "").replace(",", "").strip())
    except ValueError:
        return None


def _mentions(text: str, amount: float) -> bool:
    return any(
        abs(float(n.replace(",", "")) - amount) < 0.005 for n in AMOUNT.findall(text)
    )


def _normalise(value):
    if isinstance(value, str):
        return " ".join(value.lower().split())
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, dict):
        return {k: _normalise(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalise(v) for v in value]
    return value
