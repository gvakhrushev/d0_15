# Root bootstrap source: retain the moving cut, remove only passive re-encoding

28 October 2026, existing research parent PR #334. This continuation follows the [preserved complete chat archive index at its pinned source commit](https://github.com/gvakhrushev/d0_15/blob/063f643d7a760e9203c3f74cba870b256b36fcc3/02_REGISTRY/research/D0_CHAT_RESULTS_2026_10_27_INDEX.md) and the [current integration map](D0_CHAT_RESULTS_INTEGRATION_2026_10_28.md), and consumes Book03 section 03.25 directly rather than another programmed polynomial report.

[Proof in Russian](sources/d0_root_moving_cut_2026-10-28/PROOF_RU.md), [executed checker](sources/d0_root_moving_cut_2026-10-28/check_root_moving_cut.py), [actual result](sources/d0_root_moving_cut_2026-10-28/result.json), [file hashes](sources/d0_root_moving_cut_2026-10-28/MANIFEST.json).

At one finite fixed-rank carrier put Q=I-P, C=QUP, F=C* C, R=(I-zF)^-1 and rho_beta=exp(-beta Delta)/Tr exp(-beta Delta). For the ACTUAL admitted variation of P,U,Delta, define K=[dP,P]. Then [K,P]=dP and

    nabla U=dU-[K,U],  nabla Delta=dDelta-[K,Delta],
    dB=-Tr(rho_beta nabla Delta)
          +2z Re Tr(R C* Q(nabla U)P).

This equals the FULL derivative of the unchanged original heat-plus-logdet action. It is independent of adding any block-diagonal anti-Hermitian generator to K. Simultaneous unitary co-transport of P,U,Delta gives exactly zero; relative motion need not. No free field, projector freezing, selected target source or compulsory microscopic action is introduced. A moving underlying Gram, independent beta/z, rank changes and separate field-dependent charges retain their own explicitly stated treatment.

The source estimate is |dB| <= ||nabla Delta||_op + 2z ||C R||_F ||Q(nabla U)P||_F. Application to a native all42 or raw216 norm still needs the actual map and norm transport; it is not inferred from matrix dimensions.

Executed normal and python -O controls agree: dimensions 3,4,6,8, full exponential and determinant; moving projector, noncommuting variations, exact tangent/co-transport identities and the original Golden base. Maximum five-point discrepancy 7.698841564263148e-12; pure co-transport residual 1.7930101847696278e-16. A real moving-cut control has source 0.06218198611141448 while wrongly freezing P would give zero. These are finite structural controls, not an original native field-family replay or a new GR certificate.

The exact matrix identity is proved; the root-native physical field map and universal Einstein identification are NOT proved by it. GR_closed=false. No Lean, repository CI, merge or scientific acceptance is asserted.
