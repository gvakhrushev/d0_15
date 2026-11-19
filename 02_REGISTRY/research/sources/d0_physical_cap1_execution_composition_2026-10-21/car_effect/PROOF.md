# The two-step CAR feedback is not the cap-one query effect

21 October 2026. A narrow, exact comparison inside the existing #334
cap-one execution composition. The source snapshot is
`92c00ccbf39e6e21e4383f7a7b573ab7c7c6f1be`. This tests one concrete
candidate for the missing common field-to-CAR-to-report map; it adds no
operation, readout, price rule or physical admission premise.

## Exact spectral comparison over the full CAR observer-angle interval

The N=1 query proof defines the two-dimensional retained leakage effect
`F_query = I - W^T W`, where `W=P^T U_* P` is the original full-8D query
compressed to retained positions 0 and 2. At the flat value, direct exact
matrix multiplication gives

\[
F_{\rm query}=\begin{pmatrix}76p-46&68p-42\\68p-42&76p-46\end{pmatrix},
\qquad
F_{\rm query}(1,\pm1)^T=M_\pm(1,\pm1)^T,
\]

with
\[
L=M_-=4p^3,\qquad M_+=M=4p^3(1+p^6),\qquad p=(\sqrt5-1)/2.
\]
Thus `spec(F_query)={L,M}` and
\[
M-L=4p^9>0.
\]
The adjacent cap-one checker reconstructs the original 8D unitary and
verifies both full effect eigenvector equations, not only their Rayleigh
quotients.

The existing chronological CAR process has
\[
K=U_{n_+}U_n,\qquad F_{\rm CAR}=P_nK^T(I-P_n)KP_n,
\]
with all sixteen real exterior components and the original fixed readout
retained. Write `c=n^T G n_+ in [-1,1]`. The source-owned full-pencil
formula in `A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md`, equation (8), and
`0 <= F_CAR <= I` give the complete spectrum by blocks:

- `ell(c)` with multiplicity two;
- the two roots of `x^2-t(c)x+d(c)`, each with multiplicity two;
- the two roots of `x^2-t0(c)x+d0(c)`;
- eight zero eigenvalues.

For the first block and the repeated quadratic block, the exact identities
\[
L-\ell(c)=p^2(1-c)\{1+p^3(2+c)\}\geq0,
\qquad L-t(c)=2p^5(1-c^2)\geq0
\]
show that their eigenvalues are at most `L`: the quadratic-block roots are
nonnegative and their sum is `t(c)`. Both bounds are strict for
`-1<c<1`.

It remains to bound the trace `t0(c)`. Set `s=(c+1)/2`; the degree-four
Bernstein coefficients of `2L-t0(2s-1)` on `[0,1]` are
\[
\left(0,-45+21\sqrt5,-4+\tfrac83\sqrt5,-21+9\sqrt5,-16+8\sqrt5\right).
\]
Splitting at `s=1/2` by de Casteljau gives left and right coefficient lists
\[
\left(0,\tfrac{-45+21\sqrt5}{2},\tfrac{-141+67\sqrt5}{6},
-21+10\sqrt5,-19+9\sqrt5\right),
\]
\[
\left(-19+9\sqrt5,-17+8\sqrt5,\tfrac{-93+43\sqrt5}{6},
\tfrac{-37+17\sqrt5}{2},-16+8\sqrt5\right).
\]
In the two subdivided control lists, every entry except the left endpoint
zero is strictly positive, as follows by squaring its positive radical
term. The unsplit list has a negative interior control
`-21+9*sqrt(5)`, so the subdivision is needed for this certificate. Each
half's Bernstein basis is nonnegative; together the two halves prove
`2L-t0(c)>0` for `-1<c<=1`, with equality only at `c=-1`.

At `c=-1`, direct substitution gives `ell=0`, `t=L`, `d=0`, `t0=2L`,
`d0=L^2`; at `c=1`, it gives `ell=L`, `t=L`, `d=t0=d0=0`. Hence the
largest CAR eigenvalue is `L` at both endpoints. For `-1<c<1`, the first
and repeated quadratic blocks lie strictly below `L`. If the remaining
quadratic block has an eigenvalue at least `M>L`, its other eigenvalue is
strictly below `L`, since their sum `t0(c)` is strictly below `2L`. Thus,
for every observer angle, either `lambda_max(F_CAR)<M`, or its second
largest eigenvalue is strictly below `L`.

Cauchy interlacing says that if the eigenvalues of `F_CAR` and
`J^T F_CAR J` are listed from largest to smallest as `lambda_i` and `mu_i`,
then `mu_i<=lambda_i` for `i=1,2`. Matching the target requires
`mu_1=M>L` and `mu_2=L`. The first condition forces `lambda_1>=M`, and the
all-angle bound above then gives `lambda_2<L`, contradicting `mu_2<=lambda_2`.
Therefore **no direct same-event, same-fugacity isometric compression of
the existing two-step CAR effect can produce the cap-one two-band effect at
any observer angle**. This exact value obstruction precedes first-jet and
price comparisons. It remains conditional on this effect map and does not
exclude distinct moving encoders/decoders, leakage, heralded programmes or
additional paid stages.

At the aligned-observer point `c=1`, the raw determinant factors also
differ. The cap-one two-band factor is `(1-zM)(1-zL)`; the chronological
CAR factor is `(1-zL)^4`. For the registered `z=2^-20`,
\[
(1-zM)-(1-zL)^3
=z\{L(2-p^6)-3zL^2+z^2L^3\}>0.
\]
Indeed `1/2<p<5/8`, hence `1/2<L<125/128<1` and `p^6<1`; the brace is
greater than `1/2-3/2^20>0`. This compares these two raw determinant
pencils only. The CAR owner's `-log det` chronology price and the cap-one
complete CQ `Cost-Info` are different functionals; no equality or physical
valuation conclusion is inferred from this factor comparison.

## Scope

This rules out only a direct isometric compression of the existing
chronological CAR leakage effect to the cap-one two-dimensional leakage
effect with the same event and fugacity. It does not exclude moving distinct
encoder/decoder maps, a genuinely leaky or heralded programme, different
effects, extra paid stages, a derived probability rescaling, or another
common-carrier construction. Such a route still must reproduce the original
42 query directions, account for its complete absolute Book03 price and
all independent input equations on one admitted execution. No physical
admission, native selector or GR closure follows; `GR_closed=false`.

## Replay

Run `check_same_effect_spectrum.py` from the repository root under Python
3.10 or later with SymPy installed. It checks the source pins, replays the
cap-one query checker, reconstructs the two-dimensional effect, verifies
the full-angle block bounds and Bernstein trace certificate, checks both
endpoints, and reduces the aligned `c=1` determinant identity.
The pre-existing 469-control CAR chronology receipt is consumed with its
source and proof hashes; the full historical checker is not rewritten or
silently regenerated by this application. A direct rerun of that historical
checker against the current aggregate tree stops at its transitive input-hash
guard: `A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md` has a later append-only
extension than the hash in that receipt. It does not reach or fail the CAR
mathematical controls. This application therefore keeps the historical
receipt immutable. The all-angle result uses the pinned full-pencil blocks;
the aligned-observer replay is retained only for the separate raw-determinant
comparison.
