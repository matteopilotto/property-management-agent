import asyncio
import uuid
from pathlib import Path

import pytest
from google.adk.agents import LlmAgent
from google.adk.models.anthropic_llm import AnthropicLlm
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import Field

from pm_agent.agent import MODEL, root_agent
from pm_agent.case import load_case, view
from pm_agent.gateway import ActionGateway
from pm_agent.ledger import Ledger
from pm_agent.tools import (
    CASE_RUNS,
    MAX_TOOL_CALLS,
    CaseRun,
    ToolCallLimitExceeded,
    before_tool_callback,
    read_attachment,
)

CASES = (
    Path(__file__).resolve().parents[1] / "HackatonPublicCases" / "Property Management"
)
REASONING = {
    "facts": ["Event 31 attaches an invoice for £240.00."],
    "conflicts": [],
    "missing": [],
    "options_rejected": [],
    "uncertainty": "",
}


class ScriptedLlm(BaseLlm):
    """Plays back one list of function calls per model turn and keeps every request."""

    model: str = "scripted"
    turns: list[list[types.Part]]
    requests: list = Field(default_factory=list)

    async def generate_content_async(self, llm_request, stream=False):
        self.requests.append(llm_request)
        yield LlmResponse(content=types.Content(role="model", parts=self.turns.pop(0)))


def call(name, **args):
    return types.Part.from_function_call(name=name, args=args)


def run_agent(agent, tmp_path, case="007", through=None, message="Handle this case."):
    case_view = view(load_case(CASES / case), through, "eval")
    gateway = ActionGateway(case_view, Ledger(tmp_path / "ledger.jsonl"))
    session_id = uuid.uuid4().hex
    CASE_RUNS[session_id] = CaseRun(case_view, gateway)
    runner = Runner(
        app_name="pm_agent",
        agent=agent,
        session_service=InMemorySessionService(),
        auto_create_session=True,
    )

    async def collect():
        content = types.Content(role="user", parts=[types.Part(text=message)])
        return [
            event
            async for event in runner.run_async(
                user_id="test", session_id=session_id, new_message=content
            )
        ]

    try:
        return asyncio.run(collect()), gateway.ledger.entries
    finally:
        CASE_RUNS.pop(session_id)


def tool_results(llm_request):
    return [
        part.function_response.response
        for content in llm_request.contents
        for part in content.parts or []
        if part.function_response
    ]


def test_gateway_answers_actions_and_rejects_a_contradicting_move(tmp_path):
    model = ScriptedLlm(
        turns=[
            [call("get_case_overview")],
            [
                call(
                    "send_message",
                    to="contractor",
                    subject="Invoice",
                    body="Please resend the invoice.",
                    purpose="request",
                )
            ],
            [
                call(
                    "escalate",
                    reason="Invoice above quote",
                    handover_note={
                        "known": "Quote £198.37 + VAT, invoice £240.00.",
                        "conflicts": "Supplier name differs.",
                        "done": "Nothing paid.",
                        "needed": "Decide whether to pay.",
                    },
                ),
                call(
                    "submit_decision",
                    next_move="ask",
                    summary="Ask the contractor.",
                    answer_to_question=None,
                    reasoning=REASONING,
                ),
            ],
            [
                call(
                    "submit_decision",
                    next_move="escalate",
                    summary="Invoice exceeds the quote; property manager decides.",
                    answer_to_question=None,
                    reasoning=REASONING,
                )
            ],
        ]
    )
    _, ledger = run_agent(root_agent.clone(update={"model": model}), tmp_path)

    assert [(e["tool"], e["status"], e["rule"]) for e in ledger] == [
        ("send_message", "blocked", "R4"),
        ("escalate", "approved", None),
        ("submit_decision", "blocked", "MOVE"),
        ("submit_decision", "approved", None),
    ]
    assert tool_results(model.requests[1])[-1]["case_id"] == "007"
    blocked = tool_results(model.requests[2])[-1]
    assert blocked["status"] == "blocked"
    assert "ZZ4 3ZZ" in blocked["how_to_fix"]
    escalated, rejected = tool_results(model.requests[3])[-2:]
    assert escalated == {"status": "recorded"}
    assert rejected["status"] == "blocked"
    assert "'escalate'" in rejected["reason"]
    assert len(model.requests) == 4, "an accepted submit_decision ends the run"


def test_tool_call_limit_stops_the_run(tmp_path):
    turns = [[call("get_events", first=1, last=1)] for _ in range(MAX_TOOL_CALLS + 1)]
    model = ScriptedLlm(turns=turns)
    with pytest.raises(ToolCallLimitExceeded):
        run_agent(root_agent.clone(update={"model": model}), tmp_path)
    ledger = (tmp_path / "ledger.jsonl").read_text().splitlines()
    assert len(ledger) == 1 and '"rule": "LIMIT"' in ledger[0]


@pytest.mark.live
def test_live_agent_submits_a_valid_move_on_case_049(tmp_path):
    _, ledger = run_agent(root_agent, tmp_path, case="049", through=7)
    decisions = [e for e in ledger if e["tool"] == "submit_decision"]
    assert decisions and decisions[-1]["status"] == "approved"
    assert decisions[-1]["args"]["next_move"] in {"act", "ask", "wait", "escalate"}


@pytest.mark.live
def test_live_model_quotes_the_case_007_invoice_pdf(tmp_path):
    reader = LlmAgent(
        name="reader",
        model=AnthropicLlm(model=MODEL),
        instruction="Read the attachment the user names with read_attachment, then "
        "reply with the amount due exactly as printed on it, nothing else.",
        tools=[read_attachment],
        before_tool_callback=before_tool_callback,
    )
    events, _ = run_agent(reader, tmp_path, message="attachment-02-tax-invoice.pdf")
    answer = "".join(
        part.text or ""
        for event in events
        if event.content and event.is_final_response()
        for part in event.content.parts or []
    )
    assert "240.00" in answer
