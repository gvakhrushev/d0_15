# EXP-A4D-PRIMAL-DUAL-HODGE-PARENT-WARD

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Extend E-STAGHODGE beyond the flat tangent result to the minimum honest finite parent architecture that preserves locality and descends matter Ward covariance to centered metric stress conservation.

Repository edits: **NONE**.

## Frozen results

Do not revisit pointwise metric-only Hodge weights or diagonal staggered repairs.

Use the accepted pre-centered coframe
\[
e_r{}^a(x),
\qquad
\delta e=d_f\xi,
\]
the centered readout
\[
m=R(e)+n,
\]
and the exact flat tangent non-diagonal Hodge response
\[
\mathfrak H(d_f\xi)=-(G_\xi^*+G_\xi).
\]

For even \(L\), retain the explicit Nyquist metric residue \(n\).

## Main questions

1. What is the smallest nonlinear or \(e\)-dependent coframe transformation
   \[
   \delta_\xi e=d_f\xi+\operatorname{Transport}_\xi(e)+\cdots
   \]
   compatible with centered Cartan matter transport?
2. Is a discrete connection/spin-connection unavoidable for local frame covariance?
3. Can the primal/dual Hodge star be defined as a bounded-stencil constitutive map for finite \(e\) without forming a dense inverse?
4. Can a mixed parent action implement the codifferential locally?
5. What exact transformation law should the Nyquist residue \(n\) have?
6. Can one formulate an exact joint Ward identity for the parent action?
7. Does the parent constraint
   \[
   m=R(e)+n
   \]
   plus the coframe EOM imply
   \[
   \operatorname{centeredRoleDivergence}\Lambda=0
   \]
   for the metric multiplier/stress?
8. Which frame-kernel directions are gauge, constrained auxiliary data, or require a connection?

## No-go control

Use the integrability condition from E-STAGHODGE: a fixed \(e\)-independent centered generator cannot integrate the flat tangent covariance law for arbitrary \(e\). Do not hide this by postulating a finite \(W(e)\) with inconsistent mixed derivatives.

## Positive endpoint

A theorem-ready finite parent architecture with:

- local primal/dual carriers;
- bounded-stencil Hodge constitutive law;
- nonlinear/e-dependent matter/coframe transformation;
- exact or telescoping Ward identity;
- coframe EOM;
- honest descent to centered metric stress conservation.

## Terminal verdict

Return exactly one:

- \`PRIMAL-DUAL-PARENT-WARD-REACHED\`
- \`DISCRETE-SPIN-CONNECTION-REQUIRED\`
- \`NONLINEAR-COFRAME-TRANSPORT-MISSING\`
- \`NYQUIST-RESIDUE-COUPLING-UNSELECTED\`
- \`PRIMAL-DUAL-FINITE-LOCALITY-NOGO\`

## Deliverable

\`MEMO_47_A4D_PRIMAL_DUAL_HODGE_PARENT_WARD.md\`
