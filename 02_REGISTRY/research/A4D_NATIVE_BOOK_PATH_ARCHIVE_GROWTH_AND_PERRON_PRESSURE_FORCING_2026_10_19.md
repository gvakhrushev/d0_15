# D0 → GR: exact original path-memory capacity, canonical finite-depth archive, and forced native Perron-pressure boundary

2026-10-19. **EXACT FINITE ORIGINAL SCENE COMPOSITION / POSITIVE CONSTRUCTIVE ARCHIVE + SCOPED FULL-PATH REPRESENTATION NO-GO.** Research consumer in #384 of original #334 and BOOK03 §§03.1.1, 03.1.3, 03.3.0. Does NOT introduce a new action, gravitational term, link, physical detector, or a compulsory Book-selected positive state. Original formal proof owners: \`03_FORMALIZATION/D0/VNext2/ScenePathHistoryCanonicity.lean\` and \`03_FORMALIZATION/D0/Geometry/ArchivePathWordAlgebra.lean\`. These explicitly own the free category of ALL scene walks and note that its unrestricted path type is NOT finite when a cycle exists. Original Perron/Cost owners: [native history action boundary](A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md), [same original 718-edge Book pressure](A4D_ONE_HISTORY_SCENE_ABSOLUTE_PRESSURE_FEEDBACK_COMPLETENESS_2026_10_19.md), and [true archived future feedback](A4D_ARCHIVE_FUTURE_CAUSAL_SELF_ENERGY_AND_DETECTOR_TIME_2026_10_19.md). Precise scope: literal free path algebra versus selected finite-depth/memory quotient; this does not refute existing finitely truncated action stacks or existing finite Q8 quotient. \`GR_closed=false\`.

## 1. Two genuine ORIGINAL 3-edge cycles generate exponentially large linearly independent full histories

Original scene is complete tripartite \(\mathcal G=K(9,11,13)\) with V=33 and 718 directed edges, as proved already. Choose root \(a_0\) in the 9-zone, and two original disjoint interior triangles
\[
A=(a_0,b_0,c_0,a_0),\qquad B=(a_0,b_1,c_1,a_0)
\]
with \(b_0\ne b_1\) original 11-zone vertices and \(c_0\ne c_1\) original 13-zone vertices. Each is an actual \`IsSceneWalk\` and both compose at \(a_0\).

For every \(m\ge0\), the 2^m loop words \(\mathcal W_m=\{A,B\}^m\) are all distinct ORIGINAL 3m-edge, same-start-and-finish walks; each is a separate canonical basis vector in the literal free linear path algebra \(k[\mathcal G]\), for \(k=\mathbb Q(\varphi)\) or \(\mathbb R\). Therefore
\[
\boxed{\dim_k\operatorname{span}\mathcal W_m=2^m.}\tag{1}
\]

This is a theorem about **LINEAR SUMS of original histories**. An injective map on individual word labels is much weaker: e.g. free semigroups can inject into low-dimensional matrix semigroups, but their arbitrarily many formal LINEAR COMBINATIONS cannot all remain linearly independent in bounded-dimension End(H). BOOK03 §03.1.3 itself distinguishes faithfulness on group elements from faithfulness on their group algebra and explicitly warns against conflating them.

## 2. Exact universal archive-space capacity bound and first certified nonfaithful depths

For any **algebra-linear** representation \(\pi:k[\mathcal G]\to\mathrm{End}_k(H)\) on \(\dim_k H=d\), faithfulness on \(\operatorname{span}\mathcal W_m\) requires
\[
\boxed{d^2\ge 2^m,\quad d\ge\lceil\sqrt{2^m}\rceil.}\tag{2}
\]
If \(2^m>d^2\), some NONZERO formal algebraic sum of actual distinct 3m-step histories must map to zero under \(\pi\). No choice of 33-vertex, 718-edge or 16-CAR matrices can avoid that linear-algebra conclusion when those are their **only** fixed finite internal Hilbert carrier, regardless of representation parameter or field dependence:

| fixed Hilbert dimension d | first 3m-step lower-bound failure | histories > matrix coordinates |
|---|---|---|
| original Lorentz 4 | depth 15, m=5 | 32 > 16 |
| original CAR16 | depth 27, m=9 | 512 > 256 |
| scene-vertex 33 | depth 33, m=11 | 2048 > 1089 |
| complete original edge 718 | depth 57, m=19 | 524288 > 515524 |

This **does not** say these matrices fail to detect the six physically relevant Lorentz directions, nor that original BOOK03 requires full algebra faithfulness on each fixed physical cutoff. It says that one may not identify a single fixed-dimensional \(\ell^2(V)\), CAR16 or 718-edge matrix algebra with the **entire literal unbounded linear free path algebra** while insisting that every history sum is faithfully preserved. The BOOK03 path-*algebra description must be read with a declared finite-depth bound, finite memory quotient, or an increasing archive tower, as its actual Lean owner already anticipates. A terminal Q8 or endpoint quotient may be finite and perfectly sound for its declared tests; it cannot be silently promoted to universal all-history faithfulness.

An independent easier all-depth obstruction follows from Cayley–Hamilton: powers of ONE nontrivial length-three loop \(A^0,\ldots,A^d\) are independent literal words but the (d+1) matrices \(\pi(A)^j\) are linearly dependent in End(d) by the characteristic polynomial. Thus NO finite d is faithful on the unrestricted full path algebra at all depths.

## 3. POSITIVE canonical bounded-depth repair — a finite ordered archive with no arbitrary coefficient

For every declared finite **loop depth** \(m\), take the actual word carrier
\[
\mathscr H_{\le m}=\operatorname{span}\{\,|w\rangle:w\in\{A,B\}^{\le m}\,\},
\qquad\dim\mathscr H_{\le m}=2^{m+1}-1.
\]
Let \(|\emptyset\rangle\) be the original empty rooted history. Define TWO original path-appending letters by finite left creation
\[
L_X|w\rangle=
\begin{cases}
|Xw\rangle,&|w|<m,\\
0,&|w|=m,
\end{cases}\qquad X=A,B.
\]
At this declared cutoff, each formal path polynomial \(f=\sum_{|w|\le m}c_w w\) is recovered coefficient by coefficient from the **single vacuum column**
\[
\boxed{\Big(\sum_w c_wL_w\Big)|\emptyset\rangle
=\sum_w c_w|w\rangle.}\tag{3}
\]
Thus the finite truncated *concatenation* algebra on these two original rooted loop letters admits an EXACT faithful linear representation through depth m. No extra arbitrary basis word or new physical field is needed, and order-sensitive response is structurally available; creation is killed only by the *declared finite cutoff*. This construction is an **ordered HISTORY ARCHIVE / algebraic prefix encoder**, **NOT** a proof of a complete \(*\)-representation of BOOK03's reversal involution, nor the physical G0 right-reference/controller/clock actuation. Adjoint reversal and refinement compatibility are still separate owners; one must not claim that the compressed truncated letters represent the unrestricted \(*\)-relations.

This establishes a constructive existence side to the fixed-carrier no-go: the exact missing resource is **depth-sensitive archive dimension**, not a new coefficient. Book06's existing retained/archive split is the natural typed carrier; its physically compulsory projection, clock/Cost payment and geometric response map remain to be shown.

## 4. The OTHER side of the same structural problem: original equal-Cost unbounded Book path weights have forced Perron pressure

At the ORIGINAL native canonical primitive scene cost \(C_{uv}=1\) for every actual directed edge, \(\mathrm{Info}=0\), the raw scalar Book weight of an n-edge history is exactly \(\varphi^{-n}=p^n\). Every original vertex has at least 20 outgoing original edges, hence there are at least \(33\cdot20^n\) distinct n-edge complete walks when all original start vertices are included. Therefore their positive raw weight satisfies
\[
\boxed{Z^{\rm raw}_n=\sum_{\mathrm{all\ n-edge\ walks}}\varphi^{-n}
\ge33(20p)^n,\qquad20p>1.}\tag{4}
\]
Consequently the all-depth raw positive scalar sum \(\sum_{n\ge0}Z^{\rm raw}_n\) diverges. There is no field-independent normalized Born law on the unrestricted all-depth family obtained merely by writing \(w=p^{\mathrm{Cost}}\) without an actual depth cut, pressure normalizer or different physically derived code. At finite N, every such sum is finite, so this is **not** a no-go for BOOK03's explicitly FINITE refinement k.

The ORIGINAL three-zone adjacency quotient on (9,11,13) has
\[
M=\begin{pmatrix}0&11&13\\9&0&13\\9&11&0\end{pmatrix},\qquad
\det(xI-M)=x^3-359x-2574.
\]
Its positive Perron root is \(\rho\simeq21.8373824011252\), so the original raw cost-one weighted transfer \(pA\) has spectral radius \(p\rho\simeq13.4962445492241>1\). Thus the correct unnormalized **bulk scalar log pressure** is forced by original adjacency growth: \(\log_\varphi(p\rho)\), not zero and not an adjustable Einstein coupling. The existing Doob/Perron owners obtain the native normalized transition
\(P_{uv}=A_{uv}r_v/(\rho r_u)\) on actual original edges and retain the absolute pressure \(\log_\varphi(p\rho)\) up to genuine endpoint coboundaries, if their original complete Cost−Info action is the input.

**Two different obligations are exposed, not repaired by one arbitrary normalization:** (i) a depth-dependent ARCHIVE to faithfully carry the linear ordered history sums, and (ii) a physically derived **pressure/depth selection** to compare positive weights across histories of different depths. The Perron scalar pressure is a necessary native bulk statistic for this equal-cost path ensemble, but by the exactly proven original ordered Wilson-trace counterexample (companion PR #384), scalar pressure cannot replace the noncommutative history algebra and cannot by itself give Einstein–CAR.

## 5. The shortest valid GR bridge theorem target after these exact results

A possible rigorous physical completion must specify **one original same-run programme** with:
1. The actual full finite \(\Gamma_N\) and its archive/refinement maps, distinguishing full formal histories only as far as original retained response tests demand. No implicit claim that \(\dim H_N=33\) suffices for faithful unbounded path *-algebra.
2. A physical \(*\)-compatible memory representation \(\mathcal R_N\) (or precise quotient with proven source-kernel invariance) of BOOK03's ordered classes on the original coframe/Lorentz/CAR apparatus, including old RIGHT, preparation, counter, controller work, all failures and native clock. Full abstract faithfulness is **not** necessary if the kernel is proven invisible to every field/source test and the memory quotient is refinement-consistent.
3. The actual same-history original Cost−Info scalar weight/normalizer and the Book03 **algebra-valued** selected aggregation, with endpoints and pressure charged exactly once. Trace-preserving full Born partition is 1 and cannot itself generate GR; Perron pressure is genuine only on its original typed history carrier.
4. A same-action first source (and regularized joint Hessian) equal to original 16 coframe+24 independent Lorentz+CAR source, with owned geometric response and the raw #216/selector/curved class gates explicitly satisfied.

Only this typed programme can make the existing positive geometry and archive results into one D0→GR proof. No more spectrum/rank enumeration or fitted entropy is needed. **Negative terminal:** full unrestricted linear path memory cannot live faithfully on a fixed 33/718/16/4-dimensional Hilbert module. **Positive terminal:** a finite-depth ordered archive exists and pressure is a native original graph invariant. **Physical theorem still OPEN: compulsory apparatus/selector and the joint Einstein–CAR response.** \`GR_closed=false\`.

Exact computational certificate: \`sources/d0_physical_binary_return_2026-10-19/check_full_history_archive_capacity.py\`. It verifies all word counts, path capacities, finite prefix-archive vacuum recovery and the original Perron cubic/numerical growth. The general algebraic inequalities are supplied in this memo; the script is a bounded control, not a Lean proof.
