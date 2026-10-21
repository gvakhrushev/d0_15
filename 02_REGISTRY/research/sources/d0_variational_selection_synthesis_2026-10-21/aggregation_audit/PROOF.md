# A genuine native tangent with nonzero complete measured entropy source

21 October 2026. Bounded follow-up in existing PR #334. This separate
audit repairs an inadmissible conditional-pair witness; it does not change
the packet's earlier proofs, receipts or integration manifest.

**Statement.** In the literal original 128-outcome instrument at `theta=0`,
fixed phases `(i,i,-1,-i)` and fixed DATA density `I16/16`, the Shannon
entropy of the complete one-round measured pointer record satisfies

\[
\boxed{\frac{dH_\varphi^{128}}{d\nu}>0
\quad\text{for every }0<\nu<\sqrt3/2.}                    \tag{1}
\]

This is a tangent of the actual supplied operator family, including its
moving Julia defects. It is not a proof that a compulsory physical
controller admits this variation or prepares its Fourier input.

## 1. Original source, fixed input and literal labels

The frozen [native constructor](../inputs/02_REGISTRY/research/sources/d0_native_preparation_closure_2026-10-21/inputs/native_input.py)
has Git blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`.
The frozen [complete-record owner](../inputs/02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md)
has blob `df8611c7fa37fa71e883831b3f01f434532d99ce`; its conditional
Golden-pair identity is retained without changing `p=phi^-1`.

Keep all16 CAR grades of this invariant Fourier block and oldRIGHT128.
Fix the normalized purification `C0` with entries
`C0[j,j]=1/4`, `0<=j<16`, and all other entries zero, so
`C0 C0*=I16/16`. Its 16 active Schmidt columns sit inside the original
128 reference columns. Neither the input nor its whole RIGHT Gram varies
with `nu`. This is not the full spatial DATA128 preparation.

In the constructor, `m=0,...,31` is the Walsh label, `c=0,1` is its
coefficient component, and `j=2m+c` labels its 64 rows `N_j`.
The 128 final labels have array index `2j+b`, `b=0,1`. With

\[
A=N_0=\frac\nu{16}\sum_r
 [c_r(\zeta_r-1)+c_r^*(\bar\zeta_r-1)],\qquad
\lambda=\frac{5\nu^2}{128},\qquad A^2=\lambda I_{16},
\]

the literal matrices are

\[
K_{0j}=\delta_{j0}I-2p^2N_j^*A,\qquad
K_{1j}=-2p\sqrt p\,N_j^*A.                              \tag{2}
\]

The CAR identity for `A^2` uses
`sum_r |zeta_r-1|^2=10`. No marginal Kraus recombination, extra coin,
POVM replacement or changed Golden probability is used.

## 2. Exact Walsh-row norms and all 128 probabilities

Put `b_nu=sqrt(1-nu^2)` and `t_j=Tr(N_j N_j*)/16`.
The repeated raw words make every odd Walsh label vanish. For `m=2s`,
the creation row is `j=4s`, `0<=s<16`. Its squared norm is

\[
t_{4s}=\frac{\nu^2}{256}\sum_r|\zeta_r-\epsilon_s|^2,
\qquad \epsilon_s=(-1)^{\text{bit}_1(s)}.
\]

The two sums are 10 and 6. The defect rows follow from the actual roots
`L_r=I-(1-b_nu)n_r`, `R_r=I-(1-b_nu)(I-n_r)`:
`N_9=(1+b_nu)I/2`; at `j=13,29,45,61` they are
`(1-b_nu) sum_r chi_r(I-2n_r)/8` with the four Walsh sign rows.
The occupation involutions have normalized trace pairing `delta_rs`.
Consequently the exact table is

| Literal row indices | Count | `t_j` |
| --- | ---: | --- |
| `0` | 1 | `lambda` |
| `4s`, `s in {1,4,5,8,9,12,13}` | 7 | `lambda` |
| `4s`, `s in {2,3,6,7,10,11,14,15}` | 8 | `3nu^2/128` |
| `9` | 1 | `(1+b_nu)^2/4` |
| `13,29,45,61` | 4 | `(1-b_nu)^2/16` |
| All other rows | 43 | `0` |

The sum is `nu^2/2+(1+b_nu^2)/2=1`. At the fixed input in §1,
cyclicity and `A^2=lambda I` give the exact measured probabilities

\[
\begin{aligned}
q_{00}&=(1-2p^2\lambda)^2, &q_{10}&=4p^3\lambda^2,\\
q_{0j}&=4p^4\lambda t_j, &q_{1j}&=4p^3\lambda t_j
&& (j\ne0).                                             \tag{3}
\end{aligned}
\]

Their sum is one. All21 listed rows yield two positive outcomes for
`0<nu<1`: 42 positive measured labels, including the ordinary blank and
the port-one `j=0` orphan. The other86 labels are identically dark and
remain part of the instrument, with the usual `0 log 0=0` convention.
Nothing is conditioned on a successful or nonblank event.

For example a compact exact entropy formula uses
`eta(x)=-x log_phi x`, `r=4p^2 lambda(1-lambda)`,
`t=3nu^2/128`, `T=(1+b_nu)^2/4`, `S=(1-b_nu)^2/16`:

\[
\begin{split}
H_\varphi^{128}={}&\eta(q_{00})+\eta(q_{10})
 +7\eta(4p^2\lambda^2)+8\eta(4p^2\lambda t)\\
&+\eta(4p^2\lambda T)+4\eta(4p^2\lambda S)+(2-p)r.
                                                               \tag{4}
\end{split}
\]

The last term retains the fixed Golden entropy within every ordinary
pair. Equation (4) is the entropy of every measured label, not a binary
coarse graining and not coherent-record von Neumann entropy. OldRIGHT
remains retained; adjoining its conditional quantum entropy defines a
different valuation from this complete pointer-record entropy.

## 3. Strict sign on an explicit finite interval

For `0<nu<sqrt(3)/2`, every positive outcome other than the ordinary
blank has strictly positive derivative. For the first two creation-row
classes and the orphan this follows from their positive `nu^4` factors.
For the large defect row,

\[
\frac{d}{d\nu}\log[\nu^2(1+b_\nu)^2]
=\frac{2(2b_\nu-1)}{\nu b_\nu}>0.
\]

For the four small defect rows, both positive factors in
`nu^2(1-b_nu)^2` strictly increase. The constant Golden multipliers in
(3) preserve all these signs. The dark outcomes and their derivatives
are identically zero on the entire interval.

Moreover, throughout `0<nu<1`, `p^2<1` gives

\[
q_{00}>(59/64)^2>1/2.
\]

Each other probability is less than `1-q00<q00`. Differentiating the
complete normalized entropy and using the total derivative zero gives
the exact source formula

\[
\boxed{\frac{dH_\varphi^{128}}{d\nu}
=\sum_{\alpha\ne(0,0):q_\alpha>0}
 q_\alpha'\log_\varphi(q_{00}/q_\alpha)>0.}              \tag{5}
\]

Thus `nu=1/2` is a strict finite witness on the actual operator family,
without taking a limit or estimating a tiny eigenvalue. As a consistency
check the small-`nu` expansion is

\[
H_\varphi^{128}
=\frac{5p^2}{32\log\varphi}\nu^2\log(1/\nu^2)+O(\nu^2).
\]

The independently priced port-one mean is still exactly
`4p^3 lambda=5p^3 nu^2/32`; it has not been replaced by the entropy.

## 4. The rejected conditional-pair direction

For every ordinary positive row `j!=0`, (2) says
`K_(0j)=p L_j`, `K_(1j)=sqrt(p) L_j`. Therefore

\[
q(b=0\mid j)=p^2,\qquad q(b=1\mid j)=p,
\qquad \frac d{d\nu}q(b\mid j)=(0,0).                  \tag{6}
\]

The trial direction `(-1,+1)` preserves the sum of a hypothetical pair
but violates the actual constraint `q(0|j)-p q(1|j)=0`: its derivative
would be `-(1+p)!=0`. It is not an admitted tangent of these original
conditional pairs at fixed Golden `p`. The genuine nonzero source (5)
comes from moving complete-label weights and the actual Julia defects,
not from pretending that (6) varies.

## 5. Bounded verification and conclusion

`check_native_entropy_tangent.py` defaults to the frozen `../inputs`,
checks both source blob hashes, imports only the original constructor,
and compares (3) at the literal128 indices with its actual output on the
fixed 16-by128 purification. It recovers each `N_j` from the actual
`K_(1j)` and invertible `A`, checking the complete21/43 row table. It
also checks the entropy derivative against a five-point difference of
the full native pointer entropy and rejects the fictitious conditional
pair tangent. The constructor's returned jet is a theta derivative;
it is deliberately not misused as a nu derivative.

The all-interval sign is proved analytically in §3. The bounded numerical
replay is an implementation check, not a replacement for that proof.
No histories beyond one round, input optimization, geometry/Lean suite
or physical apparatus are replayed. This repairs a witness on the actual
supplied operator family. It neither identifies Shannon entropy with
compulsory Book03 Info nor proves a whole-D0-model impossibility or
physical controller/writer admission. `GR_closed=false`.
