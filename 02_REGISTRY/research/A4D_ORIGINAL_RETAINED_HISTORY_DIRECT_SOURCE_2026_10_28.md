# Original retained full128 history: direct source and the joint error budget

28 October 2026. Existing research PR #334 in `gvakhrushev/d0_15`.
Scientific input: `46ebed17ddfa04faa8ab1a07a6a822b717f993ef`; incoming `39b9c847dbea952016a0f464e786ad817e96d4ad` is consumed and preserved.

[Proof in Russian](sources/d0_original_retained_history_source_2026-10-28/PROOF_RU.md), [executed checker](sources/d0_original_retained_history_source_2026-10-28/check_history_source.py), [observed receipt](sources/d0_original_retained_history_source_2026-10-28/result.json).

## Direct parent application

Consume [the original direct Book source](A4D_CLOSED_HISTORY_DIRECT_PROOF_2026_10_28.md), the already-owned all-blank retained-history return, and [the full clock winding estimate](A4D_NATIVE_CLOCK_WINDING_FULL_SOURCE_2026_10_28.md). No phase Hamiltonian, HDA, price-estimator apparatus, changed decoder or freely chosen source is added. The chronological Kraus product and original all-blank return were already owned; the application here differentiates the complete varying noncommuting history and supplies its normalized error budget.

For original zero-Walsh rows a_j=N_(j,0), let A_j=a_j* a_j, k=2p^2 and C_j=I-k A_j. On the original fresh-register/no-erasure history, with the genuine initial all-blank/protected embedding, the exact complete return is

    K_n=C_n...C_1,
    D_n=(1-z)I+z K_n* K_n,
    J_n=-r_R log det D_n.

Every fine record remains in the whole isometry; the determinant reduction does not remove heat modes. r_R is only a genuine untouched spectator multiplicity. With R_j=C_(j-1)...C_1 and T_j=C_n...C_(j+1),

    W_j=Herm[R_j D_n^-1 K_n* T_j],
    dJ_n=2r_R z k sum_j Tr(W_j dA_j)
        =4r_R z k sum_j Re Tr(W_j a_j* da_j).

The one-tick case is exactly the source of 46ebed17. All da_j are pulled back through the real history map; no independently controllable continuous native gates are granted.

## Controlled history-to-quadratic-source passage

For q_n=k sum_j ||A_j||op, contractions and resolvent bounds give

    ||W_j-I||<=2q_n/(1-z),
    |dJ_n-2r_R z k d sum_j Tr A_j|
       <=4r_R z k q_n/(1-z) sum_j ||dA_j||1.

The proof also retains complete value and C2 estimates. They do not set normal second sources to zero. For the actual admitted field lift L_h, S_h=sum_j Tr A_j, V_h=sup_(||v||<=1)sum_j ||DA_j[L_h v]||1 and true Gamma_h=2r_Rzk gamma_h,

    ||db_h L_h/Gamma_h-DS_GR+matter||
      <=||DS_h L_h/gamma_h-DS_GR+matter||
        +2q_(n_h)V_h/[(1-z)|gamma_h|]
        +||DH_h L_h||/|Gamma_h|.

This applies directly to the native stationary-law implication on the same history. The first geometric-map term is NOT computed for the original full128/all42 carrier by this packet. The whole heat term can consume its existing default-scene or homogeneous-clock owner only at its actual assumptions. Original source repetitions n, raw primitive clock length ell and the incoming retention gadget depth K are distinct.

In particular, the incoming 39b9c847 supplies a positive generated-bank/material-metric/finite-comparison construction and a factorial-heat versus exponential-gain schedule for its larger ten-sign programme. That result is retained, not refuted or relabelled as the original full128 price. q_n->0 is one sufficient regime for the history above, NOT a new universal prerequisite for all other routes.

## Actual checks and a sharp non-scalar history control

163 checks executed in ordinary Python and `python -O`; complete JSON receipts are byte-identical. The original CAR order (0,2,3,1), phases (i,i,-1,-i), mirrored duplicated Julia words, 64 Walsh rows and all128 fine Kraus matrices are reconstructed from pinned constructor blob `d111c5bfeae3c384a4fe725f4a6d19277ea0005a`.

For two different successive original operators, ALL 16384 fine chronological histories are evaluated on all16 DATA columns: a 262144-by-16 retained-history isometry. Its nonblank Gram matches I-K_n* K_n within 4.43e-15; the source matrix within 9.42e-16; the full scalar finite-difference derivative within 3.03e-18. This is no iid-reset channel. oldRIGHT multiplicity in the numerical control is one; the proof separately supplies its actual tensor factor. The huge square multi-tick unitary and its full heat were not materialized.

At original r=1/9,nu=3/5,z=2^-20, exact arithmetic in Q(sqrt(5)) using the OWNED quadratic CAR identity gives

    (partial_r J1)(partial_nu J2)-(partial_nu J1)(partial_r J2)
      =2.1726591352028119199704041947535...e-16 !=0.

The two source ratios are 1.9634495925... and 1.9579348350..., so no single scalar gain identifies these one-/two-tick operator covectors. Exact nonzeroness, not a floating determinant threshold, establishes this statement. It is not a physical all42 admission theorem or a GR impossibility claim.

When A_j=h^2 B_j and n(h)h^2->0, the displayed cumulative-memory estimate supplies a controlled additive-source regime. If one B is repeated and n(h)h^2->T>0, the actual limit instead is -r_R Tr log[(1-z)I+z exp(-2kTB)]. The numeric controls check both regimes without assigning a physical refinement map.

## Evidence and unresolved application

Checker SHA256: `a05b9295a116543c037eb668651195449bb5d7b9b061c70eb73c4a045238253a`; Git blob `9d313ec496f12ac61e118511d9ce706f19e675ae`.
Proof SHA256: `d533d4581cfdb2a8e1b5466d7d30356154bce440013ba486a1da8cf83eabf31d`; Git blob `394f757b77bb28ea590e22825fc6678580853732`.
Receipt SHA256: `9da283dc3baa733a9d87a388db8c0c78359ceebd9796b338909c08cbc7b0952f`; Git blob `370da28388ab569bc7de311304ae664f31758684`.

Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0. No original full42 root, huge full-history heat, Lean, repository CI, repo-wide validation or independent scientific acceptance is claimed. The direct geometric pullback of these SAME a_j, its actual gain/refinement and independent native equations remain unproved. Constructed processor source-realizations are not substituted for them. No merge or claim promotion. `GR_closed=false`.
