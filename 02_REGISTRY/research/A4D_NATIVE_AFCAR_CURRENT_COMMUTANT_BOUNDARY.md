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
the old \(M_2\) and scalar summands, but its level-one price cut still blocks
the doubled package. In the full AF carrier the owned cut has rank
\(2d_1=10\), whereas the doubled CAR cut has rank \(2\cdot4\cdot2=16\).
An isometric intertwiner would inject a 16-dimensional range into a
10-dimensional range. Thus the larger path multiplicity alone does not weld
the record/current package at level one.

## A canonical two-copy record/current weld at level two

The actual AF split supplies the needed finite multiplicity one level later.
Write the owned first inclusion as

\[
A_1=M_2\oplus\mathbb C\longrightarrow A_2=M_3\oplus M_2,
\qquad (X,y)\longmapsto(\operatorname{diag}(X,y),X).
\]

Inside \(H_2=L^2(M_3\oplus M_2,\tau_2)\), take the old-\(M_2\)
bimodule
\[
E_2=L^2(eM_3e)\oplus L^2(M_2),\qquad e=\operatorname{diag}(1,1,0).
\]
These are the two actual diagonal \(M_2\)-to-\(M_2\) path corners selected
by the inclusion. Their normalized matrix-unit vectors give
\(\dim E_2=4+4=8\); no path labels are chosen from an unordered list.

Split the CAR spectator index as \(s=2\ell+v\), where \(\ell\) is the
old left matrix row and \(v\) is one of these two AF paths. Keep the old
right matrix column as the two-copy factor. This defines a basis permutation
\[
K_2:\mathbb C^{16}\otimes\mathbb C^2\longrightarrow
\mathbb C^4\otimes E_2,
\]
from \((\text{apparatus},s,\text{right column})\) to
\((\text{apparatus},v,\ell,\text{right column})\). It is an isometry of
32-dimensional spaces. On its image the actual AF record, price and blank
operators are exactly the doubled CAR operators
\[
K_2^*(U_{AF,2},P_{AF,2},B_{AF,2})K_2
   =(U_{CAR},P_{CAR},B_{CAR})\otimes I_2.
\]
The old right \(M_2^{\mathrm{op}}\) action on \(E_2\) is its actual
matrix-column action and corresponds to \(I_{16}\otimes x^T\). Hence all
three transported spatial CAR currents \(\alpha_i\otimes I_2\) are
right-\(M_2\)-linear on this weld.

The prepared state also binds. In the owned adapted CAR frame the whole-blank
vector is \(\psi_{CAR}=a|0,0\rangle+p|2,1\rangle\). Under \(K_2\) it
becomes the AF blank
\[
\psi_{AF}=a|0\rangle_{app}\otimes|v=0,\ell=0,r=0\rangle
       +p|2\rangle_{app}\otimes|v=1,\ell=0,r=0\rangle,
\]
inside the actual four-row frame \(V_2:\mathbb C^4\otimes H_2\to H_5\).
The AF price/blank cuts and full record step intertwine on all 32 states; on
this prepared state one actual record step gives the full CAR source current
\((1,2ap,0,0)\) and Lorentz norm \(p^6\). The full \(H_5\) carrier has
dimension 233. The welded image is 32-dimensional and its 201-dimensional
orthogonal complement stays present.

## The fixed weld does not own the full CAR current as an AF observable

Right \(M_2\)-linearity on the active corner is not enough to make the CAR
current an element of the full AF observable algebra. The path bit \(v\) in
\(K_2\) is also the simple-summand label of
\(A_2=M_3\oplus M_2\). Let \(z=(1_{M_3},0)\) be its first central projection
and let \(p_0\) project the CAR spectator onto \(v=0\). The exact weld and
the actual \(A_2\to A_5\) right action satisfy

\[
R_{\iota(z)}K_2=K_2(p_0\otimes I_2).
\]

Every AF-left observable \(T\) commutes with this right action. If it extended
the full current on the fixed weld, \(TK_2=K_2(\alpha_i\otimes I_2)\), then
the displayed identity and injectivity of \(W_2\) would force
\[
[p_0,\alpha_i\otimes I_2]=0.
\]
The exact CAR matrices violate this for \(i=1,3\); only \(i=2\) preserves
the path center. The three doubled commutator ranks are exactly \((32,0,32)\).
The certificate checks the right-center intertwiner both on
the working module and after the literal inclusion into \(H_5\), so this is
an owner-algebra obstruction, not a dimension count. Thus the complete CAR
current cannot be represented by an AF-left observable while retaining this
particular \(K_2\) path binding. The finite expectation/current value on the
prepared state remains correct; the obstruction concerns extending the full
operator tuple. It does not exclude a different encoding or a joint
AF\(\otimes\)CAR observable already owned elsewhere in the core.

## A same-simple two-copy weld carries the full current in an AF corner

At the next actual level,
\[
A_3=M_5\oplus M_3,\qquad
(X,y)\mapsto(\operatorname{diag}(X,y,X),\operatorname{diag}(X,y)),
\]
the old \(M_2\) occurs twice inside the same \(M_5\) summand. Use rows
\(0,1\) and \(3,4\) for the two copies, and the common right columns
\(0,1\). Thus
\[
E_3=\operatorname{span}\{e_{r,c}:r\in\{0,1,3,4\},\ c\in\{0,1\}\}
\subset L^2(M_5),\qquad \dim E_3=8.
\]
The CAR path label is now a row-multiplicity label within one simple block;
the right \(M_2\) column is unchanged when the current mixes paths. The
isometry
\[
K_3:\mathbb C^{16}\otimes\mathbb C^2\to\mathbb C^4\otimes E_3,
\qquad (a,\ell,v,c)\mapsto(a,\ell+3v,c)
\]
intertwines the full CAR current \(\alpha_i\otimes I_2\), record step, and
both cuts on its 32-dimensional image.

The current on the selected \(M_5\) rows is the complete CAR triple. Its
canonical support \(P_+\in M_{20}\) is identity on apparatus times rows
\(0,1,3,4\), and zero on row 2; the \(M_3\) component is zero. Thus
\[
Y_{i,+}Y_{j,+}+Y_{j,+}Y_{i,+}=2\delta_{ij}P_+,
\qquad Y_{i,-}=0.
\]
The right-\(A_3\) module closure of \(K_3\) includes all five columns over
these four rows, so this is exactly its induced support. The current extends
by zero on the unused left-module directions, so no additional current is
assigned there. Since \(Y_{i,+}\otimes I_5\) is
right-\(A_3\)-linear, the owned six-step path isometry
\(S_+:\mathbb C^{20}\to\mathbb C^{89}\) gives actual observables
\[
\widehat\alpha_{i,+}=S_+Y_{i,+}S_+^*\in M_{89},\qquad
\widehat\alpha_{i,-}=0\in M_{55},
\]
in \(A_9=M_{89}\oplus M_{55}\). Their common corner unit is
\(Q_+=S_+P_+S_+^*\), of rank 16. The full native AF complement remains
present. The same path coordinates place the owned record unitary and both
cuts in these blocks.
The actual CAR blank maps to the two row copies; after one owned record step
the native current readout is \((1,2ap,0,0)\) with Lorentz norm \(p^6\).
Because the complete current now belongs to the actual AF algebra \(A_9\),
the already proved Jones \(*\)-homomorphisms transport this operator corner
through every later level. This closes the operator-level Jones transport
for this seeded representation class. It does not yet identify the
prepared vector with the Jones GNS conditional vector or give physical
admission, a joint field tangent, source/Ward identity, or curved solution.

### The fixed prepared seed does not bind to the canonical Jones GNS vector

The next state test is now exact. In the regular \(A_9\) GNS representation,
let \(G\) be the owned six-step frame from the old \(M_5\) block into \(M_{89}\),
\(e=GG^*\), and \(S\) the owned same-simple right-module frame used for the
native current. The recorded CAR blank has the single old right column
\(c=0\). Its 20-component row-amplitude vector has
\(v_0=p\), \(v_3=p-1\), \(v_{15}=v_{18}=ap\), and all other entries zero.

Set \(y=Sv\), \(z=G e_0\), and \(X=yz^*\).

This is its rank-one GNS matrix in the \(M_{89}\) block; the \(M_{55}\) block
is zero. Its squared GNS norm is \(p^{10}=34-55p\), while
\(\tau_9(e)=p^6=5-8p\), so \(X/\sqrt{p^{10}}\) and \(e/p^3\) are both
normalized. Although the source keeps the chosen right column (\(Xe=X\)), it
is not in the left Jones corner. The exact off-corner probability is

\[
\frac{\|(1-e)X\|_{L^2(A_9,\tau_9)}^2}{\|X\|_{L^2(A_9,\tau_9)}^2}
=54-86p-94ap+58a-13\sqrt2+21\sqrt2p+21\sqrt2a-34\sqrt2ap
=0.7295098177439909\ldots,
\]

where \(a=\sqrt p\). The two states also disagree on the owned spatial
current:

\[
\omega_X(1,N_1,N_2,N_3)=(1,2ap,0,0),\qquad
\omega_e(1,N_1,N_2,N_3)
=\frac{\tau_9(e(1,N_1,N_2,N_3)e)}{p^6}=(1,0,0,0).
\]

Thus this fixed CAR blank, record, right column, and path identification do
not produce the canonical Jones conditional state. This is a scoped
state-binding obstruction for this preparation; it does not exclude a
different already-owned preparation or prove a whole-core no-go. No selector
or postulate is added to force the match.

The exact replay checks the canonical \(E_2\) corners, record/cut
intertwiners, actual old-right-\(M_2\) matrix units through the \(A_5\)
GNS frame, the prepared blank, and its source-active current. It also checks
the same-simple level-three CAR extension in the native \(A_9\) blocks. The
level-two center obstruction remains exact for its fixed \(K_2\) encoding;
the level-three multiplicity encoding bypasses that specific obstruction.
It also checks the level-three GNS comparison above, including the PF-weighted
norm, canonical conditional corner, off-corner mass, and all three current
readouts. These results still do not supply physical admission of the
preparation/operation or a joint \((q,D,b,m)\) variation.

## Scope and next route

These calculations close the one-copy obstruction, the level-one price-rank
gate, the finite level-two weld and its fixed-encoding center obstruction,
and an actual level-three native AF current corner whose operator tuple has
an all-level Jones image. They also rule out binding this fixed prepared
blank to the canonical Jones conditional vector under the owned \(A_9\) path
identification. Still open are any different already-owned state binding,
physical admission, the joint field variation, and the source/Ward/curved-
solution steps.
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
