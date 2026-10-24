import functools
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from test_run import CaseStub

from pm_agent import demo
from pm_agent.agent import root_agent
from pm_agent.run import run_case

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def client(tmp_path, monkeypatch):
    """The demo app on the real decision points, with demo runs going to tmp_path and
    live runs using the stub model."""
    monkeypatch.chdir(ROOT)
    monkeypatch.setattr(demo, "DEMO_RUNS", tmp_path / "demo")
    stub_agent = root_agent.clone(update={"model": CaseStub()})
    monkeypatch.setattr(demo, "run_case", functools.partial(run_case, agent=stub_agent))
    monkeypatch.setattr(demo, "setup_tracing", lambda: None)
    return TestClient(demo.app)


def lines(response) -> list[dict]:
    return [json.loads(line) for line in response.text.splitlines() if line.strip()]


@pytest.mark.parametrize(
    ("probe", "verdicts"),
    [
        ("R1", [("held", "R1")]),
        ("R2", [("held", "R2")]),
        ("R3", [("held", "R3")]),
        ("R4", [("blocked", "R4")]),
        ("R5", [("approved", None), ("blocked", "R5")]),
    ],
)
def test_probes_get_the_gateway_verdict_and_observe_lets_them_through(
    client, probe, verdicts
):
    enforce = client.post(f"/api/probe/{probe}?gateway=enforce").json()
    observe = client.post(f"/api/probe/{probe}?gateway=observe").json()

    assert [(s["status"], s["rule"]) for s in enforce["steps"]] == verdicts
    assert [(s["status"], s["would_status"]) for s in observe["steps"]] == [
        ("approved", status) for status, _ in verdicts
    ]
    assert enforce["case"]["id"] == demo.PROBES[probe]["point"]


def test_the_duplicate_probe_is_dropped_in_both_modes(client):
    for mode in ("enforce", "observe"):
        steps = client.post(f"/api/probe/R6?gateway={mode}").json()["steps"]

        assert [(s["status"], s["rule"]) for s in steps] == [
            ("approved", None),
            ("duplicate", "R6"),
        ]


def test_presets_list_every_category_and_which_can_be_replayed(client, monkeypatch):
    monkeypatch.setitem(demo.PRESETS["P01"], "recorded", None)
    data = client.get("/api/presets").json()

    assert {p["label"] for p in data["presets"]} == set(data["categories"])
    replay = {p["id"]: p["replay"] for p in data["presets"]}
    assert replay["PM-035-a"] and not replay["P01"]


def test_a_live_run_streams_its_events_and_replays_the_same_way(client):
    live = lines(client.post("/api/run/PM-004-a?mode=live"))
    replay = lines(client.post("/api/run/PM-004-a?mode=replay"))

    for stream, mode in ((live, "live"), (replay, "replay")):
        assert stream[0]["type"] == "case"
        assert stream[0]["mode"] == mode
        assert stream[-1]["type"] == "result"
        assert stream[-1]["result"]["next_move"] == "escalate"
        assert stream[-1]["score"]["id"] == "PM-004-a"
    assert [m["event"] for m in live[1:-1]] == [m["event"] for m in replay[1:-1]]
    calls = [
        p["function_call"]["name"]
        for m in live[1:-1]
        for p in m["event"]["content"]["parts"]
        if "function_call" in p
    ]
    assert calls == [
        "get_case_overview",
        "charge_tenant",
        "escalate",
        "submit_decision",
    ]
    assert live[-1]["recorded"] is False and replay[-1]["recorded"] is True


def test_each_live_run_retries_tracing_while_none_is_registered(client, monkeypatch):
    """Phoenix may come up after the demo server; the next live run picks it up."""
    attempts = []
    monkeypatch.setattr(demo, "setup_tracing", lambda: attempts.append(1))

    client.post("/api/run/PM-004-a?mode=live")
    client.post("/api/run/PM-004-a?mode=live")

    assert len(attempts) == 2


def test_a_replay_without_a_recording_reports_it(client):
    stream = lines(client.post("/api/run/P06?mode=replay"))

    assert [m["type"] for m in stream] == ["case", "error"]


def test_the_case_marks_events_after_the_decision_point_as_unseen(client):
    case = client.get("/api/case/PM-008-a").json()

    assert [e["number"] for e in case["events"] if e["visible"]] == list(range(1, 10))
    assert any(not e["visible"] for e in case["events"])
    assert case["outcome"] and not case["pressure"]
    assert client.get("/api/case/P05").json()["outcome"] is None


def test_slim_drops_attachment_bytes_and_empty_thoughts():
    event = {
        "content": {
            "parts": [
                {"text": "", "thought": True},
                {
                    "function_response": {
                        "name": "read_attachment",
                        "parts": [{"inline_data": {"mime_type": "a/pdf", "data": "x"}}],
                    }
                },
            ]
        }
    }

    assert demo.slim(event) == {
        "content": {
            "parts": [
                {
                    "function_response": {
                        "name": "read_attachment",
                        "parts": [{"inline_data": {"mime_type": "a/pdf"}}],
                    }
                }
            ]
        }
    }
