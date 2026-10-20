# Actual local source quotient, range inverse and canonical phase-source boundary

Input: `2cba34623e346eb75a7a9ae42a550e4a52178a54`.
Parent: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Status: completed finite construction and explicitly scoped phase obstruction,
pending CONTROL. **Native matter action, physical Ward, nonlinear GR,
soundness, recovery and global closure remain OPEN.**

This supplies the actual finite quotient described, but not proved by the
old `ArchiveStressEdgeReadout` capstone. It also identifies exactly which
range inverse it constructs. No source is installed into the native field
equations by fitting the desired gravitational response.

## 1. Literal owner binding and compiled quotient

`ArchiveLocalLaplacianVariation` already constructs the linear equivalence
between undirected edge conductances and symmetric, row-sum-zero matrices
supported on the nearest-neighbor **four-Role product** graph. Its forward
matrix uses the positive owned scale `c=L^2`, `L=n+2`. It is distinct from
the one-dimensional phase space of `ArchiveVariation`.

For an undirected edge `e={u,v}`, let

\[
 E_e=(e_u-e_v)(e_u-e_v)^T,\qquad B_cw=c\sum_e w_eE_e.              \tag{1}
\]

The owner's forward matrix is exactly (1): its off-diagonal entry is
`-c w_{uv}` on that edge and zero off the graph; the row-sum condition then
gives its diagonal. This also explains the literal inverse `-dL_uv/c`.

For every raw matrix T the exact counting pairing is

\[
 \langle T,E_e\rangle=T_{uu}+T_{vv}-T_{uv}-T_{vu}.                 \tag{2}
\]

For symmetric T the owned readout therefore equals

\[
 R_c(T)_e=c(T_{uu}+T_{vv}-2T_{uv})
           =c\langle T,E_e\rangle.                              \tag{3}
\]

The capsule compiles (2), symmetry and zero row sums of E, its genuine
membership in the **actual** four-Role local variation submodule, and (3).
It then proves the full owner-level equivalence, for every n:

\[
 \bigl[\forall D\in\mathrm{LocalLaplacianVariation}(n),
       \langle T,D\rangle=\langle U,D\rangle\bigr]
 \quad\Longleftrightarrow\quad R_c(T)=R_c(U)                     \tag{4}
\]

for symmetric T,U. This quantifies over the real variation submodule, not a
Boolean surrogate or a condition defining the requested conclusion.

Necessity tests E on every edge and uses `c!=0`. For sufficiency subtract
the sources. If all edge readouts vanish, on every edge
`T_uv=(T_uu+T_vv)/2`. The same replacement is harmless on the diagonal and
off the graph, where the variation is zero. The pairing with the diagonal
potential `(v_u+v_v)/2` vanishes by the variation's row sums and symmetry.
This argument is compiled generically, including the pairwise version (4).

## 2. Complete finite range and its quantitative bound

Let A be the **unsigned** vertex-edge incidence matrix, with two entries 1
per edge, and let B be (1) with `c=1`. The exact Gram identity is

\[
 K_c=B_c^*B_c=c^2(2I+A^TA),\qquad
 \|B_cw\|_{HS}^2=c^2(2\|w\|_2^2+\|Aw\|_2^2).                 \tag{5}
\]

This holds on every finite simple graph. For one edge the squared norm of
E is 4, while its unsigned incidence column has squared norm 2. For distinct
edges sharing one vertex both Gram entries are 1; for disjoint edges both
are zero. These exhaust the simple-graph cases and prove (5) in every size.
All norms here are the stated counting norms.

Consequently K is positive definite, independently of connectivity, with

\[
 \|K_c^{-1}\|_{2\to2}\le\frac1{2c^2},\qquad
 T_r=B_cK_c^{-1}r,\qquad R_c(T_r)=r,
 \quad\|T_r\|_{HS}\le\frac{\|r\|_2}{\sqrt2|c|}.                \tag{6}
\]

Indeed `w^T K_c w>=2c^2||w||^2` proves injectivity and the finite square
operator is surjective. The first bound follows by Cauchy--Schwarz. The
second uses `||T_r||^2=r^T K_c^{-1}r`. This gives a constructive, unique
source **inside the local matrix image**, for any supplied edge response r.
It is symmetric and conserved since every E is. There is no assertion of
uniqueness among all raw source matrices.

For V vertices and E edges, the symmetric raw-source readout kernel has
dimension `V(V+1)/2-E`; after imposing zero row sums it has dimension
`V(V-1)/2-E`. The local image has dimension E by its unique off-diagonal
coefficients and lies in the conserved subspace. Its Gram is invertible,
so the readout is onto from either domain, proving both rank-nullity counts.
The conserved subspace dimension follows by specifying the symmetric
off-diagonal entries and then fixing each diagonal by its row sum.

These kernels are genuine retained observable null directions. A finite
example below shows that they contain nonzero conserved sources. Nothing
here identifies them with physical gauge transformations.

## 3. Sharp complete four-Role spectrum

For `L>=3`, the literal product simple graph has `V=L^4`, `E=4V` and degree
8. Its unsigned incidence satisfies `AA^T=8I+Adj`. The nonzero spectra of
`A^TA` and `AA^T` coincide, by applying A or its transpose to eigenvectors.
Their zero multiplicities differ by `E-V`. Thus the full unscaled K spectrum
is

\[
 2\ \text{with an additional multiplicity }E-V,
 \qquad 10+2\sum_{a=1}^4\cos(2\pi k_a/L),\quad
 k\in(\mathbb Z/L\mathbb Z)^4.                                  \tag{7}
\]

For completeness, each product character `exp(2pi i k.x/L)` is an adjacency
eigenvector with eigenvalue `2 sum_a cos(2pi k_a/L)`. Distinct characters
are orthogonal: each one-dimensional sum of a nontrivial L-th root of unity
is zero by the finite geometric-series identity. The V product characters
therefore form a full basis; no modes are omitted in (7).

The minimum 2 is sharp because `E>V` forces an incidence kernel. The maximum
18 is attained by the constant vertex character. At the actual scale
`c=L^2`, the exact extremes are `2L^4` and `18L^4`, and the condition number
is 9. This statement applies in particular to every `L in 4N`.

At `L=2`, positive and negative neighbors coincide in the owner's **simple**
graph. It has degree 4 and E=2V, not degree 8 and E=4V. The corresponding
spectrum is extra copies of 2 and `6+sum_a (-1)^(k_a)`, giving extremes
`2L^4`, `10L^4` and condition number 5. Counting those duplicate neighbors
as separate native edges would give the wrong operator.

Equations (5)--(7) are all-size analytical proofs with exact independent
integer-matrix controls. The capsule formalizes the literal variation/readout
quotient (4); it does not claim a compiled Fourier or continuum range theorem.

## 4. Hostile source controls and the physical boundary

The exact checker constructs the full four-Role graph at L=2,3,4, verifies
(5) in integer sparse arithmetic, verifies the forward/recover entries and
all readout pairings, and compares the first four exact trace moments with
the complete symbol (7). The full L=4 matrices have V=256 and E=1024.
Lower-dimensional cases and the L=2 exception provide independent controls.

On the full four-Role L=2 graph it solves the rational local system for a
fixed supplied response. It also takes a nonedge `{u,v}`, forms E_uv and
subtracts its local source reconstruction. The remaining matrix is nonzero
(its nonedge entry is still -1), symmetric, conserved and annihilated by
all local edge tests. Thus source recovery does not remove the raw kernel.
The all-ones matrix is invisible, whereas the identity matrix has readout
`2c` on every edge. A nonsymmetric source requires both off-diagonal entries
in (2); using `-2T_uv` then gives a wrong answer.

The uniform inverse (6) is the inverse of the **source representation Gram**.
It is not the inverse of the coupled metric--connection--matter Euler
operator, does not eliminate its response-null directions, and supplies
neither a physical metric variation map nor a local matter action. Choosing
r to equal a desired Einstein tensor and reconstructing T_r would be source
fitting, not a derivation of matter. The required independent source and
joint Ward identity remain open.

## 5. Separate phase-source obstruction at the weaker variational gate

This section uses the original one-dimensional canonical phase action and
the actual `ArchiveStressCoupling` source `T=alpha C_L`, where alpha is its
supplied representation's anomaly sum. It does **not** transfer the four-Role
owner to the phase carrier.

For `L=n+2>=3`, the published all-size native seam calculation gives only
two nonzero rows of `D=C_(L+1)J-JC_L`:
`D_0=-e_0^T+e_(L-1)^T` and `D_L=-e_0^T+e_1^T`.
The actual owner gradient `G=-2J^T D` therefore has `G_00=4`,
`G_01=G_0,L-1=-2`, and every other row zero. Put
`E_0=(e_0-e_1)(e_0-e_1)^T`, `E_1=(e_1-e_2)(e_1-e_2)^T`. Both are
symmetric row-sum-zero variations with real nearest-neighbor edge support.
Direct substitution into (2) gives, at every L>=3,

\[
 \langle G,E_0\rangle=6,\quad\langle G,E_1\rangle=0,\qquad
 \langle C_L,E_0\rangle=\langle C_L,E_1\rangle=6.                  \tag{8}
\]

Thus no real alpha, and hence no anomaly-sum source of the actual owner,
solves even these two local variational equations: one forces alpha=1,
the other alpha=0. This excludes the weaker `VariationalSourcedEquation`
in this canonical class, not merely the already excluded full matrix
equation. The two-probe residual has the sharp unscaled bound

\[
 (6-6\alpha)^2+(6\alpha)^2
     =18+72(\alpha-1/2)^2\ge18.                                  \tag{9}
\]

This is not a normalized continuum obstruction: a new mesh normalization
must be included before inferring any such bound.

The exception is real. A general signed local phase source can match all
edge tests: its weights solve `K w=r`, with `r=6(delta_0+delta_(L-1))` and
`K=4I+Adj_cycle`, an instance of (5). The solution is unique and has a
negative weight. To see why nonnegative weights are impossible, the zero
response on edge 1 forces `4w_1+w_0+w_2=0`; nonnegativity then forces these
three weights to vanish and propagation through the other zero-response
edges contradicts the nonzero seam response. At L=3 it already forces all
weights zero. The exact finite controls retain these signed solutions.
Moreover, the existing frozen conserved-stress projection already supplies
a symmetric conserved representative for all phase row-sum-zero variations.
Neither construction turns the prescribed native matter source into that
representative, and neither is evidence that all weak source fibers are empty.

## 6. Verification and preserved obligations

Ten new generic/actual-owner propositions and the existing local variation
isomorphism compile with 35 transitive D0 source pins; all eleven axiom
reports use only `propext`, `Classical.choice`, `Quot.sound`. Three actual
types are printed. The source-readout theorem is a complete equivalence on
the declared local variation space. The spectral/range, dimension and
phase-source statements have the explicit all-size proofs above and exact
certificate controls; their physical extensions are not assumed.
All 59 grouped controls pass. Two deliberately falsified ledgers, changing
the sharp Riesz lower bound and the two-probe residual gap, are rejected.

```sh
cd 03_FORMALIZATION
lake env lean ../02_REGISTRY/research/certificates/a4d_native_edge_source.lean
cd ..
python3 02_REGISTRY/research/certificates/a4d_native_edge_source_check.py
```

Default replay compares a pinned immutable ledger. False ledgers replacing
the positive Riesz lower bound or the two-probe source gap by zero must fail.
No action, source law, physical gauge, selector, supported owner, claim or
parent terminal is changed. Original #310/#202/#317 obligations remain open.
