# A4D resonance divisor and exact diagonal Smith pole

**Lane:** EXP-A4D joint Palatini / resonance response

**Class:** RESEARCH / SYNTHESIS

**Status:** exact diagonal algebra recorded; multivariable response remains open

**Firewall:** no BOOK/claim promotion, no Einstein identification, no finite \(T_{\mu\nu}\).

## Terminal results

```text
A4D-RESONANCE-LOCUS-IS-A-NONEMPTY-PROPER-DIVISOR
A4D-PHASE-COUNT-NULLITY-LAW-REFUTED
A4D-DIAGONAL-LOCAL-SMITH-EXPONENTS-1x4-2x4
A4D-STATIONARY-RESPONSE-RESIDUE-UNDETERMINED
```

Withdrawn and not to be reused:

```text
A4D-ORTH3-SIMPLE-POLE-RES-110   # inconsistent Q assembly
A4D-RESONANCE-IS-TWO-POINTS     # contradicted by exact off-diagonal points
```

## 1. Exact local algebra on the diagonal

For \(Z=(z,z,z,z)\), the exact certificate rebuilds the \(24\times24\)
connection Hessian and verifies

\[
\det A(z)=\frac{(z^2+1)^{12}}{16z^{12}}.
\]

At \(z=i\), \(\operatorname{rank}A(i)=16\), so the nullity is eight, and
the induced first derivative from kernel to cokernel has rank
\(\operatorname{rank}(N_LA'(i)N_K)=4\). These exact facts determine the
local one-variable Smith exponents. For an analytic matrix germ, the
positive exponents \(e_j\) satisfy:

- their number is the nullity, eight;
- the induced first derivative has rank equal to the number with \(e_j=1\),
  here four;
- their sum is the determinant zero order, twelve.

The remaining four exponents are at least two and sum to eight. Therefore
the exact local exponents are \((1,1,1,1,2,2,2,2)\). In particular,
\(A(z)^{-1}\) has pole order exactly two on this diagonal curve.
The reproducible exact calculation is
[`a4d_ward_diagonal_smith_check.py`](certificates/a4d_ward_diagonal_smith_check.py).

The submitted histogram of coordinate-column slopes (six fitted order-one
columns and eighteen fitted order-two columns) is a separate floating-point
diagnostic at four dyadic detunings. It is basis-dependent and is not the
Smith multiplicity. It does not contradict the exact \(4+4\) invariant
factors.

## 2. The resonance set and the proposed phase-count law

The exact counterexample in merged PR #314 gives rank 24 at
\(Z=(1,1,1,1)\) and rank 22 at \(Z=(-1,-1,i,i)\). Thus the Laurent
determinant is not identically zero but vanishes at a point of the character
torus. Its zero set is a nonempty proper divisor; this does not classify
its components or rank strata.

The proposed rule based only on even counts of \(+i\) and \(-i\) is false.
At \((-1,-1,i,i)\), the counts are \((2,0)\), but exact elimination over
\(\mathbb Q(i)\) gives nullity two, while the rule predicts four. The
continuous-phase control written with \(e^{\pm2\pi i/3}\), after exact
normalization, has rank 20 over \(\mathbb Q(i,\sqrt3)\). See the merged
owner [`A4D_RESONANCE_DIVISOR_RANK_LAW.md`](A4D_RESONANCE_DIVISOR_RANK_LAW.md)
and its exact certificate.

The diagonal determinant has a zero of order twelve at \(z=\pm i\); this is
the intersection multiplicity along that curve, not a factorization of the
full four-character determinant. Exact full-torus strata remain open.

## 3. Response claims and their scope

The earlier value \(\mathrm{Res}\approx110.85\) is withdrawn: its mixed block
retained a nonzero background connection in an inconsistent slot assembly.
The supplied replacement scripts report zero floating-point norms for the
flat linear contraction at three detunings. Those samples do not by
themselves prove an identity along the detuned family. The exact owner
`E_Q(q,0)=0` from PR #249 concerns the identity-connection point; it does not
identify every mixed block or its derivative on the character-resolvent
family. The coordinate map between those owners must be stated before their
claims are composed.

There is now a separate exact result for the selected real-COS Orth3 ray:
the full 96-row \(t^3h\) connection source on the #241 slow solder has a
nonzero Fredholm pairing, so the proposed range correction does not exist.
Its direct 40-row metric coefficient is nonzero but off-shell. It is not a
stationary-sheet response or a residue. This is recorded in merged PR #314,
[`A4D_ORTH3_NONFLAT_T3H_RESPONSE.md`](A4D_ORTH3_NONFLAT_T3H_RESPONSE.md).

The user-supplied `a4d_response_pole_spectrum.py` returns zero fitted response
orders for all 24 columns at its sampled detunings. This remains a numerical
diagnostic: it neither proves exact cancellation on a divisor nor supplies a
nonflat stationary continuation. Likewise, the finite zero samples for F7
do not establish metric invisibility in every channel.

## 4. Open research gates

1. Factor or otherwise classify the full Laurent determinant and the rank
   strata inside its divisor. Do not revive the refuted phase-count formula.
2. Reconcile the exact slot conventions for the flat \(E_Q\) owner and the
   character-resolvent mixed block; then certify the proposed contraction
   symbolically rather than by finite floating-point samples.
3. For a nonflat stationary sheet, compute the mixed block and its detuned
   limit. The selected exact-resonance Orth3 ray is blocked at \(t^3h\), so
   its raw \(t^3h^2\) coefficient cannot answer this gate.

Draft #310 already owns the exact resonance-response/uniformity task boundary;
any continuation should update that owner rather than open a duplicate task.
The curved stationary search #202 is a different carrier.

## 5. Reproduction and evidence boundaries

- Exact diagonal determinant, nullity, induced-derivative rank, and local
  exponents: `certificates/a4d_ward_diagonal_smith_check.py` and its JSON.
- Exact full-torus divisor counterexample and normalized control: merged
  `certificates/a4d_resonance_divisor_counterexample_check.py`.
- Exact selected Orth3 \(t^3h\) obstruction and off-shell metric coefficient:
  merged `certificates/a4d_orth3_slow_t3h2_check.py` and its JSON.
- Floating-point column-slope and response spectra are diagnostics only.
- The old final-synthesis source headers claiming `Orth3 Res != 0` are stale;
  their sampled zero outputs do not certify a nonzero residue or a family-wide
  identity.
