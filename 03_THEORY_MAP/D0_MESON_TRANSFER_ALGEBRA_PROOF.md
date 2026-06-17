# D0 v15 Meson Transfer Algebra Proof

## Definitions

Typed carrier: MesonCarrier = Fin E × Fin Gen (e.g. E=4, Gen=3, dim=12).

liftEdge(A) = A ⊗ I_Gen   (for edge-type operators A on E)

liftGen(B) = I_E ⊗ B     (for generation/flavour-type operators B on Gen)

Lower-Hodge seed L_M (generation-blind tension, 400 as seed).

## Theorem Statement

Mesons are phason domain walls on the 1-cochain sector. The typed edge-generation transfer operator

𝒞_χFV^{D0} = Π_M ( liftEdge(L_M) + liftEdge(Γ_χ†Γ_χ) + liftGen(F_fl† F_fl) + liftEdge(V_sp† V_sp) ) Π_M

is self-adjoint and positive semidefinite on the typed carrier. The flavour defect enters exclusively through liftGen. The lower-Hodge 400 is a support/tension seed, not a physical mass. K0 gap labels apply only after the typed operator is frozen. Direct 400→mass promotion and mismatched Gen blocks on edge operators are forbidden.

## Proof (constructive)

Construct deterministic PSD blocks for L_M, Γ_χ†Γ_χ (edge E×E), F_fl†F_fl, V_sp†V_sp (gen Gen×Gen).

Build lifted terms with correct Kronecker shapes (all 12×12).

Form C = Π_M @ (sum) @ Π_M (Π_M = eye for minimal).

Verify:

- shape dim=E*Gen

- self-adjoint (C.T == C)

- PSD (eigvalsh >= -tol)

- flavour only via liftGen terms (by construction; no Gen matrix added via liftEdge)

- lower-Hodge as seed + K0 declared.

See vp_meson_defect_transfer_algebra.py .

## Negative Controls

- FAIL_MISMATCHED_GEN_BLOCK_ADDED_TO_EDGE_OPERATOR

- FAIL_DIRECT_400_TO_MESON_MASS_PROMOTION

- FAIL_GENERATION_BLIND_MESON_TOWER

- FAIL_GAP_LABEL_BEFORE_OPERATOR_FREEZE

## Cert Tokens

PASS_MESON_TYPED_CARRIER_FIN_E_X_GEN

PASS_MESON_LIFTEDGE_SHAPE

PASS_MESON_LIFTGEN_SHAPE

PASS_MESON_TRANSFER_OPERATOR_SELF_ADJOINT

PASS_MESON_TRANSFER_OPERATOR_POSITIVE

PASS_FLAVOUR_DEFECT_ENTERS_ONLY_VIA_LIFTGEN

PASS_LOWER_HODGE_400_AS_TENSION_SEED

PASS_K0_GAP_LABEL_REQUIREMENT_DECLARED

(and the four FAIL_ )

## Book Patch Text (for Book 04 / 05)

Mesons are phason domain walls on the 1-cochain sector. The lower-Hodge value 400 is the minimal eigenvalue of the generation-blind domain-wall tension operator and constitutes a support seed, not a physical mass. Meson masses and widths are read only after the typed edge-generation transfer operator

𝒞_χFV^{D0} = Π_M ( liftEdge(L_M) + liftEdge(Γ_χ†Γ_χ) + liftGen(F_fl†F_fl) + liftEdge(V_sp†V_sp) ) Π_M

is frozen on Fin E × Fin Gen.

The flavour defect enters exclusively through the typed liftGen term. Mismatched Gen×Gen blocks added to an Edge×Edge operator are forbidden. Spectral gaps must carry K0 gap labels before external comparison. Direct 400 promotion to pion/kaon/rho masses is prohibited.

The meson/chiral transfer algebra is closed at the finite typed-operator level. External meson spectroscopy remains a K0-labeled passport layer.

In Book 05 add MESON-TYPED-TRANSFER-CERT-CLOSED (finite typed edge-generation meson transfer operator exists, is self-adjoint/positive, places flavour defect only via liftGen, preserves K0 gap-label discipline).
