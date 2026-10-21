# Exact full-4D original N1 two-field causal material + regular Lorentz-gauge source bridge

Owner: existing Draft #334, \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, 21 October 2026. Full scientific proofs:
- [Causal two-CAR material Schur](../../A4D_CAUSAL_TWO_SCALAR_FULL4D_EXACT_MATTER_SCHUR_2026_10_21.md)
- [Uniform 42→36 Lorentz Ward and genuine metric10+link24](../../A4D_FULL42_CAUSAL_MATTER_LORENTZ_WARD_METRIC34_BRIDGE_2026_10_21.md)

Run from the repository root (requires numpy/scipy/sympy/mpmath):

\`\`\`sh
OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_causal_full4d_scalar_schur_2026-10-21/check_causal_4d_two_scalar_all_euler.py
OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_causal_full4d_scalar_schur_2026-10-21/check_causal_full4d_independent_cq_price.py
python3 02_REGISTRY/research/sources/d0_causal_full4d_scalar_schur_2026-10-21/check_uniform_metric34_ward.py
\`\`\`

The full-4D checker consumes the ACTUAL old original Golden n24/L8 source \`sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_n1_scalar_flux.py\`: 75,025 true F/R words; 4096 true 4D Role sites; all unequal PF; true six-face non-VSI f; original sigma-minus N1 full output law. Every q is computed from **both** material species and ALL four forward gradients. It constructs a future slice causally by 1296 local 2x2 Sherman-Morrison solves and checks all 2592 interior Euler residuals. The endpoint is numerically within 2e-16 of Euler zero; the separate theorem proves **analytical** existence for sufficiently small causal nonzero data, not an interval proof at this displayed amplitude.

The second checker differentiates the ORIGINAL full binary-CQ entropy via 70-digit complex step on six actual sites, including five forward anchor contributions per site. Both near-zero solved derivatives and NONZERO uncorrected seed derivatives agree with independent source flux, so a different surrogate action cannot pass. The third checker verifies exact symbolic SO(1,3) Ward on TWO arbitrary scalar gradients, the full 6x6 coframe pivot determinant \`B*C^2*D^3\`, and the complete 10x10 lower-coframe → TRUE metric map determinant \`-16*A*B^2*C^3*D^4\`.

**Hostile control:** the causal solution produces nonzero Tx0,Ty0,Txy; the preceding special homogeneous diagonal/pure-boost 42→12 Ward zero-test cannot be used after the real material correction. The earlier independent native spatial J12 pureboost no-go also remains valid. The new SO Ward gives a genuinely more robust 42→36 zero test; with two material Euler equations solved, the geometrical reduced source type is metric10+link24, NOT twelve target rows. The actual material outgoing boundary flux must remain in the reduced geometrical action.

**Scopes NOT proved:** full two-sided Dirichlet (separate earlier numerical owner), actual 16+24 geometry source root with corrected matter, common native Book03 absolute Info/heat/clock/controller, physical field writer/selection, uniform Cauchy stability and generic physical GR; \`GR_closed=false\`. No independent reviewer, fresh Lean formalization or remote scientific CI asserted.