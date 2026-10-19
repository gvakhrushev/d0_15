# D0→GR breakthrough boundary: canonical invariant 3+1 **history quotient**, but NO canonical 4D vertex carrier or Lorentzian Book metric

Date: 2026-10-19. **EXACT ORIGINAL SCENE THEOREM + 718-edge replay / research on existing Draft #384 / NOT a 4D Einstein proof, no Book/CORE promotion.** Current parent #334 has already proved the complete 685-dimensional Book history-Fisher/archive equivalence, the 718=359+32+327 cochain decomposition, and pretrace ordered Lorentz/Cartan face extraction. This note does **not** repeat them. It proves a new physically decisive **automorphism-naturalness test** on the very same original carrier and isolates the exact 4D role/addressing obstruction. The user requires a genuine physical bridge, not another scalar action tuned to reproduce GR. \`GR_closed=false\`.

## 1. The original graph has a rigid *full automorphism group*, and the vertex representation cannot contain 4D

The ORIGINAL primitive finite scene is the complete tripartite graph
\[
\mathcal G=K(9,11,13),\quad |V|=33,\quad |E_{\rm und}|=359,\quad |E_{\rm dir}|=718.
\]
Since the part sizes are distinct, every graph automorphism preserves each part and permutes its vertices arbitrarily:
\[
G=\operatorname{Aut}(\mathcal G)=S_9\times S_{11}\times S_{13}.
\]
The natural REAL vertex space used in Book03's \(\ell^2(V)\) geometric spectral-triple reading decomposes as
\[
\boxed{\mathbb R^{33}\cong{\bf1}^{\oplus3}
\oplus {\rm Std}_9^{(8)}
\oplus {\rm Std}_{11}^{(10)}
\oplus {\rm Std}_{13}^{(12)}.}\tag{1}
\]
Each standard zero-sum representation is irreducible over \(\mathbb R\) under its own symmetric-group factor; the three are inequivalent under the product group. All three trivials come from indicators of the original three unequal-size zones.

**Exact finite no-go:** There is NO 4-dimensional \(G\)-invariant linear subspace of \(\mathbb R^{33}\). An invariant subrepresentation is a sum of invariant trivial directions of dimension at most 3 and zero or more whole irreducible standard blocks of dimensions 8,10,12. Nor is there a \(G\)-equivariant surjective linear map \(\mathbb R^{33}\to\mathbb R^4\) where the target is the internally unlabelled/trivial 4D role carrier: any such map factors through the 3-dimensional space of zone-constant means. The same statement holds for an invariant orthogonal rank-four projector.

This is a NO-GO for a **graph-only, full-permutation-natural 4D vertex tetrad** and nothing stronger. It does NOT forbid a 4D continuum role constructed with additional original typed clock/observer, nontrivial action of \(G\) on the target, a nonlocal/refined archive, or a quotient of a more capable physical carrier. A smooth 4D manifold is not asserted to be a 4D subspace of \(\ell^2(V)\) merely because Book03 calls the scene a spectral triple.

## 2. Positive exact 3+1: only after moving from vertices to original EDGE COSTS and quotienting endpoint gauge

The 718 directed edges have precisely SIX orbits under the very same original automorphism group:
\[
A\to B,\ B\to A\ (99\ {\rm each}),\qquad
A\to C,\ C\to A\ (117\ {\rm each}),\qquad
B\to C,\ C\to B\ (143\ {\rm each}).
\]
A full-\(G\)-invariant **scalar directed primitive Book Cost−Info cochain** therefore has six parameters. Split under reversal \(d_{uv}\leftrightarrow d_{vu}\) into three symmetric pair costs \(e_{AB},e_{AC},e_{BC}\) and three antisymmetric zone-pair costs \(a_{AB},a_{AC},a_{BC}\).

The original endpoint-price coboundaries \(\xi_u-\xi_v\) are \(G\)-invariant iff \(\xi\) is constant on each original zone, modulo the common constant. Thus their image is EXACTLY 2-dimensional. Finite characteristic-zero group averaging commutes with passage to a quotient, so the **canonical symmetry-preserving cohomological Cost space** is
\[
\boxed{
[(\mathbb R^{E_{\rm dir}})/d(\mathbb R^V)]^{G}
\cong
\underbrace{\mathbb R^3}_{\text{three reciprocal pair costs}}
\oplus
\underbrace{\mathbb R}_{\text{one oriented ABC circulation}}.
}\tag{2}
\]
An explicit odd generator \(c\) is \(+1\) on \(A\to B,B\to C,C\to A\) and \(-1\) on their reversals; its gauge-invariant cycle integral around EVERY original ABC triangle is \(+3\) in this normalization.

**This is one precise intrinsic 3+1 four-dimensional invariant derived from the ORIGINAL graph.** It is a quotient of scalar EDGE HISTORIES, **NOT** four spacetime coordinates, not a Minkowski metric, not a Lorentz coframe, and not a consequence of picking four exceptional vertices. In particular the odd mode is parity/reversal sensitive, but its positive *stochastic* baseline is time-reversal invariant: the native original Perron process is reversible and has zero mean chiral cycle Cost-current.

## 3. Strong no-go: the induced scalar Book information Hessian on this '3+1' is NOT a Lorentz metric

Consume the exact already-owned native Book *all-walk* scalar action:
\[
\mathcal A_{\rm eff}(s)=-\log_\varphi\rho(\varphi^{-s}),
\quad
D^2\mathcal A_{\rm eff}[d,d]
=-\ln\varphi\sum_{uv}\pi_uP_{uv}
(d_{uv}-c-\xi_u+\xi_v)^2\le0,
\]
where \(c=\sum\pi P d\) and \((I-P)\xi=\sum_vP_{uv}d_{uv}-c\).
At equal native primitive Costs \(s\equiv1\), \(\pi P\) is the original reversible Perron law.

Restricted to all SIX invariant directed primitive Cost values, the Hessian has **EXACT rank 3**, with EXACT 3-dimensional kernel:
- one common shift of all original directed primitive edge Costs (actual absolute tick/pressure source, but no history-relaxation curvature);
- the two independent zone-potential endpoint differences.
No other kernel exists: the original finite Poisson identity says Hessian vanishes iff \(d=c+d\xi\), and those are the ONLY invariant constant-plus-coboundary directions.

After quotienting the 2 endpoint coboundaries, the native 4D history sector still has one zero history-Hessian direction. In the explicit original unnormalised cost basis \(e_{AB},e_{AC},e_{BC},c\), independent all718 evaluation yields
\[
H^{(4)}_{\rm Book}\approx
\begin{pmatrix}
-.12972842546& .0578326839& .0718957415&0\\
 .0578326839&-.1416813887& .0838487052&0\\
 .0718957415& .0838487052&-.1557444728&0\\
0&0&0&-.47637445155
\end{pmatrix},
\]
\[
\boxed{\operatorname{inertia}H^{(4)}_{\rm Book}=(n_+,n_-,n_0)=(0,3,1).}\tag{3}
\]
The first three entries sum by rows to 0 (absolute common-clock Cost shift); even/odd off-diagonals are zero by original detailed balance/reversal symmetry. Exact rank/inertia follows from the Poisson iff-kernel, not floating-point small eigenvalues.

**Therefore the most natural 4D graph-invariant edge Cost−Info/Fisher Hessian is DEGNERATE NEGATIVE SEMIDEFINITE, not the nondegenerate Lorentz metric with inertia (1,3,0) or (3,1,0).** No change of four coordinates by invertible real congruence can repair the missing nonzero time eigenvalue (Sylvester inertia theorem). Calling the one odd graph cycle 'physical time' does NOT produce Lorentzian geometry; a real native clock, noncommutative proper-Lorentz/coframe representation, and paid physical measurement remain essential.

## 4. Closed-form exact chiral history action and second source on the original 718 graph

Do NOT use a numerical rank as the chiral evidence. Deform ONLY the existing primitive original directed Cost values:
\[
s_{uv}(t)=
1+\begin{cases}
+t,&u\to v\text{ runs around }A\to B\to C\to A,\\
-t,&u\to v\text{ goes against that order}.
\end{cases}
\]
This is a finite **test of the existing Cost fiber**, not a proof that such reversal-odd costs are physically admitted by full 4D D0. Let \(q=\varphi^{-t}\). The original 33×33 weighted adjacency restricts on zone-constant vectors to the literal original three-zone quotient
\[
M(q)=
\begin{pmatrix}
0&11q&13/q\\
9/q&0&13q\\
9q&11/q&0
\end{pmatrix},
\]
whose characteristic polynomial is **EXACTLY**
\[
\boxed{
\det(xI-M(q))=x^3-359x-1287(q^3+q^{-3}).}\tag{4}
\]
With \(q=\exp(-t\ln\varphi)\), the 33-vertex Perron root \(\rho(t)\) satisfies
\[
\boxed{\rho(t)^3-359\rho(t)-2574\cosh(3t\ln\varphi)=0.}\tag{5}
\]
This is an all-\(t\) exact algebraic identity, not a Taylor estimate. It forces:
\[
\mathcal A_{\rm eff}'(0)=0,\qquad
\boxed{
\mathcal A_{\rm eff}''(0)=
-\frac{23166\,\ln\varphi}
{\rho_0(3\rho_0^2-359)}
=-0.4763744515526456\ldots<0,}\tag{6}
\]
where \(\rho_0^3-359\rho_0-2574=0\), \(\rho_0>0\).
The zero first chiral source is the exact original time-reversal symmetry; the strictly negative second source is an original observable history susceptibility. It is NOT an independent signed Lorentz/Einstein kinetic term.

## 5. Physically compulsory 4D provenance test now has a short finite yes/no answer

The original full vertex scene ALONE cannot force a four-dimensional invariant linear role carrier; its exact primitive 3+1 edge-gauge quotient has wrong metric signature. Therefore any claimed *derived* proper-Lorentz coframe/GR from the scalar original scene and full automorphism-naturalness **without additional original history/observer structure** is excluded. This is a scoped and mathematically complete statement, not a no-go for the rich D0 architecture.

The original D0 **does** already contain potentially relevant non-scalar ingredients:
- Book03's ORDERED noncommutative path-memory algebra before trace;
- original 718 edge archive with its 685-dimensional history-Fisher tangent and 327 independent ordered graph cycles;
- original finite 4-Role A4D coframe/CAR/Hodge/Palatini 16+24+2 operator and pretrace exact six-face Cartan extraction in #334;
- a two-fresh-flag Golden CAR16 complete mathematical Julia readout with native flat amplitude p, but no proven actual 4D Role→scene executable controller or compulsory complete physical Book Cost−Info + work/clock/preparation price.

The **one** missing physical theorem can now be stated narrowly:
\[
\boxed{
\text{Which ORIGINAL typed, symmetry-covariant and actually executable}
\ \mathcal R:\operatorname{BookPathMemory}_{\rm archive}
\longrightarrow(\text{4-Role coframe, six-face Lorentz, CAR and clock})
\text{ is selected, and does the SAME complete paid action have Einstein Euler?}
}
\]
It must retain both (i) the order-sensitive odd cycles and (ii) the original work/clock/preparation sources, rather than treating the intrinsic 3+1 scalar sector as spacetime. If the compiler must use only graph permutation-invariant scalar Cost channels, (1)–(6) refute the needed Lorentz response and the claim of a canonical 4D vertex projector. If a genuinely typed noncommutative role/observer structure breaks that restriction from ORIGINAL D0 axioms, the finite obstruction does not apply, but actual action-source equality remains to be proved.

This is an ORIGINAL-GR PROVENANCE NO-GO and a constructive native 3+1 invariant history quotient, **not** full gravity closure. No additional spectrum census, geometry jet, fitted coupling, Book promotion, or speculative spontaneous symmetry-breaking selector is proposed. \`GR_closed=false\`.

**Reproduction**: [exact zone cubic + all718 Poisson/Fisher code](sources/d0_physical_binary_return_2026-10-19/check_native_scene_invariant_3plus1_no_lorentz.py), independently run locally and passed. The representation-theory proof is elementary and given here; the checker verifies explicit original orbit, graph, quotient, pressure and Hessian identities.


## 6. Explicit rank obstruction against the already-built six-Lorentz physical detector

The distinction above can be tested against an EXISTING real D0 observable, not against a wished-for Einstein metric. The current #334 \`A4D_SINGLE_RUN_PERRON_BOOK_CAR16_FRESH_FLAG_SOURCE_WELD_2026_10_19.md\`, §7, owns a **complete positive** fixed CAR16 Julia/Choi detector, with native Golden coupling \(p\), all failure events retained, and local six-generator Jacobian
\[
D_\xi\mathcal D(0)=\frac{p^2}{6\sqrt2}\,I_6,\qquad\operatorname{rank}D_\xi\mathcal D(0)=6.
\]
This is a mathematically constructed native-*type* readout; actual 4D Role→scene gate/clock/price still lacks physical admission.

Now suppose a claimed graph-only, \(G\)-permutation-natural **gauge-invariant CLOSED-history** compiler from those six local Lorentz variables \(\xi\in\mathbb R^6\) passes **solely through the canonical four-dimensional scalar Cost quotient** in (2). Its six-output detector probabilities have the form \(\mathcal D(\xi)=F(q(\xi))\), with \(q:\mathbb R^6\to\mathbb R^4\). Elementary chain-rule rank gives
\[
\boxed{\operatorname{rank}D_\xi(F\circ q)(0)\le4<6.}\tag{7}
\]
Therefore it can NEVER equal the already-owned six-independent-source CAR positive detector **as a first-order physical observation**, no matter what nonlinear \(F\) and \(q\) are chosen. In particular, using only the chiral odd cycle would have rank ≤1. This is a strict **no-go for the graph-invariant scalar-closed-history-only interface**, not for the original Book noncommutative memory, whose 327 cycles can carry non-Abelian holonomy matrices and whose CAR16 source already has rank6. It also does not apply to a proposed readout which explicitly retains raw endpoint or non-invariant address data rather than passing through the gauge quotient.

Furthermore the already-owned original Perron/Doob source and target embeddings \(J_0,J_1\), and their feedback \(F_A=I-T^2\), all commute with the natural simultaneous relabeling by \(G\) at constant original primitive Cost: \(P,\pi\) are group-invariant. No word built **only** from the unlabelled scene adjacency, native scalar \(P,\pi,J_0,J_1\) and their spectral functions can silently produce an invariant rank-four orthogonal projector on the original *vertex* carrier. To obtain the measured six independent Lorentz source directions, the original CAR/Hodge/four-Role archive must be connected through a real symmetry-breaking or symmetry-covariant *typed map*, whose preparation and execution are paid and whose action-source is independently derived. A fitted scalar Book pressure or renaming of the 3+1 quotient cannot supply such a map.

This is the strongest diagnostic use of the new theorem: it **refutes a complete physical six-direction detector factorization**, not merely an interpretation of a negative Fisher matrix as Lorentzian geometry. Still no global Einstein Euler identification; \`GR_closed=false\`.
