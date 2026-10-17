# Exception desk for maintenance jobs: one-page brief

For: the operations director of a letting agency. Status: a working prototype, tested on 40
past jobs. It has not run on live data.

## What it does

Our maintenance platform already runs routine repair jobs on its own. When a job goes
off-script, it hands the job to a property manager: a contractor stops replying, an invoice
doesn't match the quote, nobody is sure who pays, or the records contradict each other.

The exception desk takes those hand-offs first. It reads the job's full history and documents,
then does one of four things:

- **acts**: for example, books the approved contractor or forwards an invoice for payment;
- **asks**: requests missing information or a decision from the tenant, landlord or contractor;
- **waits**: sets a dated follow-up;
- **escalates**: passes the job to a property manager with a short note saying what's known,
  what conflicts and what decision is needed.

It drafts every message. Anything involving money or the tenant's liability waits for a person
to approve it.

## What it costs per run

About **9p (US$0.11) per job** handled, and about **15 seconds**. A thousand exceptions a
month would cost under £100 in model usage. Hosting and integration work are not included.

## How well it works today

- On 62 past decisions it chose the same next step a good property manager would **95% of the
  time** (92% before three labels were widened).
- It answered every job.
- It made no unsafe commitments.
- On 8 deliberately tricky jobs it refused every unsafe shortcut. These included a landlord
  demanding we deduct a repair from the tenant's rent, an invoice above the quote, and a forged
  instruction hidden in an email.
- On 10 jobs it had never seen (17 decisions), it made an acceptable call every time, with no
  unsafe actions.

## What could go wrong

- **Wrong call on a judgement case.** It sometimes escalates when a person would simply wait.
  That is the safe direction, but it costs staff time.
- **A safety issue handled too slowly.** The system blocks "wait" when it sees a hazard such as
  gas or no hot water. It does not yet stop a visit booked a week out for the same hazard.
- **Closing a job too early.** Closing is not yet behind an approval step.
- **Bad data in, bad data out.** Our records contain wrong addresses and duplicate names. It
  usually spots these, but not always.

## The policy that would govern it

1. It never spends money, approves an invoice or charges a tenant without recorded approval.
   These rules are written into the software, not just into its instructions.
2. Every action it proposes is logged, with the reason, and can be audited.
3. Anything it is unsure about, or that involves safety or liability, goes to a property
   manager.
4. It starts in "draft only" mode: a property manager approves each message before it is sent,
   until the error rate on live jobs is known.

## The one metric to track

**The share of handed-off jobs that the desk resolves without a property manager changing its
decision.** Track it weekly, alongside the count of unsafe actions it proposed, which must stay
at zero.
