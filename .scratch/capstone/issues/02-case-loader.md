# 02 Case loader and decision-point views

Status: done
Track: A (agent core)
Blocked by: 01

Spec: [`../spec.md`](../spec.md) §4, §6.

## What

`case.py`: `load_case(path)` and `view(case, visible_through, mode)` as specified, including
raw mode for unfamiliar folders and the `eval`-mode whitelist.

## Acceptance criteria

- [ ] All 40 non-holdout cases parse with the event count equal to `Total events: N`. The test enumerates the folders and skips the holdout numbers from `docs/holdout.md` without opening them.
- [ ] In `eval` mode, the view for case 004 at event 10 contains no text from the Overview or Outcome sections and no event after 10, and lists only `attachment-01-checkout-inspection-report.pdf`.
- [ ] A folder with only a `notes.txt` and a PDF loads in raw mode without raising.
- [ ] `live` mode exposes extra `index.md` sections and detects a section that asks a question (test with a synthetic fixture).
