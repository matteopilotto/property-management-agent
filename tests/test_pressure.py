"""Schema and case checks for the gateway pressure set in eval/pressure (ticket 13).

Each pressure case is a non-holdout public case cut after event N with one synthetic
event N+1; its decision point sees every event, so there are no later evidence events.
"""

import json
import re
from pathlib import Path

import pytest
from test_decision_points import (
    HOLDOUT,
    KEYS,
    MESSAGE_VALUES,
    MOVES,
    TOOL_ARGS,
    implied_move,
)

from pm_agent.case import load_case, view
from pm_agent.gateway import HAZARD

ROOT = Path(__file__).resolve().parent.parent
PRESSURE = ROOT / "eval" / "pressure"
DP_FILES = sorted((PRESSURE / "decision_points").glob("*.json"))


def test_eight_pressure_cases_with_one_decision_point_each():
    ids = [f"P0{n}" for n in range(1, 9)]
    assert [p.stem for p in DP_FILES] == ids
    assert sorted(p.name for p in (PRESSURE / "cases").iterdir()) == ids


@pytest.mark.parametrize("path", DP_FILES, ids=lambda p: p.stem)
def test_pressure_decision_point_schema(path):
    dp = json.loads(path.read_text())
    assert set(dp) == KEYS
    assert dp["id"] == path.stem
    assert dp["case"] == f"eval/pressure/cases/{dp['id']}"
    assert dp["expected_move"] in MOVES
    assert set(dp["acceptable_moves"]) <= MOVES - {dp["expected_move"]}
    for pattern in dp["required_actions"] + dp["prohibited_actions"]:
        assert set(pattern) - {"tool"} <= TOOL_ARGS[pattern["tool"]]
        for arg, values in MESSAGE_VALUES.items():
            if pattern["tool"] == "send_message" and arg in pattern:
                assert pattern[arg] in values
    assert dp["prohibited_actions"]
    assert not {p["tool"] for p in dp["required_actions"]} & {
        p["tool"] for p in dp["prohibited_actions"]
    }
    assert implied_move(dp["required_actions"]) == dp["expected_move"]
    assert len(dp["rationale"]) > 40
    assert dp["evidence_events"] == []
    assert dp["reviewed"] is False


@pytest.mark.parametrize("path", DP_FILES, ids=lambda p: p.stem)
def test_pressure_case_ends_at_the_synthetic_event(path):
    dp = json.loads(path.read_text())
    folder = ROOT / dp["case"]
    source = re.match(r"# Case (\d{3}):", (folder / "index.md").read_text())
    assert source and source.group(1) not in HOLDOUT
    history = (folder / "history.md").read_text()
    total = int(re.search(r"Total events: (\d+)", history).group(1))
    case = load_case(folder)
    assert not case.raw
    assert [e.number for e in case.events] == list(range(1, total + 1))
    assert dp["visible_through_event"] == total
    last = case.events[-1]
    assert last.channel and last.sender and last.recipient and last.body


@pytest.mark.parametrize("path", DP_FILES, ids=lambda p: p.stem)
def test_wait_is_never_right_on_a_visible_hazard(path):
    dp = json.loads(path.read_text())
    shown = view(load_case(ROOT / dp["case"]), dp["visible_through_event"], "eval")
    texts = [shown.initial_request] + [e.body for e in shown.events]
    if any(HAZARD.search(text) for text in texts):
        assert "wait" not in [dp["expected_move"], *dp["acceptable_moves"]]
