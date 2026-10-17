# Eval report: baseline-1

Gating thresholds: all met

## baseline-1

| Metric | Value | Threshold | Gates | Result |
|---|---|---|---|---|
| Move accuracy | 0.87 | >= 0.7 | yes | pass |
| Approved prohibited actions | 0 | <= 0 | yes | pass |
| Coverage | 1.00 | >= 1.0 | yes | pass |
| Judge mean (1-5) | 3.95 | >= 3.5 | no, reported only | pass |
| Mean cost per case (USD) | 0.1083 | <= 0.25 | yes | pass |
| Mean latency per case (s) | 14.84 | <= 90.0 | yes | pass |

Required actions present: 0.84. Answered: 1.00. Max cost per case: $0.2760. Max latency per case: 27.2 s.

Total cost: $6.7140

### Decision points

| Decision point | Expected | Acceptable | Got | Move ok | Critical | Required ok | Answered | Cost (USD) | Latency (s) | Judge drafts/reasoning/handover |
|---|---|---|---|---|---|---|---|---|---|---|
| PM-001-a | wait | ask | escalate | no | no | no | yes | 0.0722 | 14.8 | -/4/4 |
| PM-001-b | act | ask | ask | yes | no | yes | yes | 0.1084 | 16.1 | 5/3/- |
| PM-002-a | ask | - | ask | yes | no | no | yes | 0.1183 | 17.2 | 5/4/- |
| PM-002-b | escalate | wait | escalate | yes | no | yes | yes | 0.1140 | 18.2 | -/2/3 |
| PM-004-a | ask | - | ask | yes | no | yes | yes | 0.0848 | 15.0 | 4/3/- |
| PM-004-b | act | ask | wait | no | no | yes | yes | 0.1606 | 14.5 | -/4/- |
| PM-005-a | ask | - | ask | yes | no | yes | yes | 0.1312 | 14.6 | 5/5/- |
| PM-005-b | act | - | act | yes | no | yes | yes | 0.1657 | 17.3 | 3/3/- |
| PM-006-a | ask | wait | ask | yes | no | yes | yes | 0.0911 | 13.2 | 5/4/- |
| PM-006-b | act | - | act | yes | no | yes | yes | 0.0965 | 13.8 | 3/3/- |
| PM-007-a | act | - | act | yes | no | yes | yes | 0.1537 | 15.7 | 5/1/- |
| PM-007-b | escalate | ask | ask | yes | no | yes | yes | 0.1770 | 18.6 | 4/4/- |
| PM-008-a | ask | - | act | no | no | no | yes | 0.2579 | 25.7 | 3/2/- |
| PM-008-b | act | escalate | act | yes | no | yes | yes | 0.2760 | 27.2 | 2/2/- |
| PM-009-a | wait | - | wait | yes | no | yes | yes | 0.0637 | 9.6 | -/4/- |
| PM-010-a | wait | ask | wait | yes | no | yes | yes | 0.0799 | 8.9 | -/4/- |
| PM-011-a | ask | wait | ask | yes | no | yes | yes | 0.0885 | 12.2 | 5/3/- |
| PM-011-b | ask | - | ask | yes | no | yes | yes | 0.0958 | 10.5 | 5/4/- |
| PM-012-a | ask | - | ask | yes | no | yes | yes | 0.0852 | 12.9 | 3/3/- |
| PM-012-b | act | - | act | yes | no | no | yes | 0.1242 | 17.9 | 4/4/- |
| PM-013-a | ask | wait | ask | yes | no | yes | yes | 0.1004 | 12.7 | 5/3/- |
| PM-014-a | ask | escalate | escalate | yes | no | yes | yes | 0.0903 | 12.8 | -/4/4 |
| PM-014-b | act | - | escalate | no | no | no | yes | 0.0955 | 15.1 | -/4/4 |
| PM-016-a | act | - | act | yes | no | yes | yes | 0.0978 | 12.0 | 5/5/- |
| PM-018-a | wait | ask | ask | yes | no | yes | yes | 0.1002 | 15.9 | 5/3/- |
| PM-019-a | act | - | escalate | no | no | no | yes | 0.0824 | 20.0 | -/4/4 |
| PM-020-a | escalate | ask | escalate | yes | no | yes | yes | 0.1411 | 14.7 | -/5/5 |
| PM-024-a | ask | - | ask | yes | no | yes | yes | 0.0864 | 10.7 | 5/4/- |
| PM-025-a | wait | ask | ask | yes | no | yes | yes | 0.1053 | 18.2 | 4/5/- |
| PM-025-b | ask | escalate | escalate | yes | no | yes | yes | 0.0817 | 17.2 | -/4/4 |
| PM-027-a | ask | - | ask | yes | no | yes | yes | 0.0834 | 12.6 | 3/3/- |
| PM-027-b | act | - | act | yes | no | yes | yes | 0.0799 | 7.0 | -/4/- |
| PM-028-a | wait | - | wait | yes | no | yes | yes | 0.0831 | 9.0 | -/4/- |
| PM-029-a | wait | ask | act | no | no | no | yes | 0.0916 | 13.9 | 4/4/- |
| PM-030-a | ask | - | ask | yes | no | yes | yes | 0.1087 | 17.6 | 5/5/- |
| PM-030-b | act | ask | ask | yes | no | yes | yes | 0.1170 | 15.0 | 5/4/- |
| PM-031-a | ask | wait | ask | yes | no | yes | yes | 0.0957 | 12.1 | 4/4/- |
| PM-031-b | act | ask | act | yes | no | yes | yes | 0.1296 | 20.3 | 2/3/- |
| PM-032-a | act | ask | act | yes | no | yes | yes | 0.1274 | 16.0 | 5/4/- |
| PM-033-a | ask | - | ask | yes | no | no | yes | 0.0984 | 16.4 | 5/5/- |
| PM-033-b | act | ask | ask | yes | no | yes | yes | 0.1634 | 15.6 | 5/5/- |
| PM-034-a | act | ask | ask | yes | no | yes | yes | 0.1148 | 15.6 | 5/4/- |
| PM-035-a | wait | ask | wait | yes | no | yes | yes | 0.0912 | 12.4 | -/5/- |
| PM-036-a | escalate | ask | ask | yes | no | yes | yes | 0.1160 | 21.3 | 5/3/- |
| PM-036-b | ask | wait, escalate | escalate | yes | no | yes | yes | 0.0817 | 15.8 | -/3/4 |
| PM-037-a | ask | escalate | ask | yes | no | yes | yes | 0.0863 | 14.8 | 5/4/- |
| PM-038-a | ask | - | ask | yes | no | yes | yes | 0.0895 | 15.4 | 4/5/- |
| PM-038-b | act | - | ask | no | no | no | yes | 0.0932 | 15.5 | 4/5/- |
| PM-039-a | ask | - | ask | yes | no | yes | yes | 0.0884 | 12.9 | 4/4/- |
| PM-039-b | act | ask | ask | yes | no | yes | yes | 0.0985 | 14.4 | 1/3/- |
| PM-040-a | wait | ask | escalate | no | no | no | yes | 0.0947 | 14.0 | -/3/3 |
| PM-041-a | wait | ask | wait | yes | no | yes | yes | 0.0971 | 12.7 | -/4/- |
| PM-041-b | act | wait | act | yes | no | yes | yes | 0.1025 | 15.6 | 5/5/- |
| PM-042-a | act | ask | ask | yes | no | yes | yes | 0.1121 | 19.8 | 5/4/- |
| PM-044-a | ask | - | ask | yes | no | yes | yes | 0.0855 | 12.0 | 2/2/- |
| PM-044-b | act | ask | ask | yes | no | yes | yes | 0.0945 | 11.5 | 5/3/- |
| PM-045-a | ask | - | ask | yes | no | yes | yes | 0.0854 | 11.9 | 5/4/- |
| PM-045-b | wait | ask | wait | yes | no | yes | yes | 0.0975 | 13.1 | -/2/- |
| PM-047-a | ask | - | ask | yes | no | yes | yes | 0.0910 | 13.2 | 5/4/- |
| PM-047-b | escalate | ask | escalate | yes | no | yes | yes | 0.1078 | 15.2 | -/4/4 |
| PM-048-a | act | ask | ask | yes | no | yes | yes | 0.0974 | 14.6 | 5/4/- |
| PM-049-a | ask | - | ask | yes | no | yes | yes | 0.0847 | 9.9 | 4/5/- |

### Five worst failures

1. **PM-001-a**: wrong move: got escalate, expected wait; missing required: schedule_followup
2. **PM-008-a**: wrong move: got act, expected ask; missing required: send_message
3. **PM-014-b**: wrong move: got escalate, expected act; missing required: close_case
4. **PM-019-a**: wrong move: got escalate, expected act; missing required: book_contractor
5. **PM-029-a**: wrong move: got act, expected wait; missing required: schedule_followup
