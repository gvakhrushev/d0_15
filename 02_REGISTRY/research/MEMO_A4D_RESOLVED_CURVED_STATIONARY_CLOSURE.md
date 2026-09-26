# MEMO A4D -- resolved curved stationary closure (F4 / lower wall)

**Task:** `EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE`
**Execution:** PR #202
**Status:** IN_PROGRESS / durable checkpoint (restructured F4 attack)
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`

## 0A. RESUME CHECKPOINT -- durable state

### Architecture (locked; do not reopen)

- Upper-wall F5 is closed on PR #201: flat metric Hessian of `S_star` is
  exactly `(1/4) K_{E_eta}` with `beta_sp = 0`.  `Q(R) = O(eps^10)` near flat cannot
  alter F5.
- On quotient-complete strata,
  `Crit(S_star+Q)/G_aff ~= Crit(S_star)/G_Lor`: `Q` is auxiliary on shell and
  cannot manufacture new physical curved stationary dynamics by tuning alone.
- Correct H1 for coefficient search: seek finite curved configurations with
  active residual section `R = R_*(C) != 0` and `R_*(0) = 0`, **not** force
  `R = 0` as the primary ansatz.  Do **not** run a 7x7 `(a,b)` grid or `a=b`
  ray.
- Action family under attack uses **four independent** joint-residual scalars
  (do **not** collapse adj=opp):

      I^eta_adj,  I^eta_opp,  I^n_adj,  I^n_opp

  with adj = `|S1capS2|=1`, opp = `|S1capS2|=0`, `I^eta = R^T eta R`,
  `I^n = R^T h_n R`, and
  `R_{2|1} = det(I-P1)t2 - (I-P2) adj(I-P1) t1`.

- Forbidden: Holst / phi / new I-channel; continuum Einstein; declaring adj=opp
  dead without `ker M`; editing #201 / Lean / BOOK; self-merge.

### EXACT/CERTIFIED -- inherited from main (#199/#187/#200)

- Local `E_v`: rank 16 / ker 20; Bianchi subclass ker 10 (`E_v=0` does not force `C=0`).
- Two-link #178: no nondegenerate solder-stationary representative.
- One-boost: all-site nondegenerate `E_v=0` with `C!=0`; free-B connection Euler
  rank 282 / nullity 294; four reduced origin constraints.
- Checkerboard Lorentz-null quotient nulls nonlinearly obstructed from
  canonical flat solder.

### EXACT/CERTIFIED -- F4 support + response matrix (this PR)

Certificate: `a4d_resolved_curved_stationary_f4_check.py`.

1. **Support obstruction on the `R=0` locus.**
   Solder-scale and flat->two-link witnesses at vanishing translation data have
   `Delta I_j = 0` for all four channels while `Delta S_star != 0`.  No `c in Q^4` can
   cancel those star Euler components using I-channels dormant at `R=0`.
   Scope: **not** a no-go on the H1 locus `R=R_*(C)!=0`.

2. **Exact 4-column response matrix.**
   Over 9 active edge/face translation witnesses on the owned two-link+RCD
   background:

      rank M = 4,   dim ker M = 0

   exactly over `Q`.  In particular `eta`-adj - `eta`-opp is not in `ker M`.
   Matched-edge values at `t=1`:

      I^eta_adj=-256/9, I^eta_opp=-128/9, I^n_adj=4352/81, I^n_opp=128/9.

3. **One-boost structural dead-ansatz lemmas.**
   Constant and `x0`-only slices of `ker H_v` are degenerate at boost-plane
   sites; 12 satellite complementary components are forced into `span{e0,e1}`;
   free-B necessary residuals are automatic on `ker H_v`.

4. **Span criterion with `R!=0` -- OPEN (primary next blocker).**
   Seek `C(x)!=0` and `-gradS_star in span{gradI_j}` (projected), solve `c`,
   exact-verify full Euler.  Multistart only over geometry `x`.

### EXACT/CERTIFIED -- homogeneous word no-gos (this PR, parallel packet)

Certificate: `a4d_homogeneous_curved_stationary_controls_check.py`.

Five explicit rational homogeneous word backgrounds (including the two generic
quotient-complete joint-holonomy controls) have **no** nondegenerate full
star-stationary point.  Useful negative controls; they do not exhaust the
homogeneous four-link sector.

### NUMERICAL/EXPLORATORY -- NOT A THEOREM (parallel scout)

Certificates:
`a4d_curved_stationary_cayley_scout_candidate.json` (+ scout narrative below).

Broad homogeneous four-link / Cayley-LDU scouts find nonflat candidates with
tiny raw Euler residual, `det Theta = -1`, and apparent Hessian rank ~20 /
nullity ~19.  Compatible with the word no-gos (survivors lie outside those
words).  **Must not** be promoted before exact rational reconstruction.

### CURRENT STRONGEST STABLE STATEMENT

    BOXED:
    F4-SUPPORT-OBSTRUCTION-ON-R-EQUALS-ZERO;
    RESPONSE-MATRIX-RANK-4-KER-0-ADJ-OPP-INDEPENDENT

Supporting:

    BOXED:
    ONE-BOOST-CONSTANT-AND-X0-SLICES-DEGENERATE;
    HOMOGENEOUS-WORD-CONTROLS-NO-NONDEGENERATE-STATIONARY-POINT

No exact nondegenerate four-channel curved root claimed.
No continuum Einstein claim.

### SINGLE NEXT BLOCKER

Geometry-only span criterion with active `R=R_*(C)!=0`:

- find exact root `(x,c)` with `C!=0` and full Euler zero, then L=3 hostile
  control; **or**
- prove scoped obstruction that `-gradS_star` never lies in `span{gradI_j}` on the
  declared nondegenerate curved class with active residual.

Secondary (star-only scout exactification): rationalize the apparent
Cayley/LDU stationary manifold if it survives the four-channel filter.

Do **not** restart from `(a,b)` tuning or from forcing `R=0`.

---

## 1. Research question (F4)

Does there exist a nondegenerate finite configuration with nonzero curvature
that is stationary for some `c in Q^4` in

    S = S_star
      + c_eta_adj I^eta_adj + c_eta_opp I^eta_opp
      + c_n_adj I^n_adj + c_n_opp I^n_opp ?

H1 picture: residual tracks curvature, `R_*(0)=0`, `R_*(C)!=0` at finite curve.
L=2 may discover; L=3 hostile control required before broad finite-carrier
claim.

---

## 2. Relation to star-only Crit search

On quotient-complete strata the #201 stationary-auxiliary theorem says physical
crit of `S_star+Q` match physical crit of `S_star` after gauge.  That justifies
star Euler searches as a **necessary** filter.  It does **not** justify
collapsing the four I-channels to a single `(a,b)` modulus, nor forcing `R=0`
as the geometry ansatz.  Coefficient independence is settled by `rank M=4`,
`ker M=0`.

---

## 3. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_f4_check.py
python3 02_REGISTRY/research/certificates/a4d_homogeneous_curved_stationary_controls_check.py
python3 tools/validate_work.py
python3 tools/validate_repo.py
```

---

## 4. Handoff

Draft PR #202.  Do not merge.  Continue: span search with `R!=0`, then exact
root or scoped no-go, then L=3 before Ready.


## 4. NUMERICAL/STRUCTURAL — minimal parabolic mechanism isolated

The Cayley/LDU candidate has an additional highly non-generic structure.

Stacking the six matrices (P_{rs}-I) reveals a common one-dimensional kernel.
Its generator is null with respect to (eta). After one global proper-Lorentz
gauge rotation this line is the canonical

[
n=(1,1,0,0).
]

In that gauge every link lies, to numerical precision (<10^{-14}), in the
four-dimensional null-line stabilizer (SIM(2)). In standard Lorentz-algebra
coordinates

[
(K_1,K_2,K_3,J_{12},J_{13},J_{23}),
]

each link satisfies

[
(a,b,c,b,c,d),
]

so the two combinations (K_2+J_{12}) and (K_3+J_{13}) are the null
translations.

Consequently every plaquette commutator is parabolic:

[
operatorname{tr}P_{rs}=4,
qquad
det(I-P_{rs})approx0,
qquad
(P_{rs}-I)^3approx0,
]

and both Lorentz bivector invariants of the odd curvature vanish numerically.

This explains why the roots are absent from the generic
(det(I-P)
e0) controls used for quotient-completeness: they live on a
separate parabolic curvature stratum.

### 4.1 Minimal subgroup scan

A full-Euler scan was repeated after restricting each link to subgroups of
(SIM(2)).

- one-parameter sectors: only flat roots;
- all tested two-parameter sectors: only flat roots;
- (K_1+N_2+N_3) (scale plus two null translations): curved roots survive;
- (N_2+N_3+J_{23}), i.e. the exact little group (E(2)) with no null-line
  scale: curved roots survive.

For the (E(2)) three-parameter-per-link sector, a representative root has

[
|mathrm{EL}_{m full}|_2=4.29	imes10^{-14},
qquad
|C|_{m scout}=0.34535,
]

with (detTheta=-1) and
(sigma_{min}(Theta)=0.2713).

Thus the first numerically surviving homogeneous class needs only

[
4	imes3+15=27
]

det-fixed chart variables, not the original 39.

A representative (E(2)) link coordinate set
((N_2,N_3,J_{23})) is

```text
[ 0.088504652044,  0.082911143621, -0.249807924819]
[-0.320461257769, -0.081035776131, -0.303588032463]
[-0.322033101871, -0.137571575304,  0.125148917575]
[ 0.287012659188,  0.226439735406, -0.295275453655]
```

### 4.2 Failed over-simplification control

Fixing all twelve (E(2)) link coordinates to nearby low-denominator rationals
and solving only for the solder does **not** preserve stationarity: the best
tested rounded controls stall at full residual of order (10^{-2}).

Therefore the exact witness cannot be obtained by independently rounding the
links while repairing only the solder. Exact reconstruction must move both
sectors along the stationary manifold.

### Revised exactification target

Work entirely inside the (E(2)) little-group chart. Derive the exact rational
stationary equations there, compute their generic Jacobian rank, and use the
remaining free dimensions to impose rational gauge/normal-form conditions
before elimination.

This is now the smallest observed positive F4 carrier.
