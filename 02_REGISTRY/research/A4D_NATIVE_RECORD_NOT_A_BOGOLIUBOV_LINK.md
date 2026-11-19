# The literal full CAR record is not a one-particle-hole link

**Exact scoped obstruction, 16 October 2026.** On the actual first return of
the owned autonomous whole-blank seed, the sixteen-dimensional record operator
does not act linearly on the eight creation/annihilation modes. A standard
fermionic Bogoliubov transformation, and hence the usual CAR/Spin lift of a
linear frame map, cannot supply the native link (D) for this gate.

This closes one short proposed bridge from the CAR record to a four-dimensional
link. It does not exclude an independently owned (D), a nonlinear joint
law on ((q,D,b,m)), or every possible map from a full native state to a
coframe. The separate link/action/variation and physical-admission obligations
remain open.

## Exact witness

Let (c_i) be exterior multiplication by the (i)-th basis vector on

\[
\Lambda^*\mathbb R^4\cong\mathbb R^{16},\qquad
\mathcal L=\operatorname{span}\{c_0,c_1,c_2,c_3,c_0^T,c_1^T,c_2^T,c_3^T\}.
\]

For any unitary implementation of a linear particle-hole change of CAR modes,
conjugation preserves \(\mathcal L\). The seed in the owned closed engine has
occupation masks 1 and 15, i.e. (e_0+\Omega), with all sixteen state slots
retained. Its first-grade role-0 coordinate is positive, so its actual first
autonomous return uses the literal full record (U_0=\operatorname{record}(I,e_0)).
The checker verifies that this is exactly the engine's first transition and
that (U_0^T U_0=I_{16}).

Flatten each (16\times16) operator row-major. Exact elimination over
\(\mathbb Q[a,p]/(a^2-p,\ p^2+p-1)\) gives

\[
\operatorname{rank}\mathcal L=8,\qquad
\operatorname{rank}\bigl(\mathcal L\cup\{U_0c_0U_0^T\}\bigr)=9.
\]

One certifying (9\times9) minor uses zero-based flattened rows
\((0,1,2,4,8,16,32,64,128)\) and has determinant
\[
-ap\ne0,
\]
since the owned positive roots satisfy (a>0) and (p>0). Thus
\(U_0c_0U_0^T\notin\mathcal L\). This is a direct finite witness, not an
inference from grade-mixing alone.

## Boundary and next implication

The result rules out extracting the link by saying that the record is the
ordinary exterior lift of a base transformation, or by enlarging that proposal
to a standard Bogoliubov map of the four CAR modes. It does not prevent the
kernel from owning a separate link variable whose evolution is jointly
constrained with (q,b,m). Such a law must still be supplied with its action,
allowed variations, refinement map, and full source/price; this certificate
adds none of them and introduces no selector.

The exact checker and receipt are
[`a4d_native_record_non_gaussian_link_check.py`](certificates/a4d_native_record_non_gaussian_link_check.py)
and
[`a4d_native_record_non_gaussian_link_results.json`](certificates/a4d_native_record_non_gaussian_link_results.json).
The receipt pins the consumed chronology, closed-engine, and CAR owners.
Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_record_non_gaussian_link_check.py
```

The calculation is exact Python/SymPy and has no new Lean declaration. A Lean
owner for the (9\times9) minor remains a formalization task; the mathematical
scope is only the stated CAR-mode lift obstruction.
