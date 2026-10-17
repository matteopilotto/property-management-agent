import json
import os
from pathlib import Path
from types import SimpleNamespace

import httpx
import openai
import pytest
from dotenv import find_dotenv, load_dotenv

from pm_agent import judge, scoring

FIXTURES = Path(__file__).parent / "fixtures"
FOLDER = FIXTURES / "run_folders" / "enforce-a" / "PM-901-a"
GOOD = {
    "drafts": {"score": 4, "comment": "clear"},
    "reasoning": {"score": 3, "comment": "misses a conflict"},
    "handover_note": {"score": None, "comment": "no escalate action"},
}


class FakeCompletions:
    def __init__(self, content, reject_temperature=False):
        self.content = content
        self.reject_temperature = reject_temperature
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.reject_temperature and "temperature" in kwargs:
            request = httpx.Request(
                "POST", "https://api.openai.com/v1/chat/completions"
            )
            raise openai.BadRequestError(
                "Unsupported parameter: 'temperature'",
                response=httpx.Response(400, request=request),
                body=None,
            )
        message = SimpleNamespace(content=self.content)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def fake_client(completions):
    return SimpleNamespace(chat=SimpleNamespace(completions=completions))


def agent_output():
    result = json.loads((FOLDER / "result.json").read_text())
    return {
        key: result[key] for key in ("next_move", "summary", "reasoning", "actions")
    }


def test_judge_sends_rubric_case_and_output_at_temperature_zero():
    completions = FakeCompletions(json.dumps(GOOD))
    judgement = judge.judge_decision_point(
        fake_client(completions), "m", "THE CASE", "THE RATIONALE", agent_output()
    )
    assert judgement == GOOD
    call = completions.calls[0]
    assert call["temperature"] == 0
    assert call["response_format"] == {"type": "json_object"}
    assert "# Judge rubric" in call["messages"][0]["content"]
    user = call["messages"][1]["content"]
    assert "THE CASE" in user and "THE RATIONALE" in user and "approve_invoice" in user


def test_judge_retries_without_temperature_when_model_rejects_it():
    completions = FakeCompletions(json.dumps(GOOD), reject_temperature=True)
    judge.judge_decision_point(fake_client(completions), "m", "c", "r", {})
    assert len(completions.calls) == 2
    assert "temperature" not in completions.calls[1]


@pytest.mark.parametrize(
    "content",
    [
        "not json",
        json.dumps({"drafts": GOOD["drafts"], "reasoning": GOOD["reasoning"]}),
        json.dumps({**GOOD, "reasoning": {"score": 7, "comment": ""}}),
    ],
)
def test_judge_rejects_malformed_output(content):
    with pytest.raises((ValueError, TypeError)):
        judge.judge_decision_point(
            fake_client(FakeCompletions(content)), "m", "c", "r", {}
        )


def test_judge_error_on_one_decision_point_is_recorded_not_raised():
    def broken(case, rationale, output):
        raise ValueError("judge output lacks drafts")

    points = scoring.load_decision_points(FIXTURES / "decision_points")
    run = scoring.score_run(FOLDER.parent, points, broken)
    assert run["passed"]
    assert run["rows"][0]["judge"] == {"error": "ValueError: judge output lacks drafts"}
    assert run["metrics"]["judge_mean"] is None


@pytest.mark.live
def test_live_judge_scores_one_decision_point():
    load_dotenv(find_dotenv(usecwd=True))
    if not (os.environ.get("OPENAI_API_KEY") and os.environ.get("JUDGE_MODEL")):
        pytest.skip("needs OPENAI_API_KEY and JUDGE_MODEL")
    point = json.loads((FIXTURES / "decision_points" / "PM-901-a.json").read_text())
    judgement = judge.judge_decision_point(
        judge.make_client(),
        judge.judge_model(),
        (FOLDER / "input.md").read_text(),
        point["rationale"],
        agent_output(),
    )
    assert set(judgement) == set(judge.DIMENSIONS)
    assert 1 <= judgement["reasoning"]["score"] <= 5
    assert 1 <= judgement["drafts"]["score"] <= 5  # the run sent a landlord message
