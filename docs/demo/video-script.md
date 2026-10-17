# Demo video: 75-second script

A screen recording with voice-over, under 90 seconds. Record it after the freeze, so it shows
the frozen system. Have these open: a terminal at the repo root, Phoenix
(`uvx arize-phoenix serve`, http://localhost:6006, project `pm-agent`), and
`eval/reports/final-2-board.html` in a browser.

| Time | Screen | Voice-over |
|---|---|---|
| 0–10 s | A raw `history.md` from case 008, scrolling | "Letting agencies automate routine repairs. The jobs that go off-script land on a property manager, and the records look like this: 49 events, addresses from other jobs, quotes that disagree." |
| 10–25 s | Terminal: `uv run pm-agent eval --run-id demo --only PM-008-a`, output scrolling | "This agent takes those jobs. It sees the job only up to the moment a decision is due, and decides: act, ask, wait or escalate." |
| 25–45 s | Phoenix: the PM-008-a trace. Expand the `read_attachment` calls, then the `send_message` calls | "Here it reads the check-out report PDFs, sees the landlord wants a second quote, asks the contractor for one with VAT stated, updates the landlord, and books nothing. Every action goes through a gateway written in code." |
| 45–55 s | `runs/demo/PM-008-a/ANSWER.md` | "The output is a decision, the drafted messages, and a handover note a human can pick up." |
| 55–70 s | The scoreboard HTML: headline metrics, then scroll the rows | "Across 62 past decisions: the right move 95% of the time, every job answered, zero unsafe actions, 11 cents and 15 seconds a job." |
| 70–75 s | `eval/pressure/README.md` table | "And when I tried to trick it into charging a tenant or paying an inflated invoice, it refused every time, with a code gateway behind it as the backstop." |

Before recording: run the `--only PM-008-a` command once to check it works. It costs about
$0.25, and its move can vary between runs. If the live run picks a different move, record the
committed `final-2` trace instead and say "from the final eval run".
