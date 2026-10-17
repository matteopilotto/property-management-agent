# 04 Agent, tools and playbook

Status: done
Track: A (agent core)
Blocked by: 02, 03

Spec: [`../spec.md`](../spec.md) §8. ADRs 0001 and 0002.

## What

`tools.py`, `agent.py`, `playbook.md`: the read tools, action tools, `submit_decision` with
its move-consistency check, the `before_tool_callback` wiring to the gateway (including the
30-call limit), and the instruction. `root_agent` must load in `adk web src`.
Use the mechanics recorded under "Verified API notes" at the bottom of this file.
Write `playbook.md` from the 40 non-holdout cases only.

## Acceptance criteria

- [ ] A test with a stubbed model shows an action tool call reaching the gateway, a blocked result returned to the model, and `submit_decision` rejected when `next_move` contradicts the actions.
- [ ] A `live` test runs the agent on case 049 at an early decision point and gets a `submit_decision` with a valid move.
- [ ] `read_attachment` delivers a PDF the model can quote (`live` test on case 007's invoice).
- [ ] `uv run adk web src` lists `pm_agent` and a case can be run from it (manual check, noted in the commit message).

## Verified API notes (google-adk 2.12.0, checked 2026-10-17; docs now at adk.dev)

- Model: `from google.adk.models.anthropic_llm import AnthropicLlm`;
  `LlmAgent(model=AnthropicLlm(model="claude-sonnet-5-5"), ...)`. Reads `ANTHROPIC_API_KEY`.
  `max_tokens` defaults to 8192. A plain `model="claude-..."` string routes to Vertex AI: don't.
- `before_tool_callback(tool, args, tool_context)`: parameter names must be exactly these
  (ADK passes them by keyword). It may be async. Return a dict to skip the tool and use the dict
  as its result; return `None` to run the tool.
- PDFs: a tool may return a `google.genai.types.Part.from_bytes(data=..., mime_type="application/pdf")`
  (or a dict containing one); `AnthropicLlm` sends it inside the `tool_result` as a document block.
  Fall back to `pypdf` text only if a file is unreadable.
- Runner: `Runner(app_name=..., agent=..., session_service=InMemorySessionService(), auto_create_session=True)`
  (keyword-only), then `async for event in runner.run_async(user_id=..., session_id=..., new_message=...)`.
  Sum tokens from `event.usage_metadata` (`prompt_token_count`, `candidates_token_count`,
  `cached_content_token_count`) over the events that have it.
- `adk web src` works with `src/pm_agent/__init__.py` doing `from . import agent` and
  `agent.py` defining `root_agent`.
