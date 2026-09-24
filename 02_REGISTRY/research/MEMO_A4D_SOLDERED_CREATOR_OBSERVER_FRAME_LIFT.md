# A4D soldered creator / observer frame lift

**Snapshot:** current `origin/main = 750ac39236aedd5a3b120f9251ab1bb10f8d637f`, fetched 2026-09-24. **Input:** complete canonical brief and complete `MEMO_A4D_LOCATED_METRIC_STAR_CELL_ACTION_SELECTOR.md`; PR #69/#70 treated as merged, frozen owners. **Output:** research construction and exact controls, no Lean/lifecycle or repository edits.

## 0. Terminal verdict

**FRAME-LIFT-CONSTRUCTED-STAGGERED-JET-MISSING.** The existing 16-state `ArchiveFockState` is exactly the exterior carrier. There is an explicit exterior action on it, an observer-dependent positive pairing, covariant moving creators and contractions, and a *conditional but literal* lift of the **linear part** of PR #70's affine Lorentz links. This gives a finite covariant differential whose flat limit is the owned `d` and whose observer adjoint gives the owned `D_H`. It does **not** provide an independently derived finite energy with first derivative the *entire* specified `H(e)`. The unowned step is a located, transported **cell energy and half-edge solder rule**, including the uncentered edge coefficient, endpoint average, scalar neighbor term and two paths to the corner. No nonlinear `Q(e)` is selected.

The statement `ρ(Λ)=⊕_{k=0}^4∧^kΛ` throughout is the exterior representation on the existing 16-state carrier. It is **not** a Spin/Dirac-spinor representation. The reference `n=e_A` fixes the gauge in which the observer positive form is counting; neither it nor `U_A` is proved to be physical time.

## 1. Exact exterior and CAR lift, with conventions

Order `Role=(A,B,C,D)` as in `ArchiveCARRelations.roleOrderIndex` and identify an occupation state `S` with the increasing wedge `e_S`. Given `g∈GL(V)`, set

\[
\rho(g)_{T,S}=\begin{cases}
\det[g_{t_i,s_j}]_{1\leq i,j\leq k},&|T|=|S|=k,\\
0,&|T|\ne|S|.
\end{cases}
\tag{1.1}
\]

The empty minor is one, the top minor `det g`. The Cauchy–Binet identity proves `ρ(g_1g_2)=ρ(g_1)ρ(g_2)`, `ρ(I)=I`, `ρ(g)^{-1}=ρ(g^{-1})` in all five degrees. On the **original** CAR matrices define `C^\dagger(v)=\sum_a v^a c_a^\dagger` and `C(\alpha)=\sum_a\alpha_a c_a`. Wedge and interior multiplication give

\[
\{C(\alpha),C^\dagger(v)\}=\alpha(v)I,\quad
\rho(g)C^\dagger(v)\rho(g)^{-1}=C^\dagger(gv),\quad
\rho(g)C(\alpha)\rho(g)^{-1}=C(g^{-T}\alpha).
\tag{1.2}
\]

The contraction is algebraically dual. At fixed counting, its transpose happens to equal the adjoint of the coordinate creator; under a Lorentz boost the *fixed* counting transpose is not the covariant adjoint.

## 2. Observer positive form and the two bilinear structures

Let `η=diag(+---)` and `η(n,n)=1`, with `n` timelike. Set `h_n=-η+2n^\flat\otimes n^\flat`. For `v=a n+w`, `η(w,n)=0`, one has `h_n(v,v)=a²-η(w,w)>0` for `v≠0`. The induced exterior Gram matrix has entries

\[
B_{n;k}(S,T)=\det[h_n(e_s,e_t)]_{s\in S,t\in T}.
\tag{2.1}
\]

At `n_0=e_A`, `h_{n_0}=I` and `B_{n_0}=I_{16}`, literally the existing counting pairing. For `g∈O(1,3)`,
\[
h_{gn}(gv,gw)=h_n(v,w),\qquad
\rho(g)^T B_{gn}\rho(g)=B_n .
\tag{2.2}
\]
The positive adjoint is `C^\dagger(v)^{\dagger_n}=C(h_n(v,\cdot))`; dually `C(\alpha)^{\dagger_n}=C^\dagger(h_n^{-1}\alpha)`. The observer metric must move when the frame moves.

For the rational A/B boost `g=\left(\begin{smallmatrix}5/4&3/4\\3/4&5/4\end{smallmatrix}\right)`, `n'=gn_0=(5/4,3/4)`,
\[
h_{n'}|_{AB}=
\begin{pmatrix}17/8&-15/8\\-15/8&17/8\end{pmatrix},
\qquad g^T h_{n'}g=I,\quad \det h_{n'}|_{AB}=1.
\tag{2.3}
\]
All exterior degrees satisfy (2.2), not just degree one. The different, observer-free Lorentzian exterior form `B_\eta=\bigoplus_k C_k(\eta)` satisfies `ρ(g)^TB_\eta ρ(g)=B_\eta`, and its Lorentzian star has the additional `q=3` signature exponent. `B_n` is appropriate for an observer-positive Hamiltonian and annihilator adjoints; a *possible* observer-free covariant spacetime action can use `B_\eta`, but such an action is **not** constructed by (2.1). The fixed topological placement `J` is neither of these forms. No equality of positive and Lorentzian Riesz maps is asserted.

## 3. Raw solder transformation and the centered obstruction

There are two useful conventions; stating both avoids a hidden transpose. Let the raw row covector at `x` be `E_r(x)_a=\eta_{ra}+e_r{}^a(x)`. To agree with the repository's **right** solder action choose a right Lorentz matrix `\Lambda_x` (`\Lambda_x\eta\Lambda_x^T=\eta`):
\[
E'_r(x)=E_r(x)\Lambda_x,\qquad
e'_r(x)=E_r(x)\Lambda_x-\eta_r,\qquad
v_r(x)=\eta E_r(x)^T.
\tag{3.1}
\]
The internal **vector** frame map is `g_x=\Lambda_x^{-1}`, because `v'_r=g_xv_r` by `\eta\Lambda_x^T=\Lambda_x^{-1}\eta`. Accordingly the matter lift is `Q_g(x)=ρ(g_x)` and the observer moves as `n'_x=g_xn_x`. In the alternative vector convention `v'_r=g_xv_r` one recovers (3.1) by setting `\Lambda_x=g_x^{-1}`. At `e=0`, `v_r=\eta\eta_r^T=e_r`, so **all four fixed creators** are recovered. This transformation is defined from the independently specified row-vector meaning of the solder, not by imposing the final energy covariance.

This is a real action on the **full uncentered** `e` and preserves the period-two alternating mode. It agrees with `A4DSolderMetricCompletion.solderGram_right_lorentz_invariant` when `\Lambda` is constant along the averaged edge. For a varying sitewise frame, the repository's centered `\Theta_r(x)=\frac12(E_r(x)+E_r(x-r))` instead obeys
\[
\Theta'_r(x)-\Theta_r(x)\Lambda_x
=\tfrac12 E_r(x-r)(\Lambda_{x-r}-\Lambda_x).
\tag{3.2}
\]
Thus the existing *pointwise right action on an abstract centered solder* is **not** an owned lift to sitewise action on arbitrary pre-centered `e`. A covariant center needs a **specified** row pull `R_{x-r\to x}` with `R'=\Lambda_{x-r}^{-1}R\Lambda_x` and
\[
\widehat\Theta_r(x)=\tfrac12(E_r(x)+E_r(x-r)R_{x-r\to x}),\qquad
\widehat\Theta'_r(x)=\widehat\Theta_r(x)\Lambda_x.
\tag{3.3}
\]
The raw `E_r` must remain available separately; (3.3) alone loses Nyquist. Also, (3.1) is a solder field rule, **not** an identification of `e` with PR #70's affine link shift. The latter changes under affine translations `b_x` and its relation to `E_r` requires an independent solder/Cartan compatibility axiom.

## 4. Same CAR fiber transport and a finite differential

PR #70 stores `A_{xr}:V_{x+r}\to V_x`, so its linear part `L_{x\leftarrow y}=(A_{xr}).lin` can be lifted *without a second carrier* when `V` is identified with the real four-dimensional internal Role space and `L` is restricted to Lorentz isomorphisms:
\[
T_{x\leftarrow y}=\rho(L_{x\leftarrow y}),\quad
L'_{x\leftarrow y}=g_xL_{x\leftarrow y}g_y^{-1},\quad
T'_{x\leftarrow y}=Q_xT_{x\leftarrow y}Q_y^{-1}.
\tag{4.1}
\]
The brief's `T'_{xy}=\rho_y T_{xy}\rho_x^{-1}` is the **push** `x\to y` version; it is exactly the inverse orientation of (4.1). PR #70's affine shift acts on the coframe/background; it has no automatically induced action on exterior amplitudes. Its unrestricted `GL(V)` links do not preserve the Lorentz/observer structure until a Lorentz subgroup and observer transport are stipulated.

Creator compatibility follows *literally*, not by analogy:
\[
T_{x\leftarrow y}C^\dagger(v_y)T_{x\leftarrow y}^{-1}
=C^\dagger(L_{x\leftarrow y}v_y),\quad
T_{x\leftarrow y}C(\alpha_y)T_{x\leftarrow y}^{-1}
=C(L_{x\leftarrow y}^{-T}\alpha_y).
\tag{4.2}
\]
The stronger same-leg identity `T C^\dagger(v_r(y))=C^\dagger(v_r(x))T` holds **only if** the solder is parallel on that link, `L v_r(y)=v_r(x)`. Curved solder fields need not satisfy this; its defect is part of the full curvature/torsion calculus.

Set `C_r(x)=C^\dagger(v_r(x))` and `(\mathcal T_r\psi)(x)=T_{x\leftarrow x+r}\psi(x+r)`. A finite local candidate is
\[
d_{E,L}\psi(x)=L_{\rm period}\sum_r C_r(x)(\mathcal T_r\psi(x)-\psi(x)),\qquad
D_{E,L,n}=d_{E,L}+d_{E,L}^{\dagger_{B_n}}.
\tag{4.3}
\]
With `E=\eta`, `T=I`, `n=n_0`, (4.3) equals the owned `dForward`, its counting adjoint, and `D_H`. Under (3.1) and (4.1),
\[
d_{E',L'}Q_g=Q_gd_{E,L},\quad
D_{E',L',n'}Q_g=Q_gD_{E,L,n}.
\tag{4.4}
\]
The adjoint equation uses the *moving* form (2.2). The `dConn_gauge` theorem in `ArchiveCovariantCubicalDifferential` has creators on an independent Fock factor and links on a separate coefficient fiber. It does **not** imply (4.4) for rotating CAR; (4.4) follows from the explicit same-fiber intertwining (4.2). In curved geometry `d_{E,L}^2` has link curvature **and** solder compatibility terms; no nilpotency is claimed.

Pairing-preserving dual links are contragredient to (4.1). With the brief's compatible basis convention for `J:P\to D^*` and its **push** link `T_P:P_x\to P_y`, use `T_D=J_y^{-T}T_P^{-T}J_x^T`; for PR #70's pull, swap endpoints. Relative dual holonomy is the inverse-transpose image with the `J` endpoint identifications. Similarity `J T_P J^{-1}` transports identified modes and coincides with a pairing-preserving link only under an extra isometry.

## 5. Exact failed jet and the missing common-center cell rule

The differential (4.3) is a **valid frame-covariant seed**, not an energy selector. Its `D_{E,L,n}^2` has the archive Laplacian at flat, while the accepted energy has `W(0)=I`. Even the normalized candidate `I+\lambda(d^\dagger_{E,L,n}d_{E,L}-d_0^\dagger d_0)` misses `H(e)`: if `e_A{}^A=t` is constant, `T=I` and `\psi` is a constant scalar cochain, then `d_{E,L}\psi=0` for every `t`, whereas
\[
\left.\partial_t \langle\psi,(I+H(e))\psi\rangle\right|_{0}
=\langle\psi,\tfrac12(U_A+U_A^{-1})\psi\rangle
=\|\psi\|^2.
\tag{5.1}
\]
Any energy assembled *only* from this forward derivative and a fixed flat norm misses a scalar, zeroth-order neighbor/volume coupling. An independently weighted cell term is necessary. This is a **counterexample to that explicit candidate**, not a no-go for every covariant cell energy.

The accepted full jet is
\[
H(e)=\sum_r \tfrac12(M_{e_r{}^r}U_r+U_r^{-1}M_{e_r{}^r})I
-\sum_{s,r}\left(M_{e_s{}^r}U_s A_r E_{sr}
+E_{rs}A_r^*U_s^{-1}M_{e_s{}^r}\right),\quad
A_r=\tfrac12(I+U_r^{-1}),\ E_{sr}=c_s^\dagger c_r.
\tag{5.2}
\]
The `1/2` in the scalar bond is endpoint polarization. The **different** `1/2` in `A_r` is a specified symmetric comparison of two adjacent `r` endpoints; it follows from `A_r\Delta_r=D_r` but does not follow from exterior representation, Lorentz invariance, or incidence alone. For `s\ne r`, `U_s A_r=(U_s+U_sU_r^{-1})/2` samples sources `x+s` and `x+s-r`. The second term is a corner at distance two in site coordinates, yet contained in a common elementary square closure. To make it frame covariant the two amplitudes and both factors of `E_{sr}` must be transported to a **specified** common center with two paths and an ordering; (4.3) supplies no such half-edge/path comparison or scalar bond rule. Simply writing (5.2) as the definition of the energy would restate the target, not derive its coefficients.

At `L=2`, take raw `e_A{}^A=(-2,+2)` with other components zero. Its centered solder and centered Gram see zero perturbation, but the specified one-form diagonal of `H` is `(+2,-2)`. Equation (3.1) retains these two oriented edge slots and can in principle feed them to a cell rule; (3.3) or (4.3) alone does **not** pass the target. At `L=3` with `e_A{}^B(0)=a`, the accepted matrix element from `(0,\{A\})` to `(A-B,\{B\})` is `-a/2`. The exterior identity `E_{AB}|B\rangle=|A\rangle` and the second path in `U_AA_B` reproduce its algebraic **shape**; no coefficient is derived by (1.1–4.4).

For the rational boost, (2.3), (3.1), (4.1), (4.4) pass exactly when the observer, solder, matter and link move together. The old test of a **fixed** `I` positive form under an active boost is inapplicable. The accepted `H(e)` on a Lorentz-gauge orbit must be tested jointly with `D_nW`: `D_eW[\delta e]` by itself is not a complete frame Ward when `n` moves. Since the all-order `W(e,n,L)` is missing, there is no claim that its staggered first jet passes that boosted energy test.

## 6. Located `J` and a new sitewise obstruction

On a **single common fiber**, the oriented exterior complement obeys the cofactor identity
\[
J_k\rho_k(g)=\det(g)\,\rho_{4-k}(g)^{-T}J_k.
\tag{6.1}
\]
The orientation line removes the `det g` pseudoscalar; for a signed Role permutation that also permutes the archive site coordinates, the orthogonal property reduces (6.1) to the familiar `JQ_\sigma=\operatorname{sgn}(\sigma)Q_\sigma J`. This algebraic relation is **not** an on-archive commutation theorem for a general Lorentz boost: the located `J_{PD}` sends `(x,S)` to dual site `x-\mathbf1_{S^c}`, which depends on `S`. A boost mixes `|A\rangle` and `|B\rangle` at fixed primal `x`, but `J|A\rangle` and `J|B\rangle` land at *different dual sites* `x-(B+C+D)` and `x-(A+C+D)` for every `L\ge2`. Multiplying dual components at one fixed site by `ρ(g)^{-T}` cannot reproduce both destinations. Changing the orientation sign does not move a site.

One may define the induced dual action `Q_D:=JQ_PJ^{-1}`, but it then contains grade-dependent site shifts; it is **not** the naïve sitewise exterior action. A common-center placement/transport theorem is required before asserting simultaneous **sitewise** Lorentz covariance of both colors. The reference `J` and its square/signs remain unchanged; this obstruction has no implication that `J` is a metric star or that the scalar reverse-star no-go applies to (4.3).

## 7. Direct answers to the 18 required questions

| # | Answer |
|---|---|
| 1 | Yes, `ArchiveFockState` is the 16-dimensional exterior basis `\Lambda^*V`. |
| 2 | The arbitrary invertible lift is (1.1) in all degrees, with exact composition. |
| 3 | No Spin/Dirac spinor is constructed or required for this exterior problem. |
| 4 | Yes: (2.1–2.3) reconcile counting in a reference gauge with covariance of moving positive forms. |
| 5 | Yes; `n=e_A` is a reference observer gauge, and `U_A` remains an archive Role shift. |
| 6 | Raw row/covector rule (3.1); its induced vector action is the inverse of the repository's right matrix. Local centering correction is (3.2). |
| 7 | Yes, `C_r^\dagger(x)=C^\dagger(v_r(x))` and its algebraic contraction use the same existing carrier. |
| 8 | Exterior lifted link (4.1–4.2); matching a named leg across an edge additionally requires parallel solder on that edge. |
| 9 | PR #70 supplies the **linear** affine link/gauge law, but no owned rotating-CAR lift or solder identification; (4.1) constructs a conditional Lorentz-restricted lift. Fixed-creator `dConn` is not that theorem. |
| 10 | No independently derived cell energy from this frame lift has the complete `H(e)`; (5.1) exhibits a concrete failed seed. |
| 11 | Endpoint polarization and an added symmetric `r`-endpoint comparison `A_r`; these are independent requirements. |
| 12 | The `U_sU_r^{-1} E_{sr}/2` path in `U_sA_rE_{sr}`, with a common square center. |
| 13 | Raw `e` retains Nyquist; a rule factoring through centered `\Theta` fails, and the current energy seed has **not** passed the target Nyquist jet. |
| 14 | Yes for `h_n`, exterior fields, raw solder, links and differential; boosted full staggered energy untested without `W(e,n,L)`. |
| 15 | Yes, the positive form and its adjoint depend on the transformed observer. |
| 16 | An observer-free Lorentzian exterior bilinear exists; a physical covariant spacetime **action** is not yet established. |
| 17 | Yes: located `J` stays fixed; its action on a general sitewise boost requires shifted/non-sitewise dual placement (Section 6). |
| 18 | A typed common-center solder/half-edge path rule and an independently derived finite observer-positive cell energy reproducing every term of (5.2), followed by an observer-free action if sought. |

## 8. Theorem-ready handoff

All names below are **proposals**, not existing Lean theorem names or claims of a completed physical action.

1. `ArchiveExteriorFrameLift.lean`: define `ρ` by minors on `ArchiveFockState` and prove identity, Cauchy–Binet composition, inverse, degree preservation and all identities (1.2). Include arbitrary `GL(V)` and signed Role permutation; do not call `ρ` spinorial.
2. `A4DObserverPositiveExterior.lean`: for `IsRoleLorentz` and future unit `n` prove positivity, `h_{e_A}=I`, all-degree compound Gram relation (2.2), and both formulas for observer adjoints. Formalize the exact `5/4,3/4` boost over rational matrices before the real positivity proof.
3. `A4DRawSolderFrameAction.lean`: state vector/row conventions, group action (3.1), `v'_r=g_xv_r`, and the exact local-frame centering defect (3.2). Add a **typed row transport** to prove (3.3), keeping the raw Nyquist field independent. Do not silently identify PR #70's affine shift with `e`.
4. `ArchiveAffineExteriorLink.lean`: specialize `ArchiveAffineCartanConnection.affineGauge_lin` to Lorentz linear links on `V=Role\to\mathbb R`. Exterior-lift the PR #70 *pull* and its path/curvature; prove (4.1–4.2). Define (4.3) on the same Fock fiber and prove (4.4), flat `dForward` and `D_H`. Separate link curvature from nonparallel-solder terms. Reuse `ArchivePrimalDualMovingAction` to prove the typed contragredient dual link.
5. `A4DLocatedFrameCompatibilityBoundary.lean`: prove common-fiber (6.1) with orientation line and the explicit `L=2,3` different-anchor witness. A sitewise dual frame action must either be replaced by `JQ_PJ^{-1}` with its shifts or be accompanied by an independently specified common-center transport.
6. `A4DSolderedCellEnergyJet.lean`: **missing physical primitive**. Define its local cell monomials, endpoint interpolation, two corner routes, independent observer field and connection, and exact frame law *before* comparing to (5.2). Prove every grade block, scalar neighbor, Nyquist and `L=3` corner. Keep the second-order law `Q(e)` and located `J` selection outside this module. No sourced stress Ward until a complete action and its independent Euler variations exist.

The decisive next test is to derive the `A_r` half-average and the two transported `s-r` corner paths from one local covariant cell density **without inserting (5.2) as an axiom**. The verified exterior lift and observer form make this test well-typed; they do not themselves set its coefficients.

## 9. Exact controls

The attached-in-this-memo Python below uses exact `Fraction` arithmetic and passed **79/79** assertions: degrees 0–4, all four fixed creators at identity, arbitrary nontrivial permutation and rational boost, CAR and covariant contractions, positive and Lorentzian exterior forms, observer congruence, nontrivial same-fiber link, raw/centered `L=2` separation, `L=3` corner shape, and the located `J` support mismatch. The algebraic proofs in Sections 1–6 are independent of a finite test; no full Lean build or repository edit was made.

### Reproducible checker

```python
"""Exact rational controls for the exterior/observer frame lift (research only)."""
from fractions import Fraction as F
from itertools import combinations

checks = []


def ck(label, proposition):
    assert proposition, label
    checks.append(label)


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def tr(a):
    return list(map(list, zip(*a)))


def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def det(a):
    n = len(a)
    if not n:
        return F(1)
    return sum((-1) ** j * a[0][j] * det([row[:j] + row[j + 1:] for row in a[1:]])
               for j in range(n))


def inv(a):
    n = len(a)
    work = [list(row) + list(ident(n)[i]) for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if work[i][j])
        work[j], work[pivot] = work[pivot], work[j]
        scale = work[j][j]
        work[j] = [v / scale for v in work[j]]
        for i in range(n):
            if i != j:
                scale = work[i][j]
                work[i] = [v - scale * u for v, u in zip(work[i], work[j])]
    return [row[n:] for row in work]


def wedge(a):
    out = [[F(0) for _ in range(16)] for _ in range(16)]
    for s in range(16):
        src = [i for i in range(4) if s & (1 << i)]
        for t in range(16):
            dst = [i for i in range(4) if t & (1 << i)]
            if len(dst) == len(src):
                out[t][s] = det([[a[i][j] for j in src] for i in dst])
    return out


def create(v):
    out = [[F(0) for _ in range(16)] for _ in range(16)]
    for src in range(16):
        for r in range(4):
            if not src & (1 << r):
                out[src | (1 << r)][src] = v[r] * (-1) ** ((src & ((1 << r) - 1)).bit_count())
    return out


def contract(alpha):
    return tr(create(alpha))


def add(a, b):
    return [[x + y for x, y in zip(row, brow)] for row, brow in zip(a, b)]


def gram(a):
    return mm(tr(a), a)


eye4 = ident(4)
eye16 = ident(16)
eta = [[F(i == j) * (F(1) if i == 0 else F(-1)) for j in range(4)]
       for i in range(4)]
boost = [[F(5, 4), F(3, 4), F(0), F(0)],
         [F(3, 4), F(5, 4), F(0), F(0)], eye4[2], eye4[3]]
perm = [[F(i == [0, 2, 1, 3][j]) for j in range(4)] for i in range(4)]

for name, a in [('identity', eye4), ('role-B-C-swap', perm), ('boost', boost),
                ('boost-then-permutation', mm(boost, perm))]:
    ck(name + '-rho-degree-0..4', all(
        wedge(a)[t][s] == 0 for t in range(16) for s in range(16)
        if t.bit_count() != s.bit_count()))
    ck(name + '-rho-inverse', mm(wedge(a), wedge(inv(a))) == eye16)
    ck(name + '-rho-composition', wedge(mm(a, boost)) == mm(wedge(a), wedge(boost)))
    for r in range(4):
        v = [F(i == r) for i in range(4)]
        moved = [sum(a[i][j] * v[j] for j in range(4)) for i in range(4)]
        ck(name + f'-creator-{r}',
           mm(mm(wedge(a), create(v)), wedge(inv(a))) == create(moved))
        alpha = [F(i == r) for i in range(4)]
        dual = [sum(inv(a)[j][i] * alpha[j] for j in range(4)) for i in range(4)]
        ck(name + f'-contraction-{r}',
           mm(mm(wedge(a), contract(alpha)), wedge(inv(a))) == contract(dual))

for r in range(4):
    for s in range(4):
        ck(f'CAR-{r}-{s}', add(mm(contract(eye4[r]), create(eye4[s])),
                                 mm(create(eye4[s]), contract(eye4[r]))) ==
           (eye16 if r == s else [[F(0)] * 16 for _ in range(16)]))

ck('Lorentz-boost', mm(mm(tr(boost), eta), boost) == eta)
ck('nontrivial-permutation-lorentz', mm(mm(tr(perm), eta), perm) == eta)


def h(n):
    en = [sum(eta[i][j] * n[j] for j in range(4)) for i in range(4)]
    return [[-eta[i][j] + 2 * en[i] * en[j] for j in range(4)] for i in range(4)]


n0 = eye4[0]
n1 = [sum(boost[i][j] * n0[j] for j in range(4)) for i in range(4)]
hn = h(n1)
ck('observer-flat', h(n0) == eye4)
ck('observer-moved-rational', [row[:2] for row in hn[:2]] ==
   [[F(17, 8), F(-15, 8)], [F(-15, 8), F(17, 8)]])
ck('observer-covariance', mm(mm(tr(boost), hn), boost) == eye4)
ck('observer-positive-principal-minors', all(det([row[:k] for row in hn[:k]]) > 0
                                           for k in range(1, 5)))
ck('observer-exterior-covariance',
   mm(mm(tr(wedge(boost)), wedge(hn)), wedge(boost)) == eye16)
ck('lorentzian-exterior-invariant',
   mm(mm(tr(wedge(boost)), wedge(eta)), wedge(boost)) == wedge(eta))
ck('positive-adjoint-creator',
   mm(inv(wedge(hn)), mm(tr(create(eye4[0])), wedge(hn))) ==
   contract([sum(hn[i][j] * eye4[0][j] for j in range(4)) for i in range(4)]))

# PR70 stores pull x <- y. A nontrivial pure frame has g_x=boost,g_y=I,
# L'=g_x I g_y^{-1}; it intertwines the creators at its two endpoints.
tx = wedge(boost)
cy = create(eye4[0])
cx = mm(mm(tx, cy), inv(tx))
ck('nontrivial-link-creator-pull', mm(tx, cy) == mm(cx, tx))
ck('nontrivial-link-gauge', tx == mm(wedge(boost), wedge(eye4)))

# Raw right solder matrix: E=eta+e; vector legs are eta*E_r^T.
# At constant gauge with repository Lambda=boost^{-1}, the vector gauge is boost.
new_e_plus_eta = mm(eta, inv(boost))
for r in range(4):
    original_leg = [sum(eta[i][a] * eta[r][a] for a in range(4)) for i in range(4)]
    transformed_leg = [sum(eta[i][a] * new_e_plus_eta[r][a] for a in range(4))
                       for i in range(4)]
    ck(f'raw-solder-vector-{r}', transformed_leg ==
       [sum(boost[i][j] * original_leg[j] for j in range(4)) for i in range(4)])

# The uncentered L=2 edge pair survives although its backward average is zero.
edge_nyquist = [F(-2), F(2)]
ck('L2-raw-Nyquist-not-centered', edge_nyquist != [F(0), F(0)] and
   all((edge_nyquist[x] + edge_nyquist[(x - 1) % 2]) / 2 == 0 for x in range(2)))
ck('L2-accepted-one-form-jet', [-v for v in edge_nyquist] == [F(2), F(-2)])

# At L=3, the r-shifted endpoint x+A-B of U_A A_B carries half weight.
L = 3
x = (0, 0, 0, 0)
source = (1, L - 1, 0, 0)
e_ab = F(3)
corner = -e_ab / 2 * mm(create(eye4[0]), contract(eye4[1]))[1 << 0][1 << 1]
ck('L3-distance-two-corner', source == ((x[0] + 1) % L, (x[1] - 1) % L, 0, 0)
   and corner == -F(3, 2))

# Center matching at one site fails for a degree-mixing frame: J(A) and J(B)
# have different dual anchors, even if the orientation line is transformed.
dual_anchor_A = (0, L - 1, L - 1, L - 1)
dual_anchor_B = (L - 1, 0, L - 1, L - 1)
ck('located-J-sitewise-boost-mismatch',
   wedge(boost)[1 << 1][1 << 0] == F(3, 4)
   and dual_anchor_A != dual_anchor_B)

print(f'PASS {len(checks)}/{len(checks)} exact frame controls')
```

**Terminal verdict: FRAME-LIFT-CONSTRUCTED-STAGGERED-JET-MISSING.**