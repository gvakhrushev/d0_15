# EXP-A4D-CENTERED-CARTAN-WARD-REPAIR

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Find the smallest exact replacement for the unmodified forward Cartan matter transformation that restores finite Hodge-action Ward covariance while retaining the forward topological differential and the exact metric-gauge reconstruction.

Repository edits: **NONE**.

## Frozen no-go

E-HWARD already proves:

- no placement/averaging of \(W_m\) alone repairs the Ward identity;
- the unmodified constant forward generator \(L(U-I)\) is not skew for any nondegenerate translation-covariant Hodge pairing;
- the failure is a bulk discrete-Leibniz defect, not a boundary term.

Do not reopen metric-placement-only fixes.

## Required candidates

### A. Centered contraction

Use
\[
A_r=(I+U_r^{-1})/2,
\]
\[
\iota_\xi^{cen}
=
\sum_rM_{\xi^r}A_rc_r,
\]
\[
\mathcal L_\xi^{cen}
=
d_f\iota_\xi^{cen}
+
\iota_\xi^{cen}d_f.
\]

Test exactly:

- constant-\(\xi\) reduction;
- skew-adjointness on the flat counting/Hodge pairing;
- \([d_f,\mathcal L_\xi^{cen}]\);
- constant-coframe identity;
- reconstruction to \`symmetricRoleGradient\`;
- variable-\(\xi\) discrete product defect;
- compatibility with full \(W_m\).

### B. Flux-split transport

Audit operators of the form
\[
G_{\rm flux}
=
\frac12(M_\xi D+DM_\xi)
-\frac12M_{D\xi}
\]
or the exact finite analogue suggested by the discrete continuity equation.

Determine whether such an operator can be derived from a Cartan contraction rather than declared independently.

## Positive target

One coherent finite transformation architecture satisfying simultaneously:

1. forward topological \(d_f^2=0\);
2. \(d_f\)-compatibility/commutation;
3. exact coframe reconstruction to centered metric gauge;
4. constant-vector infinitesimal isometry;
5. exact or telescoping Hodge-action Ward identity;
6. on-shell centered stress conservation.

## Negative target

If no such transformation exists in the current finite carrier class, identify the exact extra carrier/staggering/doubling primitive required.

## Terminal verdict

Return exactly one:

- \`CENTERED-CARTAN-WARD-REPAIR-REACHED\`
- \`CENTERED-CARTAN-DF-COMMUTATION-NOGO\`
- \`CENTERED-CARTAN-COFRAME-RECONSTRUCTION-NOGO\`
- \`FLUX-CARTAN-EXTRA-PRIMITIVE-REQUIRED\`
- \`FINITE-HODGE-WARD-ONLY-CONTINUUM-BRIDGE\`

## Deliverable

\`MEMO_43_A4D_CENTERED_CARTAN_WARD_REPAIR.md\`
