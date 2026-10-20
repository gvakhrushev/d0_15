# Independent review: actual paid-source connection jet

Reviewer: `native_price_bridge`, 2026-10-20.

**ACCEPTED in the precise scope below.** The initial coframe/LC mismatch
was a substantive blocker. The frozen revision corrects it and recalculates
the affected source and geometric contraction. There is no remaining
mathematical blocker to the stated finite Fourier coefficient result.
This acceptance is not a complete-action identification or a D0-to-GR
closure certificate.

## 1. Frozen objects reviewed

| Object | SHA256 |
|---|---|
| `/tmp/d0_sourced_connection_proof.md` | `b782f919536002c0099b5286290fcde7b2b2b819e9a185bb118a7f92b206dea3` |
| `/tmp/d0_sourced_connection_probe.py` | `138e8f952b2f59af6ae600691295b6e34ec58200d83b899d0b93ba7dd96c9c48` |
| `/tmp/d0_sourced_connection_probe.json` | `c0385b4d59e97e0fe259a9b459452605f3d3dcf7c867c643c87885152f9d7178` |
| `/tmp/d0_sourced_connection_inputs.json` | `e221d5c739accc81d3c6e9919ee748f77a3001ffd45445a369cb832c3fd74e38` |

I verified all seven literal checker input pins against the original files
in `/workspace/scratch/b5496e41e653/d0_15_native_integration`. These include
the original complete-record owner, original native price and smooth
operator implementation, positive-adjoint owner, actual coframe source
map, and coframe oracle transport. The historical input files were read,
not rewritten. The saved main-checker result reports `PASS`, 51 checks.
The author reports its execution under `-O -B -W error`; I inspected the
explicit exception checks and read the frozen output, without rerunning
that full CAR calculation or any historical suite.

## 2. Identity with the original paid observable

The calculation uses the original complete instrument's recycled data
channel, not a different outcome law. Its observable is

\[
\Gamma_h=\operatorname{Tr}\rho_8\mathcal L_h^*\Delta_h,
\quad \Delta_h=D_h^2,\quad
\mathcal L_h^*\Delta_h=D_h\mathcal T_h(\Delta_h)D_h-\Delta_h^2.
\]

The complete expected paid-port cost has the exact initial-clock term
\(p(\beta^2-\beta\epsilon)\Gamma_h/2\); at two rounds its coefficient is
\(p\epsilon^2\). Thus the object is an independently owned component of
the actual costs 1 and 2. The baseline and the leading R term have not
been proved absent or source-free in the complete problem. No pointer
Shannon entropy has been substituted for Book Info.

For selfadjoint D, the squared-norm expression used by the checker is
exactly the trace above:
\((1/8)\sum_W\|DWD\psi\|^2-\|D^2\psi\|^2\). The continuum factor 1/8
comes from both original shifted and unshifted Julia families, with
all four factors retained for every role. The derivation and implementation
differentiate the actual coframe factors and positive defect roots.

I inspected the compact quadratic expression term by term. Its order-two
zero-mode terms and the two first-order sidebands are the terms of that
literal norm expression. The mixed coframe/connection D2 term has no
zero-mode contribution, and the independent forward-jet route retains it
before taking the trace. This supports the full symbolic 24-variable
coefficient, rather than inferring it from the old one-link slice alone.

## 3. The corrected native-to-geometric binding

With the declared null metric and the actual positive spatial native
legs, the owned map \(V=\eta e^{-T}\) forces

\[
e^+=du/\nu,\quad e^-=(dv+Hdu/2)/\nu,
\quad e^x=-dx/\nu,\quad e^y=-dy/\nu.
\]

Its actual Cartan-torsion-free connection is
\(\omega_u=-H'N_x/2\), so \(\ell_1=-1/2\).
The old positive-sign link has nonzero torsion for these same legs.
The revision correctly preserves the old literal Gamma(H,K) calculations
while correcting their LC interpretation. It must not relabel the old
numerical output as a check of this corrected LC family.

I independently contracted the scalar curvature with the actual inverse
coframe. This gives

\[
(H_G)_{6r+j,6s+l}=2s_rs_s([G_j,G_l]\eta)_{rs},
\quad s=(1,1,-1,-1),
\]

with \(\det H_G=2^{32}\), \((b_G)_9=-1/2\), and
\(b_G=-H_G\ell/2\). All Cartan torsion components vanish at the corrected
LC sign. The true volume factor is \(\nu^{-4}\), the scalar-curvature
factor is \(\nu^2\), and therefore the actual quadratic action coefficient
is \(\alpha a^2/(4\nu^2)\). The revision's
\(g=\alpha/(2\nu^2)\) is correct; there is no implicit replacement by
the native-leg scale \(\nu^2\).

The observer \(n=(e_++e_-)/\sqrt2\) has positive one-particle Gram I;
its exterior Gram is consequently I as well. Ordinary matrix transposes
are the correct positive adjoints on this fixed observer chart. They
are not inverse Lorentz matrices. The six generators \(G_j=\eta F_j\)
span the Lorentz algebra and the four role slots give all 24 independent
connection directions in the stated Fourier jet.

## 4. Accepted source and conditional stationary contraction

At the corrected LC point the actual coefficient and connection covector
are

\[
\gamma(\ell)=81/100000,\qquad
j_1=-729/500000,\quad j_9=-81/500000,
\]

with the other 22 components zero. The connection coefficient covector
is an order-a-squared derivative with respect to t; differentiation with
respect to the physical connection amplitude B=at is order a, as stated
in the proof.

The source-connected geometric block and native Hessian are

\[
A=\begin{pmatrix}0&-2\\-2&0\end{pmatrix},\qquad
N=\operatorname{diag}(729,-2349)/125000.
\]

The full geometric contraction is
\(j^TH_G^{-1}j=-59049/250000000000\), whereas keeping only j1 would give
zero. The full connection extension therefore changes a genuine physical
source calculation, not merely its notation.

I independently solved the corrected driven block and checked the
stationary combined value against the frozen result:

\[
F(\zeta)=
\frac{81(531441\zeta^2+3645000\zeta+25000000000)}
{40000(1712421\zeta^2+62500000000)} > 1/2000
\quad(\zeta\in\mathbb R).
\]

The numerator and denominator discriminants of F-1/2000 are strictly
negative, with positive leading coefficients. The exported blocks cover
all 24 indices. The main checker verifies all 24 stationary equations,
including the unforced rows; it does not drop those rows merely because
the source is supported on two components. The sufficient whole-matrix
invertibility range is the stated \(|\zeta|<6250/81\); outside it the
reported particular solution does not assert uniqueness.

This F is the combined geometric-plus-paid stationary value divided by
the paid coefficient. It is not Gamma alone at the corrected connection.
Its geometric quadratic is indefinite, so this is auxiliary stationarity,
not a minimum over connection variables or physical histories. The use of
\(\zeta=c/[\alpha/(2\nu^2)]\) is conditional on an actual same-programme
action and normalization identification. The result does not provide that
identification, a selected physical ratio, or a complete Book action.

## 5. Finite-jet transfer and exact scope limits

The finite-to-continuum argument in proof §3.1 is valid in its declared
scope. At amplitude degree at most two, the actual C/Lambda(U)/shift
products have only finitely many transverse sidebands. The fixed Fourier
difference quotients converge O(h), and the strictly positive defect-root
margin bounds the relevant Sylvester inverses uniformly. The original
shifted right-defect conventions and positive backward adjoints are
retained. Normalized discrete Fourier orthogonality agrees with the
continuum average once the finite retained sidebands are resolved.

It follows coefficientwise, and uniformly on bounded t sets, that
\(\gamma_h\), its 24-component gradient, and its quadratic Hessian
converge to the displayed continuum jet. This is a finite-jet statement.
It does not control arbitrary high Fourier modes, an infinite history
sum, an h-dependent unbounded connection amplitude, or a fixed positive
clock with n(h) proportional to h^-2.

The retained CAR carrier is full16, but the chosen input density is the
fixed rank8 protected block in one u-momentum sector. Full128 names the
complete original outcomes, not a solved rank128 oldRIGHT preparation.
The new opposite-null perturbation is not assumed to preserve that
preparation eigenspace or solve its Euler equation. The observer is fixed
on this chart. Neither full observer nor preparation elimination is
provided by this calculation.

These are the existing positive-adjoint full-Lorentz matrix-instrument
variables. The finite-jet argument does not itself supply primitive
actuation or complete work cost for that interface. Nonzero independent
Holst coupling, the full matter action and stress, all coframe equations,
uniform positive-clock propagation, and the final D0-to-GR composition
remain outside the accepted statement. The Ward/stress discussion in
the proof is appropriately conditional and does not infer all Einstein
equations from this pp amplitude.

## 6. Independent targeted evidence preserved for the packet

No Lean build or old numerical suite was run during this review. I ran
only the small checks addressing the discovered coframe issue and its
changed stationary coefficient.

| Independent object | SHA256 | Result |
|---|---|---|
| `/tmp/d0_native_paid_port_cost/check_connection_coframe_review.py` | `5a9b815788f0caa1d793685ef54e0a07dd34d48c19a06a0af9899b6fc86861ce` | Exact independent coframe/scalar contraction script |
| `/tmp/d0_native_paid_port_cost/CONNECTION_COFRAME_REVIEW_RESULT.json` | `7cf980c756e89cebeb0dfa2dbc6ed2584b8ec6888f69e50f0b304475579307e6` | PASS, 23 checks, approximately 0.31 s |
| `/tmp/d0_native_paid_port_cost/CONNECTION_REDUCED_REVIEW_RESULT.json` | `f34ae16b49014edc2040411be087e51bb0f8cebe2ae28213abec79d88fe0ad5f` | Exact corrected two-component elimination and strict bound, approximately 0.25 s |

The first script is standalone apart from SymPy and needs no repository
imports. Its saved output can be reproduced with `python3 -Werror` in the
declared dependency environment. The reduced check consumes the reviewed
native coefficient entries; it is not claimed as an independent CAR
derivation of every native Hessian entry.
