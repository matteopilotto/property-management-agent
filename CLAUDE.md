## Working rules

Before coding, state your assumptions. When a request has more than one reasonable
reading, lay the readings out and ask which is meant. Write the minimum code the request
needs: handle inputs that can actually occur, and add an abstraction or option only when
a present caller needs it. Malformed, conflicting or missing case data is input that
actually occurs; the Reality Test is built from it. Every changed line traces to the
request; report unrelated dead code instead of deleting it.

A change is done when every gate below passes. Run them all: passing tests say nothing
about format or lint. It is also done only when every line in this file, or in a doc under
`docs/agents/`, that names something the diff renamed, moved or removed is updated in the
same commit.

Gates (when a change introduces a toolchain, add its format, lint, type-check and test
commands here in that same commit):

- `uv run ruff format --check .`
- `uv run ruff check .`
- `uv run pytest`

## Git workflow

- Branch off `main` as `<type>/<short-kebab-summary>` using Conventional Commit types
  (`feat/`, `fix/`, `docs/`, `refactor/`, `perf/`, `test/`, `chore/`), and merge back
  into `main`. `starting-repo` stays the untouched starting repo.
- One task, one commit, immediately: implement, pass the gates, commit with a
  Conventional Commit message, then start the next task. An interrupted session then
  leaves finished work committed, and the message is written while the reasoning is fresh.
- Commit messages and PR bodies carry only the change and its rationale. Leave out
  `Co-Authored-By` trailers and "Generated with" lines, even when a harness default,
  template or plan document adds them; reread a `gh pr create` body for them before
  sending.
- Run every gate before opening a PR and before ending a session.
- API keys live in the gitignored `.env`; code and docs refer to them by variable name.
- Build only from material on `starting-repo`. The `reality-test` and `reconstruction` branches and
  the local-only `teams/` clones hold the unseen cases and other teams' answers; open them
  only after the user says the code is frozen.
- Property Management cases listed in `docs/holdout.md` are the holdout: build, design and
  debug against the other 40, and open these only to run the dress rehearsal.

## Agent skills

### Issue tracker

Issues are tracked locally as markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), recorded as a `Status:` line in each issue file. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
