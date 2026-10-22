# Actual active-label count for the original one-boost full128 instrument

22 October 2026. Existing PR #334. This supplies the **active alphabet size**
needed by the stationary first-label occupation law. It does not change the
128-label output register or remove zero-probability columns from its unitary
completion. No new preparation, price, source, or physical admission is inferred.

The literal input is
[`check_uniform_book_source.py`](../d0_book_uniform_source_2026-10-21/check_uniform_book_source.py),
git blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`, functions `creators` and
`native`. Fix its phases `(i,i,-1,-i)`, `nu=3/5`, and proper role-1 boost
`u=exp(theta G)`, `G=c_0 c_1^*+c_1 c_0^*`. The strict Julia chart is

\[
  \nu^2\cosh(2\theta)<1.
\]

The statements below concern this one-boost Fourier family, not arbitrary
spatial fields or other phase choices. In particular both `theta=0` and `.08`
belong to it.

## 1. Labels and the exact answer

Write the original output label as

\[
 a=4\ell+2b+s,\qquad 0\leq\ell<32,\quad b,s\in\{0,1\},
\]

where `ell` is the Walsh label, `b` the coefficient port, and `s` the Golden
port. If `N_(ell,b)` denotes the literal Walsh row and `A=N_(0,0)`, then

\[
 K_{4\ell+2b}=\mathbf1_{\ell=b=0}I-2p^2N_{\ell,b}^*A,
 \qquad K_{4\ell+2b+1}=-2p\sqrt p\,N_{\ell,b}^*A.
 \tag{1}
\]

The active labels, meaning `K_a` is a nonzero operator, are exactly:

| Field | Nonzero Walsh rows | Active original labels | Count `m` |
|---|---|---|---:|
| `theta=0` | All even `ell` at `b=0`; `ell=4,6,14,22,30` at `b=1` | All `a` with `a & 6 == 0`, together with `{18,19,26,27,58,59,90,91,122,123}` | 42 |
| `theta != 0` in the strict chart | Both `b` for every even `ell` | Exactly `a & 4 == 0` | 64 |

The complete original carrier remains 128-dimensional in either row.

## 2. Why no other labels occur

Every original word is duplicated. The least significant Walsh bit therefore
cancels each duplicate pair when `ell` is odd. Both `N_(ell,b)` vanish then,
including in the moving field. This proves the 64 identically zero output
columns throughout this family without a tolerance or spectrum test.

For even `ell`, put `epsilon_1=(-1)^bit_1(ell)`,
`epsilon_2=(-1)^bit_2(ell)`, and let `chi_r` be the Walsh character of the
two role bits. At `theta=0`, the coefficient-zero row is

\[
 N_{\ell,0}=\frac{\nu}{16}\sum_{r=0}^3\chi_r
  \big[(z_r-\epsilon_2)c_r
       +\epsilon_1(\bar z_r-\epsilon_2)c_r^*\big].
 \tag{2}
\]

The role-3 coefficient, `z_3=-i`, never vanishes for either `epsilon_2`.
Creators and annihilators are linearly independent. Consequently all 16
even-`ell` coefficient-zero rows are nonzero. This argument also works at
nonzero boost: role 3 is unchanged, and role-1 terms act only on modes 0,1.

Set `n_r=c_r c_r^*` and `b_0=sqrt(1-nu^2)=4/5`. The flat defect roots obey

\[
 L_r=I+(b_0-1)n_r,\qquad
 R_r=b_0I+(1-b_0)n_r,
\]

and hence

\[
 N_{\ell,1}=\frac{1-\epsilon_2}{16}
                 \sum_r\chi_r(L_r+\epsilon_1R_r).
 \tag{3}
\]

If `epsilon_2=1`, this is zero. If `epsilon_2=-1, epsilon_1=1`, use
`L_r+R_r=(1+b_0)I`: only the constant role character survives, giving
`ell=4`. If `epsilon_2=epsilon_1=-1`, use
`L_r-R_r=(1-b_0)(I-2n_r)`: all four role characters are nonzero because
`I,n_0,n_1,n_2,n_3` are linearly independent. These are precisely
`ell=6,14,22,30`. Thus there are 21 nonzero flat Walsh rows.

## 3. The eleven newly active rows at nonzero boost

Let `c=cosh(theta)`, `s=sinh(theta)`, and `C=c^2+s^2=cosh(2theta)`.
Restrict to the two boosted CAR modes in their standard Fock order. The
boosted right defect on the single-particle block is

\[
 R(x_1)\big|_{\{|10\rangle,|01\rangle\}}
   =I_2+\frac{\sqrt{1-\nu^2C}-1}{C}
       \begin{pmatrix}c^2&cs\\cs&s^2\end{pmatrix}.
 \tag{4}
\]

The global CAR ordering changes possible matrix-entry signs, not the
nonvanishing of this block. The corresponding boosted left defect is
diagonal in the occupation basis, as are all unboosted defects. Therefore
the only contribution to this offdiagonal in each even-`ell` row
`N_(ell,1)` is

\[
 \frac{\chi_1\epsilon_1}{16}\,
 \frac{\sqrt{1-\nu^2C}-1}{C}\,cs.\tag{5}
\]

For nonzero real `theta` on the strict chart, every factor except the sign
is nonzero: `cs != 0`, `C>0`, and `0<sqrt(1-nu^2 C)<1`.
Thus **every** even-`ell` coefficient-one row is nonzero. Exactly eleven
previously zero rows appear, giving 32 nonzero Walsh rows.

For a purely rational check of the scalar premises, at `s=3/4,c=5/4`
one has `C=17/8`, `nu^2 C=153/200<1` and the offdiagonal is
`(15/34)(sqrt(47/200)-1) != 0`. No numerical radical comparison is needed.

## 4. Passing from Walsh rows to active Kraus labels

Here `A=A^*` and it is invertible. One direct bound in the same family is
obtained with Majoranas `gamma_r=c_r+c_r^*`, `eta_r=i(c_r-c_r^*)`:

\[
 \frac{16A}{\nu}=L+S,\qquad
 L=-\gamma_0+\eta_0-\gamma_1+\eta_1
      +(\cosh\theta-1)n_0\eta_1-\sinh\theta\,n_1\eta_0,
 \quad S=-2\gamma_2-\gamma_3-\eta_3.
\]

The two summands are odd on disjoint CAR mode sets, so `{L,S}=0`, while
`S^2=6I`. Hence

\[
 A^2=\frac{\nu^2}{256}(L^2+6I)
       \succeq\frac{3\nu^2}{128}I\succ0.\tag{6}
\]

Thus `N^*A=0` iff `N=0`. Each nonzero row gives two nonzero outputs in
(1). For the exceptional blank output, row contractivity gives
`B=I-2p^2 A^2 >= (1-2p^2)I > 0`, so it too is nonzero. This proves the
counts 42 and 64 without assuming generic rank.

The existing preparation result is consumed, not recomputed:
[`d0_native_preparation_closure/PROOF.md`](../d0_native_preparation_closure_2026-10-21/PROOF.md)
§§1–4 gives the actual original channel, its faithful inverse-square
stationary state, the fixture's recycling bound, and the moving preparation
jet. In the present normalization `H=A^2`, its density is
`rho_*=H^(-1)/Tr(H^(-1))`. The full-stencil notation there is
`H=(h^2/256)Delta`, so the scalar normalization cancels. For this faithful
density, `Pr(a)>0` iff `K_a != 0`; the present operator alphabet is exactly
the stationary probability support needed by the occupation law.

## 5. The support jump and its precise use

When the stationary first-label occupation law's recurrence hypotheses
hold, its uncapped mean trial factor is `m+1`: this supplies **43 at flat
field and 65 on the nonzero one-boost chart**, not 129. The freshly active
probabilities tend to zero as `theta -> 0`, while their conditional mean
return times diverge. Their limiting occupation contributions must not be
discarded before removing the cap. Finite-cap probabilities and prices are
smooth; the uncapped active-count formula has a nonuniform limit at the
support-changing point.

Consequently `dm=0` may be used on either fixed-support chart only. It is
not a derivative through `theta=0`, and it does not justify freezing the
moving invariant preparation. All first-label comparison work, complete
labels, clock, and oldRIGHT remain in the original execution. A scalar
count identity does not select its physical preparation or complete price.

[`check_native_label_support.py`](check_native_label_support.py) checks the
Walsh coefficients and alphabet lists with integer/Fraction arithmetic.
It then reads only the unchanged constructor definitions and confirms the
formula-predicted column sets at exactly `theta=0,.08`, `nu=.6`. The latter
checks are floating-point diagnostics; the support theorem is (2)–(6).
No stationary-state, geometry, or old source suite is executed.
