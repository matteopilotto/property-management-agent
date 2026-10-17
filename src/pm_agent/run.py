import argparse
import asyncio
import json
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from opentelemetry import trace

from . import render
from .agent import root_agent
from .case import load_case, view
from .gateway import ActionGateway
from .ledger import Ledger
from .telemetry import setup_tracing
from .tools import CASE_RUNS, CaseRun

CASES_ROOT = Path("HackatonPublicCases/Property Management")
DECISION_POINTS = Path("eval/decision_points")
RUNS = Path("runs")
CASE_TIMEOUT_S = 240
EVAL_CONCURRENCY = 5

# Claude Sonnet 5.5 API prices in USD per million tokens, from
# https://platform.claude.com/docs/en/about-claude/pricing (checked 2026-10-17):
# base input $2, cache hits $0.10, output $10. Prompt caching is not configured,
# so cache writes ($2.50) do not occur.
INPUT_USD_PER_MTOK = 2.00
CACHED_INPUT_USD_PER_MTOK = 0.10
OUTPUT_USD_PER_MTOK = 10.00

tracer = trace.get_tracer("pm_agent")


async def run_case(
    case_path: Path,
    out_dir: Path,
    *,
    case_id: str,
    view_mode: str,
    visible_through: int | None,
    gateway_mode: str,
    agent: BaseAgent = root_agent,
) -> dict:
    """Run one case into out_dir. Never raises: a failure is written as an answer."""
    out_dir.mkdir(parents=True, exist_ok=True)
    ledger = Ledger(out_dir / "ledger.jsonl")
    trace_file = out_dir / "trace.jsonl"
    trace_file.write_text("", encoding="utf-8")
    tokens = {"input": 0, "output": 0, "cached_input": 0}
    case_view, error, trace_id = None, None, None
    started = time.monotonic()
    with tracer.start_as_current_span(f"case {case_id}") as span:
        if span.get_span_context().is_valid:
            trace_id = format(span.get_span_context().trace_id, "032x")
        try:
            case_view = view(load_case(case_path), visible_through, view_mode)
            (out_dir / "input.md").write_text(
                render.input_markdown(case_view), encoding="utf-8"
            )
            gateway = ActionGateway(case_view, ledger, gateway_mode)
            async with asyncio.timeout(CASE_TIMEOUT_S):
                await _run_agent(agent, CaseRun(case_view, gateway), trace_file, tokens)
        except TimeoutError:
            error = f"TimeoutError: the case took longer than {CASE_TIMEOUT_S} s"
        except Exception as exc:  # noqa: BLE001 - any crash must still write an answer
            error = f"{type(exc).__name__}: {exc}"
    decision = next(
        (
            e["args"]
            for e in reversed(ledger.entries)
            if e["tool"] == "submit_decision" and e["status"] == "approved"
        ),
        None,
    )
    if decision is None and error is None:
        error = "the agent stopped without an accepted submit_decision"
    if error is not None:
        decision = None
    if decision is not None:
        decision = {**decision, "reasoning": _reasoning(decision.get("reasoning"))}
    result = {
        "id": case_id,
        "case_path": str(case_path),
        "view_mode": view_mode,
        "visible_through_event": visible_through,
        "gateway_mode": gateway_mode,
        "next_move": decision and decision.get("next_move"),
        "summary": decision and decision.get("summary"),
        "answer_to_question": decision and decision.get("answer_to_question"),
        "reasoning": decision and decision.get("reasoning"),
        "actions": [
            {key: e[key] for key in ACTION_KEYS}
            for e in ledger.entries
            if e["tool"] != "submit_decision"
        ],
        "tokens": tokens,
        "cost_usd": round(cost_usd(tokens), 6),
        "latency_s": round(time.monotonic() - started, 2),
        "trace_id": trace_id,
        "error": error,
    }
    if not (out_dir / "input.md").exists():
        (out_dir / "input.md").write_text(
            f"Case not shown: {error}\n", encoding="utf-8"
        )
    try:
        answer = render.answer_markdown(result, case_view)
        reasoning = render.reasoning_markdown(result)
    except Exception as exc:  # noqa: BLE001 - a rendering bug must not lose the case
        error = f"rendering failed: {type(exc).__name__}: {exc}"
        result["error"] = error if result["error"] is None else result["error"]
        raw = json.dumps(result, indent=2, ensure_ascii=False)
        answer = (
            f"# Case {case_id}: {render.FAILURE}\n\n{error}\n\n```json\n{raw}\n```\n"
        )
        reasoning = f"# Case {case_id}: reasoning\n\n{render.FAILURE}: {error}\n"
    (out_dir / "ANSWER.md").write_text(answer, encoding="utf-8")
    (out_dir / "REASONING.md").write_text(reasoning, encoding="utf-8")
    (out_dir / "result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        f"{case_id}: {result['next_move'] or render.FAILURE} "
        f"${result['cost_usd']:.4f} {result['latency_s']:.1f}s"
        + (f" ({error})" if error else "")
    )
    return result


ACTION_KEYS = ("seq", "tool", "args", "status", "would_status", "rule", "reason")
REASONING_LISTS = ("facts", "conflicts", "missing", "options_rejected")


def _reasoning(value) -> dict:
    """Claude sometimes sends reasoning as a JSON string or free text, not an object."""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            value = {"facts": [value]}
    if not isinstance(value, dict):
        value = {} if value is None else {"facts": [str(value)]}
    return {
        **value,
        **{
            key: [value[key]]
            for key in REASONING_LISTS
            if isinstance(value.get(key), str)
        },
    }


async def _run_agent(
    agent: BaseAgent, case_run: CaseRun, trace_file: Path, tokens: dict
) -> None:
    session_id = uuid.uuid4().hex
    CASE_RUNS[session_id] = case_run
    runner = Runner(
        app_name="pm_agent",
        agent=agent,
        session_service=InMemorySessionService(),
        auto_create_session=True,
    )
    message = types.Content(
        role="user",
        parts=[types.Part(text="Handle this case at its decision point.")],
    )
    try:
        with trace_file.open("a", encoding="utf-8") as f:
            async for event in runner.run_async(
                user_id="pm-agent", session_id=session_id, new_message=message
            ):
                f.write(event.model_dump_json(exclude_none=True) + "\n")
                usage = event.usage_metadata
                if usage:
                    tokens["input"] += usage.prompt_token_count or 0
                    tokens["output"] += (usage.candidates_token_count or 0) + (
                        usage.thoughts_token_count or 0
                    )
                    tokens["cached_input"] += usage.cached_content_token_count or 0
    finally:
        CASE_RUNS.pop(session_id, None)


def cost_usd(tokens: dict) -> float:
    """prompt_token_count already includes cached tokens, so they are split out."""
    uncached = tokens["input"] - tokens["cached_input"]
    return (
        uncached * INPUT_USD_PER_MTOK
        + tokens["cached_input"] * CACHED_INPUT_USD_PER_MTOK
        + tokens["output"] * OUTPUT_USD_PER_MTOK
    ) / 1_000_000


async def _bounded(jobs: list, concurrency: int) -> list[dict]:
    semaphore = asyncio.Semaphore(concurrency)

    async def one(job):
        async with semaphore:
            return await job()

    return await asyncio.gather(*(one(job) for job in jobs))


async def run_cases(
    cases_dir: Path,
    out: Path,
    concurrency: int,
    gateway_mode: str,
    agent: BaseAgent = root_agent,
) -> list[dict]:
    """Every subfolder of cases_dir is a case in live mode (the Reality Test)."""
    folders = sorted(p for p in Path(cases_dir).iterdir() if p.is_dir())
    jobs = [
        lambda folder=folder: run_case(
            folder,
            out / folder.name,
            case_id=folder.name,
            view_mode="live",
            visible_through=None,
            gateway_mode=gateway_mode,
            agent=agent,
        )
        for folder in folders
    ]
    return await _bounded(jobs, concurrency)


async def run_eval(
    run_id: str,
    gateway_mode: str,
    only: list[str] | None,
    decision_points: Path = DECISION_POINTS,
    agent: BaseAgent = root_agent,
) -> list[dict]:
    """Every decision point in eval mode, into runs/<run_id>/<dp_id>/."""
    points = [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted(Path(decision_points).glob("*.json"))
    ]
    if only:
        points = [p for p in points if p["id"] in only]
    jobs = [
        lambda point=point: run_case(
            CASES_ROOT / point["case"],
            RUNS / run_id / point["id"],
            case_id=point["id"],
            view_mode="eval",
            visible_through=point["visible_through_event"],
            gateway_mode=gateway_mode,
            agent=agent,
        )
        for point in points
    ]
    return await _bounded(jobs, EVAL_CONCURRENCY)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="pm-agent")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="run the agent on every case in a folder")
    run.add_argument("cases_dir", type=Path)
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--concurrency", type=int, default=5)
    run.add_argument("--gateway", choices=["enforce", "observe"], default="enforce")
    evaluate = commands.add_parser("eval", help="run every decision point")
    evaluate.add_argument("--run-id", required=True)
    evaluate.add_argument(
        "--gateway", choices=["enforce", "observe"], default="enforce"
    )
    evaluate.add_argument("--only", nargs="+", metavar="dp_id")
    score = commands.add_parser("score", help="score an eval run")
    score.add_argument(
        "run_ids",
        nargs="+",
        metavar="run_id",
        help="runs under runs/; with two, the lower move accuracy is the headline",
    )
    score.add_argument(
        "--judge", action="store_true", help="add OpenAI rubric scores (JUDGE_MODEL)"
    )
    score.add_argument(
        "--compare",
        metavar="observe_run_id",
        help="list an observe run's unsafe proposals next to approved prohibited actions",
    )
    args = parser.parse_args(argv)
    load_dotenv()
    if args.command == "run":
        setup_tracing()
        asyncio.run(run_cases(args.cases_dir, args.out, args.concurrency, args.gateway))
        return
    if args.command == "eval":
        setup_tracing()
        asyncio.run(run_eval(args.run_id, args.gateway, args.only))
        return
    if args.command == "score":
        from pm_agent import scoring

        raise SystemExit(scoring.cli(args.run_ids, args.judge, args.compare))
    print(f"{args.command}: not implemented")
