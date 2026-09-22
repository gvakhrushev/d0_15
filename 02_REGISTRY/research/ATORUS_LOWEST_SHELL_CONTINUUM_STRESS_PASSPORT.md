# E-LSHELL-T4 — Lowest-Shell Continuum Stress Passport

CONTROL disposition: **ACCEPT AS RESEARCH / LOWEST-SHELL-LORENTZ-HAMILTONIAN-BRIDGE-OPEN**

Source memo: MEMO_44_ATORUS_LOWEST_SHELL_CONTINUUM_STRESS_PASSPORT.

For every \(L=N+2\ge3\), the lowest positive spatial shell uses the same eight integer labels
\[
\mathcal S_1=\{\pm e_r:r\in Role\}.
\]

With cell-volume normalized finite inner product \(v_L=L^{-4}\), the finite characters map isometrically label-by-label to the same continuum characters on a fixed unit \(T^4\). Thus the direct shell reconstruction
\[
R_L\chi_{k,L}=e^{2\pi i k\cdot x}
\]
is unitary and yields
\[
R_LQ_{1,L}R_L^*=Q_{1,\infty}
\]
exactly for every \(L\ge3\).

Therefore an exact finite interlevel shell isometry \(J_N\) is not needed for this continuum passport.

The mixed shell state reconstructs exactly:
\[
R_L\rho_{1,L}R_L^*=\rho_{1,\infty}.
\]

Stress normalization is also fixed. For raw counting pairing,
\[
T_{ab,L}^{raw}
=
-\frac{\lambda_{1,L}}{4L^4}\delta_{ab},
\]
while the continuum-density tensor is
\[
T_{ab,L}^{dens}
=
L^4T_{ab,L}^{raw}
=
-\frac{\lambda_{1,L}}4\delta_{ab}.
\]
Since
\[
\lambda_{1,L}\to4\pi^2,
\]
the Euclidean continuum tensor is
\[
T_{\infty,ab}^{E}
=
-\pi^2\delta_{ab}
\]
up to the declared stress-sign convention.

This removes exact-refinement and normalization debt for the lowest-shell Euclidean passport.

The remaining physical blocker is genuinely Lorentz/Hamiltonian. The present state occupies a four-Role Euclidean shell. A physical matter interpretation needs:

- a distinguished D0 time Role tied to the causal/Pisot axis;
- a three-dimensional spatial slice;
- a spatial CAR/Hodge operator;
- a positive Hamiltonian such as \(|D_\Sigma|\);
- the lowest spatial mixed shell;
- time evolution;
- Lorentzian stress variation.

Flat Lorentz \(T^4\) is not globally hyperbolic because periodic time produces closed timelike curves, so a physical Hamiltonian passport requires a local Lorentz patch, an unwrapped \(\mathbb R\times T^3\) target, or another globally hyperbolic target.

The homogeneous source also exposes an exact flat-background solvability obstruction: the derivative-only finite gravity response has zero spatial mean, whereas the lowest-shell stress has nonzero mean. This does not invalidate the source. It means the source-free flat background is the wrong expansion point; a sourced background equation must be solved before linearization.

Terminal result:
\[
\boxed{\texttt{LOWEST-SHELL-LORENTZ-HAMILTONIAN-BRIDGE-OPEN}}.
\]
