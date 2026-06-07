# D0 v15 core13 baryon 40/56 synthesis changelog

## 1. PDG/Core-13 three-orbit geometry linked to (V_{\rm shell}).

The PDG/Core-13 passport is re-read as external validation of the frozen three-orbit shell geometry. Its internal content is identified with the finite carrier

V_shell = span{|9>, |11>, |13>} ≅ C^3 .

This supplies the concrete orbital origin for the baryon flavour carrier V_shell^{\otimes 3} without importing PDG labels into the internal algebra.

## 2. Rank-40 and rank-56 carriers certified.

The decomposition

Pi_B^{40} = Pi_S3^flavour \otimes Pi_S3^spin , rank 40

Pi_B^{56} = (1/6) sum_sigma P_sigma^flavour \otimes P_sigma^spin , rank 56

is certified by 05_CERTS/vp_cvft_baryon_40_56_decomposition.py together with the prior spin-flavour scaffold.

## 3. Rank-16 mixed sector identified.

The inclusion algebra

Pi_B^{56} Pi_B^{40} = Pi_B^{40} = Pi_B^{40} Pi_B^{56}

yields the orthogonal complement of rank 16 as the mixed spin-flavour diagonal-symmetric sector. This 16D complement remains internal and anonymous until later transfer.

56 = 40 + 16 .

## 4. Book 04 patched.

Inserted section

04.CVFT.F3c Core-13 orbitals and baryon spin-flavour transfer

after the existing baryon S3 scaffold (F3b). The section states the V_shell identification, the three-body lift, the two carriers, the decomposition, the U_eff anonymous poles, and that PDG names / GeV / widths remain passport-layer operations only.

## 5. PDG passport boundary preserved.

Book 08 PDG/Core-13 passport section now carries the explicit cross-reference:

"The PDG/Core-13 passport validates the three-orbit shell geometry as an external shadow of the internal V_shell carrier. It does not choose the baryon spin-flavour projectors."

Book 05 closure law and forbidden shortcuts updated to enforce carrier certification before external labels. No PDG sorting before frozen poles.

## 6. Remaining work: freeze (U_{\rm eff}^{B,40}) and (U_{\rm eff}^{B,56}), generate anonymous pole sets, then passport.

Next steps after this synthesis:

- freeze the concrete U_eff^{B,40} and U_eff^{B,56} (positive contraction on the certified carriers)
- solve the anonymous pole equations det(I - zeta U_eff^{B,k}) = 0 for k in {40,56}
- transfer the resulting internal pole sets through the spin-flavour dressing map
- apply PDG/Core-13 passport for physical naming, GeV conversion, widths and decay channels only after the frozen internal poles exist.

No .lake, no __pycache__, no external data beyond pinned PDG passport, no PDG sorting before frozen poles.
