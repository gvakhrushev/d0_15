# E-CDIFF — Centered Cubical Differential / Ward Compatibility

CONTROL disposition: **ACCEPT AS RESEARCH / WARD-CARTAN-INTERTWINER-MISSING**

Source memo: MEMO_39_A4D_CENTERED_CUBICAL_DIFFERENTIAL_WARD.

The canonical topological differential should remain the forward cubical operator
\[
d_f=(N+2)\sum_r(U_r-I)C_r^\dagger.
\]
Commuting site translations plus creation-creation CAR imply \(d_f^2=0\); degree raising is a separate support theorem.

A centered exterior differential
\[
d_c=\sum_rD_rC_r^\dagger
\]
is also nilpotent, but it is not a valid replacement for the topological cubical differential. At \(L=2\), every centered derivative vanishes, so \(d_c=0\) on the full cochain space; more generally every even \(L\) has a Nyquist zero-mode doubling. The centered calculus therefore has the wrong finite cohomological kernel.

The key positive finite identity is exact:
\[
D_r=A_r\nabla_r^+,
\qquad
A_r=\frac{I+U_r^{-1}}2.
\]
Thus forward link derivatives reconstruct to the owned centered vertex derivative by link-to-vertex averaging.

Define contraction by local Role vectors from the CAR annihilators,
\[
\iota_\xi=\sum_rM_{\xi^r}C_r,
\]
and the forward Cartan operator
\[
\mathcal L_\xi^f=d_f\iota_\xi+\iota_\xi d_f.
\]
For constant coframes,
\[
\mathcal L_\xi^f\theta^b=d_f\xi^b.
\]
After exact one-form centering and symmetrization this yields
\[
\delta_\xi m
=
\texttt{symmetricRoleGradient}(N,\xi)
\]
exactly. The forward matter calculus and centered metric gauge therefore admit one common finite algebraic provenance.

The remaining theorem is action-level:
\[
D_mS[K_N\xi]
+
D_\psi S[\mathcal L_\xi^f\psi]
=
0,
\]
or an equivalent Hodge-weight covariance/telescoping identity. A naive unstaggered scalar control fails exactly, so this Ward theorem cannot be claimed from \(d^2=0\) and Cartan alone.

The first implementation package should formalize full CAR relations, the literal cochain carrier, forward differential, nilpotency/degree, exact forward-to-centered averaging, Cartan, and the capstone reconstruction to \`symmetricRoleGradient\`.

Terminal result:
\[
\boxed{\texttt{WARD-CARTAN-INTERTWINER-MISSING}}.
\]
