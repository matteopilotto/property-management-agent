import asyncio
import json
import re
import shutil
from pathlib import Path

import pytest
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types

from pm_agent.agent import root_agent
from pm_agent.render import FAILURE
from pm_agent.run import cost_usd, run_cases, run_eval

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "HackatonPublicCases" / "Property Management"
FILES = {
    "ANSWER.md",
    "REASONING.md",
    "input.md",
    "ledger.jsonl",
    "trace.jsonl",
    "result.json",
}
RESULT_KEYS = [
    "id",
    "case_path",
    "view_mode",
    "visible_through_event",
    "gateway_mode",
    "next_move",
    "summary",
    "answer_to_question",
    "reasoning",
    "actions",
    "tokens",
    "cost_usd",
    "latency_s",
    "trace_id",
    "error",
]
TEMPLATE_HEADINGS = re.findall(
    r"^## .+$",
    (ROOT / "submission-template/ANSWERS/1/ANSWER.md").read_text(),
    re.MULTILINE,
)


class CaseStub(BaseLlm):
    """Overview, then a held tenant charge plus an escalation, then the decision.
    Raises for the case folder named 'boom'."""

    model: str = "stub"

    async def generate_content_async(self, llm_request, stream=False):
        responses = [
            part.function_response.response
            for content in llm_request.contents
            for part in content.parts or []
            if part.function_response
        ]
        if not responses:
            parts = [call("get_case_overview")]
        elif len(responses) == 1:
            if responses[0]["case_id"] == "boom":
                raise RuntimeError("forced failure")
            parts = [
                call("charge_tenant", amount_gbp=50, reason="Clean", evidence="1"),
                call(
                    "escalate",
                    reason="Liability unclear",
                    handover_note={
                        "known": "Tenant reported a fault.",
                        "conflicts": "None.",
                        "done": "Nothing sent.",
                        "needed": "Decide who pays.",
                    },
                ),
            ]
        else:
            parts = [
                call(
                    "submit_decision",
                    next_move="escalate",
                    summary="Liability is unclear; the property manager decides.",
                    answer_to_question=None,
                    reasoning={
                        "facts": ["Event 1: request received."],
                        "conflicts": [],
                        "missing": ["Who caused the fault."],
                        "options_rejected": ["act: liability unknown."],
                        "uncertainty": "Medium.",
                    },
                )
            ]
        yield LlmResponse(
            content=types.Content(role="model", parts=parts),
            usage_metadata=types.GenerateContentResponseUsageMetadata(
                prompt_token_count=1000, candidates_token_count=100
            ),
        )


def call(name, **args):
    return types.Part.from_function_call(name=name, args=args)


@pytest.fixture
def stub_agent():
    return root_agent.clone(update={"model": CaseStub()})


def test_run_writes_every_file_and_isolates_a_crash(tmp_path, stub_agent):
    cases = tmp_path / "cases"
    shutil.copytree(CASES / "004", cases / "004")
    shutil.copytree(CASES / "049", cases / "049")
    shutil.copytree(CASES / "049", cases / "boom")
    (cases / "junk").mkdir()
    (cases / "junk" / "notes.txt").write_text("Tenant: the boiler is making a noise.")
    out = tmp_path / "ANSWERS"

    results = asyncio.run(run_cases(cases, out, 3, "enforce", agent=stub_agent))

    assert [r["id"] for r in results] == ["004", "049", "boom", "junk"]
    for name in ("004", "049", "boom", "junk"):
        assert {p.name for p in (out / name).iterdir()} == FILES
        result = json.loads((out / name / "result.json").read_text())
        assert list(result) == RESULT_KEYS
        assert result["view_mode"] == "live"
        assert result["visible_through_event"] is None
        assert result["trace_id"] is None  # Phoenix is not running in tests
        assert (out / name / "trace.jsonl").read_text()

    good = json.loads((out / "004" / "result.json").read_text())
    assert good["error"] is None
    assert good["next_move"] == "escalate"
    assert [(a["tool"], a["status"]) for a in good["actions"]] == [
        ("charge_tenant", "held"),
        ("escalate", "approved"),
    ]
    assert set(good["actions"][0]) == {
        "seq",
        "tool",
        "args",
        "status",
        "would_status",
        "rule",
        "reason",
    }
    assert good["tokens"] == {"input": 3000, "output": 300, "cached_input": 0}
    assert good["cost_usd"] == pytest.approx(cost_usd(good["tokens"]))
    assert json.loads((out / "junk" / "result.json").read_text())["error"] is None

    answer = (out / "004" / "ANSWER.md").read_text()
    assert re.findall(r"^## .+$", answer, re.MULTILINE) == TEMPLATE_HEADINGS
    assert "awaiting property manager approval" in answer
    assert "Decide who pays." in answer
    assert (
        "## Facts\n\n- Event 1: request received."
        in (out / "004" / "REASONING.md").read_text()
    )
    assert "Flat 2, 172 Alder Lane" in (out / "004" / "input.md").read_text()

    failed = json.loads((out / "boom" / "result.json").read_text())
    assert failed["error"] == "RuntimeError: forced failure"
    assert failed["next_move"] is None and failed["reasoning"] is None
    failed_answer = (out / "boom" / "ANSWER.md").read_text()
    assert failed_answer.startswith(f"# Case boom: {FAILURE}")
    assert "forced failure" in failed_answer
    assert re.findall(r"^## .+$", failed_answer, re.MULTILINE) == TEMPLATE_HEADINGS


def test_eval_runs_only_the_named_decision_point(tmp_path, monkeypatch, stub_agent):
    points = tmp_path / "decision_points"
    points.mkdir()
    for dp_id, case, through in (("PM-004-a", "004", 10), ("PM-049-a", "049", 7)):
        (points / f"{dp_id}.json").write_text(
            json.dumps({"id": dp_id, "case": case, "visible_through_event": through})
        )
    monkeypatch.chdir(ROOT)
    monkeypatch.setattr("pm_agent.run.RUNS", tmp_path / "runs")
    asyncio.run(
        run_eval(
            "r1", "observe", ["PM-004-a"], decision_points=points, agent=stub_agent
        )
    )
    assert [p.name for p in (tmp_path / "runs" / "r1").iterdir()] == ["PM-004-a"]
    result = json.loads((tmp_path / "runs/r1/PM-004-a/result.json").read_text())
    assert result["case_path"] == "HackatonPublicCases/Property Management/004"
    assert (result["view_mode"], result["visible_through_event"]) == ("eval", 10)
    assert result["gateway_mode"] == "observe"
    assert result["actions"][0]["status"] == "approved"
    assert result["actions"][0]["would_status"] == "held"


@pytest.mark.live
def test_live_eval_runs_one_decision_point(tmp_path, monkeypatch):
    points = tmp_path / "decision_points"
    points.mkdir()
    (points / "PM-049-a.json").write_text(
        json.dumps({"id": "PM-049-a", "case": "049", "visible_through_event": 7})
    )
    monkeypatch.chdir(ROOT)
    monkeypatch.setattr("pm_agent.run.RUNS", tmp_path / "runs")
    [result] = asyncio.run(
        run_eval("live", "enforce", ["PM-049-a"], decision_points=points)
    )
    assert {p.name for p in (tmp_path / "runs/live/PM-049-a").iterdir()} == FILES
    assert result["error"] is None
    assert result["next_move"] in {"act", "ask", "wait", "escalate"}
    assert result["tokens"]["input"] > 0
    assert result["cost_usd"] > 0
