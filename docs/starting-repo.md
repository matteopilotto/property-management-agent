# Real-World Agents Hackathon: starting repo

> This was the README of `starting-repo`, the untouched starting repo. The project built on it is described in the [root README](../README.md).

This is the material participants had when building began at 10:00 on Saturday 10 October 2026, at the Dwelly London AI Hackathon ("AI Transformation of Services"). It is reconstructed so the hackathon can be redone solo.

> Build an AI agent that can take an operational case from first contact to a positive outcome, and that knows when to escalate to a human.

## What's here

| Path | What it is |
|---|---|
| [`HackatonPublicCases/`](../HackatonPublicCases/) | The synthetic data: **200 public practice cases**, 50 per track. A verbatim copy of `DwellyOrg/HackatonPublicCases` (the spelling is the organisers'). Start with its [README](../HackatonPublicCases/README.md). |
| [`docs/rules.md`](rules.md) | **Official rules**: the "Rules, Judging & Submission Guide — v1". If anything else here disagrees, this wins. |
| [`docs/hacker-guide.md`](hacker-guide.md) | The organisers' Notion Hacker Guide: agenda, tracks, prizes, judging, submission, fair play. |
| [`docs/kickoff-transcript.md`](kickoff-transcript.md) | The 09:30 welcome talk: the Dwelly host, then Anthropic's Applied AI team on building agents. |
| [`docs/elevenlabs-guide.md`](elevenlabs-guide.md) | ElevenLabs Hacker Guide, for the voice prize. |
| [`docs/solo-redo.md`](solo-redo.md) | How to run the day on your own: the clock, testing against the practice cases, and the Reality Test procedure. |
| [`submission-template/`](../submission-template/) | The required submission layout: LICENSE, README sections, `ANSWERS/<n>/ANSWER.md` + `REASONING.md`, demo video, form fields. |

## The challenge in one page

**Tracks.** Pick one: Insurance Claims Processing, Property Management, Banking & Financial Services, or Delivery & Logistics. The synthetic data is "an environment, not a specification": you choose the scope and architecture.

**Cases.** Each case folder has the following files (details in the [public cases README](../HackatonPublicCases/README.md)):

- `index.md`: the request, case details, and sometimes a summary or outcome.
- `history.md`: emails, calls and notes in time order.
- `attachments/`: optional documents, images or data.

**The day.**

| Time (BST) | What happens |
|---|---|
| 10:00–16:30 | Build against the public cases. |
| 16:30 | **Code and 60-second demo video freeze.** Unseen "Reality Test" cases are released, 30 per track. |
| 16:30–17:00 | The frozen system processes the unseen cases **unattended**. There is deliberately not enough time to do them by hand. |
| 17:00 | **Results freeze.** `ANSWERS/` must be committed. |

**What the Reality Test checks.** The test cases include conflicting information, failed actions, missing context, unusual exceptions, noise and larger context. For each case the system decides what to do next, acts where appropriate, and escalates what needs a human. **Doing nothing or escalating can be the correct decision.** There is no single exact textual answer. The organisers' per-case rubric may define required outcomes, acceptable alternatives, positive behaviours, red flags, prohibited actions and critical failures.

**Judging.** Overall score = 70% technical + 30% demo.

| Technical criterion | Weight within technical |
|---|---|
| Correct outcomes | 35% |
| Coverage (how many of the cases the system actually completes) | 20% |
| Judgement & safety | 20% |
| Engineering quality | 15% |
| Real-world applicability | 10% |

Claude-based judging agents score submissions against the framework, and human judges review close or ambiguous cases. More agents, a bigger codebase, a fancier UI or a pricier model earn nothing. A simple, reliable system can win. Never put text aimed at the judge in your outputs: it can zero your score.

**On the day.** No tool API was supplied: teams mocked or recorded their tools (sending messages, booking, holds, escalation). Make clear in your answers which actions really ran and which were only recorded.

## Branches

- `starting-repo` is your starting point. Develop on your own branch from here.
- `reality-test` holds the unseen cases and material for evaluating afterwards. **Don't open it until your code is frozen.** [`docs/solo-redo.md`](solo-redo.md) explains how to pull in only the cases at "16:30".
