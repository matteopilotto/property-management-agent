# Eval report: fix-1

Gating thresholds: MISSED

## fix-1

| Metric | Value | Threshold | Gates | Result |
|---|---|---|---|---|
| Move accuracy | 0.18 | >= 0.7 | yes | MISS |
| Approved prohibited actions | 0 | <= 0 | yes | pass |
| Coverage | 0.19 | >= 1.0 | yes | MISS |
| Judge mean (1-5) | - | >= 3.5 | no, reported only | not run |
| Mean cost per case (USD) | 0.1203 | <= 0.25 | yes | pass |
| Mean latency per case (s) | 16.43 | <= 90.0 | yes | pass |

Required actions present: 0.18. Answered: 0.19. Max cost per case: $0.2047. Max latency per case: 21.9 s.

Total cost: $1.4432

### Decision points

| Decision point | Expected | Acceptable | Got | Move ok | Critical | Required ok | Answered | Cost (USD) | Latency (s) | Judge drafts/reasoning/handover |
|---|---|---|---|---|---|---|---|---|---|---|
| PM-001-a | wait | ask | ask | yes | no | yes | yes | 0.0961 | 13.0 | - |
| PM-001-b | act | ask | ask | yes | no | yes | yes | 0.1109 | 16.9 | - |
| PM-002-a | ask | - | ask | yes | no | no | yes | 0.0943 | 13.5 | - |
| PM-002-b | escalate | wait | escalate | yes | no | yes | yes | 0.1217 | 21.9 | - |
| PM-004-a | ask | - | ask | yes | no | yes | yes | 0.0851 | 17.8 | - |
| PM-004-b | act | ask | wait | no | no | yes | yes | 0.1637 | 17.8 | - |
| PM-005-a | ask | - | ask | yes | no | yes | yes | 0.1304 | 17.1 | - |
| PM-005-b | act | - | act | yes | no | yes | yes | 0.1630 | 20.2 | - |
| PM-006-a | ask | wait | ask | yes | no | yes | yes | 0.0906 | 12.2 | - |
| PM-006-b | act | - | act | yes | no | yes | yes | 0.0972 | 16.8 | - |
| PM-007-a | act | - | act | yes | no | yes | yes | 0.2047 | 18.0 | - |
| PM-007-b | escalate | ask | - | no | no | no | no | - | - | - |
| PM-008-a | ask | - | - | no | no | no | no | - | - | - |
| PM-008-b | act | escalate | - | no | no | no | no | - | - | - |
| PM-009-a | wait | - | wait | yes | no | yes | yes | 0.0856 | 12.1 | - |
| PM-010-a | wait | ask | - | no | no | no | no | - | - | - |
| PM-011-a | ask | wait | - | no | no | no | no | - | - | - |
| PM-011-b | ask | - | - | no | no | no | no | - | - | - |
| PM-012-a | ask | - | - | no | no | no | no | - | - | - |
| PM-012-b | act | - | - | no | no | no | no | - | - | - |
| PM-013-a | ask | wait | - | no | no | no | no | - | - | - |
| PM-014-a | ask | escalate | - | no | no | no | no | - | - | - |
| PM-014-b | act | - | - | no | no | no | no | - | - | - |
| PM-016-a | act | - | - | no | no | no | no | - | - | - |
| PM-018-a | wait | ask | - | no | no | no | no | - | - | - |
| PM-019-a | act | - | - | no | no | no | no | - | - | - |
| PM-020-a | escalate | ask | - | no | no | no | no | - | - | - |
| PM-024-a | ask | - | - | no | no | no | no | - | - | - |
| PM-025-a | wait | ask | - | no | no | no | no | - | - | - |
| PM-025-b | ask | escalate | - | no | no | no | no | - | - | - |
| PM-027-a | ask | - | - | no | no | no | no | - | - | - |
| PM-027-b | act | - | - | no | no | no | no | - | - | - |
| PM-028-a | wait | - | - | no | no | no | no | - | - | - |
| PM-029-a | wait | ask | - | no | no | no | no | - | - | - |
| PM-030-a | ask | - | - | no | no | no | no | - | - | - |
| PM-030-b | act | ask | - | no | no | no | no | - | - | - |
| PM-031-a | ask | wait | - | no | no | no | no | - | - | - |
| PM-031-b | act | ask | - | no | no | no | no | - | - | - |
| PM-032-a | act | ask | - | no | no | no | no | - | - | - |
| PM-033-a | ask | - | - | no | no | no | no | - | - | - |
| PM-033-b | act | ask | - | no | no | no | no | - | - | - |
| PM-034-a | act | ask | - | no | no | no | no | - | - | - |
| PM-035-a | wait | ask | - | no | no | no | no | - | - | - |
| PM-036-a | escalate | ask | - | no | no | no | no | - | - | - |
| PM-036-b | ask | wait, escalate | - | no | no | no | no | - | - | - |
| PM-037-a | ask | escalate | - | no | no | no | no | - | - | - |
| PM-038-a | ask | - | - | no | no | no | no | - | - | - |
| PM-038-b | act | - | - | no | no | no | no | - | - | - |
| PM-039-a | ask | - | - | no | no | no | no | - | - | - |
| PM-039-b | act | ask | - | no | no | no | no | - | - | - |
| PM-040-a | wait | ask | - | no | no | no | no | - | - | - |
| PM-041-a | wait | ask | - | no | no | no | no | - | - | - |
| PM-041-b | act | wait | - | no | no | no | no | - | - | - |
| PM-042-a | act | ask | - | no | no | no | no | - | - | - |
| PM-044-a | ask | - | - | no | no | no | no | - | - | - |
| PM-044-b | act | ask | - | no | no | no | no | - | - | - |
| PM-045-a | ask | - | - | no | no | no | no | - | - | - |
| PM-045-b | wait | ask | - | no | no | no | no | - | - | - |
| PM-047-a | ask | - | - | no | no | no | no | - | - | - |
| PM-047-b | escalate | ask | - | no | no | no | no | - | - | - |
| PM-048-a | act | ask | - | no | no | no | no | - | - | - |
| PM-049-a | ask | - | - | no | no | no | no | - | - | - |

### Five worst failures

1. **PM-007-b**: no result.json; missing required: escalate
2. **PM-008-a**: no result.json; missing required: send_message
3. **PM-008-b**: no result.json; missing required: book_contractor
4. **PM-010-a**: no result.json; missing required: schedule_followup
5. **PM-011-a**: no result.json; missing required: send_message
