# Holdout cases

Ten of the 50 Property Management public cases are held out as a private dress rehearsal
for the Reality Test (see [`solo-redo.md`](solo-redo.md) §3). Build, design and debug
against the other 40; open these only to run the dress rehearsal.

Drawn without reading any case, reproducible with:

```bash
python3 -c "import random; print(sorted(random.Random(20261010).sample(range(1, 51), 10)))"
```

| Case | Path |
|---|---|
| 003 | `HackatonPublicCases/Property Management/003/` |
| 015 | `HackatonPublicCases/Property Management/015/` |
| 017 | `HackatonPublicCases/Property Management/017/` |
| 021 | `HackatonPublicCases/Property Management/021/` |
| 022 | `HackatonPublicCases/Property Management/022/` |
| 023 | `HackatonPublicCases/Property Management/023/` |
| 026 | `HackatonPublicCases/Property Management/026/` |
| 043 | `HackatonPublicCases/Property Management/043/` |
| 046 | `HackatonPublicCases/Property Management/046/` |
| 050 | `HackatonPublicCases/Property Management/050/` |
