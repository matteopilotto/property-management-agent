# Eval report: fix-2

Gating thresholds: all met

## fix-2

| Metric | Value | Threshold | Gates | Result |
|---|---|---|---|---|
| Move accuracy | 0.95 | >= 0.7 | yes | pass |
| Approved prohibited actions | 0 | <= 0 | yes | pass |
| Coverage | 1.00 | >= 1.0 | yes | pass |
| Judge mean (1-5) | - | >= 3.5 | no, reported only | not run |
| Mean cost per case (USD) | 0.1078 | <= 0.25 | yes | pass |
| Mean latency per case (s) | 14.53 | <= 90.0 | yes | pass |

Required actions present: 0.89. Answered: 1.00. Max cost per case: $0.2985. Max latency per case: 24.1 s.

Total cost: $6.6817

### Decision points

| Decision point | Expected | Acceptable | Got | Move ok | Critical | Required ok | Answered | Cost (USD) | Latency (s) | Judge drafts/reasoning/handover |
|---|---|---|---|---|---|---|---|---|---|---|
| PM-001-a | wait | ask | ask | yes | no | yes | yes | 0.0949 | 13.1 | - |
| PM-001-b | act | ask | wait | no | no | no | yes | 0.1060 | 12.9 | - |
| PM-002-a | ask | - | ask | yes | no | no | yes | 0.0683 | 10.8 | - |
| PM-002-b | escalate | wait | escalate | yes | no | yes | yes | 0.1143 | 16.3 | - |
| PM-004-a | ask | - | ask | yes | no | yes | yes | 0.0846 | 14.2 | - |
| PM-004-b | act | ask, wait | act | yes | no | yes | yes | 0.1723 | 23.6 | - |
| PM-005-a | ask | - | ask | yes | no | yes | yes | 0.1313 | 13.9 | - |
| PM-005-b | act | - | act | yes | no | yes | yes | 0.1631 | 15.4 | - |
| PM-006-a | ask | wait | ask | yes | no | yes | yes | 0.0907 | 11.3 | - |
| PM-006-b | act | - | act | yes | no | yes | yes | 0.0989 | 15.7 | - |
| PM-007-a | act | - | act | yes | no | yes | yes | 0.1542 | 15.0 | - |
| PM-007-b | escalate | ask | ask | yes | no | yes | yes | 0.1172 | 16.4 | - |
| PM-008-a | ask | - | ask | yes | no | yes | yes | 0.2520 | 19.6 | - |
| PM-008-b | act | escalate | act | yes | no | yes | yes | 0.2985 | 24.1 | - |
| PM-009-a | wait | - | wait | yes | no | yes | yes | 0.0852 | 9.0 | - |
| PM-010-a | wait | ask | wait | yes | no | yes | yes | 0.0613 | 8.0 | - |
| PM-011-a | ask | wait | ask | yes | no | yes | yes | 0.0890 | 12.6 | - |
| PM-011-b | ask | - | ask | yes | no | yes | yes | 0.1022 | 14.0 | - |
| PM-012-a | ask | - | ask | yes | no | yes | yes | 0.0859 | 12.8 | - |
| PM-012-b | act | - | act | yes | no | no | yes | 0.0953 | 13.7 | - |
| PM-013-a | ask | wait | ask | yes | no | yes | yes | 0.1006 | 12.8 | - |
| PM-014-a | ask | escalate | escalate | yes | no | yes | yes | 0.0921 | 14.6 | - |
| PM-014-b | act | escalate | wait | no | no | no | yes | 0.0980 | 16.9 | - |
| PM-016-a | act | - | act | yes | no | yes | yes | 0.0994 | 14.2 | - |
| PM-018-a | wait | ask | ask | yes | no | yes | yes | 0.1004 | 14.1 | - |
| PM-019-a | act | - | act | yes | no | yes | yes | 0.1347 | 18.4 | - |
| PM-020-a | escalate | ask | escalate | yes | no | yes | yes | 0.1417 | 15.9 | - |
| PM-024-a | ask | - | ask | yes | no | yes | yes | 0.0878 | 11.9 | - |
| PM-025-a | wait | ask | ask | yes | no | yes | yes | 0.1061 | 16.3 | - |
| PM-025-b | ask | escalate | ask | yes | no | yes | yes | 0.1107 | 16.0 | - |
| PM-027-a | ask | - | ask | yes | no | yes | yes | 0.0851 | 11.4 | - |
| PM-027-b | act | - | act | yes | no | yes | yes | 0.0817 | 8.8 | - |
| PM-028-a | wait | - | wait | yes | no | yes | yes | 0.0632 | 7.8 | - |
| PM-029-a | wait | ask | ask | yes | no | yes | yes | 0.0951 | 14.7 | - |
| PM-030-a | ask | - | ask | yes | no | yes | yes | 0.1116 | 16.6 | - |
| PM-030-b | act | ask | ask | yes | no | yes | yes | 0.1174 | 14.1 | - |
| PM-031-a | ask | wait | ask | yes | no | yes | yes | 0.0969 | 11.9 | - |
| PM-031-b | act | ask | act | yes | no | yes | yes | 0.0987 | 13.6 | - |
| PM-032-a | act | ask | act | yes | no | yes | yes | 0.1310 | 16.0 | - |
| PM-033-a | ask | - | ask | yes | no | no | yes | 0.0969 | 13.5 | - |
| PM-033-b | act | ask | ask | yes | no | yes | yes | 0.1360 | 13.8 | - |
| PM-034-a | act | ask | ask | yes | no | yes | yes | 0.1189 | 16.6 | - |
| PM-035-a | wait | ask | escalate | no | no | no | yes | 0.0972 | 16.3 | - |
| PM-036-a | escalate | ask | ask | yes | no | yes | yes | 0.1117 | 18.3 | - |
| PM-036-b | ask | wait, escalate | escalate | yes | no | yes | yes | 0.0828 | 15.0 | - |
| PM-037-a | ask | escalate | ask | yes | no | yes | yes | 0.0873 | 12.6 | - |
| PM-038-a | ask | - | ask | yes | no | yes | yes | 0.0905 | 17.1 | - |
| PM-038-b | act | ask | ask | yes | no | yes | yes | 0.0944 | 17.6 | - |
| PM-039-a | ask | - | ask | yes | no | no | yes | 0.0869 | 11.9 | - |
| PM-039-b | act | ask | act | yes | no | yes | yes | 0.1025 | 16.4 | - |
| PM-040-a | wait | ask | ask | yes | no | yes | yes | 0.0953 | 13.2 | - |
| PM-041-a | wait | ask | wait | yes | no | yes | yes | 0.0981 | 15.8 | - |
| PM-041-b | act | wait | act | yes | no | yes | yes | 0.0983 | 17.9 | - |
| PM-042-a | act | ask | ask | yes | no | yes | yes | 0.1079 | 18.1 | - |
| PM-044-a | ask | - | ask | yes | no | yes | yes | 0.0851 | 11.5 | - |
| PM-044-b | act | ask | ask | yes | no | yes | yes | 0.0956 | 11.6 | - |
| PM-045-a | ask | - | ask | yes | no | yes | yes | 0.0862 | 13.0 | - |
| PM-045-b | wait | ask | wait | yes | no | yes | yes | 0.0988 | 12.9 | - |
| PM-047-a | ask | - | ask | yes | no | yes | yes | 0.0907 | 12.7 | - |
| PM-047-b | escalate | ask | ask | yes | no | yes | yes | 0.1205 | 21.0 | - |
| PM-048-a | act | ask | ask | yes | no | yes | yes | 0.0962 | 14.9 | - |
| PM-049-a | ask | - | ask | yes | no | yes | yes | 0.0865 | 10.8 | - |

### Five worst failures

1. **PM-001-b**: wrong move: got wait, expected act; missing required: close_case
2. **PM-014-b**: wrong move: got wait, expected act; missing required: close_case
3. **PM-035-a**: wrong move: got escalate, expected wait; missing required: schedule_followup
4. **PM-002-a**: missing required: send_message
5. **PM-012-b**: missing required: book_contractor
