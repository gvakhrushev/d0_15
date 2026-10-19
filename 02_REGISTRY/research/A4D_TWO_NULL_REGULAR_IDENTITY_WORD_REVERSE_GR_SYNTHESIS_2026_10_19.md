# D0 → GR: two-null regular identity word and an order-memory geometric completion

**Date:** 2026-10-19  
**Owner:** existing scientific integrator #334, \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`  
**Class:** RESEARCH / exact finite Lorentz-algebra and operational coordinate theorem; no physical GR promotion  
**Consumer:** original full 16-coframe + 24 independent-Lorentz-link Euler programme, same-history Golden/Book physical compiler, nonlinear refinement and null/Ward Einstein closure.  
**Reproduction:** \`sources/d0_two_null_regular_atlas_2026-10-19/check_regular_two_null_atlas.py\`.  
**Status:** \`GR_closed=false\`, \`native_12_step_admission=false\`, \`same_history_Cost_Info_binding=false\`, \`joint_root_refinement=false\`.

## 0. Strategic result — a nontrivial flat *operational* history can be the REGULAR geometric origin

Existing #334 already establishes the six-generator proper-Lorentz algebra of four opposite-null directions, a positive full16 Julia order-sensitive tester, and full exact original 40 Euler on arbitrary sourced Brinkmann data. This memo does NOT re-own those results. It gives a different and stronger **two-primitive finite atlas theorem**:

1. ONE original crossed null pair \`A=N2\`, \`B=barN3\` generates all six proper-Lorentz directions by brackets of depth <=4.
2. A fixed 12-step **nonzero, exactly closed** word \`W(t0)=I\` has a **full-rank six-parameter endpoint derivative**. This avoids the singular two-direction tangent at the empty word.
3. Therefore every sufficiently short original proper-Lorentz parallel transport of an arbitrary bounded smooth spin connection can be compiled *locally analytically* into exactly this fixed word by changing six controls only by \`O(h)\`; there is no fractional-power parameter singularity and no new Lorentz primitive.
4. A 22-step fourth-order nested commutator and a commuting reordering have exactly the SAME signed primitive counts, but different actual Lorentz holonomies. A count-only/commutative history quotient cannot, BY ITSELF, determine the original full ordered geometric holonomy. This is a **physical admissibility filter** on a proposed Book observation algebra, not a new Book selector.

The one missing physical programme remains: admit and price this ordered history on the **real original full carrier** with fresh flags, oldRIGHT/reference, matter, preparation, controller and clock, and show its field first covector has the actual required same-action geometric+physical structure. No geometry-only algebra proves that admission.

## 1. Exact original η-Lorentz Lie algebra, with only TWO primitive controls

In the fixed original null basis \`(+,-,2,3)\`, define

\`\`\`
eta = [[0,1,0,0], [1,0,0,0], [0,0,-1,0], [0,0,0,-1]],
A = E_{-,2} + E_{2,+} = N2,
B = E_{+,3} + E_{3,-} = barN3.
\`\`\`

Both are in \`so(eta)\`, with \`A^3=B^3=0\` and original exact nilpotent exponential \`exp(tA)=I+tA+(t²/2)A²\`, analogously for B. Let

\`\`\`
C=[A,B]                 = E23 - E32,
D=[A,C]                 = E_{-,3}+E_{3,+},
E=[B,C]                 = -(E_{+,2}+E_{2,-}),
F=[A,E]=[B,D]          = E_{++}-E_{--}.
\`\`\`

These SIX real matrices are independent and close the six-dimensional full \`so(1,3)\`. Their Lie-word filtration has exact dimensions

\`\`\`
depth <=1 : 2 (A,B)
depth <=2 : 3 (add C)
depth <=3 : 5 (add D,E)
depth <=4 : 6 (add F).
\`\`\`

This is the growth vector **(2,3,5,6)** of this chosen bracket-generating Lorentz control. It does *not* assert G2 symmetry, 4 spacetime directions from bracket length, nor that the four material generator families owned by #334 are superfluous to its already selected native instrument. It proves sufficiency of the narrower pair as a geometric CONTROL alphabet.

## 2. Explicit regular 12-operation identity word

For \`X=(A,B,A,B,A,B)\` let

\`\`\`
G(t) = exp(t1 A) exp(t2 B) exp(t3 A)
       exp(t4 B) exp(t5 A) exp(t6 B),
t0 = (1,1,1,1,2,1)/40.
W(t) = G(t) G(t0)^(-1).
\`\`\`

The last six inverse gates are fixed (reverse order, negative base amplitudes), so \`W\` uses exactly twelve original null-flow gates, not a new matrix type.

At the nonzero baseline \`t=t0\`,

\`\`\`
W(t0)=I_4,   W(t0)^T eta W(t0)=eta.
\`\`\`

At each primitive, \`|t_i| <= 1/20 < 1/10\`, which is **inside** the pre-existing small-\`||X||<=1/10\` Julia-contraction *mathematical* chart in #334 (the null matrix spectral norm is 1). Thus the algebraic witness does not demand an arbitrarily strong primitive gate. It does NOT establish the fresh-register/readout/control cost or literal G0 fullStep implementation.

Writing \`P_{j-1}=\prod_{i<j}\exp(t_{0,i}X_i)\`, the left-trivialized differential is

\`\`\`
[dW(t0)(delta t)] = Σ_j delta t_j Ad(P_{j-1}) X_j.
\`\`\`

Flatten the genuine 4×4 real matrices into 16 rows in row-major order. With 0-index row extraction

\`\`\`
(0,2,3,6,7,11),
\`\`\`

the exact six-by-six derivative minor is

\`\`\`
det J_minor = 1/26214400000000 != 0.
\`\`\`

Therefore \`rank dW(t0)=6\`. Since \`SO^+(1,3)\` is six-dimensional and W is analytic, the standard inverse-function theorem supplies a true analytic coordinate chart around \`W(t0)=I\` with six independent original null controls. This is an EXACT finite algebraic rank theorem plus a standard analytic consequence, not a numerical root.

**Reverse geometric construction.** For a compact local coframe chart carrying any bounded smooth Lorentz connection \`omega_mu(x)\`, its original short edge parallel transports satisfy \`U_{x,mu}(h)=I+h omega_mu(x)+O(h²)\`. On sufficiently fine meshes all links belong to the same W-chart and admit analytic controls

\`\`\`
t_{x,mu}(h)=t0+O(h)
W(t_{x,mu}(h))=U_{x,mu}(h).
\`\`\`

The implied constants depend on the fixed regular baseword and a bound on the smooth connection, not on mesh index h. This is a **representation** result for prescribed smooth Lorentz links; it does not construct true exact D0 stationary roots over arbitrary metrics.

## 3. Full ORIGINAL 24-link Euler tangent access — not a restricted ansatz

Treat the six controls \`t_{x,mu}\` as independent per original proper Lorentz edge. The link map \`W\` is a local analytic diffeomorphism onto its six-dimensional Lorentz-neighborhood. For the **unchanged original six-plaquette star action** \`S_star(q,U)\`, merely change variables \`U=W(t)\`:

\`\`\`
D_t (S_star(q,W(t))) = [D_t W(t)]^T D_U S_star(q,U).
\`\`\`

The Jacobian is invertible in the Lie tangent directions near \`t0\`; consequently

\`\`\`
D_t S_star(q,W(t))=0  iff  D_U S_star(q,U)=0
\`\`\`

for all six original independent proper-link Euler directions **per edge**, with all sixteen original coframe variations unchanged. Thus the original 40 equations are preserved under this reparametrization; this is NOT gauge fixing, restricted ansatz stationarity or a new geometric action. The correct link cotangent packing/left-trivialization is inherited from the original owner.

The equivalence is for the pulled-back \`S_star\`. The **actual physically priced sequence** of 12 Julia/Golden operations may add derivatives with respect to t from full code cost, controller, fresh flags, reference, preparation, clock, and work. Their actual complete source MUST be evaluated; declaring them absent would replace the native action.

## 4. Exact order-memory obstruction: signed counts cannot encode the geometry

Define the exact group commutator word in primitive signed gates by \`[x,y]=xyx^-1y^-1\`:

\`\`\`
C_word=[a,b]                     length 4,  leading ab C,
E_word=[b,[a,b]]                 length 10, leading ab² E,
F_word=[a,[b,[a,b]]]             length 22, leading a²b² F.
\`\`\`

All these words use only the ORIGINAL finite \`exp(±aA)\`, \`exp(±bB)\`. The 22-gate F_word contains precisely five \`a\`, five \`a^-1\`, six \`b\`, six \`b^-1\`. The reordered word

\`\`\`
a^5 (a^-1)^5 b^6 (b^-1)^6
\`\`\`

has *exactly the same signed count vector*, and its actual Lorentz holonomy equals I identically. Yet the true original ordered F_word has

\`\`\`
W_F(a,b) = I + a²b² F + O((|a|+|b|)^5)
\`\`\`

with F nonzero. Exact nilpotent matrix multiplication at \`a=b=1/40\` verifies \`W_F != I\` and \`W_F^T eta W_F=eta\`.

Consequently there exists NO mapping from signed primitive counts alone to the complete original Lorentz holonomy on these histories. This conclusion is independent of how the Einstein tensor is defined and of any tuned coupling.

**Precise physical scope:** if a purported native *sole geometric readout* identifies all histories with equal counts, it cannot reproduce the original ordered Lorentz geometry, even when it knows signed counts. A Book programme that retains independent Lorentz links or an additional ordered witness may still distinguish the two; this no-go does not prove the mandatory original physical Cost−Info picks a particular history algebra. The genuinely positive six-Lorentz Julia/POVM response and native order tests already owned by #334 provide such a candidate ordered witness, but its compulsory admission and supply remain open.

The depth-four appearance of the final boost F is **structurally aligned** with #334's genuinely nontrivial \`[a²b²]\` quartic Cartan work. These are different maps (Lie control-word filtration versus geometric Euler jet), and they must not be identified without a typed operator-to-field map.

## 4.1. Compose with the ALREADY-owned six-direction positive Julia information readout

The existing #334 \`A4D_OPPOSITE_NULL_LIE_COMPLETE_JULIA_ORDER_MEMORY_BOOK_SOURCE_2026_10_19.md\` owns one fixed complete CAR16 × fresh-reference Julia/POVM instrument with genuine positive outcomes and **all failures retained**. On its registered six original Lorentz coordinates \`xi\` it proves

\`\`\`
D_xi (D1,...,D6)|_(xi=0) = (24 sqrt(2))^-1 I6.
\`\`\`

In the current narrower basis \`(A,B,C,D,E,F)\`, the six Lie-coordinate transformation differs from the original owner's \`(N2,N3,barN2,barN3,J,B_original)\` by only a signed permutation. Moreover the extraction of row-major matrix rows \`(0,2,3,6,7,11)\` from OUR six Lie basis has determinant +1 (verified independently), so the regular identity-word endpoint determinant in Lie coordinates is exactly the same \`1/26214400000000\` as the flattened minor.

Therefore the mathematical composite \`t -> W(t) -> (single FINAL U Julia tester)\` has at t0 the genuine nonzero full six-source Jacobian

\`\`\`
|det D_t (D1,...,D6)| =
     1 / [ 26214400000000 * (24 sqrt(2))^6 ] > 0.
\`\`\`

This is a full-rank **positive-measurement statistical distinguishability** statement for the final ordered holonomy, with no fitted detector coefficients and no new POVM. The existing #334 owner already proves the actual nonnegative POVM effects and six-direction coefficient; this memo adds the chain-rule composition with the regular two-primitive identity atlas. It does **not** equate a FINAL-U Julia operation to the native execution or cost of all twelve internal primitive gates. That exact process map, flags, oldRIGHT-preservation and resource accounting are the remaining physical question.

## 5. Whole-GR reverse assembly and one decisive physical gate

A valid end-to-end route would now read:

1. **Existing geometric owner:** arbitrary smooth Lorentz solder/connection, original independent full40 six-plaquette Euler, exact smooth EH probe law from merged #377.
2. **New algebraic completion:** above W gives one fixed, nonsingular, finite-depth two-null operational representation of EVERY sufficiently short smooth Lorentz edge, with ALL six independent geometric link variations accessible. This removes an algebraic control-span concern without assuming a LC connection is the physical root.
3. **Existing physical order witness:** full CAR16 + actual old record, positive Julia+Golden complete flags can distinguish ordered Lorentz actions. A count-only full-history mean/MAP is not a complete geometry readout; #384 independently sees dramatic MDL change under time-position forgetting.
4. **One real remaining same-programme bridge:** install the ordered W history on the literal admitted original fresh-wire/G0/FULL-Book carrier, preserve all oldRIGHT/reference and failure complements, and derive the actual Cost−Info + clock + work + preparation + coherent/fine KL **FIRST source**. Determine whether its six control covectors factor through the original geometric \`D_U S_star\` and independently derived matter source, or yield a nonzero residual. Do not select the answer by matching Einstein.
5. **Einstein closure after physical bridge:** use original full field/link roots, #377 limit, nine null + genuine full Ward (or actual admissible universal null orbit law) and uniform recovery/realization erasure to recover \`G+Lambda g=kappa T\`. No numerical Lambda, native T or original RAW-216 terminal is claimed by this memo.

**Decisive now:** a SINGLE full retained 12-gate closed-baseline history vs the geometric identity, and the six independent \`t_i\` source jets at that same actual physical cut. Include the entire complete failure/complement and code costs. Does its native priced covector, on preparation/clock stationary roots, descend to the original SIX geometric edge Euler directions with one source convention? If yes, the last geometric generator/operational-history weld has a constructive owner. If not, the measured difference is a scoped record-source obstruction, not a reason to search new Lorentz generators.

Do NOT call a nontrivial baseline identity word a Y vacuum: it has no asserted exact full Euler stationarity. Do NOT put its individual gate amplitude \`O(1)\` into the old near-identity physical link log bound: the resulting physical edge transfer W is still I+O(h), and the old fixed-source escape remains unchanged.

## Validation and provenance

The proposed checker repeats all six exact \`so(eta)\` invariance identities, Lie growth ranks (2,3,5,6), 12-gate identity, full-rank Jacobian with pinned rational minor, 22-gate Lie-order control, and a same-signed-count / nontrivial-holonomy negative control using genuine finite null exponentials. Matching local SymPy script executed and passed all assertions before this check was committed. New repo script CI result is not claimed here.

\`GR_closed=false\`; no new task, Book/claims/CORE edits, physical action, new operator alphabet, or source coefficient.
