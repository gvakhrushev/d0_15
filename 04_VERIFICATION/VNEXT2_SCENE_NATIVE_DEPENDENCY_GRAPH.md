# D0 vNext+2 Scene-Native Refinement — Dependency Graph

Refine directly from K(9,11,13). Grounded verdict: **Outcome D (refinement rule underdetermined)**.

```
K(9,11,13) [fingerprint: L {0:1,20:12,22:10,24:8,33:2}, trace 718, struct R(3)+K(8,10,12)]  (CERT)
  refinement family: W (all-walks, A, dim 33) | NB (non-backtracking, 718) | E (directed-edge, 718)
    depth-2 carriers 15708 (W) != 14990 (NB)  -> INEQUIVALENT                       [NO-GO Outcome D]
  endpoint measure: counting vs degree-weighted vs random-walk -> non-unique        [underdetermined]
  Xi = endpoint conditional expectation: family/measure-dependent -> not canonical   [NO-GO]
  scene spectral lift / Feshbach: blocked (no canonical Xi)                          [PROOF-TARGET]
  Dirac scale cocycle: refinement-dependent -> not unique                            [NO-GO/PROOF-TARGET]
```

## Verdict
No unique scene-native refinement rule is forced. New upstream primitive
`PRIM-SCENE-HISTORY-REFINEMENT-RULE`; the two earlier interfaces `PRIM-COMPARISON-MAP-XI-N` and
`PRIM-DIRAC-SCALE-SELECTION` remain INDEPENDENT. All downstream physics gates stay CLOSED.
