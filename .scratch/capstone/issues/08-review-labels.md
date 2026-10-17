# 08 Human review of decision-point labels

Status: ready-for-human
Blocked by: 06

## What

Review 10 decision points picked across the move mix from `eval/decision_points/README.md`
(about 20 minutes). For each: does the expected move match your judgement, and are the
acceptable alternatives and prohibited actions fair? Fix or note disagreements, then set
`"reviewed": true` on the ones you checked. This breaks the circle of Claude writing labels
for a Claude agent.

## Acceptance criteria

- [ ] 10 files have `"reviewed": true`; corrections are committed as `test: review decision point labels`.
