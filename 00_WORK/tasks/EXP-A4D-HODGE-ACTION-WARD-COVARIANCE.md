# EXP-A4D-HODGE-ACTION-WARD-COVARIANCE

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Attack the exact remaining conservation theorem identified by E-CDIFF.

Assume the forward cubical differential, CAR Cartan calculus and exact reconstruction
\[
\mathcal C_1(d_f f)=Df,
\qquad
\delta_\xi m=\texttt{symmetricRoleGradient}(N,\xi)
\]
as the intended finite architecture.

Determine whether a full-metric Hodge matter action admits an exact joint transformation identity sufficient for on-shell centered Role stress conservation.

Repository edits: **NONE**.

## Required reading

- \`02_REGISTRY/research/A4D_CENTERED_CUBICAL_DIFFERENTIAL_WARD.md\`
- \`02_REGISTRY/research/A4D_CAR_HODGE_METRIC_ACTION.md\`
- finite metric carrier/Hodge packets;
- centered Role integration-by-parts owners;
- active CAR/metric workers if landed.

## Main target

For a matter action \(S_N[m,\psi]\), test the exact identity
\[
D_mS_N[m,\psi][K_N\xi]
+
D_\psi S_N[m,\psi][\mathcal L_\xi^f\psi]
=
0
\]
or a finite total-divergence/telescoping equivalent, where
\[
K_N\xi=\texttt{symmetricRoleGradient}(N,\xi).
\]

The resulting theorem should imply, on the matter equation of motion,
\[
\operatorname{div}_cT_N=0
\]
using the already-owned adjoint theorem for \(K_N\).

## Hodge-weight covariance

Derive the precise finite condition on the metric-dependent exterior weight \(W_m\):
\[
\dot W_m[K_N\xi]
+
(\mathcal L_\xi^f)^*W_m
+
W_m\mathcal L_\xi^f
=
\text{lattice divergence / telescoping term}
\]
or determine the corrected identity.

Do not assume the continuum Leibniz rule: the forward derivative obeys a shifted discrete product rule.

## Staggering audit

Compare the minimum exact choices:

1. site-diagonal \(W_m(x)\);
2. cell-anchor metric weights;
3. cell-center/corner averages;
4. link/staggered metric reconstruction compatible with the forward differential;
5. an explicitly modified Cartan action.

Use exact small-lattice controls where helpful.

The goal is to find the **smallest corrected action**, not merely to report that the naive one fails.

## Actions

Audit both:
\[
S_D=\langle\psi,D_m\psi\rangle_{W_m}
\]
and
\[
S_2=\tfrac12\langle D_m\psi,D_m\psi\rangle_{W_m}.
\]

State whether the Ward theorem holds off-shell, on-shell, or only after a boundary/telescoping sum.

## Firewalls

Do not claim continuum diffeomorphism invariance.

Do not replace the exact forward Cartan transformation by an independently declared centered matter transformation.

Do not infer conservation just because the limit is identified with a covariant continuum theory.

## Terminal verdict

Return exactly one:

- \`HODGE-WARD-COVARIANCE-REACHED\`
- \`HODGE-WARD-STAGGERED-ACTION-REQUIRED\`
- \`HODGE-WARD-DISCRETE-LEIBNIZ-NOGO\`
- \`HODGE-WARD-METRIC-WEIGHT-INTERTWINER-MISSING\`
- \`HODGE-WARD-ONLY-CONTINUUM-BRIDGE\`

## Deliverable

\`MEMO_41_A4D_HODGE_ACTION_WARD_COVARIANCE.md\`
