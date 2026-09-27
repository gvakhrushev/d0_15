# A4D E-LIN E_sp Executable Owner

Disposition: **ELIN-ESP-EXECUTABLE-OWNER-CERTIFIED**

Primary certificate:

\`02_REGISTRY/research/certificates/a4d_elin_esp_executable_owner_check.py\`

## Scope

This packet reconstructs the accepted E-LIN Lorentz degree-two response family
from the E-LIN finite axioms only.  It does not read or fit #262/#265 carrier
data and does not use any J2 orbit for normalization.

The fixed Role order is \((0,1,2,3)\), with
\[
\eta=\operatorname{diag}(1,-1,-1,-1).
\]

All output, input, and derivative Sym² factors use the ordered basis

\[
(00,01,02,03,11,12,13,22,23,33).
\]

Thus the unrestricted coefficient tensor
\[
C[\mathrm{out},\mathrm{in},\mathrm{deriv}]
\]
has \(10^3=1000\) rational coordinates.  A derivative pair \((r,s)\) denotes
\(D_rD_s\) once, with no hidden off-diagonal multiplicity.

## Exact symmetry scaffold

The signature-preserving signed-hypercubic group is taken literally as

\[
(\mathbb Z_2)^4\rtimes S_3,
\]

where the time Role is fixed by permutations, \(S_3\) permutes Roles
\(\{1,2,3\}\), and all four independent sign reflections are allowed.  Its
order is 96.

Six generators (four reflections and two adjacent spatial transpositions)
generate all 96 elements.  The exact equivariance rows have incidence form
\(x_i-sx_j=0\), \(s=\pm1\).  Signed exact elimination gives

\[
1000 \xrightarrow{\mathrm{rank}\ 963} 37.
\]

The six-generator solve and the full 96-element solve both give raw invariant
dimension 37.

## Exact Noether constraints

Self-adjointness uses the Lorentz-induced pairing on covariant symmetric
two-tensors.  In the stored Sym² basis the component weight is

\[
w_{ab}=
\begin{cases}
\eta_a\eta_b,&a=b,\\
2\eta_a\eta_b,&a<b.
\end{cases}
\]

Gauge and divergence conventions are

\[
(K\xi)_{ab}=D_a\xi_b+D_b\xi_a,
\qquad
(\operatorname{div}E)_b=D^aE_{ab}
=\sum_a\eta_aD_aE_{ab}.
\]

After symmetry reduction to 37 variables, exact rational ranks are:

| condition | exact rank | surviving dimension |
|---|---:|---:|
| self-adjointness | 11 | 26 |
| gauge-nullity | 28 | 9 |
| divergence freedom | 28 | 9 |
| all three together | 35 | **2** |

Therefore the recorded E-LIN Lorentz statement is now executable:

\[
\dim \mathcal E_{\eta}^{(2)}=2.
\]

## E_eta membership

The certificate constructs the five-term Lorentz response directly from

\[
(A,B,C,D,F)=(1,-1,1,1,-1),
\]

using

\[
E_{ab}
=
\Box h_{ab}
-(D_av_b+D_bv_a)
+D_aD_bt
+\eta_{ab}q
-\eta_{ab}\Box t,
\]

with
\[
v_b=D^ch_{cb},\quad
t=h^c{}_c,\quad
q=D^cD^dh_{cd}.
\]

Its coefficient vector satisfies equivariance, self-adjointness, gauge
nullity, and divergence exactly.

## Deterministic E_sp owner

No orbit data select the complement.

1. Every nonzero equivariance component is represented by its smallest ambient
   coefficient index.
2. The 37 reduced variables are ordered by those representatives.
3. The combined exact constraint matrix is put in RREF.
4. Each canonical null ray is primitive-integer normalized with first nonzero
   coefficient positive.
5. Among canonical null rays independent of \(E_\eta\), the
   lexicographically smallest ray is named \(E_{sp}\).

The resulting ray is independently equal, up to the already-fixed projective
sign, to the ordinary three-dimensional Euclidean five-term response embedded
in spatial Roles \(\{1,2,3\}\).  All coefficients touching Role 0 in output,
input, or derivative slots vanish.

With the canonical sign, the first nonzero ambient coefficient is

\[
C[(11),(22),(33)]=+1.
\]

The complete nonzero coefficient ledger is:

| out | in | derivative | coefficient |
|---|---|---|---:|
| 11 | 22 | 33 | 1 |
| 11 | 23 | 23 | -2 |
| 11 | 33 | 22 | 1 |
| 12 | 12 | 33 | -1 |
| 12 | 13 | 23 | 1 |
| 12 | 23 | 13 | 1 |
| 12 | 33 | 12 | -1 |
| 13 | 12 | 23 | 1 |
| 13 | 13 | 22 | -1 |
| 13 | 22 | 13 | -1 |
| 13 | 23 | 12 | 1 |
| 22 | 11 | 33 | 1 |
| 22 | 13 | 13 | -2 |
| 22 | 33 | 11 | 1 |
| 23 | 11 | 23 | -1 |
| 23 | 12 | 13 | 1 |
| 23 | 13 | 12 | 1 |
| 23 | 23 | 11 | -1 |
| 33 | 11 | 22 | 1 |
| 33 | 12 | 12 | -2 |
| 33 | 22 | 11 | 1 |

Equivalently, for spatial indices \(i,j\in\{1,2,3\}\), the canonical owner is
the negative of the standard embedded 3D five-term normalization; its overall
sign is only the declared primitive projective convention.

## Callable symbol API

The certificate exports:

- \`esp_coefficients()\`: the immutable primitive 1000-entry \(E_{sp}\) owner;
- \`eeta_coefficients()\`: the primitive 1000-entry \(E_\eta\) owner;
- \`fourier_symbol(coeffs, p)\`: exact \(10\times10\) degree-two symbol;
- \`esp_fourier_symbol(p)\`;
- \`eeta_fourier_symbol(p)\`.

Here \(p=(p_0,p_1,p_2,p_3)\) are the exact centered-derivative symbol values
on the carrier being evaluated.  This is the executable interface required by
the downstream same-carrier comparison.

## Hostile controls

The certificate independently replays equivariance using all 96 group
elements, not only the six generators.  It also changes the first nonzero
\(E_{sp}\) coefficient by \(+1\); that one-coefficient perturbation is rejected
by the exact constraint package.

## Firewall

This owner recovery proves only the finite E-LIN operator classification and
publishes its missing complementary symbol owner.  It does not identify an
operator span with the metric-amplitude kernel of #262, does not prove a
stationary-sheet stress statement, and does not promote any Einstein/GR,
BOOK, or release claim.  The typed #265 comparison becomes executable only
after this owner lands.
