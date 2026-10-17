"""Load a case folder and cut it into the view the agent sees at a decision point."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

STANDARD_SECTIONS = {
    "Case details",
    "Initial request",
    "Overview",
    "Outcome",
    "History",
    "Attachments",
}
EVAL_DETAILS = ("Source role", "Created", "Property")
LIVE_HIDDEN_DETAILS = {"Status", "Updated", "Completed"}

TITLE = re.compile(r"^# (.+)$", re.MULTILINE)
SECTION_HEADING = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
DETAIL = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$", re.MULTILINE)
EVENT_ANCHOR = re.compile(r'^<a id="event-\d+"></a>\s*$')
EVENT_HEADING = re.compile(r"^## (.+?) — event (\d+)\s*$")
EVENT_FIELD = re.compile(r"^- \*\*(Channel|From|To):\*\*\s*(.*)$")
ATTACHMENT_LINK = re.compile(r"\]\(attachments/([^)]+)\)")
QUESTION_HEADING = re.compile(
    r"(?i)\b(question|task|decision|decide|answer|what should|advise)\b"
)
QUESTION_TEXT = re.compile(
    r"(?i)\?|\b(please (decide|advise|confirm)|what should|recommend|your decision)\b"
)


@dataclass
class Event:
    number: int
    timestamp: str
    channel: str
    sender: str
    recipient: str
    body: str
    attachment_files: list[str] = field(default_factory=list)


@dataclass
class Case:
    case_id: str
    path: Path
    raw: bool = False
    title: str = ""
    source_role: str = ""
    created: str = ""
    property: str = ""
    initial_request: str = ""
    details: dict[str, str] = field(default_factory=dict)
    events: list[Event] = field(default_factory=list)
    attachments: list[str] = field(default_factory=list)
    raw_sections: dict[str, str] = field(default_factory=dict)
    files: list[str] = field(default_factory=list)


@dataclass
class CaseView:
    case_id: str
    path: Path
    mode: Literal["eval", "live"]
    raw: bool
    visible_through: int | None
    details: dict[str, str]
    initial_request: str
    sections: dict[str, str]
    question: str | None
    events: list[Event]
    attachments: list[str]
    files: list[str]


def load_case(path: Path) -> Case:
    """Parse the known case layout; fall back to raw mode for anything else."""
    path = Path(path)
    try:
        return _parse(path)
    except (OSError, ValueError, UnicodeError):
        return _raw(path)


def _parse(path: Path) -> Case:
    index_file, history_file = path / "index.md", path / "history.md"
    if not index_file.is_file() or not history_file.is_file():
        raise ValueError("missing index.md or history.md")
    index = index_file.read_text(encoding="utf-8")
    sections = _sections(index)
    if "Case details" not in sections:
        raise ValueError("no Case details section")
    events = _events(history_file.read_text(encoding="utf-8"))
    if not events:
        raise ValueError("no parsable events")
    details = dict(DETAIL.findall(sections["Case details"]))
    title = TITLE.search(index)
    attachments_dir = path / "attachments"
    return Case(
        case_id=path.name,
        path=path,
        title=title.group(1).strip() if title else "",
        source_role=details.get("Source role", ""),
        created=details.get("Created", ""),
        property=details.get("Property", ""),
        initial_request=sections.get("Initial request", ""),
        details=details,
        events=events,
        attachments=sorted(f.name for f in attachments_dir.glob("*") if f.is_file()),
        raw_sections=sections,
    )


def _raw(path: Path) -> Case:
    files = sorted(str(f.relative_to(path)) for f in path.rglob("*") if f.is_file())
    return Case(case_id=path.name, path=path, raw=True, files=files)


def _sections(index: str) -> dict[str, str]:
    headings = list(SECTION_HEADING.finditer(index))
    sections = {}
    for i, heading in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else len(index)
        sections[heading.group(1)] = index[heading.end() : end].strip()
    return sections


def _events(history: str) -> list[Event]:
    events: list[Event] = []
    lines: list[str] = []
    for line in history.splitlines():
        heading = EVENT_HEADING.match(line)
        if heading:
            if events:
                _finish(events[-1], lines)
            events.append(
                Event(
                    number=int(heading.group(2)),
                    timestamp=heading.group(1).strip(),
                    channel="",
                    sender="",
                    recipient="",
                    body="",
                )
            )
            lines = []
        elif events and not EVENT_ANCHOR.match(line):
            lines.append(line)
    if events:
        _finish(events[-1], lines)
    return events


def _finish(event: Event, lines: list[str]) -> None:
    """Read the leading Channel/From/To bullets, then keep the rest as the body."""
    fields: dict[str, str] = {}
    rest = list(lines)
    while rest:
        if not rest[0].strip():
            rest.pop(0)
            continue
        match = EVENT_FIELD.match(rest[0])
        if not match or match.group(1) in fields:
            break
        fields[match.group(1)] = match.group(2).strip()
        rest.pop(0)
    event.channel = fields.get("Channel", "")
    event.sender = fields.get("From", "")
    event.recipient = fields.get("To", "")
    event.body = "\n".join(rest).strip()
    event.attachment_files = list(dict.fromkeys(ATTACHMENT_LINK.findall(event.body)))


def view(
    case: Case, visible_through: int | None, mode: Literal["eval", "live"]
) -> CaseView:
    """What the agent may see: a whitelist in eval mode, nearly everything in live mode."""
    events = [
        e for e in case.events if visible_through is None or e.number <= visible_through
    ]
    if mode == "eval":
        details = {k: case.details[k] for k in EVAL_DETAILS if k in case.details}
        sections: dict[str, str] = {}
        referenced = {name for e in events for name in e.attachment_files}
        attachments = [a for a in case.attachments if a in referenced]
    else:
        details = {
            k: v for k, v in case.details.items() if k not in LIVE_HIDDEN_DETAILS
        }
        sections = {
            heading: text
            for heading, text in case.raw_sections.items()
            if heading not in ("Case details", "Initial request")
        }
        attachments = list(case.attachments)
    return CaseView(
        case_id=case.case_id,
        path=case.path,
        mode=mode,
        raw=case.raw,
        visible_through=visible_through,
        details=details,
        initial_request=case.initial_request,
        sections=sections,
        question=_question(sections),
        events=events,
        attachments=attachments,
        files=list(case.files),
    )


def _question(sections: dict[str, str]) -> str | None:
    """Heuristic: a non-standard section whose heading or text asks for a decision."""
    asks = [
        f"{heading}: {text}"
        for heading, text in sections.items()
        if heading not in STANDARD_SECTIONS
        and (QUESTION_HEADING.search(heading) or QUESTION_TEXT.search(text))
    ]
    return "\n\n".join(asks) or None
