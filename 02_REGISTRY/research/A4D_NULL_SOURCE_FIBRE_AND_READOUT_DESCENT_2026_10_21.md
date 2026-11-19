# Null two-field source: complete nonlinear fibre and exact native-gauge boundary

21 October 2026. Supporting continuation in existing Draft #334,
EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE / native-programme-v1.
Scientific input: 5edac80c86c17014fc83e0aa608e192f43c1fdba.
Publication preserves concurrent c55fcde1091dc5ed5e208ec4234a717433de3505.
Phase: source descent and interpretation of the already-owned continuum
class; no new scientific task or physical price. GR_closed=false.

The [full proof and exact checks](sources/d0_null_source_fibre_2026-10-21/PROOF.md)
resolve a nonlinear identification issue left by the existing
[finite-source/covariant synthesis](A4D_FINITE_SOURCE_AND_COVARIANT_TWO_FIELD_SYNTHESIS_2026_10_21.md).
This is not another spacetime construction. It reuses that source's
rank-two non-VSI witness and the actual weighted-null first-covector identity.

## 1. Complete source fibre, not just one invisible direction

In the positive regular rank-two null sector, put Psi=psi1+i psi2 and
T=Lambda sum_A dpsi_A tensor dpsi_A, with q=tr_g(sum_A dpsi_A^2)=0.
Every local change preserving the SAME g and the ENTIRE T is exactly

    Psi -> f(Psi), Lambda -> Lambda/|f'(Psi)|^2,

with a locally invertible holomorphic or antiholomorphic f. There are no
additional local source-fibre branches on that chart. The null multiplier
representation is invariant off shell, and both scalar-current equations
are transported exactly. This is a complete analytical classification,
not a numerical kernel census. Nonzero kinetic sectors do not inherit
arbitrary target-conformal freedom.

## 2. Intrinsic necessary-and-sufficient inverse

For a positive semidefinite, conserved, Lorentz-traceless rank-two tensor T,
a local representation by two independent exact scalar gradients and one
positive multiplier exists exactly when ker(T) is integrable and

    Lie_V T = beta_V T for every V in ker(T).

Frobenius produces a two-dimensional transverse positive metric up to a
factor; a harmonic coordinate and its harmonic conjugate reconstruct the
scalars. Conservation then forces BOTH scalar equations, by independence
of their gradients. With T=G(g), these are intrinsic necessary-and-sufficient
conditions for the stated regular null metric class. Positivity, rank,
trace and conservation alone are insufficient; an explicit exact hostile
tensor verifies the omitted-condition failure.

## 3. Resolve the characteristic warning with the full coupled source

The old witness has principal speeds +1,-1,+i,-i in an orthonormal frame.
The growing scalar/multiplier branch nevertheless has EXACTLY zero stress
perturbation. It integrates to a full nonlinear family with unchanged g,T:

    f_n(z)=z+(c/k_n)exp[k_n(z-s1)], 0<c<1/2,
    Lambda_n/Lambda=|1+c exp[k_n(s-s1)+i k_n x]|^-2.

All fixed finite-order initial label jets tend to the original data, while
the final multiplier has an explicit nonzero L2 separation. This proves
failure of continuous dependence for those unquotiented label variables
on the fixed covariant chart; it proves no instability of g or T, which
remain identical. An initial nonzero-stress conjecture was rejected by
calculation and is recorded as rejected, not published as a result.
Neither physical gauge nor well-posedness of a quotient is assumed.

## 4. Original native gauge and actual PF-weight application

The native gauge is Lambda vol_g=k0 mu0, k0=-lambda_minus(2^-20).
Holding the native metric, mu0 and k0 fixed also fixes Lambda. Consequently
the complete same-source fibre at FIXED native metric shrinks to

    psi -> O psi+a, O in O(2), a constant vector.

A nonconstant conformal target map instead requires the exact positive
volume Jacobian and generally nonzero shift derived in the proof. It is
not an automatically admitted clock relabeling or an unchanged-collar map.
Each transported null representative retains the original finite Golden
ratio and solves the declared weighted continuum price for every prescribed
positive PF density under its existing constant-slope/zero-baseline-source
hypotheses. This is not a finite-lattice or compulsory-Book transport.

## 5. Concrete readout consumer; concurrent processor work stays distinct

The complete fibre gives an exact local criterion for a supplied observable
to depend only on (g,T): invariance under all the maps above. Its differential
must vanish on

    delta Psi=h(Psi), delta Lambda=-2 Lambda Re h'(Psi), delta g=0,

with the genuine native volume/cut/clock transport retained when applicable.
The test applies to the FULL admitted record/price, not just r(0,0).

The concurrent [fixed-processor/resource theorem](A4D_FIXED_PROCESSOR_JOINT_RESOURCE_SOURCE_2026_10_21.md)
is preserved and consumed at its stated scope. It provides processing-source
stationarity for the supplied independently variable resources of the
primary finite family and retains their physical supply/absolute Book costs.
It does not automatically provide a finite resource map for this distinct
rank-two continuum class. Conversely, the present conformal theorem does
not declare those independently supplied resources physically equivalent.
The common-map and Book03 gates are not relabeled closed by this result.

## Verification

87 exact author-check groups pass in normal and optimized Python, with
byte-identical outputs. Proof/checker/result blobs and SHA256 values are
frozen in [VALIDATION.json](sources/d0_null_source_fibre_2026-10-21/VALIDATION.json).
The universal fibre and intrinsic inverse are analytical proofs; the
checker verifies their algebra and decisive positive/negative applications.
No independent review, fresh historical all40/full128/Lean replay, complete
repository-guard run, or remote CI acceptance is claimed. Existing source
proofs, current parallel work and all physical acceptance states are retained.
