# D0→GR breakthrough: an EXACT Spin(1,3) and native Q8 carrier INSIDE original CAR16, preserving true Fock parity — with a two-line Golden central-sign readout

20 October 2026. **NEW EXACT CONSTRUCTIVE ORIGINAL FOUR-MODE CAR16 → REAL Cl(1,3) → Spin^+(1,3) / Q8 REPRESENTATION / GOLDEN COHERENCE THEOREM, and a scoped nonunitary-boost physical-selection gate.** Integrated into existing #334. NO NEW physical state, graph, detector constant, Clifford primitive, Book action, field tensor, face choice or spin coefficient. **Research proof, not a theorem the complete G0 executes the controlled Q8 bit, spinorial gravity/matter action or Einstein.** No Book/CORE/claim promotion. \`GR_closed=false\`.

## 1. The earlier separation of CAR16 exterior from Spin is a REPRESENTATION choice, not a new-carrier necessity

Literal upstream formalized owners:
- \`03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean\`: original 4 physical Role modes, \(\mathcal F=\mathbb R^{16}\) basis \(\mathrm{Role}\to\mathrm{Bool}\).
- \`03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean\`: original integer-shadow Jordan–Wigner \(c_r,c_r^\dagger\) with the full anticommutators \(\{c_r,c_s^\dagger\}=\delta_{rs}I,\ \{c_r,c_s\}=0=\{c_r^\dagger,c_s^\dagger\}\).
- \`03_FORMALIZATION/D0/Geometry/ArchiveCARDirac.lean\`: \`fockGamma r=carAnnihilate r+carCreate r\`, real symmetric native Majorana, parity operator \((-1)^N\) and its exact anticommutation with each odd Clifford generator.
- \`03_FORMALIZATION/D0/Foundation/Omega8Center.lean\` and Book01 §01.7.1B–C: native \(Q_8=\{\pm1,\pm i,\pm j,\pm k\}\), actual order-memory center \([i,j]=-1\), spinor double-cover sheet.
- \`GoldenCoherentMemory.lean\`: full original 4×4 orthogonal \`fullStep(a,p)\`, \(a^2=p,\ p+p^2=1,\ p=\varphi^{-1}\).
- Original #334 \`A4D_Q8_SPIN_SHEET_327_TRIANGLE_INVERSE_AND_960_COHERENCE_GATES_2026_10_20.md\`: whole native scene all327 central sheets via existing 1287 triangle syndromes and 960 consistency checks. The older exterior representation \(\Lambda^\bullet U\) FACTORS through SO and is blind to \(Q_8\) central -1.

That last mathematical **SO/exterior-blindness is correct**, but it does not imply that the SAME underlying 16-dimensional Fock carrier cannot admit ANOTHER representation which *does* see the Spin sign. In fact the already-defined actual creation/annihilation operators give such a representation constructively.

Choose an already existent FOUR-ROLE time section (A timelike, B/C/D spacelike); no claim the compulsory D0 temporal Role interwiner or observer choice selects A. Let
\[
c_0=c_A,\quad c_1=c_B,\quad c_2=c_C,\quad c_3=c_D
\]
and, solely by reusing the original CAR operators, define on THE SAME real \(\mathcal F_{16}\)
\[
\boxed{
\Gamma^0=c_0+c_0^\dagger,\qquad
\Gamma^j=c_j^\dagger-c_j\quad(j=1,2,3).
}\tag{1}
\]
All these are operators on the EXISTING sixteen states, with integer entries \(\{0,\pm1\}\); no new spinor Hilbert carrier and no new coefficient or fundamental gamma postulate is involved. The full original CAR identities imply EXACTLY
\[
\boxed{
\Gamma^a\Gamma^b+\Gamma^b\Gamma^a=2\eta^{ab}I_{16},
\qquad \eta=\mathrm{diag}(1,-1,-1,-1).
}\tag{2}
\]
Moreover \((\Gamma^0)^T=\Gamma^0\), \((\Gamma^j)^T=-\Gamma^j\) (so the time and spatial signatures have the correct REAL involution).

Crucial correction to a misleading shortcut: making spatial \(\Gamma^j=\Gamma^0(c_j+c_j^\dagger)\) would ALSO algebraically give \((+---)\) but would make those spatial generators **even** and the associated boosts **odd**, violating original fermion-parity superselection. Definition (1) does NOT: ALL four \(\Gamma^a\) are odd under the original CAR parity \(\Pi=(-1)^N\):
\[
\boxed{\Pi\Gamma^a=-\Gamma^a\Pi.}\tag{3}
\]

## 2. Six exact faithful native Spin–Lorentz bivectors, no new infinitesimal axes

Using ONLY products of the original \(\Gamma\), set
\[
\boxed{\Sigma_{ab}=\tfrac14[\Gamma^a,\Gamma^b]
=\tfrac12\Gamma^a\Gamma^b\quad(a<b,\ a,b=0,\ldots,3).}\tag{4}
\]
Then the complete Lorentz-vector infinitesimal action is the EXACT CAR-matrix identity
\[
\boxed{
[\Sigma_{ab},\Gamma^c]
=\eta^{bc}\Gamma^a-\eta^{ac}\Gamma^b.
}\tag{5}
\]
The resulting six generators close the genuine \(\mathfrak{spin}(1,3)\cong\mathfrak{so}(1,3)\) Lie bracket. Every \(\Sigma_{ab}\) is even and COMMUTES with true native CAR parity \(\Pi\). Native even and odd Fock sectors are 8+8 states, each invariant for every proper Spin boost/rotation. Thus this is a parity-preserving finite Spin representation on original CAR16; it is NOT a re-labelling of the non-spinorial \(\Lambda^\bullet SO\) representation.

Exact finite Lorentz group controls: with \(B=\Gamma^0\Gamma^1\), \(B^2=+I\), the noncompact boost
\[
S_{01}(t)=\exp[\tfrac t2 B]
=\cosh(t/2)I+\sinh(t/2)B
\]
acts on \((\Gamma^0,\Gamma^1)\) by the ordinary proper vector boost
\(\Gamma^0\mapsto\cosh(t)\Gamma^0-\sinh(t)\Gamma^1,\quad
\Gamma^1\mapsto\cosh(t)\Gamma^1-\sinh(t)\Gamma^0\).
For \(R=\Gamma^1\Gamma^2,\ R^2=-I\), the spatial spin rotation
\(S_{12}(\theta)=\cos(\theta/2)I+\sin(\theta/2)R\)
acts on \((\Gamma^1,\Gamma^2)\) by a proper rotation. EVERY intermediate operator stays on \(\mathcal F_{16}\). The vector/SO action is recovered by **CONJUGATION of these gamma matrices** rather than by identifying the spin matrix itself with a 4×4 SO matrix.

## 3. Completely exact faithful embedded ORIGINAL Q8, including the central Book order-memory

The ORIGINAL Q8's three quaternion axes are realized by EXISTING native spatial CAR Clifford products
\[
\boxed{
\widehat i=\Gamma^2\Gamma^3,\quad
\widehat j=\Gamma^3\Gamma^1,\quad
\widehat k=\Gamma^1\Gamma^2=\widehat i\widehat j.
}\tag{6}
\]
The verified EXACT identities are
\[
\widehat i^2=\widehat j^2=\widehat k^2=-I_{16},\quad
\widehat i\widehat j=\widehat k=-\widehat j\widehat i,\quad
[\widehat i,\widehat j]_{\rm group}=-I_{16},
\]
with all eight distinct matrices \(\pm I,\pm\widehat i,\pm\widehat j,\pm\widehat k\). Hence the existing BOOK01 \(\Omega_8\cong Q_8\) admits an **EXACT FAITHFUL, parity-preserving** group representation on the existing CAR16 Fock state space:
\[
\boxed{\rho_{\rm CARSpin}(z=-1)=-I_{16}.}\tag{7}
\]
This is NOT the Fock parity operator \(\Pi\) (which has 8 positive and 8 negative eigenvalues). The central spin sheet \(-I_{16}\) is a scalar on BOTH parity sectors. A spatial **2π** vector rotation has Spin representative \(-I_{16}\); **4π** has \(+I_{16}\), matching the original Book01 Q8 corollary exactly.

Therefore the earlier exact group-algebra kernel \(\mathfrak e_-=(1-[z])/2\), which is NONZERO in \(\mathbb Q(\varphi)[Q_8]\) but is annihilated by the vector/exterior CAR16 action, satisfies
\[
\boxed{
\rho_{\rm exterior}(\mathfrak e_-)=0,\qquad
\rho_{\rm CARSpin}(\mathfrak e_-)=I_{16}.
}\tag{8}
\]
This is the KEY POSITIVE RECOVERY: **the ORIGINAL same CAR16 carrier has sufficient algebra to represent the previously SO-invisible native Q8 central memory, without adding any physical spin state or spin generator.** The all327 original ABC triangle parity inverse and 960 octahedral conditions can now feed a GENUINE finite Spin-sensitive CAR16 representation. The actual original G0 Book→scene-edge typed coupling remains to be proved, and no identity equating this \(\operatorname{Spin}\) connection to the physically selected matter action is asserted.

## 4. Original Golden fullStep gives a complete TWO-LINE discriminating INTERFEROMETER if controlled Q8 sign actuation is admitted

The original native finite coherent memory has (literal compiled Lean basis \(|00\rangle,|01\rangle,|10\rangle,|11\rangle\))
\[
U_{\rm Golden}=\begin{pmatrix}
a&0&-p&0\\0&a&0&-p\\0&p&0&a\\p&0&a&0
\end{pmatrix},
\quad a^2=p,\ p+p^2=1.
\]
It sends the actual blank \(|00\rangle\) to \(a|00\rangle+p|11\rangle\), with the entire joint record retained. Suppose one can apply an actual **CONTROLLED** already-represented native Q8 center \(z=\pm I_{16}\) to ONLY the \(|11\rangle\) retained history branch, while acting as identity on \(|00\rangle\), and then apply the REVERSE already-owned \(U_{\rm Golden}^T\). The full two-line return-port probability is
\[
\boxed{\Pr(00\mid z)=(p+z\,p^2)^2.}\tag{9}
\]
For \(z=+1\), \(\Pr(00)=1\), alternative-port probability0. For \(z=-1\),
\[
\boxed{
\Pr(00)= (p-p^2)^2=(\sqrt5-2)^2,\quad
\Pr(10)=1-(p-p^2)^2=4p^3\approx0.94427191.}\tag{10}
\]
No failure event or port is postselected: the exact final probabilities sum to one. This is a single-primitive-Golden-constant, complete coherent operational TARGET showing the original Q8 central sheet IS NOT merely a global phase **when it is retained relative to a distinct reference history**. If the center is applied uniformly to every branch, it IS a global phase and normalized probabilities cannot see it; a relative branch is mathematically necessary.

**Absolute typing firewall:** the actual existing \`GoldenCoherentMemory.fullStep(a,p): Fin4→Fin4\` does NOT yet contain this controlled \(Q_8\) actuation or actual scene/oldRIGHT/ref128 spinor reference. The explicit matrix \(\operatorname{diag}(1,1,1,z)\) above is a CONDITIONAL controlled coupling to an ALREADY OWNED Q8 sign, not an already compiled compulsory Golden primitive. Its cost/Kraft/clock/readout and ability to act on a coherent original Book path branch MUST be derived/paid from literal G0/Book/M1. The math shows exactly which missing actuation is needed and that no *extra measurement constant* or new carrier is required.

## 5. One final PHYSICAL obstruction that can no longer be hidden: Lorentz boosts are NOT fixed-positive-norm Golden unitaries

Our constructed native real Lorentz generators have
\[
(\Sigma_{ij})^T=-\Sigma_{ij}\text{ (spatial rotations),}\qquad
(\Sigma_{0i})^T=+\Sigma_{0i}\text{ (boosts).}
\]
Consequently real CAR16 spin boost \(S_{0i}(t)\) is parity-even with \(\det S=1\) but is not orthogonal in the ordinary positive native Fock inner product for \(t\ne0\):
\[
\boxed{S_{0i}(t)^TS_{0i}(t)\ne I_{16},\qquad
\mathrm{singular\ values}=e^{\pm t/2}.}\tag{11}
\]
Each of the two singular values occurs with multiplicity8 for this real 16-dimensional Clifford representation. The literal native Golden \`fullStep\` IS orthogonal and all trace-preserving physical closed circuits act isometrically on a suitable total Hilbert space. Therefore the full NONCOMPACT Spin(1,3) action cannot be naively inserted as a single unconditional positive-norm 16×16 closed Golden gate on this carrier. One requires the **ACTUAL** selected observer-dependent positive form/pseudo-unitarity, or a complete dilation/heralded nonunitary operation with all success/fail and its native price, or an equivalently owned full dynamical encoding. No invented Bernoulli success probability or fitted normalization can replace this derivation. On the compact spatial \(Q_8\) subgroup the matrices are orthogonal, so the exact central-sheet target §4 has no such noncompact boost-norm problem (but still needs controlled program selection).

This strengthens the precise physical next step: the existing \`Omega8Center\`, \`ArchiveCARRelations\`, \`GoldenCoherentMemory\` and 1287 native ABC sign syndromes now produce **all the algebraic ingredients of the true Spin-sensitive matter archive** on the SAME native16 states. The ONLY new bridge needed for the spin-specific layer is an ACTUALLY admitted, paid, parity-preserving scene/Book Q8 memory→native CAR16 controlled operation (on true oldRIGHT/reference and Golden site), with physical noncompact boost normalization and full original spinor kinetic/stress Ward. This does NOT derive the complete H+J+R gravitational source or refining Einstein–Dirac solutions; those remain independently OPEN.

## 6. Exact independently reproduced original finite certificate

\`sources/d0_native_spin_q8_car16_2026-10-20/check_original_car16_clifford_spin_golden.py\` constructs the genuine all16 Jordan–Wigner \(c,c^\dagger\) integer matrices in original ABCD role order, checks all four-mode CAR and **all sixteen exact Cl(1,3) anticommutators**, six exact Lorentz conjugation commutators, true CAR parity commutation, exact faithful quaternion Q8 central commutator, all eight distinct sheet operators, finite proper Spin boost/rotation and 2π/4π, genuine literal \`fullStep\` 4×4 and the conditional sign-sensitive COMPLETE Golden positive probabilities, and the nonunitary CAR boost gate. Machine checks of source algebra are exact integer; only exponential group sanity checks use floating arithmetic. No physical G0 programme or new Lean compiler is claimed by this certificate.

\`GR_closed=false\`.
