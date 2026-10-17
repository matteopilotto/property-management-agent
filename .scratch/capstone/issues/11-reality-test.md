# 11 Reality Test run

Status: done
Blocked by: 10

## What

Follow [`docs/solo-redo.md`](../../../docs/solo-redo.md) §4: `git checkout reality-test --
HackatonChallenges`, run `pm-agent run "<Property Management folder>" --out ANSWERS` unattended
within 30 minutes, never hand-edit an answer, commit `ANSWERS/`, `git tag results`. Only then
read `evaluation/README.md` on the `reality-test` branch and score.

## Acceptance criteria

- [ ] Every Reality Test case has an answer folder; `results` tag exists; `git diff freeze -- src/` is empty.
