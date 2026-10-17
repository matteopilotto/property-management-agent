"""Offline HTML scoreboard for one eval run (ticket 12): no server, no JS, no fetches."""

import sys
from html import escape
from pathlib import Path

from pm_agent import scoring
from pm_agent.telemetry import PHOENIX_HOST, PHOENIX_PORT

STATUSES = ("approved", "held", "blocked", "duplicate")

CSS = """
body { margin: 0; padding: 24px 32px; background: #fff; color: #111;
  font: 22px/1.4 system-ui, -apple-system, "Segoe UI", sans-serif; }
h1 { font-size: 40px; margin: 0 0 16px; }
h2 { font-size: 28px; margin: 32px 0 12px; }
.tiles { display: flex; flex-wrap: wrap; gap: 16px; }
.tile { border: 4px solid #111; border-radius: 10px; padding: 12px 18px; min-width: 220px; }
.tile .label { font-size: 18px; }
.tile .value { font-size: 40px; font-weight: 700; }
.tile .limit { font-size: 18px; }
.tile.pass { border-color: #0a6b2d; }
.tile.miss { border-color: #b00020; background: #fde7ea; }
.verdict { font-size: 26px; font-weight: 700; margin: 16px 0; }
.legend { margin: 8px 0 16px; }
.grid { display: grid; align-items: center; gap: 12px;
  grid-template-columns: 8em 9em 7em 5em 1fr 6em 5em 9em; }
.head { font-weight: 700; border-bottom: 4px solid #111; padding: 8px 12px; }
details { border-bottom: 2px solid #999; }
details > summary { list-style: none; cursor: pointer; padding: 10px 12px; }
details > summary::-webkit-details-marker { display: none; }
details[open] > summary { background: #eef; }
.id { font-weight: 700; font-family: ui-monospace, Menlo, monospace; }
.result { font-weight: 700; padding: 2px 10px; border-radius: 6px; color: #fff;
  text-align: center; }
.result.pass { background: #0a6b2d; }
.result.fail { background: #b00020; }
.chip { display: inline-block; margin: 3px 4px; padding: 3px 10px; border-radius: 16px;
  border: 3px solid; font-size: 18px; }
.chip.approved { background: #d8f3dc; border-color: #0a6b2d; }
.chip.held { background: #fff1c2; border-color: #8a5a00; }
.chip.blocked { background: #fde7ea; border-color: #b00020; }
.chip.duplicate { background: #e6e6e6; border-color: #555; }
.num { text-align: right; font-variant-numeric: tabular-nums; }
.trace { font-family: ui-monospace, Menlo, monospace; font-size: 16px;
  word-break: break-all; }
.body { padding: 4px 24px 18px; }
.body h3 { font-size: 22px; margin: 14px 0 4px; }
.body dt { font-weight: 700; }
.body dd { margin: 0 0 8px 24px; white-space: pre-wrap; }
.reasons { color: #b00020; font-weight: 700; }
"""


def phoenix_url(trace_id: str) -> str:
    """Phoenix resolves a trace's project from its OpenTelemetry id via this UI route."""
    return f"http://{PHOENIX_HOST}:{PHOENIX_PORT}/redirects/traces/{trace_id}"


def _tile(check: dict) -> str:
    digits = 4 if check["key"] == "mean_cost_usd" else 2
    if check["value"] is None and not check["gates"]:
        state, word = "", "not run"
    else:
        state, word = ("pass", "pass") if check["passed"] else ("miss", "MISS")
    gates = "" if check["gates"] else ", reported only"
    return (
        f'<div class="tile {state}"><div class="label">{escape(check["metric"])}</div>'
        f'<div class="value">{escape(scoring._fmt(check["value"], digits))}</div>'
        f'<div class="limit">{escape(check["comparison"])} {check["threshold"]}{gates}: '
        f"<b>{word}</b></div></div>"
    )


def _chip(action: dict) -> str:
    status = escape(str(action.get("status")))
    args = action.get("args") or {}
    label = escape(str(action.get("tool")))
    if args.get("to"):
        label += f" to {escape(str(args['to']))}"
    if args.get("purpose"):
        label += f" ({escape(str(args['purpose']))})"
    if status != "approved":
        label = f"<b>{status}</b> {label}"
    title = ""
    if action.get("reason"):
        title = (
            f' title="{escape(str(action.get("rule")))}: {escape(action["reason"])}"'
        )
    return f'<span class="chip {status}"{title}>{label}</span>'


def _text(value) -> str:
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    return str(value)


def _handover(action: dict) -> str:
    args = action.get("args") or {}
    parts = [f"<h3>Handover note (escalate, seq {escape(str(action.get('seq')))})</h3>"]
    if args.get("reason"):
        parts.append(f"<p><b>Reason:</b> {escape(str(args['reason']))}</p>")
    note = args.get("handover_note")
    if isinstance(note, dict):
        items = "".join(
            f"<dt>{escape(str(key))}</dt><dd>{escape(_text(value))}</dd>"
            for key, value in note.items()
        )
        parts.append(f"<dl>{items}</dl>")
    elif note:
        parts.append(f'<p style="white-space: pre-wrap">{escape(_text(note))}</p>')
    return "".join(parts)


def _row(row: dict, result: dict | None) -> str:
    result = result or {}
    actions = result.get("actions") or []
    reasons = scoring._failure_reasons(row)
    expected = row["expected_move"]
    if row["acceptable_moves"]:
        expected += f" (+{', '.join(row['acceptable_moves'])})"
    trace_id = result.get("trace_id")
    trace = (
        f'<a class="trace" href="{escape(phoenix_url(trace_id))}">{escape(trace_id)}</a>'
        if trace_id
        else "-"
    )
    verdict = "fail" if reasons else "pass"
    cost = scoring._fmt(row["cost_usd"], 4)
    latency = scoring._fmt(row["latency_s"], 1)
    summary = (
        f'<div class="grid"><span class="id">{escape(row["id"])}</span>'
        f"<span>{escape(expected)}</span>"
        f"<span><b>{escape(scoring._fmt(row['next_move']))}</b></span>"
        f'<span class="result {verdict}">{verdict}</span>'
        f"<span>{''.join(_chip(a) for a in actions) or 'no actions'}</span>"
        f'<span class="num">{"$" + cost if cost != "-" else cost}</span>'
        f'<span class="num">{latency if latency == "-" else latency + " s"}</span>'
        f"<span>{trace}</span></div>"
    )
    body = []
    if reasons:
        body.append(f'<p class="reasons">{escape("; ".join(reasons))}</p>')
    if result.get("summary"):
        body.append(f"<h3>Summary</h3><p>{escape(str(result['summary']))}</p>")
    if result.get("error"):
        body.append(f"<h3>Error</h3><p>{escape(str(result['error']))}</p>")
    body += [_handover(a) for a in actions if a.get("tool") == "escalate"]
    return (
        f'<details><summary>{summary}</summary><div class="body">'
        f"{''.join(body) or '<p>No summary.</p>'}</div></details>"
    )


def render_board(run_dir: Path, points: list[dict]) -> str:
    run = scoring.score_run(run_dir, points)
    metrics = run["metrics"]
    rows = [
        _row(row, scoring._read_result(run_dir / row["id"])[0]) for row in run["rows"]
    ]
    legend = " ".join(
        f'<span class="chip {status}">{status}</span>' for status in STATUSES
    )
    head = "".join(
        f'<span class="{"num" if label in ("Cost", "Latency") else ""}">{label}</span>'
        for label in (
            "Decision point",
            "Expected",
            "Next move",
            "Result",
            "Actions",
            "Cost",
            "Latency",
            "Phoenix trace",
        )
    )
    title = f"Scoreboard: {escape(run['run_id'])}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<h1>{title}</h1>
<div class="verdict">Gating thresholds: {"all met" if run["passed"] else "MISSED"}</div>
<div class="tiles">{"".join(_tile(check) for check in run["thresholds"])}</div>
<p>{metrics["decision_points"]} decision points.
Required actions present: {scoring._fmt(metrics["required_ok_rate"])}.
Answered: {scoring._fmt(metrics["answered_rate"])}.
Total cost: ${metrics["total_cost_usd"]:.4f}.</p>
<h2>Decision points</h2>
<div class="legend">Action gateway status: {legend}. Click a row for the summary and,
for escalations, the handover note.</div>
<div class="grid head">{head}</div>
{chr(10).join(rows)}
</body>
</html>
"""


def cli(run_id: str, points_dir: Path, out: Path | None) -> int:
    """`pm-agent board`: 0 when the board is written, 2 on bad input."""
    run_dir = scoring.RUNS_DIR / run_id
    if not run_dir.is_dir():
        print(f"error: no run folder {run_dir}", file=sys.stderr)
        return 2
    points = scoring.load_decision_points(points_dir)
    if not points:
        print(f"error: no decision points in {points_dir}", file=sys.stderr)
        return 2
    out = out or run_dir / "board.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_board(run_dir, points), encoding="utf-8")
    print(f"Board written to {out}")
    return 0
