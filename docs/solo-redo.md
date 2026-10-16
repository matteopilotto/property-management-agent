# Running the hackathon solo

The official rules assume a team of 2–5 on a fixed day. Team size, registration, the submission form and the launch posts don't apply when you're on your own. Everything else does, especially the clock and the "no human in the loop at 16:30" rule. Those are what make the Reality Test meaningful.

## 1. Before you start

1. Pick a track.
2. Read [`rules.md`](rules.md), then [`hacker-guide.md`](hacker-guide.md), then the [public cases README](../HackatonPublicCases/README.md).
3. Skim [`kickoff-transcript.md`](kickoff-transcript.md). It's an automatic transcript, and "Core 30" means 16:30.
4. Create your working branch from `main`, e.g. `git switch -c solution`.

## 2. The clock

You can spread the build over several sessions. Two rules keep it honest:

| Official time | Solo equivalent |
|---|---|
| 10:00–16:30 build (6.5 h) | Build only against `HackatonPublicCases/`. Keep a rough count of build hours if you want to compare with the event. |
| 16:30 freeze | Commit the code and the demo video, then tag the commit: `git tag freeze`. From here on, no code changes. |
| 16:30–17:00 Reality Test | Bring in the unseen cases (§4) and run the frozen system unattended, with a 30-minute wall-clock budget. |
| 17:00 results freeze | Commit `ANSWERS/`, then tag it: `git tag results`. Only then look at evaluation material (§5). |

## 3. Testing on the public cases (the organisers' method)

From the [public cases README](../HackatonPublicCases/README.md):

1. Choose a decision point in the history.
2. Give the system only the events and attachments available at that point.
3. Hide later events and any summary or outcome that reveals the ending.
4. Compare the system's decision with the later evidence. The recorded outcome is one acceptable answer, not the only one.

Practical additions:

- **Hold out 10–15 of your track's 50 cases** and don't look at them while building. They are your private dress rehearsal.
- **Cut more than one decision point per case.** Many cases have several moments where the right move is to act, ask, wait or escalate. Doing nothing or escalating can be correct.
- **Rehearse the 16:30 run** on the holdout cases: one command, unattended, timed, writing `ANSWERS/<n>/ANSWER.md` + `REASONING.md`.
- **Expect the unexpected.** The organisers warned that the 16:30 cases would be unusual and "in real life sometimes everything is broken". Make your loader and agent tolerant of input they haven't seen before.

Advice from the kickoff talk (Anthropic Applied AI):

- Build the test suite first and rerun it on every significant change; fixes for one case quietly regress others.
- Test messy cases, not only the happy path.
- Give tools timeouts and report failures back to the agent, so it never hangs waiting.
- Use structured outputs for anything another system consumes, and put a human-in-the-loop hook before irreversible actions.
- Let Claude read documents and images directly instead of building OCR.

## 4. The Reality Test

At your "16:30", with the freeze tag in place, run this from your working branch:

```bash
git checkout reality-test -- HackatonChallenges   # brings in the cases only, nothing else
```

Then follow the rules:

- Run the frozen system unattended, and make sure every case gets an answer. A clear "failed, escalated to a human" record beats a missing folder.
- **Never hand-edit an answer.** Re-running the same frozen code on a crashed case is fine; patching the code isn't.
- Write `ANSWERS/<n>/ANSWER.md` and `REASONING.md` for each case, plus a trace where practical (see [`../submission-template/`](../submission-template/)).
- Commit `ANSWERS/` and tag `results`.

## 5. Afterwards

Switch to the `reality-test` branch and read `evaluation/README.md`. It explains how to score your answers against the judging criteria and compare them with what the real teams did on the same cases.
