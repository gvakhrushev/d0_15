# D0 vNext Isometric Dirac Tower — Dependency Graph

Single candidate primitive `PRIM-ISOMETRIC-DIRAC-J_N`. Grounded verdict: **A(isometry)+C(scale)+D(Laplacian)**.

```
golden cylinder language -> Fibonacci Bratteli AF algebra (D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001)
  -> Perron trace (compat 1+phi^-1=phi)
  -> GNS isometric tower J_N   D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001        [CERT-CLOSED: isometry EXISTS]
  -> martingale Dirac scale    D0-VNEXT-MARTINGALE-DIRAC-OWNER-001       [NO-GO: scale underdetermined (Outcome C)]
  -> D0 Laplacian comparison   D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY... [NO-GO: no Xi_N, 33 skipped (Outcome D)]
  -> Feshbach transport        D0-VNEXT-FESHBACH-TOWER-COMPATIBILITY...  [PROOF-TARGET: blocked upstream]
  -> quantum-metric            D0-VNEXT-QUANTUM-METRIC-EXTENSION-PASSPORT[PASSPORT-CLOSED: formalism only]
  -> master tower              D0-VNEXT-ISOMETRIC-DIRAC-TOWER-OWNER-001  [PROOF-TARGET: isometry done; +2 primitives]
  -> master no-go              D0-VNEXT-ISOMETRIC-DIRAC-TOWER-NOGO-001   [NO-GO: primitive does not collapse to 1 datum]
```

## Verdict
The isometry half is FREE (Perron trace). The full Dirac-compatible primitive splits into two further
independent primitives: `PRIM-DIRAC-SCALE-SELECTION` and `PRIM-COMPARISON-MAP-XI-N`. Downstream alpha/CMB/
Higgs/smooth-geometry gates stay CLOSED.
