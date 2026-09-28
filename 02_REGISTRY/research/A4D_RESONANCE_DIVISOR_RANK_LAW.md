# A4D resonance divisor: the phase-count nullity rule is false

**Status:** `A4D_PHASE_COUNT_NULLITY_LAW_REFUTED_ON_FULL_TORUS`
**Certificate:** [`certificates/a4d_resonance_divisor_counterexample_check.py`](certificates/a4d_resonance_divisor_counterexample_check.py)

The exact character Hessian is generically full rank: at
\(Z=(1,1,1,1)\), \(\operatorname{rank}A=24\). At
\[
Z=(-1,-1,i,i),
\]
exact elimination over \(\mathbb Q(i)\) gives
\[
\operatorname{rank}A=22,\qquad \operatorname{nullity}A=2.
\]
Here \(n_{+i}=2\) and \(n_{-i}=0\), so the proposed rule
\(\operatorname{nullity}=2\max(n_{+i},n_{-i})\) predicts 4. This is an
exact counterexample on the full character torus.

The determinant is nonzero at the generic point above and zero at this
rank-22 point. Since its entries are Laurent polynomials in the nonzero
characters, its zero set is a nonempty proper hypersurface in the torus; the
rank strata inside that divisor still require separate classification. This
counterexample belongs to \(\{1,-1,i,-i\}^4\), so the rule also fails on
that finite subset.

The supplied continuous-phase scan also reported rank 21 at the point written
as \(i e^{\pm 2\pi i/3}\) in two coordinates. Exact reduction to
\((-\sqrt3/2-i/2,\sqrt3/2-i/2,i,i)\) gives rank 20 over
\(\mathbb Q(i,\sqrt3)\); the rank-21 reading from unevaluated roots of unity
is not used here.

The earlier diagonal identity
\[
\det A(z,z,z,z)=\frac{(z^2+1)^{12}}{16z^{12}}
\]
remains compatible with this conclusion. It identifies a multiplicity-12
intersection with the diagonal curve, not the full multivariable divisor or
its rank stratification.
