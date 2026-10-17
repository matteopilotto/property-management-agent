# Eval report: final-2

Gating thresholds: all met

## final-2

| Metric | Value | Threshold | Gates | Result |
|---|---|---|---|---|
| Move accuracy | 0.95 | >= 0.7 | yes | pass |
| Approved prohibited actions | 0 | <= 0 | yes | pass |
| Coverage | 1.00 | >= 1.0 | yes | pass |
| Judge mean (1-5) | 4.34 | >= 3.5 | no, reported only | pass |
| Mean cost per case (USD) | 0.1136 | <= 0.25 | yes | pass |
| Mean latency per case (s) | 15.05 | <= 90.0 | yes | pass |

Required actions present: 0.89. Answered: 1.00. Max cost per case: $0.4012. Max latency per case: 31.3 s.

Total cost: $7.0462

### Decision points

| Decision point | Expected | Acceptable | Got | Move ok | Critical | Required ok | Answered | Cost (USD) | Latency (s) | Judge drafts/reasoning/handover |
|---|---|---|---|---|---|---|---|---|---|---|
| PM-001-a | wait | ask | ask | yes | no | yes | yes | 0.0955 | 13.6 | 5/4/- |
| PM-001-b | act | ask | wait | no | no | no | yes | 0.1078 | 14.1 | -/3/- |
| PM-002-a | ask | - | ask | yes | no | no | yes | 0.0950 | 14.2 | 5/5/- |
| PM-002-b | escalate | wait | escalate | yes | no | yes | yes | 0.1180 | 19.0 | -/4/4 |
| PM-004-a | ask | - | ask | yes | no | yes | yes | 0.0848 | 12.9 | 5/5/- |
| PM-004-b | act | ask, wait | act | yes | no | yes | yes | 0.1702 | 19.8 | 2/4/- |
| PM-005-a | ask | - | ask | yes | no | yes | yes | 0.1322 | 14.1 | 5/5/- |
| PM-005-b | act | - | act | yes | no | yes | yes | 0.2262 | 18.6 | 4/4/- |
| PM-006-a | ask | wait | ask | yes | no | yes | yes | 0.0924 | 13.4 | 4/4/- |
| PM-006-b | act | - | act | yes | no | yes | yes | 0.1216 | 14.6 | 5/5/- |
| PM-007-a | act | - | act | yes | no | yes | yes | 0.1539 | 13.6 | 5/4/- |
| PM-007-b | escalate | ask | ask | yes | no | yes | yes | 0.1797 | 18.1 | 3/3/- |
| PM-008-a | ask | - | ask | yes | no | yes | yes | 0.2512 | 18.5 | 5/5/- |
| PM-008-b | act | escalate | act | yes | no | yes | yes | 0.4012 | 26.7 | 5/4/- |
| PM-009-a | wait | - | wait | yes | no | yes | yes | 0.0848 | 8.8 | -/4/- |
| PM-010-a | wait | ask | wait | yes | no | yes | yes | 0.0826 | 11.0 | -/5/- |
| PM-011-a | ask | wait | ask | yes | no | yes | yes | 0.0891 | 12.1 | 4/4/- |
| PM-011-b | ask | - | ask | yes | no | yes | yes | 0.1004 | 13.0 | 5/4/- |
| PM-012-a | ask | - | ask | yes | no | yes | yes | 0.0897 | 14.8 | 5/5/- |
| PM-012-b | act | - | act | yes | no | no | yes | 0.0975 | 15.8 | 4/3/- |
| PM-013-a | ask | wait | ask | yes | no | yes | yes | 0.1023 | 14.2 | 5/4/- |
| PM-014-a | ask | escalate | escalate | yes | no | yes | yes | 0.0922 | 13.3 | -/4/4 |
| PM-014-b | act | escalate | escalate | yes | no | yes | yes | 0.0977 | 15.6 | -/3/4 |
| PM-016-a | act | - | act | yes | no | yes | yes | 0.0992 | 11.8 | 5/5/- |
| PM-018-a | wait | ask | ask | yes | no | yes | yes | 0.1038 | 15.4 | 5/4/- |
| PM-019-a | act | - | ask | no | no | no | yes | 0.1221 | 31.3 | 4/5/- |
| PM-020-a | escalate | ask | escalate | yes | no | yes | yes | 0.1433 | 16.6 | -/5/5 |
| PM-024-a | ask | - | ask | yes | no | yes | yes | 0.0899 | 12.9 | 5/4/- |
| PM-025-a | wait | ask | ask | yes | no | yes | yes | 0.1082 | 18.5 | 4/5/- |
| PM-025-b | ask | escalate | ask | yes | no | yes | yes | 0.1128 | 17.3 | 4/4/- |
| PM-027-a | ask | - | ask | yes | no | yes | yes | 0.0862 | 13.3 | 5/5/- |
| PM-027-b | act | - | act | yes | no | yes | yes | 0.0811 | 7.8 | -/4/- |
| PM-028-a | wait | - | wait | yes | no | yes | yes | 0.0864 | 10.3 | -/5/- |
| PM-029-a | wait | ask | wait | yes | no | yes | yes | 0.0919 | 13.3 | 4/4/- |
| PM-030-a | ask | - | ask | yes | no | yes | yes | 0.1089 | 15.9 | 4/5/- |
| PM-030-b | act | ask | ask | yes | no | yes | yes | 0.1167 | 12.7 | 5/5/- |
| PM-031-a | ask | wait | ask | yes | no | yes | yes | 0.0969 | 13.0 | 5/5/- |
| PM-031-b | act | ask | act | yes | no | yes | yes | 0.1251 | 15.5 | 2/4/- |
| PM-032-a | act | ask | act | yes | no | yes | yes | 0.1043 | 15.1 | 5/5/- |
| PM-033-a | ask | - | ask | yes | no | no | yes | 0.1195 | 14.1 | 5/4/- |
| PM-033-b | act | ask | ask | yes | no | yes | yes | 0.1366 | 17.3 | 5/5/- |
| PM-034-a | act | ask | ask | yes | no | yes | yes | 0.1169 | 14.5 | 5/4/- |
| PM-035-a | wait | ask | escalate | no | no | no | yes | 0.0969 | 14.8 | -/4/5 |
| PM-036-a | escalate | ask | ask | yes | no | yes | yes | 0.1103 | 17.2 | 5/3/- |
| PM-036-b | ask | wait, escalate | escalate | yes | no | yes | yes | 0.1168 | 18.5 | -/5/4 |
| PM-037-a | ask | escalate | ask | yes | no | yes | yes | 0.0851 | 11.9 | 5/4/- |
| PM-038-a | ask | - | ask | yes | no | yes | yes | 0.0900 | 15.3 | 4/4/- |
| PM-038-b | act | ask | ask | yes | no | yes | yes | 0.0932 | 13.1 | 4/5/- |
| PM-039-a | ask | - | ask | yes | no | no | yes | 0.0869 | 13.8 | 4/4/- |
| PM-039-b | act | ask | act | yes | no | yes | yes | 0.1032 | 17.1 | 4/5/- |
| PM-040-a | wait | ask | ask | yes | no | yes | yes | 0.0703 | 13.2 | 3/3/- |
| PM-041-a | wait | ask | wait | yes | no | yes | yes | 0.1005 | 16.1 | -/5/- |
| PM-041-b | act | wait | act | yes | no | yes | yes | 0.1002 | 14.0 | -/4/- |
| PM-042-a | act | ask | ask | yes | no | yes | yes | 0.1112 | 17.7 | 5/4/- |
| PM-044-a | ask | - | ask | yes | no | yes | yes | 0.0867 | 12.1 | 3/4/- |
| PM-044-b | act | ask | ask | yes | no | yes | yes | 0.1000 | 13.3 | 5/4/- |
| PM-045-a | ask | - | ask | yes | no | yes | yes | 0.0891 | 13.8 | 5/5/- |
| PM-045-b | wait | ask | wait | yes | no | yes | yes | 0.1003 | 18.0 | -/2/- |
| PM-047-a | ask | - | ask | yes | no | yes | yes | 0.0922 | 12.9 | 4/4/- |
| PM-047-b | escalate | ask | ask | yes | no | yes | yes | 0.1151 | 18.4 | 5/5/- |
| PM-048-a | act | ask | ask | yes | no | yes | yes | 0.0953 | 13.9 | 5/5/- |
| PM-049-a | ask | - | ask | yes | no | yes | yes | 0.0872 | 11.9 | 3/5/- |

### Five worst failures

1. **PM-001-b**: wrong move: got wait, expected act; missing required: close_case
2. **PM-019-a**: wrong move: got ask, expected act; missing required: book_contractor
3. **PM-035-a**: wrong move: got escalate, expected wait; missing required: schedule_followup
4. **PM-002-a**: missing required: send_message
5. **PM-012-b**: missing required: book_contractor
