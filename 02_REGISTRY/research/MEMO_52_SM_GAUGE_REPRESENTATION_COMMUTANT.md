# Joint commutant on ArchiveCochain: Hodge Dirac and diagonal Role transport

**Snapshot:** `origin/main=750ac39236aedd5a3b120f9251ab1bb10f8d637f`, fetched 2026-09-24. Canonical task `EXP-SM-GAUGE-REPRESENTATION-COMMUTANT` read completely. **Carrier:** real `ArchiveCochain N=(ArchiveRolePhaseGroup N\times ArchiveFockState)\to\mathbb R`, period `L=N+2\ge2`. No repository edits.

## 0. One terminal verdict

**ARCHIVE-COCHAIN-JOINT-COMMUTANT-STRICTLY-LARGER-CLASSIFIED.** The joint commutant of the *corrected* `D_H` and the entire diagonal signed `S_4` action is already nontrivial on the constant-site kernel and is much larger on positive spectral levels. The analogous commutant of `D_H^2` is strictly larger still: it permits cross mixing of the two Dirac-sign eigenspaces on each positive Laplacian level. Equations (2.5–2.7) classify **both real associative algebras for every archive period**, including all accidental energy degeneracies. The complexified square commutant contains number phase `U(1)_N`; the real carrier has `N` and parity but does not literally carry that complex phase without complexification.

The discrete diagonal Role image is itself **not** a subgroup of its full `S_4` centralizer: generic permutations do not commute with one another. The joint commutant's nonlocal spectral unit group is **not** thereby the Standard Model gauge group. A locality, grading, carrier and interaction criterion would have to be added and proved before a gauge interpretation.

## 1. Frozen owners and exact scope

`ArchiveCubicalDifferential.lean` defines the site×Fock cochain carrier and oriented shifts. `ArchiveHodgeCARDirac.lean` defines `D_H=d+d^\dagger` with its counting adjoint. `ArchiveHodgeCARDiracSquare.lean` proves `D_H^2=\Delta_{\rm site}\otimes I_{16}` with the oriented period-two collision treated explicitly. `ArchiveHodgeCARDiracKernel.lean` proves that precisely the 16 constant-site Fock amplitudes are the kernel. `ArchiveDiagonalRoleTransport.lean` proves a **simultaneous** signed Fock and site-coordinate `S_4` action commuting with `D_H`. The fixed-site `ArchiveFockIntrinsicCommutant.lean` statement requires the *full* separate creation and annihilation family; it does not compute this archive joint commutant.

The object classified is
\[
\mathcal C_D(L)=\{A\in\operatorname{End}_{\mathbb R}(\mathrm{ArchiveCochain}):
[A,D_H]=0,\ [A,Q_\sigma]=0\ \forall\sigma\in S_4\},
\quad
\mathcal C_\square(L)=\mathcal C(D_H^2,Q(S_4)).
\tag{1.1}
\]
The carrier has dimension `16L^4` over `\mathbb R`. No shell projection, site-locality, CAR preservation, unitary condition or boundary holonomy is assumed in (1.1).

## 2. General-period spectral and representation classification

Complexify only as a computational device for the finite Fourier transform; the final eigenspaces and algebras below are **real**. For `p\in(\mathbb Z/L)^4`,
\[
\lambda(p)=4L^2\sum_{r=1}^4\sin^2(\pi p_r/L),\qquad
D_H(p)^2=\lambda(p)I_{16}.
\tag{2.1}
\]
For each distinct `\lambda\ge0` define
\[
n_\lambda=\#\{p:\lambda(p)=\lambda\},\qquad
t_\lambda=\#\{(a,a,a,b):\lambda(a,a,a,b)=\lambda\}.
\tag{2.2}
\]
The second number counts momenta fixed by **one** 3-cycle, say `(ABC)`. Any conjugate has the same count. Accidental equality of energies from different momentum orbits is intentionally included in `n_\lambda,t_\lambda`.

The character of the 16-dimensional exterior `S_4` representation is `\chi_F(\sigma)=\det(I+P_\sigma)`. In the class order `(1^4),(2\,1^2),(2^2),(3\,1),(4)` it is
\[
\chi_F=(16,0,0,4,0).
\tag{2.3}
\]
Consequently the real square eigenspace `E_\lambda=\ker(D_H^2-\lambda I)` has character `\chi_{E_\lambda}(\sigma)=\chi_F(\sigma)\,\#\{p\text{ fixed by }\sigma,\lambda(p)=\lambda\}`. All five irreducible `S_4` representations are of real type. In the order `\mathbf1,\operatorname{sgn},\mathrm{Std}_3,\mathrm{Std}_3\otimes\operatorname{sgn},V_{(2,2)}`, character orthogonality yields
\[
\operatorname{mult}(E_\lambda)=
\left(\frac{2n_\lambda+4t_\lambda}{3},
      \frac{2n_\lambda+4t_\lambda}{3},
      2n_\lambda,2n_\lambda,
      \frac{4(n_\lambda-t_\lambda)}{3}\right).
\tag{2.4}
\]
This is an integer tuple because it comes from the actual finite representation. At `\lambda=0` only `p=0` occurs, `n_0=t_0=1`, giving `(2,2,2,2,0)`. Thus **the actual S₄-equivariant commutant on the 16-dimensional kernel**, as a subblock of the archive problem, is `M_2(\mathbb R)^{\oplus4}`, dimension 16; it is not `M_{16}`.

For every `\lambda>0`, `D_H` has eigenvalues `\pm\sqrt\lambda`. Parity `\Gamma=(-1)^N` commutes with `S_4,D_H^2` and anticommutes with `D_H`, so `E_{\lambda,+}\cong E_{\lambda,-}` as `S_4` representations. Each has **half** the multiplicities (2.4):
\[
m_\lambda=
\left(a_\lambda,a_\lambda,n_\lambda,n_\lambda,b_\lambda\right),\quad
a_\lambda=\frac{n_\lambda+2t_\lambda}{3},\quad
b_\lambda=\frac{2(n_\lambda-t_\lambda)}{3}.
\tag{2.5}
\]
Here `E_{\lambda,\pm}=\ker(D_H\mp\sqrt\lambda I)`. The real spectral theorem and real-type Schur lemma now give the promised exact full-carrier algebra isomorphisms:
\[
\boxed{\displaystyle
\mathcal C_D(L)\cong M_2(\mathbb R)^{\oplus4}\ \oplus\
\bigoplus_{\lambda>0}\ \bigoplus_{\epsilon=\pm}
\bigl(M_{a_\lambda}(\mathbb R)^{\oplus2}\oplus
M_{n_\lambda}(\mathbb R)^{\oplus2}\oplus
M_{b_\lambda}(\mathbb R)\bigr)}
\tag{2.6}
\]
\[
\boxed{\displaystyle
\mathcal C_\square(L)\cong M_2(\mathbb R)^{\oplus4}\ \oplus\
\bigoplus_{\lambda>0}
\bigl(M_{2a_\lambda}(\mathbb R)^{\oplus2}\oplus
M_{2n_\lambda}(\mathbb R)^{\oplus2}\oplus
M_{2b_\lambda}(\mathbb R)\bigr).}
\tag{2.7}
\]
Zero multiplicity means omit that factor. These are **abstract algebra decompositions**, not canonical choices of eigenbases or local generators. Algebraic units are corresponding products of `GL` groups; counting-orthogonal units are corresponding products of `O` groups. The square has off-diagonal maps `E_{\lambda,+}\leftrightarrow E_{\lambda,-}` unavailable to the Dirac commutant.

For a quick dimension check,
\[
\dim\mathcal C_D(L)
=16+\sum_{\lambda>0}\frac83(2n_\lambda^2+t_\lambda^2),
\qquad
\dim\mathcal C_\square(L)
=16+\sum_{\lambda>0}\frac{16}{3}(2n_\lambda^2+t_\lambda^2).
\tag{2.8}
\]
The `\lambda=0` contribution is **once**, since there is one kernel, not two Dirac signs.

## 3. Exact small-period controls and a local exception

For `L=2`, a nonzero momentum component contributes `16` to (2.1), so levels are `\lambda_m=16m`, `m=0,\ldots,4`. The pairs `(n_m,t_m)` are `(1,1),(4,1),(6,0),(4,1),(1,1)`. The table gives the five multiplicities on **each positive Dirac-sign eigenspace**; the row `m=0` instead describes the undivided kernel.

| `m` | `\lambda_m` | `(n_m,t_m)` | `S_4` multiplicities: trivial, sign, standard, twisted standard, (2,2) | `\dim E_{m,+}` |
|---:|---:|---:|---|---:|
| 0 | 0 | (1,1) | (2,2,2,2,0), kernel | 16 (undivided) |
| 1 | 16 | (4,1) | (2,2,4,4,2) | 32 |
| 2 | 32 | (6,0) | (2,2,6,6,4) | 48 |
| 3 | 48 | (4,1) | (2,2,4,4,2) | 32 |
| 4 | 64 | (1,1) | (1,1,1,1,0) | 8 |

Thus on the full `16\cdot2^4=256` dimensional cochain, `\dim\mathcal C_D(2)=392` and `\dim\mathcal C_\square(2)=768`. For `L=3`, levels `\lambda_m=27m` have `n_m=(1,8,24,32,16)` and `t_m=(1,2,0,2,4)`. Direct substitution yields `\dim\mathcal C_D(3)=10320` and `\dim\mathcal C_\square(3)=20624` on a `16\cdot3^4=1296` dimensional cochain. These numbers concern *all* endomorphisms; their size is evidence of large spectral multiplicity, not of a local gauge group.

There is an extra **site-local period-two exception**. Write `\gamma_r=c_r^\dagger+c_r`, `\beta_r=c_r-c_r^\dagger`, and `\Gamma=(-1)^N`. At `L=2`, `U_r^{-1}=U_r`, hence
\[
D_H=L\sum_r(U_r-I)\gamma_r,\qquad
K_{\rm loc}:=\Gamma\sum_r\beta_r,\quad
[K_{\rm loc},\gamma_r]=0,\quad K_{\rm loc}^2=4I.
\tag{3.1}
\]
The signed Role action permutes the `\beta_r`, so `I_X\otimes K_{\rm loc}` commutes with **both** operators in (1.1), changes Fock degree and is non-scalar. At `L\ge3`, the independent `U_r` and `U_r^{-1}` coefficients of `D_H` force a **site-independent fixed-fiber** `I_X\otimes M` commuting with `D_H` to commute separately with every `c_r^\dagger` and `c_r`; by the owned full-CAR commutant theorem, `M` is scalar. Thus the fixed-site scalar result is true for this restricted archive test at `L\ge3`, while the `L=2` collision makes it false for the **weaker Dirac-only** fixed-fiber test. There is no conflict with the owned full-CAR theorem at either period.

## 4. Hostile witnesses and group boundaries

- **Strictly larger at every period, independent of (3.1).** Let `u` be the normalized constant-site vacuum and `v` the normalized constant-site sum of the four one-form basis vectors. Both are `S_4`-fixed, orthogonal and annihilated by `D_H`. The rank-two skew map `X=|v\rangle\langle u|-|u\rangle\langle v|` commutes with `D_H` (by self-adjointness and the kernel characterization) and every diagonal Role transport. Its rotations `\exp(\theta X)` form a continuous orthogonal circle **inside** `\mathcal C_D(L)`. It mixes Fock degrees, unlike any element of the discrete Role image. Even after one removes the zero modes by specified holonomy, the positive blocks (2.6) still exhibit multiplicities; the holonomy-modified operator itself would require a separate calculation.
- **Parity and number.** `\Gamma D_H=-D_H\Gamma`, `[\Gamma,D_H^2]=0`. `[N,D_H^2]=0` but `[N,D_H]\ne0`. Only after complexifying the real cochains does `e^{i\theta N}` define the claimed number `U(1)` of square-level **unitary** symmetries. The real positive counting-orthogonal commutant is described by the `O` factors above.
- **Discrete Role image versus commutant.** `Q_\sigma D_H=D_HQ_\sigma`, but `Q_\sigma Q_\tau\ne Q_\tau Q_\sigma` for noncommuting `\sigma,\tau`. An individual group element is in the joint centralizer only if its image is central (the action is faithful, so only the identity). Group-algebra class sums and irreducible central projectors can lie in the commutant. Thus “the commutant equals `S_4`” is not even type-correct as a group comparison.
- **Role-A stabilizer.** `U_A` commutes with `D_H` and with `S_3` permuting `B,C,D`, but not with the full `S_4`: a swap `A\leftrightarrow B` sends it to `U_B`. A commutant calculated with this stabilizer alone is a different, larger object.
- **Shell versus whole carrier.** The owned spatial lowest shell has real rank `96` at `L\ge3` (`48` at `L=2`), using only `B,C,D` momenta and constant `A`. Full `S_4` moves some of those vectors outside that shell. On the **full** `L=3` first Laplacian level all four axes contribute, giving `8\cdot16=128` dimensions; at `L=2` the first level has `4\cdot16=64`. Neither spatial shell is a substitute for (1.1).
- **A failing site-dependent field.** For `f(x)=1_{\{x_A=0\}}`, `[M_f,U_A]\psi(x)=(f(x)-f(x+A))\psi(x+A)` is nonzero at every `L\ge2` for a suitable `\psi`. Site dependence does not automatically commute with translations or `D_H`. The large spectral centralizer does not say that arbitrary local gauge functions are symmetries.

No algebraic factor count above identifies `SU(3)\times SU(2)\times U(1)` or particle generations. The 70-dimensional degree-preserving fiber endomorphism space is **not** the CAR-bilinear Lie algebra; the 16 kernel endomorphisms are **not** a licensed `M_{16}` gauge block after imposing `S_4`; Albert, anomaly and other dimension comparisons are not definitions of (1.1).

## 5. Theorem-ready Lean handoff

The following are *proposed* formal statements, with no modification of existing owners.

1. `ArchiveJointCommutantBasis.lean`: define the two centralizers (1.1) as `\mathbb R`-subalgebras of endomorphisms of `ArchiveCochain N`. Prove self-adjointness and `S_4` equivariance using `ArchiveHodgeCARDirac`, `ArchiveDiagonalRoleTransport`; prove `E_0\simeq\Lambda^*\mathbb R^4` equivariantly via `hodgeKernelEquiv`.
2. `ArchiveJointCommutantFourierCharacter.lean`: prove (2.1), `\chi_F=\det(I+P_\sigma)` by exterior character, then the full `E_\lambda` trace formula. Use parity to identify the two real `E_{\lambda,\pm}`; the trace of `Q_\sigma D_H|E_\lambda` vanishes. Formalize the ordinary real `S_4` character table (its irreps are of real type) and derive integer multiplicities (2.4–2.5).
3. `ArchiveJointCommutantSpectralDecomposition.lean`: apply finite-dimensional real spectral decomposition and real Schur/Wedderburn to obtain the *typed* algebra equivalences (2.6–2.7) and dimensions (2.8). Do not assert a canonical Fourier eigenbasis where there are coincident energies. Add separately the complexification map and `U(1)_N` square inclusion.
4. `ArchiveJointCommutantSmallPeriods.lean`: evaluate exact `L=2,3` energy/3-cycle counts, the five multiplicity rows and dimensions `392,768,10320,20624`. Keep the period-two forward/backward collision rather than treating its two oriented edges as distinct sites.
5. `ArchiveJointCommutantHostileWitnesses.lean`: construct the kernel skew rotation `X`, its Dirac and `S_4` commutation and degree mixing. Prove (3.1) on `L=2` using the owned CAR; for `L\ge3` prove the site-independent fixed-fiber scalar result from independent shift coefficients. Add `U_A` versus full `S_4`, failing site multiplication, and the full-`S_4` noninvariance of the spatial shell.

The next **physical** gate is a precise extra constraint selecting local, grade/observer compatible transformations and testing them against a sourced cell action and links. Until those constraints exist, (2.6–2.7) are exact spectral symmetry algebras, not a gauge representation theorem.

## 6. Reproducible exact controls

The appended rational checker passed **62/62** assertions. It enumerates all 24 signed Role permutations for the site-local `L=2` witness; checks its square and Majorana commutation, its failure against a separate creator; enumerates exact `L=2,3` momentum and 3-cycle counts; verifies integer multiplicities, all eigenspace dimensions and the four full-carrier centralizer dimensions. The arbitrary-period (2.1–2.8) remains a mathematical proof from Fourier, parity and character orthogonality, not an inference from these two finite examples.

### Standalone checker

```python
"""Exact S4 spectral multiplicities and a local L=2 centralizer witness."""
from fractions import Fraction as F
from itertools import permutations, product
from math import comb

checks = []


def ck(name, assertion):
    assert assertion, name
    checks.append(name)


def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(row, brow)] for row, brow in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(row, brow)] for row, brow in zip(a, b)]


def tr(a):
    return list(map(list, zip(*a)))


def create(r):
    out = [[F(0)] * 16 for _ in range(16)]
    for s in range(16):
        if not s & (1 << r):
            out[s | (1 << r)][s] = F((-1) ** ((s & ((1 << r) - 1)).bit_count()))
    return out


def wedgeperm(p):
    out = [[F(0)] * 16 for _ in range(16)]
    for s in range(16):
        images = [p[r] for r in range(4) if s & (1 << r)]
        t = sum(1 << a for a in images)
        inversions = sum(images[i] > images[j] for i in range(len(images))
                         for j in range(i + 1, len(images)))
        out[t][s] = F((-1) ** inversions)
    return out


I = ident(16)
zero = [[F(0)] * 16 for _ in range(16)]
parity = [[F((-1) ** i.bit_count() if i == j else 0) for j in range(16)]
          for i in range(16)]
cs = [create(r) for r in range(4)]
as_ = [tr(c) for c in cs]
gammas = [add(c, a) for c, a in zip(cs, as_)]
skews = [sub(a, c) for c, a in zip(cs, as_)]
K = mm(parity, [list(map(sum, zip(*(b[i] for b in skews)))) for i in range(16)])
ck('period2-K-not-scalar', K != I and K != zero and K[1][0] != 0)
ck('period2-K-square-four', mm(K, K) == [[4 * v for v in row] for row in I])
for r in range(4):
    ck(f'period2-K-commutes-Majorana-{r}', mm(K, gammas[r]) == mm(gammas[r], K))
ck('period3-K-fails-separate-creator', mm(K, cs[0]) != mm(cs[0], K))
for p in permutations(range(4)):
    q = wedgeperm(p)
    ck('period2-K-commutes-S4-' + ''.join(map(str, p)), mm(K, q) == mm(q, K))

for L in (2, 3):
    counts = {}
    fixed3 = {}
    # For L=2,3 nonzero momenta have one common single-coordinate energy.
    for p in product(range(L), repeat=4):
        m = sum(v != 0 for v in p)
        counts[m] = counts.get(m, 0) + 1
        if p[0] == p[1] == p[2]:
            fixed3[m] = fixed3.get(m, 0) + 1
    d_joint = 16
    d_square = 16
    for m in range(1, 5):
        n, t = counts[m], fixed3.get(m, 0)
        # S4 irreps in order: trivial, sign, standard, standard*sign, (2,2).
        eplus = (F(n + 2 * t, 3), F(n + 2 * t, 3), F(n), F(n),
                 F(2 * (n - t), 3))
        ck(f'L{L}-m{m}-integral-multiplicities', all(v.denominator == 1 for v in eplus))
        ck(f'L{L}-m{m}-correct-eigenspace-dimension',
           sum(a * d for a, d in zip(eplus, (1, 1, 3, 3, 2))) == 8 * n)
        dj = 2 * sum(v * v for v in eplus)
        ds = sum((2 * v) ** 2 for v in eplus)
        ck(f'L{L}-m{m}-character-commutant-dimension',
           ds == F((16 * n) ** 2 + 8 * (4 * t) ** 2, 24)
           and dj * 2 == ds)
        d_joint += int(dj)
        d_square += int(ds)
    ck(f'L{L}-full-cochain-dimension', sum(counts.values()) * 16 == 16 * L ** 4)
    ck(f'L{L}-joint-commutant-dimension', d_joint == {2: 392, 3: 10320}[L])
    ck(f'L{L}-square-commutant-dimension', d_square == {2: 768, 3: 20624}[L])
    print(f'L={L}: n={counts}, t={fixed3}, Comm(D,S4)={d_joint}, Comm(D^2,S4)={d_square}')

# Fixed-site CAR centralizer hypothesis is stronger than only the gamma_r
# constraints surviving the period-two collision of U and U^{-1}.
ck('CAR-gamma-distinction', all(mm(K, gammas[r]) == mm(gammas[r], K)
                                     for r in range(4)) and mm(K, cs[0]) != mm(cs[0], K))
print(f'PASS {len(checks)}/{len(checks)} exact controls')
```

**Terminal verdict: ARCHIVE-COCHAIN-JOINT-COMMUTANT-STRICTLY-LARGER-CLASSIFIED.**