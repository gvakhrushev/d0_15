# D0 Toral Lucas–Voronoi Markov — Dependency Graph (Iteration 22, OUTCOME B)

Grounded per VERIFIED_CLOSURE_PROTOCOL. **Decision: Outcome B** — the canonical periodic seed exists,
but a *canonical* Markov partition (and hence the symbolic SSE to the golden cylinder shift) does NOT
follow from a 3-point seed. Closures + named gaps in `TORAL_MARKOV_BLOCKERS.csv`.

```
T = [[0,1],[1,-1]]  (det -1, infinite order in GL(2,ℤ); q_T=44 is a modulus, T⁴⁴ ≠ I)
  └─ A. integral conjugacy  C T C⁻¹ = −M_φ   D0-TORAL-INTEGRAL-CONJUGACY-OWNER-001   [CERT-CLOSED ✓ new]
        C=[[0,-1],[1,0]] unimodular; tr T=-1, det T=-1 (charpoly x²+x-1); eigenvalues φ⁻¹,-φ; entropy log φ.
        INTEGRAL matrix conjugacy ONLY — −M_φ has a negative entry, so NOT the symbolic SSE.
  └─ A. periodic seed  #Fix_n=|det(Tⁿ−I)|=1,1,4,5,11   D0-TORAL-LUCAS-PERIODIC-SEED-OWNER-001  [CERT-CLOSED ✓ new]
        primitive period-3 set = #Fix_3−#Fix_1 = 3 = single f_T orbit (the canonical unordered seed).
  └─ B/C. canonical Markov partition   D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001   [NO-GO ✓ new]
        −M_φ ≠ M_φ (negative entry) ⇒ integral conjugacy ≠ symbolic SSE; a 3-point seed does not
        canonically determine a Markov partition (Adler–Weiss partitions are non-unique).
  └─ B Voronoi / C Markov-rectangle / D coding / E boundary-quotient                  [PROOF-TARGET ← NO-GO]
  └─ F. Williams SSE to M_φ   D0-TORAL-WILLIAMS-SSE-OWNER-001                          [PROOF-TARGET]
        exact missing artifact: an explicit nonnegative-integer elementary SSE chain A_LV ~ … ~ M_φ from
        a canonical (blocked) adjacency A_LV. Ordinary shift equivalence is NOT sufficient for conjugacy.
  └─ F. full toral conjugacy   D0-TORAL-TIME-MARKOV-CONJUGACY-001                      [PROOF-TARGET]
        (external Adler–Weiss stays the cited bridge owner, never a core import)
  └─ umbrella  D0-TORAL-LUCAS-MARKOV-CLOSURE-001 = decided Outcome B                   [NO-GO]
```

## Closed this campaign (3)
- `D0-TORAL-INTEGRAL-CONJUGACY-OWNER-001` (CERT-CLOSED): `C T C⁻¹ = −M_φ`, entropy `log φ` — integral
  matrix conjugacy only.
- `D0-TORAL-LUCAS-PERIODIC-SEED-OWNER-001` (CERT-CLOSED): the determinant fixed-point counts and the
  canonical primitive period-3 orbit seed.
- `D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001` (NO-GO): no canonical Markov partition / SSE from the seed.

## Why this matters
Same root-cause pattern as the role-carrier, Higgs-orbit, and n_s no-gos: the finite algebra closes
cleanly (the integral conjugacy to the golden matrix, the Lucas periodic counts), but the *canonical
symbolic* object — a seed-determined Markov partition giving a nonnegative adjacency matrix SSE-equivalent
to `M_φ` — is not forced. The integral conjugacy lands on `−M_φ` (negative entries), which is the golden
*algebra* but not the golden *adjacency matrix*. No Adler–Weiss import, no manual rectangles, no
raw-shift-is-torus claim, no `T⁴⁴=I`.
