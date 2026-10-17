# 01 Scaffold the project and gates

Status: ready-for-agent
Track: A (agent core)
Blocked by: none

Spec: [`../spec.md`](../spec.md) §5, §12.

## What

Create the uv project (`pyproject.toml`, Python 3.13, console script `pm-agent`), the
`src/pm_agent/` package skeleton, `tests/`, `.env.example`, and add `runs/` to `.gitignore`.
Dependencies: `google-adk>=2.12`, `anthropic`, `openai`, `pypdf`, `arize-phoenix`,
`arize-phoenix-otel`, `openinference-instrumentation-google-adk`, `python-dotenv`; dev: `ruff`,
`pytest`. Do not add `litellm` or `openinference-instrumentation-litellm` (the latter would
duplicate every LLM span).
Add `telemetry.py` with a single `setup_tracing()` that calls
`phoenix.otel.register(project_name="pm-agent", auto_instrument=True)` (Phoenix on port 6006,
started with `uvx arize-phoenix serve`) and is a no-op when Phoenix is unreachable.

## Acceptance criteria

- [ ] `uv sync` succeeds; `uv run pm-agent --help` prints usage.
- [ ] The three gates pass: `uv run ruff format --check .`, `uv run ruff check .`, `uv run pytest`.
- [ ] `CLAUDE.md` "Gates" lists exactly those three commands in place of "none yet", in this same commit (CLAUDE.md requires it).
- [ ] `pytest` skips tests marked `live` unless `-m live` is passed.
