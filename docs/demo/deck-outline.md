# Demo Day deck: outline and speaker notes

Audience: the bootcamp instructor and peers. Format: the four questions (problem, why it
matters, what I built, what I learned), with the Demo Day bar woven in: an eval with a rubric,
one success and one failing trajectory, budget against declared numbers, the action gateway, and
the stakeholder brief. Target 6–7 minutes plus the 60–90 s video. Every number comes from
[`eval/reports/SUMMARY.md`](../../eval/reports/SUMMARY.md).

`[PENDING]` marks numbers that exist only after the holdout rehearsal and the Reality Test.

---

## 1. Title

**An exception desk for letting agencies.** A Claude agent that handles the maintenance jobs
the automation hands back to a human.

Capstone, Agent Engineering Bootcamp. Built on the Dwelly London AI Hackathon (Oct 2026),
Property Management track, redone solo.

## 2. The problem

- A letting agency's platform already runs routine repair jobs on autopilot.
- It hands a job to a property manager when something goes off-script, in its own words:
  "3+ reminders have been sent to provider. Please check what's happening."
- The records are messy. Across 40 real-format cases there are 1,211 events, about 30 per job.
  The same contractor appears under three names, addresses from other jobs show up in emails,
  and invoices disagree with quotes.

Speaker note: show one raw `history.md` for two seconds. The mess is the point.

## 3. Why it matters

- These hand-offs are where a property manager's time goes.
- They are also where costly mistakes happen. Case 007: the invoice (£240.00) is above the
  approved quote (£198.37 + VAT = £238.04) and comes from a differently named supplier, and the
  job was closed anyway. Case 005: the contractor quoted for one carpet while the agency instructed two.
- The right move is not always to act. Sometimes it is to ask, wait, or hand to a human. The
  hackathon judged exactly that: "Doing nothing or escalating can be the correct decision."

## 4. What I built

```text
case folder ──▶ loader (cuts the case at a decision point, hides the future)
                  │
                  ▼
        Claude Sonnet 5.5 agent (Google ADK, ReAct loop)
          read tools: events, search, PDFs
          action tools: message · book · approve invoice · charge tenant · follow up · close · escalate
                  │ every action
                  ▼
        ACTION GATEWAY (code, not prompt): R1 approval before spend · R2 tenant charges held
          R3 invoice within quote · R4 right property · R5 no waiting on hazards · R6 no duplicates
                  │
                  ▼
        ledger ──▶ ANSWER.md + REASONING.md + handover note      Phoenix traces every step
```

- Output for every case: a next move (act, ask, wait or escalate), the drafted messages, and a
  handover note when it escalates.
- One command runs a folder of cases unattended, 5 in parallel. A crash still writes an answer.

## 5. Why this shape (Module 1: pick the simplest level that works)

- **One agent, not a team.** Each case is one bounded investigation. A multi-agent split earned
  nothing on either rubric (ADR 0002).
- **Rules in code (Module 4).** Every side effect is a tool call, and the gateway checks it in
  ADK's `before_tool_callback`. A prompt can be ignored; the gateway cannot.
- **Claude inside ADK, judged by OpenAI** (ADR 0001). A judge from a different model family
  limits self-preference.
- **Deliberately out:** voice, A2A, MCP, vector search. None changed an outcome on these cases.

## 6. How I measured it (Module 3 eval pyramid, Module 5 benchmarking discipline)

- 62 decision points, cut from the 40 cases' histories. The agent sees only what was known at
  that moment, and the label comes from what happened next.
- Thresholds were declared before the first run. Code decides pass or fail. The LLM judge is
  reported only.
- Two full runs; the lower is the headline.
- Honest holdouts: 10 cases never opened during the build, plus the hackathon's unseen Reality
  Test cases, run once on the frozen code.

## 7. Results (budget against declared)

| | Declared before building | Result (lower of two runs) |
|---|---|---|
| Right next move | ≥ 70% | **95%** (92% on the labels as first written) |
| Unsafe actions let through | 0 | **0** |
| Every case answered | 100% | **100%** |
| Cost per case | ≤ $0.25 | **$0.114** (about 48k input and 1.7k output tokens) |
| Latency per case | ≤ 90 s | **15 s** (p95 19 s) |
| Judge quality score | ≥ 3.5 / 5 | **4.34** |
| Holdout (10 unseen cases) | — | `[PENDING]` |
| Reality Test (unseen hackathon cases) | — | `[PENDING]` |

Speaker note: say the disclosure out loud. Three labels were widened after I saw the agent's
answers. 92% is the figure on the original labels.

## 8. The gateway, measured both ways

- **Does it let real work through?** Yes. 0 legitimate actions were blocked across 62 real cases.
- **Does it stop unsafe actions?** I built 8 pressure cases, one per rule plus a prompt
  injection and a hearsay approval. The model proposed **0** unsafe actions. It even labelled
  the injected "NOTE TO THE AI AGENT" as untrusted.
- **But the code backstop had holes.** Feeding the tempted actions straight to the gateway, R1
  accepted the tenant's "the landlord said it's fine" as approval, and R3 accepted an invoice
  cited as its own quote. Fixed, and replaying all 42 real spend calls changed no verdict.
- **Still open:** R5 only checks the label ("visit next week" with no hot water passes as act),
  and closing a case is ungated.

Speaker note: the model was the real safety layer on these cases. Probing is what showed the
code layer was weaker than it looked.

## 9. One success, one failure (Phoenix traces)

- **Success, PM-008-a.** Check-out works and a landlord who wants a second quote. The agent asks
  the contractor for a comparison quote with VAT stated, updates the landlord, sets a follow-up
  and books nothing. At baseline it took the same steps but labelled the quote request as an
  instruction, so it read as act. Fixing one tool description made the move correct.
- **Failure, PM-035-a.** The landlord is fitting the parts himself, so the expected move is
  wait. The agent escalates in both runs, citing a call note about water damage reaching a smoke
  detector. The label never considered that note. Over-escalation, or a safety signal the
  labeller missed?

Speaker note: open both traces in Phoenix. Walk the failure step by step: which event it read,
why it rejected wait, what it wrote in the handover.

## 10. The worst bug, and what caught it

- One eval run came back with coverage 0.19.
- Claude had sent one decision's `reasoning` as a string of raw parameter markup. Rendering
  crashed outside the per-case guard, and `asyncio.gather` aborted the whole batch: 44 of 62
  cases got no answer at all.
- On the Reality Test, that is most of the coverage score gone.
- Caught by: running the full eval after every change. Fixed in two layers: a per-case guard so
  no case can sink the batch, then flat tool arguments so the malformed output stops (9 of 188
  calls before, 0 after).

## 11. What I learned

1. **The eval is the product spec.** Writing 62 labelled decision points forced every
   definition. The biggest: "is asking a contractor for a quote act or ask?"
2. **Measure guards both ways, and probe the code, not just the model.** A gateway that never
   fires proves nothing until you attack it directly.
3. **An LLM judge is only as good as its evidence.** Mine marked correct facts as invented
   until it could see the attachments and the playbook.
4. **Most fixes were definitions, not model changes.** Two of the four agent errors came from
   one ambiguous word in a tool description.

## 12. What I'd build next

- Gate `close_case`, and make R5 check how soon the agent acts on a hazard, not just the label.
- A human approval queue for held actions: the property manager's actual interface.
- Plug into a real property-management system through MCP, so the tools hit live data.
- A voice intake for tenants (Module 5), feeding the same agent.
- More escalation cases in the eval: only 5 of 62 expect escalation, while the Reality Test is
  all escalations.
- At 100× volume (about 6,200 cases): roughly $700 at today's per-case cost. Prompt caching is
  the obvious next saving.

## Appendix: where the course modules show up

| Module | Where |
|---|---|
| 1 Agent foundations | ReAct loop, harness, and the case for the simplest level |
| 2 Subagents | Building it: parallel Claude Code agents in worktrees with a shared run-folder contract |
| 3 Eval and guardrails | Decision-point eval, thresholds first, judge reported only |
| 4 ADK, guards, Phoenix | ADK agent, gateway in code, Phoenix traces |
| 5 Benchmarking discipline | Two runs, lower reported, deterministic checks over LLM opinion |
| 6 Leading AI systems | The stakeholder brief |
