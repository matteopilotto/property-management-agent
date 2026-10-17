import json
import re
from dataclasses import asdict
from pathlib import Path

import pytest

from pm_agent.case import load_case, view

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "HackatonPublicCases" / "Property Management"
HOLDOUT = set(
    re.findall(r"^\| (\d{3}) \|", (ROOT / "docs/holdout.md").read_text(), re.MULTILINE)
)
PUBLIC = sorted(p.name for p in CASES.iterdir() if p.is_dir() and p.name not in HOLDOUT)


def test_holdout_list_is_read():
    assert len(HOLDOUT) == 10
    assert len(PUBLIC) == 40


@pytest.mark.parametrize("name", PUBLIC)
def test_public_case_parses_every_event(name):
    case = load_case(CASES / name)
    total = re.search(r"Total events: (\d+)", (CASES / name / "history.md").read_text())
    assert not case.raw
    assert len(case.events) == int(total.group(1))
    assert [e.number for e in case.events] == list(range(1, len(case.events) + 1))
    assert all(e.channel and e.sender and e.recipient for e in case.events)
    assert case.property


def test_event_fields_and_attachment_reference():
    event = load_case(CASES / "004").events[5]
    assert event.number == 6
    assert event.timestamp == "2025-10-24 01:32:44 UTC"
    assert (event.channel, event.sender, event.recipient) == (
        "Email",
        "Northbridge Lettings",
        "Contractor",
    )
    assert event.body.startswith("Address: Flat 2, 172 Alder Lane")
    assert event.attachment_files == ["attachment-01-checkout-inspection-report.pdf"]


def test_eval_view_withholds_the_ending():
    case = load_case(CASES / "004")
    shown = json.dumps(asdict(view(case, 10, "eval")), default=str)
    for section in ("Overview", "Outcome"):
        for sentence in re.split(r"(?<=\.) ", case.raw_sections[section]):
            assert sentence not in shown
    case_view = view(case, 10, "eval")
    assert [e.number for e in case_view.events] == list(range(1, 11))
    # Event 10 itself attaches the quotation, so only the invoice stays hidden at 10;
    # the ticket's "only attachment-01" holds through event 9.
    assert case_view.attachments == [
        "attachment-01-checkout-inspection-report.pdf",
        "attachment-02-cleaning-quotation.pdf",
    ]
    assert view(case, 9, "eval").attachments == [
        "attachment-01-checkout-inspection-report.pdf"
    ]
    assert set(case_view.details) == {"Source role", "Created", "Property"}
    assert case_view.sections == {}
    assert case_view.question is None


def test_unfamiliar_folder_loads_in_raw_mode(tmp_path):
    (tmp_path / "notes.txt").write_text("Tenant says the boiler is broken.")
    (tmp_path / "quote.pdf").write_bytes(b"%PDF-1.4 not really")
    case = load_case(tmp_path)
    assert case.raw
    assert case.events == []
    assert case.files == ["notes.txt", "quote.pdf"]
    assert view(case, None, "live").files == ["notes.txt", "quote.pdf"]


def test_index_without_parsable_events_is_raw(tmp_path):
    (tmp_path / "index.md").write_text(
        "# Case X\n\n## Case details\n\n- **Status:** Open\n"
    )
    (tmp_path / "history.md").write_text("Nothing here in the usual format.\n")
    assert load_case(tmp_path).raw


def test_live_view_exposes_extra_sections_and_the_question(tmp_path):
    (tmp_path / "index.md").write_text(
        "# Case 900: Leak\n\n## Case details\n\n"
        "- **Source role:** Tenant\n- **Status:** Open\n- **Created:** 2026-10-01\n"
        "- **Updated:** 2026-10-02\n- **Completed:** -\n"
        "- **Property:** 1 High St, Town, AB1 2CD\n\n"
        "## Initial request\n\nWater coming through the ceiling, can you help?\n\n"
        "## Escalation\n\nThe contractor has not replied in a week. "
        "What should the agency do next?\n\n"
        "## Background\n\nThe landlord is abroad.\n"
    )
    (tmp_path / "history.md").write_text(
        "# Case 900 history\n\nTotal events: 1\n\n"
        '<a id="event-001"></a>\n## 2026-10-01 09:00:00 UTC — event 001\n\n'
        "- **Channel:** Email\n- **From:** Tenant\n- **To:** Agency / system\n\n"
        "Water is dripping.\n"
    )
    case_view = view(load_case(tmp_path), None, "live")
    assert "Status" not in case_view.details and "Updated" not in case_view.details
    assert case_view.details["Property"] == "1 High St, Town, AB1 2CD"
    assert case_view.sections["Background"] == "The landlord is abroad."
    assert case_view.question.startswith("Escalation: The contractor has not replied")
    assert "Background" not in case_view.question
