import json
import re
import shutil
from pathlib import Path

import pytest

from pm_agent.run import main

FIXTURES = Path(__file__).parent / "fixtures"
TRACE_ID = "8c12dad0a6987d3f2c6d8a1eb968e6d6"


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    """runs/enforce-a and eval/decision_points/ from the fixtures, with one decision point
    given an escalation, a blocked and a duplicate action, and a trace id."""
    shutil.copytree(FIXTURES / "run_folders" / "enforce-a", tmp_path / "runs" / "e")
    shutil.copytree(FIXTURES / "decision_points", tmp_path / "eval" / "decision_points")
    path = tmp_path / "runs" / "e" / "PM-903-a" / "result.json"
    result = json.loads(path.read_text())
    note = {"known": "Leak <reported>", "conflicts": "none", "done": "-", "needed": "x"}
    result["actions"] += [
        {"seq": 2, "tool": "escalate", "status": "approved", "rule": None,
         "args": {"reason": "safety", "handover_note": note}},
        {"seq": 3, "tool": "send_message", "status": "blocked", "rule": "R4",
         "reason": "wrong postcode", "args": {"to": "landlord", "purpose": "update"}},
        {"seq": 4, "tool": "schedule_followup", "status": "duplicate", "rule": "R6",
         "args": {}},
    ]  # fmt: skip
    result["trace_id"] = TRACE_ID
    path.write_text(json.dumps(result))
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_board_has_a_row_per_decision_point_and_status_chips(workspace):
    with pytest.raises(SystemExit) as exit_info:
        main(["board", "e"])
    assert exit_info.value.code == 0
    page = (workspace / "runs" / "e" / "board.html").read_text()

    assert page.count("<details>") == 3
    for dp_id in ("PM-901-a", "PM-902-a", "PM-903-a"):
        assert f'<span class="id">{dp_id}</span>' in page
    for status in ("approved", "held", "blocked", "duplicate"):
        assert f'class="chip {status}"' in page
    assert "send_message to landlord (request)" in page
    assert "Handover note" in page and "Leak &lt;reported&gt;" in page
    assert "Move accuracy" in page


def test_board_links_only_to_the_local_phoenix_trace(workspace):
    out = workspace / "elsewhere" / "board.html"
    with pytest.raises(SystemExit):
        main(["board", "e", "--out", str(out)])
    page = out.read_text()

    urls = re.findall(r"""(?:https?:)?//[^\s"'<>)]+""", page)
    assert urls == [f"http://localhost:6006/redirects/traces/{TRACE_ID}"]
    assert "<script" not in page and "<link" not in page


def test_board_rejects_a_missing_run(workspace):
    with pytest.raises(SystemExit) as exit_info:
        main(["board", "nope"])
    assert exit_info.value.code == 2
