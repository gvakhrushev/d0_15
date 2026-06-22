# D0_V15_INTEGRATED_CLOSURE_REPORT

**Canonical integration release.** Source-to-theorem audit of the scene `K(9,11,13)`. Every node resolves to
exactly one of `THE / NO-GO / CONDITIONAL-EXTENSION / REJECTED / EMPIRICAL-PASSPORT`. The statuses below are
machine-checked: `D0.Integration.V15.Reconciliation.manifest_statuses` proves each by `decide`, and
`the_nodes_are_backed` / `nogo_nodes_are_backed` tie them to the actual proved theorems.

> **D0 is NOT complete.** This release closes the *audit*: it states precisely what the finite structure
> determines (one genuinely-new present-core `THE`, plus one algebraic identity) and what it does not (every
> physical bridge remains gated by an explicitly named missing primitive).

## Truth table

| Claim | Result | Scope | Missing primitive |
|---|---|---|---|
| A — zone-current `G`-Hermitian spectral split | **THE** | canonical part-size inner product `G=diag(9,11,13)`; linear algebra on frozen `D,A` | — (firewall: not a physical current) |
| E1 — Schur/Feshbach det factorization | **THE (algebraic identity)** | finite block split | — |
| B — branch CP readout | NO-GO | full Stinespring class | `PRIM-BRANCH-ISOTROPIC-READOUT` |
| D — lepton mass ratios | NO-GO | finite branch class `{0,1/4,1/3}` | `PRIM-EFT-IR-MATCHING-FUNCTIONAL` |
| E2 — physical EOS / `w` | NO-GO | same-response class | `PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT` |
| F1 — archive regular refinement | NO-GO | regular `mod-N` covers | — (true map is contracting `359/160`) |
| C — physical edge cover | CONDITIONAL-EXTENSION | `λ`-family | `PRIM-EDGE-HOLONOMY-SELECTOR` |
| F2 — Sturmian refinement | CONDITIONAL-EXTENSION | substitution tower | `PRIM-STURMIAN-REFINEMENT-OWNER` |
| G — present-core limits | NO-GO suite | each named owner | per-owner (unchanged) |
| H — AMS heavy nuclei | EXTERNAL-PASSPORT | comparison only | internal nuclear-flux transfer operator |
| 8× `*_RESULT.md` | REJECTED | non-existent inputs | n/a |

No prose below contradicts this table.

## 1. Frozen source inventory

Present-core facts derive ONLY from: Books `BOOK_00..BOOK_09`, frozen D0-v14 source, and declarations actually
imported by `D0.All`. The v15 nodes trace to these frozen owners:

- `D0-KERNEL-ZONE-SPLIT-001` (`D0.Claims.KernelZoneSplit`) — scene `K(9,11,13)`, parts `9,11,13`, degrees
  `24,22,20`, adjacency rank 3 / nullity 30 / zone split `8+10+12`. Source of A.
- `D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001` — Feshbach block transfer. Source of E1.
- `D0-EDGE-ALPHA-001` (`D0.Spectral.ZetaResidueAlpha`) — edge carrier dim `359`. Source of C.
- `D0-PHI-STURMIAN-CYLINDER-CONJUGACY-001` — Sturmian frozen data. Source of F2.
- `D0-ARCHIVE-CONTRACTION-NOGO-001` — archive window `359/160`. Source of F1, E2.
- `D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001` — lepton underdetermination. Source of B, D.

**The 8 referenced `*_RESULT.md` files do not exist in the repo** and are REJECTED (see §5).

## 2. Proven present-core theorems (THE)

- **A. Zone-current spectral split** — `D0.Integration.V15.RawZone.zone_current_spine`. On `ran(A)` with
  `D_W=diag(24,22,20)`, `A_W=!![0,11,13;9,0,13;9,11,0]`: `comm³=−2840·comm` (char.poly `t³+2840t`, spectrum
  `{0,±2√710}`); `J=i·comm` is `G`-Hermitian in the canonical part-size inner product `G=diag(9,11,13)`
  (`(G·comm)ᵀ=−(G·comm)`); the spectral projectors `P_act,P₀` are genuine `G`-orthogonal idempotents
  (`(G·P)ᵀ=G·P`), complementary, `tr P_act=2` / `tr P₀=1`. Cert `05_CERTS/vp_zone_current_spine.py`
  (4 reachable FAIL-controls, incl. *naive-Euclidean-not-Hermitian*).
  **Hermiticity correction:** the naive Euclidean build gave oblique projectors (a `CONDITIONAL`); the rescue
  is the graph's own equitable-partition cell-size weighting `G` — a frozen structure — under which the split
  is genuinely orthogonal. *Firewall:* not a physical neutral current / neutrino count / charge / generation.
- **E1. Schur/Feshbach determinant factorization** — `D0.Integration.V15.Feshbach.feshbach_schur_factorization`.
  `det !![2,1,1,0;0,3,1,1;0,1,1,0;1,0,0,1] = 4 = det(A−B·C)`. An algebraic identity only; the additive
  log-derivative response split `R_Q+R_P` is its corollary. **Not** an energy-pressure tensor.

## 3. Proven present-core no-go theorems (NO-GO)

- **B. Branch CP readout non-unique** — `branch_readout_not_unique`. Commutant dim `3 > 1`; `rho1 ≠ rho2` with
  identical frozen marginals. Negative control: two admissible readouts share marginals, differ in coherence.
- **D. Lepton mass-ratio underdetermination** — `mass_ratio_underdetermined`. Vandermonde at `{0,1/4,1/3}` has
  `det = 1/144 ≠ 0`, so every `(r_μ,r_τ)` is realized by a smooth matching function.
- **E2. Physical EOS underdetermined** — `eos_underdetermined`. `(ρ,p)=(3,1)` and `(1,3)`: same total response
  `4`, distinct `w` (`1/3 ≠ 3`).
- **F1. Archive ≠ regular cover** — `archive_window_not_measure_preserving`. `359/160 ≠ 1`: the archive map is
  contracting, not a measure-preserving regular cover.
- **G. Present-core limits regression** — `regression_owners_present`. The 6 established limits remain owned and
  unchanged (heat-trace no pole, α blocked, `c_D0=1≠c_SI`, internal flow ≠ `w(z)`, …).

## 4. Conditional extensions and their new primitives (CONDITIONAL-EXTENSION)

- **C. Physical edge cover** — `edge_cover_is_family`. `z³`-coefficient `= −λ` (injective): distinct `λ` give
  inequivalent observables; frozen data fixes no `λ`. Missing `PRIM-EDGE-HOLONOMY-SELECTOR`. (Halmos: dilation
  existence ≠ uniqueness of a physical edge operator.)
- **F2. Sturmian refinement** — `sturmian_golden_tower`. Incidence `!![1,1;1,0]`, `det=−1`, `trace=1`
  (char.poly `t²−t−1`, Perron `φ`). A valid tower; identifying it with the frozen archive maps needs
  `PRIM-STURMIAN-REFINEMENT-OWNER`.

## 5. Removed or downgraded claims

- **8 phantom inputs REJECTED** (do not exist in the repo): `D0_INTERFACE_DISPLACEMENT_RESULT`,
  `D0_DYADIC_REFINEMENT_AND_SEAM_GROUPOID_RESULT`, `D0_UNIVERSAL_PHASE_BRANCH_AND_FESHBACH_RESULT`,
  `D0_X5_INTERFACE_BRANCH_ROUTE_FINAL_NO_GO`, `D0_CANONICAL_ZONE_CURRENT_RESULT`,
  `D0_ZONE_STURMIAN_PHI_CLOSURE_RESULT`, `D0_LEPTON_BRANCH_COUPLING_CLOSURE`,
  `D0_PHYSICAL_EDGE_COVER_AND_EFT_IR_BOUNDARY`.
- **A downgraded-then-corrected:** the adversarial audit downgraded the naive zone-current build to
  `CONDITIONAL` (oblique projectors); it was corrected to `THE` via the canonical inner product `G`. The
  overclaim ("orthogonal projectors" in the naive Euclidean metric) was removed.

## 6. Branch coupling classification

NO-GO. The full Stinespring class `V:W→H_br⊗E` with `V†(E_j)V=Q_j` admits a family of CP readouts because the
branch representation has 3 isotypic generation blocks (commutant ⊋ `ℂ·I`). The maximally-mixed block state is
not forced by frozen symmetry; selecting it requires the twirling primitive `PRIM-BRANCH-ISOTROPIC-READOUT`.
The mark audit (`V₉=Ω₈∪{ω₀}`, …) is not promoted: orbit projectors are not individual sheets without a
symmetry-breaking owner.

## 7. Physical edge classification

CONDITIONAL-EXTENSION. The edge carrier (dim `359`) is frozen, but the cover holonomy `λ` is a free parameter:
the characteristic factor `(1−λ(zc_b)⁴)(1−λ(zc_b)³)` varies with `λ` (z³-coefficient `−λ`), and neither
symmetry, unitarity, nor feedback `F` pins it. Registered `D0-EDGE-COVER-FAMILY-001 : PROOF-TARGET` (conditional),
not a present-core theorem.

## 8. Refinement classification

The two refinements are kept distinct. F1 (archive): NO-GO — the real bonding map carries the contraction window
`359/160 ≠ 1`, so it is not a regular measure-preserving cover; substituting a regular `mod-N` cover is invalid.
F2 (Sturmian): CONDITIONAL-EXTENSION — a valid golden-substitution tower (Perron `φ`), but not identified with
the archive maps without a new owner. No CFT/Virasoro is imported.

## 9. Physical-boundary firewall

`D0.Integration.V15.PhysicalBoundary`. Internal refinement coordinate, internal `φ`-scale, and observable
cosmological redshift are kept separate; no `1+z=φⁿ` redshift law and no physical `w(z)` is asserted. The internal
tick `c_D0=1` is structural, not the SI speed of light. Operator-type firewall respected: the zone generator is
neither `L_archive`-as-`QUQ`/`S_DE` nor a physical current.

## 10. External passports

H. `D0-AMS-HEAVY-NUCLEI-PASSPORT-001 : EMPIRICAL-PASSPORT`. External targets `b≈1/3` (P,S,Cl), `b≈1/2` (Ar,K,Ca)
in `Φ_X=a_X·Φ_Si+b_X·Φ_F`. No internal nuclear carrier/transfer owner exists (`amsHasInternalOwner=false`); no D0
prediction is claimed. Literature firewall: external papers supply comparison/analogy/test/bridge-constraint
only — never a D0 primitive, selector, label, or closure status.

## 11. Final open-joints register

Each is a NAMED missing primitive required to cross a physical bridge (see `artifacts/v15_final_open_joints.md`):

1. `PRIM-BRANCH-ISOTROPIC-READOUT` (branch CP readout uniqueness).
2. `PRIM-EFT-IR-MATCHING-FUNCTIONAL` (lepton mass ratios).
3. `PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT` (physical EOS / `w`).
4. `PRIM-EDGE-HOLONOMY-SELECTOR` (edge cover `λ`).
5. `PRIM-STURMIAN-REFINEMENT-OWNER` (Sturmian-as-archive refinement).
6. An internal nuclear-flux transfer operator (AMS, currently passport-only).

No other joint is open: the present-core finite structure is machine-checked, the 8 phantom files are rejected,
and no physical `THE` is claimed beyond A's spectral split and E1's algebraic identity.

## 12. Reproducibility commands

```sh
# Lean (from 09_LEAN_FORMALIZATION)
python ../tools/generate_lean_aggregates.py
lake build D0.All

# Certificate (exact rational LA, with FAIL-controls)
python 05_CERTS/vp_zone_current_spine.py

# Artifacts (regenerate the 6 machine-readable reports)
python tools/gen_v15_artifacts.py

# Registry + gates
python tools/validate_csv.py
python tools/d0_status_model.py        # status model / scoring
```
