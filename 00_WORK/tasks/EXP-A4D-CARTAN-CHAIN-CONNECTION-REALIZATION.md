# EXP-A4D-CARTAN-CHAIN-CONNECTION-REALIZATION

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Construct or terminally classify the first genuinely new geometric object required by E-PDH-PARENT: a local discrete Cartan/chain transport connection whose curvature closes the centered-Cartan matter transport while preserving the accepted primal/dual Hodge parent architecture.

Repository edits: **NONE**.

## Frozen no-go

Do not revisit coframe-only nonlinear transport or a directly stored global Hodge matrix.

Accepted facts:

- the affine coframe gauge remains \(\delta e=d_f\xi\);
- the centered metric gauge remains \(\delta m=K_N\xi\);
- on the odd-\(L\) one-role sector the metric constraint forces nonlinear coframe transport to vanish;
- exact \(L=5\) centered-Cartan commutators already contain radius-two curvature;
- no radius-one \(e\)-dependent generator can absorb it;
- direct Hodge congruence evolution grows stencil.

## Main construction target

Identify a local associative link group or groupoid \(\mathcal G\) with elementary transports
\[
\Omega_r(x)\in\mathcal G
\]
acting on primal and dual cochain fibres.

Required properties:

1. exact Wilson-like link transformation law;
2. a finite-dimensional local representation on the 16-state cochain fibre or the minimum bounded local enlargement;
3. degree preservation and compatibility with the forward cubical differential;
4. flat infinitesimal generator equal to centered Cartan;
5. curvature reproducing/absorbing the known commutator closure;
6. no growth into an explicitly stored dense global matrix.

Use the existing generic Wilson-link covariance owner only as an algebraic template; it does not select the required group.

## Constitutive Hodge target

Construct or classify a bounded-stencil equivariant law
\[
\star=\mathcal S(e,n,\Omega)
\]
such that:

- \(\mathcal S\) is local with \(N\)-independent stencil;
- at the flat point,
  \[
  D_e\mathcal S[d_f\xi]
  \]
  reproduces the accepted staggered Hodge tangent response;
- under the full transformation,
  \[
  \delta\mathcal S=G_D\mathcal S-\mathcal S G_P;
  \]
- the mixed primal/dual parent action therefore has an exact finite Ward identity.

## Structure-group audit

Test in increasing order:

- chain automorphism stabilizer / local matrix group on exterior degrees;
- semidirect Cartan-transport × frame/Lorentz component;
- Clifford/exterior representation naturally inherited from landed CAR;
- whether a genuine local factorization theorem exists or an extra primitive must name the group/representation.

A pure SO(1,3) spin connection is not sufficient unless the scalar obstruction is also represented.

## Terminal verdict

Return exactly one:

- \`CARTAN-CHAIN-CONNECTION-REACHED\`
- \`LOCAL-CHAIN-GROUP-REPRESENTATION-MISSING\`
- \`HODGE-CONSTITUTIVE-MAP-MISSING\`
- \`CONNECTION-LOCAL-FACTORIZATION-NOGO\`
- \`CARTAN-CONNECTION-NEW-PRIMITIVE\`

## Deliverable

\`MEMO_49_A4D_CARTAN_CHAIN_CONNECTION_REALIZATION.md\`
