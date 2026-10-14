# Full CAR current cannot be a single-copy AF right-module observable

Research continuation for the existing #310 current/AF weld. This tests the
next proposed step after the base-level eight-state weld: embed the complete
sixteen-state CAR current in the four-row Fibonacci AF working module while
retaining its old right-module covariance.

## Exact finite result

Use the existing adapted CAR frame
\[
C_{\rm frame}=B_0(T^T\otimes I_4),
\]
the literal four-row record step \(U_4\), its price and blank projections
\(P_4,B_4\), and the three full CAR current matrices
\(\alpha_i=\beta_{e_0}\gamma_{e_i}\), \(i=1,2,3\). In this frame put
\[
 U=U_4\otimes I_4,\qquad P=P_4\otimes I_4,\qquad B=B_4\otimes I_4,
 \qquad A_i=C_{\rm frame}^T\alpha_iC_{\rm frame}.
\]
The common commutant
\[
 \mathcal C=\{X\in M_{16}(\mathbb C):
 [X,U]=[X,P]=[X,B]=[X,A_1]=[X,A_2]=[X,A_3]=0\}
\]
has complex dimension exactly one. Thus \(\mathcal C=\mathbb C I_{16}\).

For a reproducible exact rank proof, vectorize \(X\) columnwise and stack the
six commutator maps. Their coefficient matrix has shape \(1536\times256\).
After the adapted-frame products, all entries are integer polynomials in
\(a,p\), hence lie in \(\mathbb Z[a]\) after substituting \(p=a^2\), where
\[
 p=a^2,\qquad p^2+p=1,\qquad a^4+a^2-1=0.
\]
The last polynomial is the minimal polynomial of \(a\): \(p\) has degree two
and norm \(-1\) in \(\mathbb Q(p)\), so it is not a square there. Reduce the
matrix modulo 11 using \(a\mapsto5\) and \(p\mapsto3\). This is a valid
specialization because \(5^4+5^2-1=0\pmod {11}\), and 2 is invertible.
The exact modular row reduction produces a \(255\times255\) minor with
determinant \(6\pmod {11}\). Its algebraic determinant is therefore nonzero,
so the complex rank is at least 255. The identity matrix is in the kernel,
so the rank is at most 255. Hence the common commutant has dimension one.

The exact replay also checks the boundary controls: the current matrices alone
have commutant dimension 32; the record step and two cuts alone have
commutant dimension 16; omitting the actual record step leaves dimension 2.
Thus the scalar result depends on combining the actual current with the
existing record dynamics.

## Consequence for the AF weld

The four-row AF working module is a right module over the old AF algebra.
Every operator in its existing right-module endomorphism algebra commutes
with that right action. At the first level where a sixteen-state spectator
could fit, \(H_1=L^2(M_2(\mathbb C)\oplus\mathbb C)\) has dimension five and
\(\mathbb C^4\otimes H_1\) has dimension twenty. Its \(M_2\) part accounts
for sixteen dimensions; the only scalar right-module part accounts for four.
Therefore any sixteen-dimensional invariant copy must carry a nontrivial
right \(M_2\) action.

If the full CAR current and the record step/cuts were all transported as
fixed right-module endomorphisms on that single copy, the right \(M_2\) image
would lie in \(\mathcal C=\mathbb C I_{16}\). Its \(M_2\) summand acts
nontrivially, as the \(M_1\)-isotypic subspace has dimension only four;
simplicity then makes its unit act as the identity on the CAR copy. A unital
representation of \(M_2(\mathbb C)^{\rm op}\) cannot have scalar image: the matrix units
\(e_{00},e_{11}\) would be scalar orthogonal idempotents summing to one, while
\(e_{01}e_{10}=e_{00}\) and \(e_{10}e_{01}=e_{11}\) force both to vanish.
This is a contradiction.

So the dimension-based one-copy extension at the \(20\)-dimensional working
module fails for an algebraic reason: the full CAR current plus the record
step leaves no nontrivial commutant for the old AF spectator action. The
base-level eight-state weld is unaffected; its carrier is not invariant under
all three full current operators, as the existing leakage ranks show.

## The obstruction has a sharp abstract two-copy boundary

Write the six operators above as \(S_1,\ldots,S_6\). On two identical copies,
set \(S_j^{(2)}=S_j\otimes I_2\). If a \(32\times32\) matrix \(X\) commutes
with every \(S_j^{(2)}\), write it in \(2\times2\) blocks of size \(16\times16\).
Each block then commutes with every \(S_j\), so the proved scalar-commutant
result forces each block to be scalar. Therefore

\[
  \operatorname{Comm}(S_1^{(2)},\ldots,S_6^{(2)})
      = I_{16}\otimes M_2(\mathbb C).
\]

The old right action now has an explicit algebraic home:
\(x^{\mathrm{op}}\mapsto I_{16}\otimes x^T\) is a unital representation of
\(M_2(\mathbb C)^{\mathrm{op}}\) in that commutant. The certificate checks its
matrix-unit relations and commutation with all six doubled operators. Thus
the one-copy obstruction is sharp as a representation-theoretic statement:
twofold multiplicity suffices abstractly, while one copy cannot work.

The actual level-one AF path module has right multiplicities \((34,21)\) for
the old \(M_2\) and scalar summands. Thus its nontrivial branch has enough
dimension for the sixteen multiplicity slots needed by the two-copy carrier.
This removes a raw dimension objection, but is only a capacity check: the
construction has not identified those slots with the prepared state or shown
that the owned record and refinement maps preserve the proposed carrier.

This does not yet identify those two copies with AF path multiplicity. The
actual inclusion must supply the twofold multiplicity together with its
prepared state, record transition, and refinement maps. That owner-level
identification is now the narrow next test; choosing two path labels alone
would not establish it.

## Scope and next route

This excludes only a **single-copy, fixed-operator, right-module** extension
of the current/record package. The doubled tuple gives an explicit abstract
representation with a nontrivial right \(M_2\) action, but its admission into
an actual AF level is open. Also open are higher multiplicity, a covariant
current that transforms nontrivially with the AF right action, a different
owned refinement, and a whole-core interaction that changes the apparatus
Gram. The Jones map continues to transport the prepared record corner; this
result explains why transporting that corner alone cannot transport the full
CAR current.

The next admissible test is to derive, from existing AF incidence and record
data, either a multiplicity representation with its complete current,
preparation and refinement, or a covariant action of the old AF matrix
coordinates on the current. A chosen subspace of a path basis is not enough.
No physical action, selector, clock, stress law, source/Ward identity, curved
root, GR limit, or #310/#202/#317 terminal is added or closed here.

## Reproduction

The certificate pins the original CAR-current, reference-frame, AF activation
and Jones owners. Its checker reconstructs the literal matrices, verifies the
modular specialization and pivot minor, and records the exact scope controls.
The finite rank is established by an exact modular minor argument. A narrow
Lean capsule separately proves the algebraic consequence that no unital
ring homomorphism \(M_2(\mathbb C)\to\mathbb C\) exists; the concrete
1536-by-256 rank computation is not claimed as a Lean theorem.
