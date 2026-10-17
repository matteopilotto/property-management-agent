"""Per-case action ledger: one JSON line per gated call (spec §9.1)."""

import json
from datetime import UTC, datetime
from pathlib import Path


class Ledger:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch()
        self.entries: list[dict] = []

    def append(
        self,
        *,
        tool: str,
        args: dict,
        status: str,
        would_status: str,
        rule: str | None,
        reason: str | None,
        mode: str,
    ) -> dict:
        entry = {
            "seq": len(self.entries) + 1,
            "ts": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tool": tool,
            "args": args,
            "status": status,
            "would_status": would_status,
            "rule": rule,
            "reason": reason,
            "mode": mode,
        }
        self.entries.append(entry)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
        return entry
