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


## 7. Even stronger native result: Spin-INVARIANT observer pairing and an automatically FUTURE-CAUSAL CAR16 current

The non-orthogonality of a Lorentz boost in the positive Euclidean Fock norm (§5) has a precise **intrinsic** resolution at the level of the already-owned CAR16 *indefinite observer form*, without any new metric or mass scale. The SAME time generator \(\mathscr A=\Gamma^0\) is real symmetric with \(\mathscr A^2=I\) and exactly 8 positive plus 8 negative eigenvalues. From (3)–(5), for every original Spin Lie generator \(\Sigma_{ab}\) one has
\[
\boxed{\Sigma_{ab}^{T}\mathscr A+\mathscr A\Sigma_{ab}=0.}\tag{12}
\]
Therefore every connected Spin group element \(S\) constructed by exponentials of these **native six** generators preserves the original observer bilinear form:
\[
\boxed{S^T\Gamma^0S=\Gamma^0.}\tag{13}
\]
This is not ordinary real orthogonality \(S^TS=I\); boosts are indefinite-orthogonal. It matches the already-owned *moving observer-positive form* concern in \`MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION.md\`, but does NOT by itself construct its true finite located common-center action.

For any **real** original CAR16 spin state \(\psi\in\mathbb R^{16}\) define, using NO new primitive observable,
\[
\boxed{
J^a(\psi)=\psi^T\Gamma^0\Gamma^a\psi,\qquad
J^0=\psi^T\psi\ge0.
}\tag{14}
\]
Set \(\alpha_j=\Gamma^0\Gamma^j\). From the original CAR exactly
\[
\alpha_j^T=\alpha_j,\quad
\alpha_j^2=I,\quad
\alpha_i\alpha_j+\alpha_j\alpha_i=0\ (i\ne j).
\tag{15}
\]
For any spatial Euclidean unit vector \(n\), the real symmetric matrix \(A_n=\sum_jn_j\alpha_j\) has \(A_n^2=I\), so its spectral norm is EXACTLY one and
\(|\psi^T A_n\psi|\le\psi^T\psi\). Maximizing the left over \(\|n\|=1\) gives the **global exact future-causal quadratic current bound**
\[
\boxed{
(J^0)^2-(J^1)^2-(J^2)^2-(J^3)^2\ge0,\quad
J^0\ge0,
\quad |\boldsymbol J|\le J^0.
}\tag{16}
\]
No continuum approximation, freely chosen light-speed cap, detector threshold, Born assumption or fitted bilinear constant enters this elementary native CAR proof. Under a full connected native Spin transformation \(\psi\mapsto S\psi\), the current transforms as the vector of the associated proper Lorentz transformation (possibly with conventional active/passive sign for boost orientation). For \(S_{01}(t)=\exp(t\Gamma^0\Gamma^1/2)\) as in §2,
\[
\boxed{
\begin{pmatrix}J'^0\\J'^1\end{pmatrix}
=\begin{pmatrix}\cosh t&\sinh t\\\sinh t&\cosh t\end{pmatrix}
\begin{pmatrix}J^0\\J^1\end{pmatrix},\quad
J'^2=J^2,\ J'^3=J^3.
}\tag{17}
\]
Algebraically the lift both preserves the indefinite Spin bilinear (13) and carries an observer-dependent **positive** density \(J^0=\|\psi\|^2\) satisfying the causal bound (16). Thus the noncompact boost is not an *algebraic positivity impossibility*: it requires the ACTUAL native preparation/detector to change the observer/positive norm correctly, rather than declaring a nonorthogonal \(S\) to be an unconditional fixed-norm Golden unitary. The true paid G0 total completely positive instrument, oldRIGHT/reference, matter kinetic action, real 4D coframe and divergence/conservation Ward have still NOT been constructed.

Finally, the native \(-I_{16}\) central Q8 acts as \(\psi\mapsto-\psi\), so this bilinear current \(J^a\) by itself is BLIND to central -1, just as any unconditioned bilinear measurement is. The **conditional two-line Golden coherent INTERFERENCE** in §4 is therefore genuinely necessary to distinguish relative central memory on this carrier. This pinpoints which physical observables detect matter transport versus matter spin-sheet memory; neither may be silently substituted for the other.

New independent native certificate controls use 100 random existing Fock16 state vectors as examples but all structural identities and the causality bound are proved by the finite CAR algebra itself. \`GR_closed=false\`.


## 8. NEW exact endogenous LORENTZ HODGE and complex structure on THE SAME REAL16 CAR state space

The physical GR response already owns six proper-Lorentz bivector curvature components, the original Hodge dual and a sign-sensitive Cartan/Palatini star contraction. To join them to Spin-sensitive original CAR matter without importing an imaginary generator, define from the ALREADY constructed four genuine native CAR \(\Gamma^a\) the ORIENTED Clifford VOLUME operator
\[
\boxed{\Omega_{\rm CAR}:=\Gamma^0\Gamma^1\Gamma^2\Gamma^3\in\operatorname{End}_{\mathbb R}(\mathcal F_{16}).}\tag{18}
\]
The verified **EXACT INTEGER** native Clifford identities give
\[
\boxed{
\Omega_{\rm CAR}^2=-I_{16},\quad
\Omega_{\rm CAR}^T=-\Omega_{\rm CAR},\quad
\Omega_{\rm CAR}\Gamma^a=-\Gamma^a\Omega_{\rm CAR},\quad
[\Omega_{\rm CAR},\Sigma_{ab}]=0,\quad
[\Omega_{\rm CAR},\Pi]=0.
}\tag{19}
\]
Thus \(\Omega_{\rm CAR}\) is a canonical **real orthogonal complex structure** generated internally by the native four Role CAR matrices; it is invariant under the connected Spin(1,3) representation and preserves Fock parity. It is NOT an external complex amplitude/field and not the same as \(Q_8\)'s central \(-I\). In each actual invariant Fock parity sector \(\mathbb R^8\), it defines a complex vector space of dimension four. No chiral projection or new physical Weyl fermion content is declared by that simple counting statement.

The same real operator implements the true 4D Lorentzian Hodge pairing on all six native spin bivectors \(B_{ab}=\Gamma^a\Gamma^b\):
\[
\boxed{
\begin{aligned}
\Omega_{\rm CAR}B_{01}&=B_{23},&
\Omega_{\rm CAR}B_{23}&=-B_{01},\\
\Omega_{\rm CAR}B_{02}&=B_{31},&
\Omega_{\rm CAR}B_{31}&=-B_{02},\\
\Omega_{\rm CAR}B_{03}&=B_{12},&
\Omega_{\rm CAR}B_{12}&=-B_{03}.
\end{aligned}}\tag{20}
\]
This is EXACTLY the algebraic Lorentzian six-bivector duality with \(*^2=-1\); signs follow the native ordered Role orientation \(A,B,C,D\). In particular it supplies the same correct compact-rotation/noncompact-boost dual pairs whose signed projection was already owned by the original all40 six-plaquette Palatini star. It is not a theorem that the compulsory Book/G0 action contracts its geometric faces with this CAR Hodge — that **intertwiner/physical source** must still be proved — but the needed Lorentz algebra/complex/dual structures now have one explicit SAME-CARRIER realization, not three independently nominated reference operators.

All finite identities (18)–(20) were checked using literal original 16-state Jordan–Wigner **integer** CAR matrices, not floating fit or geometrical assumptions. This closes the *algebraic* CAR16→Q8→Spin(1,3)→\(\mathfrak{so}(1,3)\) six-bivector Hodge compatibility layer, while leaving actual physical native Book action and causal matter stress/refinement open. \`GR_closed=false\`.


## 9. GLOBAL new all-Role source gate: local original scene Spin sheets do not select the 16 flat \(T^4\) spin boundary sectors

The original Role-Phase product carrier is EXACTLY \(\mathrm{Role}\to\operatorname{Fin}(n+2)\), with four cyclic directions (\`ArchiveRolePhaseProductCarrier.lean\`). For \(L=n+2\ge2\), this finite regulator has a genuine periodic four-dimensional CW-lattice \(T_L^4\) underlying its difference/Role links. This is NOT the 33-vertex K(9,11,13) graph; the original scene is an **internal** Cost and Book memory carrier coupled sitewise to Golden LEFT Role addresses.

For an identity \(SO^+(1,3)\) background on the 4-Role torus, a flat central \(\operatorname{Spin}\) lift can assign a sign \((-1)^{\varepsilon_r}\) across the seam of each of the four cyclic Role directions, \(\varepsilon\in\{0,1\}^4\). Every elementary spin plaquette has exactly +1 central holonomy, while the four noncontractible winding cycles have independent signs \((-1)^{\varepsilon_r}\). A local central vertex-gauge transformation cannot change these four winding holonomies. Conversely any flat ±1 link connection on the 4-torus is classified by its four windings. Thus the finite source topology already contains
\[
\boxed{H^1(T_L^4,\mathbb F_2)\cong(\mathbb F_2)^4,\quad
\#\{\text{global flat Spin sectors}\}=16.}\tag{21}
\]
This is NOT \(2^{327}\): that is the unfilled graph *edge-lift fiber before triangle constraints*. The original ABC triangle-filled scene instead has \(H^1(\mathrm{Clique}_2(K913),\mathbb F_2)=0\), already proved in the scene spin-sheet owner. These two results are **perfectly compatible** because the scene and the genuine 4D Role torus are different mathematical complexes. Recovering all local Q8 sheets on the SCENE does NOT by itself choose the GLOBAL four independent Spin boundary signs of the 4D Role geometry.

An independently reproduced exact original \(L=2\), \(2^4=16\) Role-site benchmark makes the difference physically operational. For each twist \(\varepsilon\), let \(T_r^\varepsilon\) be the signed unitary translation of lattice sites by one site along original Role r, multiplying by \((-1)^{\varepsilon_r}\) only across the cyclic seam. All four shifts commute, every elementary plaquette product is I, and \((T_r^\varepsilon)^L=(-1)^{\varepsilon_r}I\). On the ORIGINAL 16-state internal Fock spin carrier, the mathematically natural nonnegative twisted scalar-difference kinetic benchmark is
\[
\Delta_\varepsilon=\sum_{r=0}^3(2I-T_r^\varepsilon-(T_r^\varepsilon)^T)\otimes I_{16}.
\]
Its exact eigenvalues are
\[
\boxed{\lambda_\varepsilon(k)=4\sum_{r=0}^3
\sin^2\!\left(\frac{\pi(k_r+\varepsilon_r/2)}L\right),\quad
k\in\{0,\ldots,L-1\}^4.}\tag{22}
\]
All SO and all local Spin face flux observables are IDENTICAL for every \(\varepsilon\), but the **global spinor kinetic spectrum** is not. At original L=2, the fully periodic sector has ONE zero site mode, hence EXACTLY 16 zero modes including real CAR16 fiber; ANY \(\varepsilon\ne0\) has NO zero modes and gap \(2|\varepsilon|\) in this exact benchmark. The 16 possible winding sign vectors are distinct, proven directly by their \((T_r)^2\) native holonomies, with no floating eigenvalue-based identity inference.

**Scope:** this is a finite CONDITIONAL central-Spin boundary/kinetic theorem, not a selection of physical spin structures from M1 or oldRIGHT, and \(\Delta_\varepsilon\) is a declared spin-twisted nearest-neighbor kinetic benchmark — it is NOT automatically the real original \`hodgeCarDirac\`/matter stress action. Nonetheless any full physical Einstein–DIRAC claim on the periodic Golden LEFT regulator MUST specify or derive which global winding signs are allowed by the original retained observer/oldRIGHT/Book/G0 preparation and how the nonlocal choice is recorded/priced, or prove that all allowed signs yield the same desired physical observables and uniform refinement. The original 327 local Q8 history bits and 960 clique identities do not silently discharge this GLOBAL 4-bit test.

Companion exact 16-sector bounded source checker: \`sources/d0_native_spin_q8_car16_2026-10-20/check_original_role4_global_spin_twists.py\`. This augments rather than reopens original local scene Hodge. \`GR_closed=false\`.


## 10. Exact FINITE Spin→SO→six-Palatini TRACE INTERTWINER, not just Hodge pairs

New **independently certified original-carrier theorem** [\`A4D_NATIVE_CAR16_TRACE_CLOSED_NONLINEAR_SPIN_TO_PALATINI_ALL40_2026_10_20.md\`](A4D_NATIVE_CAR16_TRACE_CLOSED_NONLINEAR_SPIN_TO_PALATINI_ALL40_2026_10_20.md) closes the algebraic seam between this memo's already-constructed Spin action and the ORIGINAL finite six-face Palatini curvature source. Consume only native Fock16 four-CAR Clifford: \(\eta^{ab}=\mathrm{Tr}_{16}(\Gamma^a\Gamma^b)/16\), \(\varepsilon^{abcd}=-\mathrm{Tr}_{16}(\Omega\Gamma^a\Gamma^b\Gamma^c\Gamma^d)/16\) **for ALL 256 index quadruples**, and for any finite native Spin word \(S\), \(\Lambda(S)^a{}_b=\eta_{bc}\mathrm{Tr}_{16}(\Gamma^c S\Gamma^aS^{-1})/16\). Thus the original vector-face \(\mathscr F=(\Lambda-\Lambda^{-1})/2\), Lorentzian Hodge and epsilon-coframe Palatini kernel are ALL read from one native CAR16, with unchanged original 16+24 Role Euler jets whenever the full Spin links are genuine lifts. Checked on NONCOMMUTING exact rational boosts/rotations and six true commutator faces formed from FOUR SHARED Spin links, with non-diagonal invertible coframe; the full original Levi-Civita kernel and direct CAR trace give identical rational \(3325188579/200000000\). No new metric, complex field, orientation tensor or action coefficient was installed: the original Role order itself supplies orientation.

**Essential correction:** finite spin odd \((S-S^{-1})/2\) is NOT the finite vector SO odd used by Palatini. Native boost half-angle gives exact ratio 5/2 and compact spin rotation ratio 6/5; Q8 pure 180° spin rotation has nonzero spin odd but *zero* SO odd because its vector Lorentz representative is an involution. Consequently gravity must reconstruct \(\Lambda(S)\) by the actual CAR adjoint trace while **spinor memory retains S itself and its central sign**. This is now the precise same-representation positive resolution of earlier exterior CAR16 center blindness. The actual paid G0/Book Q8 Spin link selection, full H+J+R action, stress Ward and refinement remain OPEN. \`GR_closed=false\`.
