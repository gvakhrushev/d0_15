# D0 → GR: two-/three-cycle history tomography and one absolute Book-return source

19 October 2026. **RESEARCH / EXACT FINITE STRUCTURE / CONDITIONAL PHYSICAL CONSUMER of PR #334. GR_closed=false.** Disjoint new lemma; no modification to BOOK/CORE/claims, original #216, task registry, actual native action or selectors.

**Existing inputs, not re-claimed:** [native scene Perron/Book](A4D_SCENE_PERRON_DOOB_SINGLE_HISTORY_GOLDEN_INFO_SOURCE_2026_10_19.md), [Info coboundary](A4D_BOOK_INFO_ENDPOINT_COHOMOLOGY_FULL_GRAVITY_QUOTIENT_2026_10_19.md), [#380 triangle 960 conditions](https://github.com/gvakhrushev/d0_15/pull/380), [#381 Slater binary source gate](https://github.com/gvakhrushev/d0_15/pull/381), [exact all40 arbitrary Brinkmann+CAR source](A4D_ARBITRARY_BRINKMANN_ALL40_CARTAN_DISCRETE_EINSTEIN_2026_10_19.md), [nine Golden null + Bianchi](A4D_TWO_SIDED_NULL_BIANCHI_GLOBAL_COMPLETION.md), [six Lorentz Julia order tests](A4D_OPPOSITE_NULL_LIE_COMPLETE_JULIA_ORDER_MEMORY_BOOK_SOURCE_2026_10_19.md). The Perron/Doob law is a mathematically specified positive transfer, NOT yet the obligatorily selected native D0 process.

## 1. Theorem — 359 two-returns + 327 triangle odds uniquely determine a stochastic history

The original complete tripartite scene K(9,11,13) has N=33 vertices, 359 undirected edges, 718 directed edges, 1287 A-B-C triangular faces. Its 2-dimensional triangle clique complex has the already-proved H1=0. The 359-edge cycle space has dimension 359-33+1=327, and triangle-boundary rank is 327. The map from edge antisymmetry to the 1287 triangle contrasts has 960=(9-1)(11-1)(13-1) independent compatibility conditions (as independently treated in #380).

Let P,Q be ANY strictly positive *row-stochastic* matrices on the allowed 718 directed edges and zero elsewhere. For each undirected edge define B_uv(P)=P_uv P_vu; for each A-B-C triangle define

\[
A_{abc}(P)=\log\frac{P_{ab}P_{bc}P_{ca}}{P_{ac}P_{cb}P_{ba}}.
\]

**EXACT UNIQUENESS.** If the 359 B and a spanning set of 327 triangle affinities A of P and Q agree, then P=Q.

**Proof.** Put t_uv=log(Q_uv/P_uv). Equal B implies t_uv=-t_vu. Equal A implies t_ab+t_bc+t_ca=0 on all generating triangles. Since H1=0, the real closed one-cochain is a gradient: t_uv=f_v-f_u. Hence Q_uv=P_uv exp(f_v-f_u). Both row sums equal 1, so P exp(f)=exp(f). An irreducible stochastic matrix admits only constant positive harmonic right vectors. Thus f is constant and Q=P. The same proof linearized proves immersion on its entire row-normal tangent. QED.

**Dimensional significance.** P has 718-33=685 free stochastic coordinates, but cycle observables number 359+327=686. The one nonlinear compatibility is EXACTLY Perron normalization: construct a positive edge matrix K0 from arbitrary positive B and 327 compatible triangle affinities (all 960 triple-contrast equations must vanish); it is unique modulo a 32-dimensional vertex-potential similarity. These 686 observables come from a stochastic P iff rho(K0)=1. Then P_uv=K0_uv r_v/r_u using its positive right Perron vector, and the cycle invariants are preserved. The one spectral condition removes one dimension. This does NOT infer a new physical degree of freedom.

## 2. Exact OFF-SHELL global scale identity: ONE absolute Book two-cycle fixes all closed-path scalar prices

For the ALREADY DEFINED optional positive 33-scene transfer, let

\[
K_{uv}(y)=\varphi^{-s_{uv}(y)},\quad
s_{uv}=C_{uv}-\theta I_u-(1-\theta)I_v,
\quad
P_{uv}=K_{uv}\frac{r_v}{\lambda r_u},
\]

where lambda(y)>0 and r(y)>0 are Perron eigen-data; ALL field and Info derivatives are retained. On EVERY original directed CLOSED path gamma of length n:

\[
\boxed{W_{\rm Book}(\gamma;y)=\prod_{\gamma}K_{uv}
=\lambda(y)^n\,P(\gamma;y).}
\tag{1}
\]

The endpoint r telescopes; an open path retains its endpoint ratio. Existing endpoint-Info coboundary cancellation makes the closed W independent of theta without freezing node Info. For ONE actual u->v->u return,

\[
\boxed{\lambda(y)^2=\frac{W_{\rm Book}(u,v,u;y)}{P_{uv}(y)P_{vu}(y)},}
\tag{2}
\]
\[
\boxed{D\log_\varphi\lambda[V]
=\tfrac12D\log_\varphi W_{\rm Book}(u,v,u)[V]
-\tfrac12D\log_\varphi(P_{uv}P_{vu})[V].}
\tag{3}
\]

Therefore the complete normalized positive Markov history plus ONE absolute unnormalized native-Book closed event price mathematically recover every scalar closed-loop absolute price and all its first jets. This is an exact reduction of the cost *interface*, NOT proof that the compulsory native Book process measures or prices this K or that the absolute W is inferable from normalized Born probabilities. In particular the true moving normalizer, old-address preparation, clock and work remain physical source terms. Lambda is Perron pressure, NOT automatically the cosmological Lambda, Newton's constant, the J2 coupling, or a physical selector.

## 3. Essential physical warning — positive scalar pressure cannot replace signed Lorentz Palatini

#380 already proves that the scalar Perron pressure Hessian is positive semidefinite on any affine real edge-price pullback, whereas the original full 24-dimensional proper-Lorentz Palatini Hessian has 12 positive and 12 negative eigenvalues. Hence even exact recovery of all 685 stochastic coordinates does NOT yield the full GR action. Scalar triangle orientation is not noncommuting Lorentz matrix order; distinct AB versus BA can share identical scalar Book weights.

Use instead the already constructed opposite-null CAR16 six-generator proper Lorentz tester with **TWO fresh retained Julia flags**, preserving every failure outcome and original RIGHT/ref128. Reusing a flag introduces the previously proved spurious 3/4 I contribution. The role of its Lorentz ordered response is separate from, and complementary to, the Markov price theorem. Likewise the current exact density-dressed coframe and new quartic orbit-area correction are separate indispensable geometric inputs, not consequences of scalar cycle odds.

### 3.1. Ordered matrix triangles reconstruct a general group connection up to gauge

Scalar return/triangle statistics do not contain the Lorentz matrix order. A
different and exact geometric statement is available if the *matrix-valued*
triangle holonomies are part of the readout. Let the three vertex classes be

\[
A_0,\ldots,A_8,\qquad B_0,\ldots,B_{10},\qquad C_0,\ldots,C_{12},
\]

and let every oriented edge carry \(U_{uv}\in\mathcal G\), with
\(U_{vu}=U_{uv}^{-1}\), for any group \(\mathcal G\) (in particular
\(SO(1,3)\)). Use the 32-edge spanning tree
\(A_0B_j, A_0C_k, A_iB_0\ (i>0)\) to choose tree gauge, so all those
transports are the identity. Write the consistently tree-transported,
ordered face matrix as
\[
H_{ijk}=U_{A_iB_j}U_{B_jC_k}U_{C_kA_i}.
\]

The following 327 face matrices recover every remaining edge, with products
kept in their stated noncommutative order:
\[
\begin{aligned}
U_{B_jC_k}&=H_{0jk} &&(11\cdot13=143),\\
U_{A_iC_k}&=H_{i0k}^{-1}H_{00k} &&(8\cdot13=104),\\
U_{A_iB_j}&=H_{ij0}U_{A_iC_0}U_{B_jC_0}^{-1} &&(8\cdot10=80).
\end{aligned}
\]
The remaining 960 faces obey the exact ordered identity
\[
H_{ijk}=H_{ij0}H_{i00}^{-1}H_{000}H_{0j0}^{-1}
         H_{0jk}H_{00k}^{-1}H_{i0k},\qquad i,j,k>0.
\]
These formulas follow by substituting the tree-gauge edge expressions into
the face products. Thus 327 appropriately based/transported triangle
matrices form a complete cycle-coordinate readout of all 359 edge links;
the only residual ambiguity is the chosen common root frame, i.e. gauge.
The exact free-group checker verifies all 359 edge reconstructions and all
960 omitted-face identities without assuming commutativity; the adjacent
SO(1,3) numerical checker supplies a noncommuting sample and hostile control.

This closes a *geometric reconstruction* question, not the physical source
question. Triangle conjugacy classes alone, scalar affinities, or matrices
left in unrelated local frames are insufficient. The native run must supply
these ordered matrix readouts, their tree-frame transport, and their complete
record/work/clock price on the same carrier before this reconstruction can
be used as a D0 field-to-link map. It therefore complements, but does not
replace, the two-fresh-flag source test above.

## 4. One decisive same-programme physics gate, not a new catalogue

A genuine positive D0→GR derivation should use ONE admitted complete retained programme and check the following typed composition, retaining all its physical price terms:

**Native events:** an addressable starting old scene label u, real two-step returns u->v->u and opposite fully labelled triangle histories, with ALL alternative outcomes retained. Verify that their **actual** conditional history probabilities coincide with the mathematically reconstructed P. If the geometric route uses the matrix reconstruction in §3.1, retain ordered triangle matrices transported into one tree frame; scalar affinities or unrelated local conjugacy classes do not suffice. An unconditioned stationary probability pi_u P_uv P_vu is NOT the same as the required conditional return probability. The Slater good/complement event from #381 is an additional distinct sample space; identify it by a genuine same-instrument map or do not equate them.

**One true absolute price:** obtain W_Book(u,v,u) and its complete field derivative from the same original Cost−Info; check equation (3), all normalizers, old preparation, clock, control and source/work. If physical Book is not this positive Perron transfer, record a scoped failure of the proposed scene-transfer bridge, not a general D0 or Einstein no-go.

**Physical tensor:** transfer the one fully recorded sample law and the six noncommuting Julia order contrasts through one native oldLEFT/oldRIGHT/ref128/CAR16/coframe/link preparation. Evaluate the genuine complete 16+24+2 physical source and ALL additional independent observer/preparation/clock Euler rows, comparing to the already owned finite star+CAR source, without inserting its Einstein ratio as a fitted cost.

**Nonlinear and global GR:** existing nine Golden null shears read the trace-free ten-tensor up to g; on-shell full retained Ward plus Bianchi makes its trace coefficient constant, and one independently recorded global scale response fixes its value. The exact 40→3→1 arbitrary Brinkmann sector and 840×1008 crossed quartic local jet supply strong geometric test families. Generic exact joint roots, source convergence, proper non-null quotient and original raw #216 remain OPEN.

This single compulsory physical return-price and ordered-source gate is the new consuming target of PR #334. It discharges no accepted GR obligation until the actual native programme is established.

## 5. Test and status

[Dependency-free numerical checker](sources/d0_two_three_cycle_tomography_2026-10-19/check_two_three_cycle_tomography.mjs): all 33 nodes, 359 undirected edges, 1287 triangles, Perron–Doob reconstruction after nontrivial diagonal similarity and global scaling, 960 triple contrast identities, single absolute return reconstruction and hostile controls. The theorem is algebraic, not inferred from that numerical fixture.

[Exact free-group checker](sources/d0_nonabelian_triangular_tomography_2026-10-19/check_free_group_reconstruction.py) verifies the noncommutative word identities for the 327-face connection reconstruction and all 960 complementary faces. [The finite \(SO(1,3)\) checker](sources/d0_nonabelian_triangular_tomography_2026-10-19/check_so13_triangle_reconstruction.mjs) checks a noncommuting curved sample, gauge recovery and an independently corrupted omitted face.

**New results:** exact 2-/3-cycle scalar history tomography and one absolute pressure scale; exact arbitrary-group reconstruction of all edge links from 327 ordered tree-transported triangle matrices, with 960 complementary identities. The free-group checker certifies the latter word equalities; the SO(1,3) numerical checker tests a noncommuting sample. **Reused:** 327/H1=0, triangle-image 960, Perron/Doob, 9-null/Bianchi, Julia Lorentz, all40 null/CAR and quartic response. **Not proved:** compulsory physical Markov or matrix-holonomy selection, Book/Born same-event equality and full normalizer, J2 equivalence, complete preparation/clock, generic exact uniform joint-root, raw #216 or GR_closed.
