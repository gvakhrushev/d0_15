# Worker Task TOWER-I — all-N inductive spectral-triple embedding theorem

## Scope

This is an ordinary worker/Lean task, not an expensive research task.

The finite certificate vp_inductive_spectral_triple_isometric_leg.py shows exact
Dirac-compatible isometric embeddings for the first four transitions of the
graded Fibonacci/Christensen-Ivan tower. It does not prove the all-N theorem.

Do not redo the finite checks. Generalize them.

## Given finite pattern

Level dimensions begin

2, 3, 5, 8, 13, ...

The certificate models the graded Dirac spectrum at level N as the multiset

spec(D_N) = union_{k=0..N} {k}^{m_k}

with initial multiplicities

m_0=2, m_1=1, m_2=2, m_3=3, m_4=5.

The observed transition is monotone: D_(N+1) adds only the new eigenspace at eigenvalue N+1.

## Task 1 — identify the actual general multiplicity formula

Do not extrapolate the finite list by name alone.

Read the existing Fibonacci Bratteli / graded Dirac definitions and prove the exact formula
for m_N from the owned tower.

If the certificate's spectrum is not literally induced by an existing repository Dirac,
record the mismatch and stop the promotion.

## Task 2 — all-N nesting theorem

Prove for every N:

multiset(spec(D_N)) <= multiset(spec(D_(N+1)))

with the exact multiplicity notion used by the formal carrier.

Prefer a theorem stronger than cardinality growth: each old eigenspace must occur unchanged
inside the next level.

## Task 3 — canonical finite-level inclusion once bases are fixed

Construct J_N : H_N -> H_(N+1) as the inclusion of the old graded eigenspaces.

Prove:

J_N^* J_N = I,

J_N^* D_(N+1) J_N = D_N.

If possible prove the stronger intertwining D_(N+1) J_N = J_N D_N.

## Task 4 — basis/canonicity audit

The 0/1 selection matrix in the Python certificate is canonical only after an eigenbasis ordering.

Determine what is genuinely canonical:
- subspace inclusion;
- inclusion up to unitary on repeated eigenspaces;
- or a distinguished map induced by the Bratteli embedding itself.

Do not call a basis-selected map canonical without a theorem.

## Task 5 — relation to the downward archive tower

Do not conflate the Fibonacci AF/CI tower with the 4D role-product metric archive tower.

State explicitly whether this J_N belongs to:
- the Fibonacci AF spectral tower only;
- the archive projective tower;
- or a proved functor between them.

If no bridge exists, preserve that as the residual.

## Negative controls

1. A non-nesting diagonal pair must not admit the claimed inclusion construction.
2. Repeated-eigenvalue basis rotations should demonstrate any non-canonicity of a matrix-level J_N.
3. Dimension growth alone must not imply Dirac compatibility.

## Definition of done

The claim D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001 may gain a Lean-proved EXISTENCE leg only if:
- the all-N spectrum formula is derived from an actual repository Dirac/tower;
- nesting is proved for every N;
- J_N is typed and isometric;
- Dirac compatibility is literal.

The overall row remains PROOF-TARGET unless the separate canonicity/forcing relation to the
owned projective tower is also solved.
