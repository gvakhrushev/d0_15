# CVFT Overclaim Audit

Scope: Books 00-08, theory-map documents, claim maps and CVFT certificates.

## Checked Forbidden Phrases

The following phrases must not appear as positive claims:

```text
D0 solved quantum gravity
QFT destroyed
virtual particles do not exist
dark matter does not exist
H0 does not exist
DESI resolved
SPARC resolved
IceCube fixed
Yang-Mills mass gap solved
Hawking spectrum closed
alpha derived / α derived without proved trace identity
CERT-CLOSED without theorem/cert/runner
```

Audit result after this pass:

```text
No positive occurrence found for the forbidden natural-language overclaims.
Existing CERT-CLOSED rows are retained only where a theorem/cert/runner is
listed in the claim/status map.
```

## Rewrites Applied

- Feedback-return operator is `F_N=P_N U_N^dagger Q_N U_N P_N`.
- Positive response is `R_N^resp=D_N^dagger D_N`.
- Feedback pressure is `P_fb=beta^(-1)d_V log Z_N`; pressure is not written as
  `P_N`, because `P_N` is the retained-sector projector.
- Bare positive `F_N` supplies stability/leakage diagnostics only.
- Complex resonance poles are assigned to `U_eff=P_N U_N P_N` or an explicitly
  defined Feshbach-Schur effective operator.
- DESI/SPARC failure is a boundary-derivative diagnostic, not a resolution.
- IceCube dynamic feedback remains an external passport candidate.
- Hawking/greybody, hadron pole transfer, coefficient-origin trace identities,
  UV feedback-tail cuts, Yang-Mills leakage lower bounds and boundary-rank
  localization are frontier programs.

## Accepted Claims

- The derived feedback-return object is admissible as a finite operator layer.
- The unitarity-defect identities and positivity are the intended formal owner
  for the core CVFT layer.
- Resolvent and log-det expansions require the stated finite spectral domain.
- Pressure-capacity gravity may use `P_fb` only as source/regime selector, while
  heat-trace/capacity owners remain separate.

## Weakened Claims

- "Matter poles" are weakened to terminally projected near-critical
  feedback-defect modes unless `U_eff` or Feshbach-Schur dynamics is supplied.
- "DESI/SPARC correction" is weakened to derived boundary-derivative feedback
  with no root/window/arbitrary-kernel refit.
- "Dark/halo response" remains non-terminal feedback-pressure response
  candidate, not a particle/no-particle verdict.
- "Hawking spectrum" and "Yang-Mills mass gap" remain frontier proof targets.

## Rejected Overclaims

- `Q_N != 0` implies `F_N != 0`.
- Determinant trace expansion without the logarithm.
- Complex poles from bare positive `F_N`.
- DESI, SPARC or IceCube resolved without frozen operator and external runner.
- LQG/string/AdS equivalence without bridge proof.
- Yang-Mills mass gap without a positive leakage lower-bound theorem.
- `S=A/4` replacement without capacity witness and boundary-rank lemma.

## Remaining Proof Obligations

See `03_THEORY_MAP/D0_CVFT_FRONTIER_OPERATOR_PROGRAM.md` F1-F7.

## CVFT_V3_V4_V5_FORBIDDEN_PATTERNS

Machine-readable forbidden patterns for CVFT frontier theoremization:

```text
DESI resolved
SPARC resolved
IceCube fixed
H0 does not exist
dark matter does not exist
QFT destroyed
Yang-Mills mass gap solved
Hawking spectrum closed
alpha derived
alpha derived from 359
baryon decuplet masses computed
PDG roots assigned
A/4 from rank bound
A/4 from rank bound alone
delta0^12 radius of convergence
delta12 convergence radius
complex poles from F
complex poles from F_N
z/(1-z) logdet bound
z/(1-z) log-det bound without rho
rank bound as A4 proof
S_DE EP as DESI pass
H0 nonexistence overclaim
random non-Hermitian resonance operator
```

Accepted tightened wording:

- log-det and UV-tail bounds use `a=|z|rho(F)<1`;
- boundary rank supports localization only, not A/4;
- F3 is `OPERATOR-SCAFFOLD-COMPLETE`, not baryon-mass closure;
- S_DE EP is effective two-mode transfer algebra, not DESI/H0/cosmology
  closure;
- complex poles require `U_eff` or Feshbach-Schur.
