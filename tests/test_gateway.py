import json
from dataclasses import replace
from pathlib import Path

import pytest

from pm_agent.case import Event, load_case, view
from pm_agent.gateway import ActionGateway
from pm_agent.ledger import Ledger

CASES = (
    Path(__file__).resolve().parents[1] / "HackatonPublicCases" / "Property Management"
)
LEDGER_FIELDS = {
    "seq",
    "ts",
    "tool",
    "args",
    "status",
    "would_status",
    "rule",
    "reason",
    "mode",
}


def gateway(tmp_path, case="004", through=None, mode="enforce"):
    case_view = view(load_case(CASES / case), through, "eval")
    return ActionGateway(case_view, Ledger(tmp_path / "ledger.jsonl"), mode)


def message(
    to="landlord", body="Flat 2, 172 Alder Lane, Bellmere, ZZ3 1ZZ: may we proceed?"
):
    return {"to": to, "subject": "Cleaning quote", "body": body, "purpose": "request"}


UPDATE = {
    "to": "tenant",
    "subject": "Update",
    "body": "We are waiting for the Landlord.",
    "purpose": "update",
}


def booking(approval_event):
    return {
        "contractor": "Stonebridge Solutions",
        "work": "Checkout clean",
        "slot": "2025-11-10 09:00",
        "approved_amount_gbp": 90,
        "approval_event": approval_event,
    }


def invoice(quote, invoice_amount, quote_evidence, invoice_evidence):
    return {
        "contractor": "Willow Homes",
        "invoice_amount_gbp": invoice_amount,
        "approved_quote_gbp": quote,
        "quote_evidence": quote_evidence,
        "invoice_evidence": invoice_evidence,
    }


def test_r1_agency_approval_update_passes(tmp_path):
    # Case 004 event 2: "Landlord approval confirmed. Proceed to provider selection."
    result = gateway(tmp_path, through=10).review("book_contractor", booking(2))
    assert result == {"status": "recorded"}


def test_r1_landlord_email_passes(tmp_path):
    # Case 004 event 12, from Landlord: "Pls go ahead."
    assert gateway(tmp_path).review("book_contractor", booking("event 12")) == {
        "status": "recorded"
    }


def test_r1_without_approval_is_held(tmp_path):
    # Case 004 event 3: "Maintenance provider assigned" is no approval.
    gate = gateway(tmp_path, through=10)
    result = gate.review("book_contractor", booking(3))
    assert result["status"] == "held_for_property_manager"
    assert gate.ledger.entries[-1]["rule"] == "R1"


def test_r1_approval_event_not_yet_visible_is_held(tmp_path):
    result = gateway(tmp_path, through=10).review("book_contractor", booking(12))
    assert result["status"] == "held_for_property_manager"


def test_r2_tenant_charge_is_always_held(tmp_path):
    gate = gateway(tmp_path)
    result = gate.review(
        "charge_tenant",
        {"amount_gbp": 90, "reason": "Checkout clean", "evidence": "12"},
    )
    assert result["status"] == "held_for_property_manager"
    assert gate.ledger.entries[-1]["rule"] == "R2"


def test_r3_invoice_matching_quote_passes(tmp_path):
    args = invoice(
        "£90.00",
        90,
        "attachment-02-cleaning-quotation.pdf",
        "attachment-03-cleaning-invoice.pdf",
    )
    assert gateway(tmp_path).review("approve_invoice", args) == {"status": "recorded"}


def test_r3_case_007_invoice_above_quote_is_held(tmp_path):
    # Quote £198.37 plus VAT (= £238.04) in event 8; invoice PDF says £240.00.
    gate = gateway(tmp_path, case="007")
    result = gate.review(
        "approve_invoice", invoice(238.04, 240.00, 8, "attachment-02-tax-invoice.pdf")
    )
    assert result["status"] == "held_for_property_manager"
    assert gate.ledger.entries[-1]["rule"] == "R3"
    result = gate.review(
        "approve_invoice", invoice(198.37, 240.00, 8, "attachment-02-tax-invoice.pdf")
    )
    assert "exceeds the approved quote £198.37" in result["reason"]


def test_r3_amount_missing_from_evidence_is_held(tmp_path):
    result = gateway(tmp_path, case="007").review(
        "approve_invoice", invoice(240.00, 240.00, 8, "attachment-02-tax-invoice.pdf")
    )
    assert "not found" in result["reason"]


def test_r4_message_naming_the_property_passes(tmp_path):
    assert gateway(tmp_path).review("send_message", message()) == {"status": "recorded"}


def test_r4_other_cases_postcode_is_blocked(tmp_path):
    # ZZ2 0ZZ is case 012's property, quoted in a message about case 004.
    body = (
        "Re Flat 9, 89 Juniper Mews, Willowbank, ZZ2 0ZZ and ZZ3 1ZZ: please approve."
    )
    gate = gateway(tmp_path)
    result = gate.review("send_message", message(body=body))
    assert result["status"] == "blocked"
    assert "ZZ20ZZ" in result["reason"]
    assert "Flat 2, 172 Alder Lane" in result["how_to_fix"]
    assert gate.ledger.entries[-1]["rule"] == "R4"


def test_r4_contractor_message_without_property_is_blocked(tmp_path):
    result = gateway(tmp_path).review(
        "send_message", message(to="contractor", body="Please send your invoice.")
    )
    assert result["status"] == "blocked"


def test_r4_tenant_message_may_omit_the_postcode(tmp_path):
    result = gateway(tmp_path).review(
        "send_message", message(to="tenant", body="When can the cleaner visit?")
    )
    assert result == {"status": "recorded"}


def test_r4_is_inactive_in_raw_mode(tmp_path):
    (tmp_path / "case").mkdir()
    (tmp_path / "case" / "notes.txt").write_text("boiler broken")
    raw_view = view(load_case(tmp_path / "case"), None, "live")
    gate = ActionGateway(raw_view, Ledger(tmp_path / "ledger.jsonl"))
    assert gate.review("send_message", message(body="ZZ9 9ZZ")) == {
        "status": "recorded"
    }
    assert "R4 inactive" in gate.ledger.entries[-1]["reason"]


def decision(move):
    return {
        "next_move": move,
        "summary": "s",
        "answer_to_question": None,
        "reasoning": {
            "facts": [],
            "conflicts": [],
            "missing": [],
            "options_rejected": [],
            "uncertainty": "",
        },
    }


def test_r5_wait_on_no_hot_water_is_blocked(tmp_path):
    case_view = view(load_case(CASES / "004"), 3, "eval")
    body = "Tenant called: there is no hot water since Monday."
    hazard = Event(4, "2025-10-24 09:00:00 UTC", "Call", "Tenant", "Agency", body)
    case_view = replace(case_view, events=[*case_view.events, hazard])
    gate = ActionGateway(case_view, Ledger(tmp_path / "ledger.jsonl"))
    gate.review("schedule_followup", FOLLOWUP)
    result = gate.review("submit_decision", decision("wait"))
    assert result["status"] == "blocked"
    assert "event 4 (no hot water)" in result["reason"]
    assert gate.ledger.entries[-1]["rule"] == "R5"


def test_r5_wait_without_hazard_passes(tmp_path):
    gate = gateway(tmp_path, through=10)
    gate.review("schedule_followup", FOLLOWUP)
    assert gate.review("submit_decision", decision("wait")) == {"status": "recorded"}


FOLLOWUP = {"due_date": "2025-10-27", "reason": "Waiting for Landlord"}
ESCALATION = {
    "reason": "Invoice above quote",
    "handover_note": {"known": "k", "conflicts": "c", "done": "d", "needed": "n"},
}


@pytest.mark.parametrize(
    ("actions", "move"),
    [
        ([("escalate", ESCALATION), ("send_message", message())], "escalate"),
        ([("send_message", message()), ("close_case", {"reason": "done"})], "act"),
        ([("send_message", {**message(), "purpose": "instruct"})], "act"),
        ([("send_message", message()), ("schedule_followup", FOLLOWUP)], "ask"),
        ([("schedule_followup", FOLLOWUP), ("send_message", UPDATE)], "wait"),
    ],
)
def test_move_must_match_the_actions(tmp_path, actions, move):
    gate = gateway(tmp_path, through=10)
    for tool, args in actions:
        gate.review(tool, args)
    for other in {"act", "ask", "wait", "escalate"} - {move}:
        result = gate.review("submit_decision", decision(other))
        assert result["status"] == "blocked", other
        assert gate.ledger.entries[-1]["rule"] == "MOVE"
        assert repr(move) in result["how_to_fix"]
    assert gate.review("submit_decision", decision(move)) == {"status": "recorded"}


def test_move_without_any_action_is_blocked(tmp_path):
    result = gateway(tmp_path).review("submit_decision", decision("escalate"))
    assert result["status"] == "blocked"
    assert "not backed by any recorded action" in result["reason"]


def test_blocked_actions_do_not_count_towards_the_move(tmp_path):
    gate = gateway(tmp_path)
    gate.review("send_message", message(to="contractor", body="No postcode here."))
    gate.review("schedule_followup", FOLLOWUP)
    assert gate.review("submit_decision", decision("wait")) == {"status": "recorded"}


def test_r6_repeated_message_is_duplicate(tmp_path):
    gate = gateway(tmp_path)
    assert gate.review("send_message", message()) == {"status": "recorded"}
    repeat = message(
        body="  flat 2, 172 Alder Lane, Bellmere, ZZ3 1ZZ:   may we PROCEED? "
    )
    assert gate.review("send_message", repeat) == {"status": "duplicate"}
    assert gate.ledger.entries[-1]["rule"] == "R6"


def test_r6_retrying_a_blocked_action_is_judged_again(tmp_path):
    gate = gateway(tmp_path)
    blocked = message(to="contractor", body="Please send your invoice.")
    assert gate.review("send_message", blocked)["status"] == "blocked"
    assert gate.review("send_message", blocked)["status"] == "blocked"


ACTIONS = [
    ("book_contractor", booking(3)),
    ("charge_tenant", {"amount_gbp": 90, "reason": "clean", "evidence": "12"}),
    ("send_message", message(to="contractor", body="ZZ9 9ZZ")),
    ("send_message", message()),
    ("send_message", message()),
    ("close_case", {"reason": "done"}),
]


def test_observe_mode_approves_everything_and_keeps_the_enforce_status(tmp_path):
    enforce = gateway(tmp_path / "e", through=10)
    observe = gateway(tmp_path / "o", through=10, mode="observe")
    for tool, args in ACTIONS:
        enforce.review(tool, args)
        assert observe.review(tool, args) == {"status": "recorded"}
    assert [e["status"] for e in observe.ledger.entries] == ["approved"] * len(ACTIONS)
    assert [e["would_status"] for e in observe.ledger.entries] == [
        e["status"] for e in enforce.ledger.entries
    ]
    assert [e["status"] for e in enforce.ledger.entries] == [
        "held",
        "held",
        "blocked",
        "approved",
        "duplicate",
        "approved",
    ]
    assert {e["mode"] for e in observe.ledger.entries} == {"observe"}


@pytest.mark.parametrize("mode", ["enforce", "observe"])
def test_each_call_appends_one_complete_ledger_line(tmp_path, mode):
    gate = gateway(tmp_path, through=10, mode=mode)
    for i, (tool, args) in enumerate(ACTIONS, start=1):
        gate.review(tool, args)
        lines = (tmp_path / "ledger.jsonl").read_text().splitlines()
        assert len(lines) == i
        entry = json.loads(lines[-1])
        assert set(entry) == LEDGER_FIELDS
        assert (entry["seq"], entry["tool"], entry["args"]) == (i, tool, args)
        assert entry["ts"].endswith("Z")
