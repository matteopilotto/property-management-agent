# Property Management

The back office of a letting agency that coordinates maintenance jobs between tenants,
landlords and contractors. The system handles the moments where routine automation stops
and a property manager would otherwise have to step in.

## Parties

**Agency**:
The letting agency that manages the property on the landlord's behalf and coordinates every job.
_Avoid_: Northbridge, company, platform

**Property Manager**:
The agency staff member who owns a job and receives every escalation.
_Avoid_: PM, agent, operator, supervisor

**Tenant**:
The person living in the property who usually reports the problem.
_Avoid_: TT, T, Ts, resident, customer

**Landlord**:
The property owner who approves and pays for work unless the tenant is liable.
_Avoid_: LL, owner, client

**Contractor**:
The third party that quotes for, visits and does the work.
_Avoid_: Provider, maintenance provider, supplier, tradesperson

## Cases

**Case**:
One maintenance job at one property: the initial request, its time-ordered history of events and any attachments.
_Avoid_: Ticket, request, job (in code), issue

**Event**:
One timestamped entry in a case history: an email, call summary, SMS, note, hold or system update.
_Avoid_: Message, log entry

**Decision Point**:
A moment in a case at which only the events up to that moment are known and the agency must choose what to do next.
_Avoid_: Cutoff, checkpoint, snapshot

**Next Move**:
The single choice made at a decision point: **act**, **ask**, **wait** or **escalate**. When a decision point involves several actions, the move is the most consequential one, ranked escalate > act > ask > wait.
_Avoid_: Decision, outcome, resolution

**Act**:
The agency moves the job forward itself, for example by instructing a contractor, forwarding an invoice to the landlord for payment, confirming a visit or closing the job. Sending a quote to the landlord for approval is ask, not act.

**Ask**:
The agency requests missing information or a decision from the tenant, landlord or contractor, including chasing a party already asked.
_Avoid_: Chase, remind (as separate moves)

**Wait**:
The agency sends nothing now and schedules a dated follow-up with a reason.
_Avoid_: Hold, pause, no action

**Escalate**:
The system hands the case to the property manager with a handover note because it should not decide alone.
_Avoid_: Refer, flag, defer

**Outcome**:
What actually happened in a case after a decision point, as recorded later in its history. One acceptable answer, not the only one.
_Avoid_: Ground truth, label, expected answer

## Acting

**Action**:
A concrete side effect the system proposes, such as sending a message, booking a contractor or escalating to the property manager.
_Avoid_: Tool call, step, task

**Action Gateway**:
The single checkpoint every action passes through, which approves, blocks or holds it for human approval according to agency policy.
_Avoid_: Guard, gate, filter, middleware

**Handover Note**:
The summary left for the property manager when a case is escalated: what is known, what conflicts, what was done and what is needed.
_Avoid_: Summary, escalation message

## Evaluation

**Holdout**:
The ten public cases listed in `docs/holdout.md`, kept unseen during building and opened only for the dress rehearsal.
_Avoid_: Test set, validation set

**Reality Test**:
The unseen escalation cases released after the code freeze, run unattended by the frozen system.
_Avoid_: Challenge set, final test
