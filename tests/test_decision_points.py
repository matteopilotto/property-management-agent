"""Schema, holdout and move-mix checks for eval/decision_points (spec §10).

Only non-holdout case folders are read: each file's case is checked against
docs/holdout.md before its history is opened.
"""

import json
import re
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DP_DIR = ROOT / "eval" / "decision_points"
CASES_DIR = ROOT / "HackatonPublicCases" / "Property Management"

MOVES = {"act", "ask", "wait", "escalate"}
MOVE_RANK = {"wait": 0, "ask": 1, "act": 2, "escalate": 3}
MIN_MOVES = {"act": 5, "ask": 5, "escalate": 5, "wait": 3}
KEYS = {
    "id",
    "case",
    "visible_through_event",
    "expected_move",
    "acceptable_moves",
    "required_actions",
    "prohibited_actions",
    "rationale",
    "evidence_events",
    "reviewed",
}
# Action tools and their args (spec §8).
TOOL_ARGS = {
    "send_message": {"to", "subject", "body", "purpose"},
    "book_contractor": {
        "contractor",
        "work",
        "slot",
        "approved_amount_gbp",
        "approval_event",
    },
    "approve_invoice": {
        "contractor",
        "invoice_amount_gbp",
        "approved_quote_gbp",
        "quote_evidence",
        "invoice_evidence",
    },
    "charge_tenant": {"amount_gbp", "reason", "evidence"},
    "schedule_followup": {"due_date", "reason"},
    "close_case": {"reason"},
    "escalate": {"reason", "handover_note"},
}
MESSAGE_VALUES = {
    "to": {"tenant", "landlord", "contractor"},
    "purpose": {"request", "instruct", "update"},
}


def holdout_cases() -> set[str]:
    text = (ROOT / "docs" / "holdout.md").read_text()
    return set(re.findall(r"^\| (\d{3}) \|", text, flags=re.MULTILINE))


def total_events(case: str) -> int:
    history = (CASES_DIR / case / "history.md").read_text()
    return int(re.search(r"Total events: (\d+)", history).group(1))


# The move each action implies (spec §8); update messages imply none.
TOOL_MOVE = {
    "escalate": "escalate",
    "book_contractor": "act",
    "approve_invoice": "act",
    "charge_tenant": "act",
    "close_case": "act",
    "schedule_followup": "wait",
}
PURPOSE_MOVE = {"instruct": "act", "request": "ask"}


def implied_move(actions: list[dict]) -> str | None:
    """The move a set of actions implies, by the precedence escalate > act > ask > wait."""
    moves = [
        PURPOSE_MOVE.get(a.get("purpose"))
        if a["tool"] == "send_message"
        else TOOL_MOVE[a["tool"]]
        for a in actions
    ]
    moves = [m for m in moves if m]
    return max(moves, key=MOVE_RANK.__getitem__) if moves else None


DP_FILES = sorted(DP_DIR.glob("*.json"))
HOLDOUT = holdout_cases()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def test_holdout_list_is_parsed():
    assert len(HOLDOUT) == 10


@pytest.mark.parametrize("path", DP_FILES, ids=lambda p: p.stem)
def test_decision_point_schema(path):
    dp = load(path)
    assert set(dp) == KEYS
    assert dp["id"] == path.stem
    assert re.fullmatch(r"PM-\d{3}-[a-z]", dp["id"])
    assert dp["case"] == dp["id"][3:6]
    assert dp["case"] not in HOLDOUT

    assert dp["expected_move"] in MOVES
    alternatives = dp["acceptable_moves"]
    assert set(alternatives) <= MOVES
    assert len(alternatives) == len(set(alternatives))
    assert dp["expected_move"] not in alternatives

    for pattern in dp["required_actions"] + dp["prohibited_actions"]:
        tool = pattern["tool"]
        assert tool in TOOL_ARGS, tool
        assert set(pattern) - {"tool"} <= TOOL_ARGS[tool]
        if tool == "send_message":
            for arg, values in MESSAGE_VALUES.items():
                if arg in pattern:
                    assert pattern[arg] in values
    required_tools = {p["tool"] for p in dp["required_actions"]}
    assert not required_tools & {p["tool"] for p in dp["prohibited_actions"]}

    if dp["required_actions"]:
        assert implied_move(dp["required_actions"]) == dp["expected_move"]

    assert isinstance(dp["rationale"], str) and len(dp["rationale"]) > 40
    assert dp["reviewed"] in (True, False)


@pytest.mark.parametrize("path", DP_FILES, ids=lambda p: p.stem)
def test_evidence_comes_after_the_cut(path):
    dp = load(path)
    assert dp["case"] not in HOLDOUT
    total = total_events(dp["case"])
    cut = dp["visible_through_event"]
    assert isinstance(cut, int) and 1 <= cut < total
    assert dp["evidence_events"]
    for event in dp["evidence_events"]:
        assert isinstance(event, int) and cut < event <= total


def test_no_file_references_a_holdout_case():
    pattern = re.compile(
        r"(PM-|case\s*|Property Management/)(" + "|".join(sorted(HOLDOUT)) + r")\b",
        flags=re.IGNORECASE,
    )
    for path in DP_FILES:
        assert not pattern.search(path.read_text()), path.name


def test_case_coverage():
    per_case = Counter(load(path)["case"] for path in DP_FILES)
    public = {p.name for p in CASES_DIR.iterdir() if p.is_dir()}
    assert len(DP_FILES) >= 40
    assert max(per_case.values()) <= 2
    assert set(per_case) == public - HOLDOUT


def test_move_mix_minimums():
    mix = Counter(load(path)["expected_move"] for path in DP_FILES)
    for move, minimum in MIN_MOVES.items():
        assert mix[move] >= minimum, (move, mix[move])
