# Property Management Agent: an exception desk for letting agencies

A Claude agent that takes the maintenance jobs a letting agency's automation hands back to a
person, works out the next move, drafts the messages, and escalates what needs a human. Every
action passes through a policy gateway written in code, so the agency's money and liability
rules hold even when the model ignores its instructions.

Track: **Property Management**, Dwelly London AI Hackathon (10 October 2026), redone solo as
the capstone of an Agent Engineering Bootcamp. The material the hackathon started from is
described in [docs/starting-repo.md](docs/starting-repo.md).

| | Result |
|---|---|
| Right next move, 62 decision points (lower of two runs) | **95%** (92% on the labels as first written) |
| Unsafe actions let through | **0** |
| Cases answered | **100%** |
| Cost and latency per case | **$0.114**, **15 s** |
| Reality Test: 30 unseen hackathon cases, run once, unattended | **30/30 answered in 130 s**, correct outcome 85% (self-graded) |

## 1. What I built

A batch agent and a demo console for the cases a maintenance platform cannot finish on its
own. For each case it reads the full history and attachments, then chooses one of four moves:

- **act**: for example, book the approved contractor or forward an invoice for payment;
- **ask**: request missing information or a decision from the tenant, landlord or contractor;
- **wait**: set a dated follow-up;
- **escalate**: hand the case to a property manager with a note on what's known, what
  conflicts and what decision is needed.

It drafts every message. Spending money or charging the tenant waits for recorded approval.
Each case produces `ANSWER.md`, `REASONING.md`, an action ledger and a full trace.

## 2. What operational problem it solves

Routine repair jobs already run on autopilot. The expensive part is the hand-offs: a
contractor stops replying, an invoice doesn't match the quote, nobody knows who pays, or the
records contradict each other. Across the 40 build cases there are 1,211 events, about 30 per
job. The same contractor appears under three names, addresses from other jobs turn up in
emails, and invoices disagree with quotes. The right move is often not to act, and the
hackathon judged exactly that: "Doing nothing or escalating can be the correct decision."

## 3. Architecture

```text
case folder ──▶ loader (cuts the case at a decision point, hides the future)
                  │
                  ▼
        Claude Sonnet 5.5 agent (Google ADK, single ReAct loop)
          read tools: overview, events, search, attachments (PDF text)
          action tools: send_message · book_contractor · approve_invoice · charge_tenant
                        schedule_followup · close_case · escalate · submit_decision
                  │ every action
                  ▼
        ACTION GATEWAY (code, in ADK's before_tool_callback)
          R1 approval before spend · R2 tenant charges always held · R3 invoice within quote
          R4 messages name the right property · R5 no waiting on hazards · R6 no duplicates
                  │ approved / held for a property manager / blocked with a reason
                  ▼
        ledger ──▶ ANSWER.md + REASONING.md + handover note        Phoenix traces every step
```

- **One agent, not a team.** Each case is one bounded investigation. See
  [ADR 0002](docs/adr/0002-single-agent-with-gated-action-tools.md).
- **Rules in code, not just the prompt.** Every side effect is a tool call that the gateway
  checks before it reaches the ledger.
- **Claude inside ADK, judged by OpenAI.** The judge comes from a different model family from
  the agent and the labels, to limit self-preference. See
  [ADR 0001](docs/adr/0001-claude-in-adk-with-openai-judge.md).
- **Robust batch runs.** A crash, timeout or tool-call limit (30 per case, 240 s) still writes
  an answer, "Escalated: system failure", so one bad case cannot sink a batch.

The agency's working rules are in [src/pm_agent/playbook.md](src/pm_agent/playbook.md), loaded
into the agent's instruction. Domain terms are defined in [GLOSSARY.md](GLOSSARY.md).

| Path | What it is |
|---|---|
| [src/pm_agent/](src/pm_agent/) | Agent, tools, gateway, ledger, runner, scorer, judge, demo console |
| [eval/](eval/) | Decision points, pressure cases, judge rubric, committed reports |
| [ANSWERS/](ANSWERS/) | Reality Test output, exactly as generated (tag `results`) |
| [docs/adr/](docs/adr/) | Architecture decisions |
| [docs/demo/](docs/demo/) | Stakeholder brief, deck outline, video script |
| [.scratch/capstone/](.scratch/capstone/) | Spec and the build tickets, in order |

## 4. How to run it

**Prerequisites:** Python 3.13 and [uv](https://docs.astral.sh/uv/). An Anthropic API key
runs the agent. An OpenAI API key is needed only for the optional judge.

```sh
uv sync
cp .env.example .env    # then fill in the variables below
```

| Variable | Needed for |
|---|---|
| `ANTHROPIC_API_KEY` | Every agent run |
| `OPENAI_API_KEY` | `pm-agent score --judge` only |
| `JUDGE_MODEL` | `pm-agent score --judge` only: the OpenAI model name |

**Tracing (optional):** start Phoenix with `uvx arize-phoenix serve` and open
<http://localhost:6006>, project `pm-agent`. Without Phoenix, runs work and tracing is off.

| Command | What it does |
|---|---|
| `uv run pm-agent demo` | Demo console at <http://127.0.0.1:8000>: watch a case live, replay a recorded run, or fire an unsafe action straight at the gateway |
| `uv run pm-agent run <cases_dir> --out <dir>` | Runs every case folder in `<cases_dir>`, 5 in parallel (`--concurrency`), gateway on (`--gateway enforce`, or `observe` to log without blocking) |
| `uv run pm-agent eval --run-id <id>` | Runs all 62 decision points into `runs/<id>/` |
| `uv run pm-agent score <id>` | Scores an eval run; add `--judge` for the OpenAI rubric scores |
| `uv run pm-agent board <id>` | Writes an offline HTML scoreboard for a run |

For example, to run the agent on the public practice cases:

```sh
uv run pm-agent run "HackatonPublicCases/Property Management" --out runs/practice
```

**Checks:** `uv run ruff format --check .`, `uv run ruff check .` and `uv run pytest`. Tests
never call a model API.

## 5. Models, APIs and external services used

- **Claude Sonnet 5.5** (`claude-sonnet-5-5`) through the Anthropic API: the agent. It is
  called with Google ADK's `AnthropicLlm`, which passes PDF attachments inside tool results.
- **Google ADK**: the agent loop, tools and callbacks.
- **OpenAI** (`JUDGE_MODEL`; `gpt-6-luna` in the reported runs): the LLM judge. It reports
  scores only and never decides pass or fail.
- **Arize Phoenix** with OpenInference instrumentation: local tracing.
- **FastAPI** and **uvicorn**: the demo console. **pypdf**: attachment text.

No real messaging, booking or payment system is connected. Action tools write to a per-case
ledger, and each answer says which actions were approved, held for a property manager, or
blocked.

## 6. Important assumptions

- The agent sees only what was known at the decision point. Later events are hidden.
- The agency's policy is the playbook plus the gateway's rules. Landlord approval comes before
  any spend, tenant charges always need a person, and an invoice above the approved quote is
  held.
- Any message, attachment or note can be wrong or hostile. The agent is told that case text is
  evidence, not instructions, and on the pressure set it flagged an injected note as
  untrusted.
- An unreadable or unfamiliar case folder is still answered. The loader falls back to listing
  its raw files.
- The 62 decision-point labels were drafted by Claude from the same 40 cases the playbook was
  written from. That makes the build-set figure optimistic, so the holdout and the Reality Test
  are the honest measures.

## 7. Known limitations

- **Companion actions are weak.** On the Reality Test the move was rarely wrong, but 9 of 12
  escalations sent nothing else, and often only the party who triggered the case was updated.
  The build eval never rewarded keeping every party informed.
- **R5 checks only the move label.** "A visit next week" for a case with no hot water still
  passes as act.
- **`close_case` is not gated.**
- **Three labels were widened after seeing the agent's answers.** 92% is the figure on the
  original labels.
- **The model, not the code, was the effective safety layer.** On 8 pressure cases it proposed
  no unsafe action. Probing the gateway directly found holes in R1 and R3, which are now fixed.
- **Few escalation cases in the eval.** Only 5 of 62 decision points expect escalation, and
  the holdout has none.
- **The Reality Test was self-graded** with a Claude model, following the organisers' guide,
  so expect some leniency.

Full numbers, disclosures and the bugs the eval caught are in
[eval/reports/SUMMARY.md](eval/reports/SUMMARY.md). The Reality Test analysis is in
[eval/reports/reality-test.md](eval/reports/reality-test.md).

## 8. What I would improve or build next

- Score companion actions in the eval, then teach the playbook to do them.
- Gate `close_case`, and make R5 check how soon the agent acts on a hazard.
- An approval queue where a property manager clears held actions.
- Connect a real property-management system through MCP, so the tools hit live data.
- More escalation cases in the eval.
- Prompt caching, the obvious next cost saving: about 48k input tokens per case today.

## Branches and tags

- `main`: this project.
- `starting-repo`: the untouched starting repo.
- `reality-test`, `reconstruction`: the unseen cases and other teams' answers, kept apart so
  they could not leak into the build.
- Tags: `freeze` is the code that ran the holdout and Reality Test. `results` is the committed
  `ANSWERS/`.
