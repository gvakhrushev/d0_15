# Independent review of the final main composition, section 3

20 October 2026. Read-only bounded review by full_price_weld.

Reviewed main file:
`02_REGISTRY/research/A4D_EXISTING_PARTS_TO_FULL_PRICE_SYNTHESIS_2026_10_20.md`
in the existing book-source-universality worktree.
SHA-256: `d1d5fb4e3c3008b94356c5cd74d2714494593dbb69b03beb53759ecfa1597b13`.

**PASS for equations (5)-(9) and their physical scope. No blocking defect.**
No additional search, numerical replay, graph census or repository edit.

Assumptions used: K and q have the same fixed positive original718 support,
q is row-stochastic, and the supplied field families are sufficiently smooth
for the stated derivatives. P and pi are the existing K-Perron kernel and
its stationary distribution. f is nonnegative, balanced and normalized.

1. Substituting Omega=c+V_u-V_v+E_uv into S=-log_phi K gives exactly
   `A(f)=sum_u f_u KL_phi(T^f_u||q_u)-c-sum_uv f_uv E_uv`.
   The potential term cancels by balance, including at boundary flows with
   the standard zero-row convention.
2. Canonical c=sum mu Omega and balance give sum mu E=0 identically.
   The exact identity is `A_eff=-c+D`, where
   `D=sum pi_u KL_phi(P_u||q_u)`. At P=q each row's KL value and entire
   first differential vanish. Therefore `dA_eff=-dc` at that point even if
   q and P differ nearby. This does not identify an absolute source from
   normalized q alone or prove equality of higher jets.
3. At P=q, the rowwise KL second differential is
   `sum_uv pi_u (dP_uv-dq_uv)(d'P_uv-d'q_uv)/(P_uv ln(phi))`.
   The factor is 1/ln(phi), with no extra factor two. Row normalization
   removes second-derivative terms, and derivatives of pi multiply the zero
   KL value/first differential. Equation (9) is correct without reversibility.
4. When E=0 the minimizing balanced flow is pi^q q, uniquely on the
   irreducible original graph. All-family binding gives A_eff=-c as an
   identity. A single point match alone does not establish higher-jet binding.

The final revision incorporates both requested precision fixes: the
all-family statement supplies a sufficient guarantee of all-jet equality,
without claiming logical necessity for arbitrary smooth functions; smooth
row-normalization of q is explicit. These clarifications preserve the
reviewed equations and scope. This receipt update performs no new
computations. The root additionally reports its composition checker PASS
(P3/Schur, normalized-KL mixed jet, original 502 suffix; about 0.35 seconds);
that additional execution was not independently repeated by this reviewer.

The synthesis explicitly distinguishes the original scalar33/718 rate,
finite clocks, Julia conditional flags and the stopped all128 operator.
Section 4 forbids applying the scalar Info source to all128 without the
actual same-execution map. It retains Info/work, preparation, absolute
normalization and the compulsory task as unresolved physical inputs.
No scalar-graph-to-full128 or positive-GR promotion was found.
