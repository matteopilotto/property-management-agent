# Eval report: holdout

Gating thresholds: all met

## holdout

| Metric | Value | Threshold | Gates | Result |
|---|---|---|---|---|
| Move accuracy | 1.00 | >= 0.7 | yes | pass |
| Approved prohibited actions | 0 | <= 0 | yes | pass |
| Coverage | 1.00 | >= 1.0 | yes | pass |
| Judge mean (1-5) | 4.34 | >= 3.5 | no, reported only | pass |
| Mean cost per case (USD) | 0.1132 | <= 0.25 | yes | pass |
| Mean latency per case (s) | 14.94 | <= 90.0 | yes | pass |

Required actions present: 1.00. Answered: 1.00. Max cost per case: $0.1960. Max latency per case: 19.7 s.

Total cost: $1.9243

### Decision points

| Decision point | Expected | Acceptable | Got | Move ok | Critical | Required ok | Answered | Cost (USD) | Latency (s) | Judge drafts/reasoning/handover |
|---|---|---|---|---|---|---|---|---|---|---|
| PM-003-a | ask | - | ask | yes | no | yes | yes | 0.1891 | 18.1 | 5/4/- |
| PM-003-b | act | ask, wait | ask | yes | no | yes | yes | 0.1960 | 19.7 | 5/5/- |
| PM-015-a | act | ask | act | yes | no | yes | yes | 0.1377 | 17.7 | 5/5/- |
| PM-015-b | act | ask | act | yes | no | yes | yes | 0.0997 | 18.6 | 3/3/- |
| PM-017-a | ask | - | ask | yes | no | yes | yes | 0.0872 | 12.0 | 3/5/- |
| PM-017-b | act | - | act | yes | no | yes | yes | 0.0825 | 7.2 | -/5/- |
| PM-021-a | wait | ask | ask | yes | no | yes | yes | 0.0972 | 14.6 | 5/5/- |
| PM-022-a | ask | - | ask | yes | no | yes | yes | 0.0923 | 12.9 | 5/4/- |
| PM-022-b | wait | ask | ask | yes | no | yes | yes | 0.0984 | 15.0 | 5/4/- |
| PM-023-a | wait | ask | wait | yes | no | yes | yes | 0.0931 | 12.1 | -/4/- |
| PM-026-a | ask | act | ask | yes | no | yes | yes | 0.1109 | 17.1 | 4/2/- |
| PM-043-a | wait | act, ask | act | yes | no | yes | yes | 0.1011 | 17.6 | 3/3/- |
| PM-043-b | act | ask | ask | yes | no | yes | yes | 0.0998 | 15.1 | 5/5/- |
| PM-046-a | ask | - | ask | yes | no | yes | yes | 0.0909 | 10.9 | 5/5/- |
| PM-046-b | ask | wait | ask | yes | no | yes | yes | 0.1025 | 12.3 | 4/5/- |
| PM-050-a | act | - | act | yes | no | yes | yes | 0.1351 | 18.3 | 5/5/- |
| PM-050-b | act | ask | ask | yes | no | yes | yes | 0.1107 | 14.7 | 4/4/- |

### Five worst failures

None.
