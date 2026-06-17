# D0 v15 PDG/Core-13 to baryon 40/56 synthesis

**Status:** internal sector law closure for CVFT-F3c.
**Rule:** PDG/Core-13 passport validates the frozen three-orbit shell geometry as external shadow only. It does not select or define the internal baryon spin-flavour projectors. The internal decomposition 56 = 40 + 16 is certified before any external labels.

## Chain

```text
PDG mass passport
→ frozen φ-lattice coordinates
→ Core-13 three-orbit shell geometry
→ V_shell = span{|9>, |11>, |13>} ≅ C^3
→ V_shell^⊗3, dim 27
→ Sym^3(C^3), rank 10
→ spin dyad C^2
→ rank-40 separable symmetric sector
→ rank-56 diagonal spin-flavour carrier
→ U_eff anonymous pole law
→ PDG passport boundary
```

## Core synthesis

The existing PDG/Core-13 passport does not merely show that masses have φ-lattice representatives. Its structural content is the frozen three-orbit shell geometry. D0 now identifies this three-orbit geometry with the finite shell carrier

\[
V_{\rm shell}
=============

\operatorname{span}{|9\rangle,|11\rangle,|13\rangle}
\cong
\mathbb C^3.
\]

The baryon flavour carrier is the three-body lift

\[
\mathcal V_B^{flavour}
======================

V_{\rm shell}^{\otimes3},
\qquad
\dim=27.
\]

The exchange-symmetric flavour sector has rank

\[
\dim\operatorname{Sym}^3(\mathbb C^3)=10.
\]

With the binary spin dyad (D_2\cong\mathbb C^2), D0 obtains two internal spin-flavour carriers before any PDG passport:

\[
\Pi_B^{40}
==========

\Pi_{S_3}^{flavour}
\otimes
\Pi_{S_3}^{spin},
\qquad
\operatorname{rank}=40,
\]

and

\[
\Pi_B^{56}
==========

\frac16
\sum_{\sigma\in S_3}
P_\sigma^{flavour}
\otimes
P_\sigma^{spin},
\qquad
\operatorname{rank}=56.
\]

The rank-40 carrier is a canonical subcarrier of the rank-56 diagonal spin-flavour carrier:

\[
\Pi_B^{56}\Pi_B^{40}=\Pi_B^{40},
\qquad
\Pi_B^{40}\Pi_B^{56}=\Pi_B^{40}.
\]

Thus the internal decomposition is

\[
56=40+16.
\]

The rank-16 complement is the mixed spin-flavour diagonal-symmetric sector. Anonymous pole sets are then defined by

\[
U_{\rm eff}^{B,k}
=================

\Pi_B^kPUP\Pi_B^k,
\qquad
k\in{40,56},
\]

\[
\det(I-\zeta U_{\rm eff}^{B,k})=0.
\]

PDG names, GeV conversion, physical mass assignment and decay widths remain passport-layer operations. The internal spin-flavour carrier is finite and closed before those external labels are applied.

## Certificate

`05_CERTS/vp_cvft_baryon_40_56_decomposition.py`

Required PASS tokens:

```text
PASS_S3_FLAVOUR_AND_SPIN_REPRESENTATIONS
PASS_FLAVOUR_S3_SYMMETRIC_RANK_10
PASS_SPIN_S3_SYMMETRIC_RANK_4
PASS_BARYON_SPIN_FLAVOUR_RANK_40
PASS_BARYON_DIAGONAL_SPIN_FLAVOUR_RANK_56
PASS_RANK40_SUBSECTOR_OF_RANK56
PASS_BARYON_MIXED_SPIN_FLAVOUR_RANK_16
PASS_BARYON_SPIN_FLAVOUR_NO_PDG_ASSIGNMENT
```

Expected rejected-shortcut (negative control) tokens:

```text
FAIL_RANK40_AS_FULL_BARYON_CARRIER
FAIL_PDG_SORTING_BEFORE_SPIN_FLAVOUR_TRANSFER
FAIL_COMPLEX_POLES_FROM_BARE_F
FAIL_RANDOM_NONHERMITIAN_RESONANCE_OPERATOR
```

## Frontier map update

See `D0_CVFT_FRONTIER_OPERATOR_TARGETS.csv`:

- CVFT-F3a remains OPERATOR-SCAFFOLD-CERTIFIED
- CVFT-F3b becomes SPIN-FLAVOUR-CARRIER-CERTIFIED
- CVFT-F3c = CORE13-ORBITAL-LINK-CERTIFIED

External passport remains required for physical particle naming.

## Closure

This completes the positive internal sector law:

finite V_shell (Core-13 three-orbit) → Sym^3 flavour × Sym^3 spin decomposition → rank-40 / rank-56 carriers with inclusion algebra → anonymous U_eff poles → PDG passport boundary only.

No PDG data enters the carrier definition or projector choice. The passport is diagnostic shadow, not constructor.
