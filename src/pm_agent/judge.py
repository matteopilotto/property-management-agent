"""OpenAI rubric judge (ADR 0001). Its scores are reported, never used for pass/fail."""

import json
import os
from pathlib import Path

import openai

RUBRIC_PATH = Path(__file__).resolve().parents[2] / "eval" / "rubric.md"
DIMENSIONS = ("drafts", "reasoning", "handover_note")


class JudgeConfigError(Exception):
    pass


def judge_model() -> str:
    model = os.environ.get("JUDGE_MODEL")
    if not model:
        raise JudgeConfigError(
            "JUDGE_MODEL is not set; add it to .env (see .env.example) to use --judge"
        )
    return model


def make_client() -> openai.OpenAI:
    if not os.environ.get("OPENAI_API_KEY"):
        raise JudgeConfigError(
            "OPENAI_API_KEY is not set; add it to .env (see .env.example) to use --judge"
        )
    return openai.OpenAI()


def _prompt(visible_case: str, rationale: str, agent_output: dict) -> str:
    return (
        "## Visible case\n\n"
        f"{visible_case}\n\n"
        "## Labeller rationale\n\n"
        "Written with hindsight of later events; one acceptable answer, not the only one.\n\n"
        f"{rationale}\n\n"
        "## Agent output\n\n"
        f"```json\n{json.dumps(agent_output, indent=2)}\n```\n"
    )


def _complete(client, model: str, messages: list[dict]):
    kwargs = {
        "model": model,
        "messages": messages,
        "response_format": {"type": "json_object"},
    }
    try:
        return client.chat.completions.create(temperature=0, **kwargs)
    except openai.BadRequestError as error:
        # Reasoning models reject a temperature setting; they run at their fixed default.
        if "temperature" not in str(error):
            raise
        return client.chat.completions.create(**kwargs)


def _parse(content: str) -> dict:
    data = json.loads(content)
    judgement = {}
    for dimension in DIMENSIONS:
        entry = data.get(dimension)
        if not isinstance(entry, dict):
            raise TypeError(f"judge output lacks {dimension}")
        score = entry.get("score")
        if score is not None and (
            isinstance(score, bool) or not isinstance(score, int) or not 1 <= score <= 5
        ):
            raise ValueError(f"judge {dimension} score out of range: {score!r}")
        judgement[dimension] = {
            "score": score,
            "comment": str(entry.get("comment", "")),
        }
    return judgement


def judge_decision_point(
    client, model: str, visible_case: str, rationale: str, agent_output: dict
) -> dict:
    """Score one decision point's output on the rubric dimensions (1-5, or None if N/A)."""
    messages = [
        {"role": "system", "content": RUBRIC_PATH.read_text()},
        {"role": "user", "content": _prompt(visible_case, rationale, agent_output)},
    ]
    response = _complete(client, model, messages)
    return _parse(response.choices[0].message.content)
