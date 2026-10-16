# The existing full matter state records one equal-endpoint path distinction

**Exact finite memory witness, 16 October 2026.** The affine shift endpoint
for the two paths `0 then 1` and `1 then 0` is the same, but the actual
sixteen-component matter vector obtained by applying the corresponding CAR
returns to the existing whole-blank seed is different. Thus the existing
matter carrier can hold this order bit without adding a register.

The transition that chooses a return from an affine edge has not been
physically admitted by D0. This is a pairwise kinematic/action witness, not
an all-history encoding theorem, refinement law, source, or GR result.

## Exact calculation

The actual seed in the closed record engine is
\[
m_*=e_0+\Omega,
\]
with all sixteen exterior coordinates retained (the scalar and top-grade
coordinates are both one in the unnormalized seed). Let
\(U_r=\operatorname{record}(I_4,e_r)\) be the four actual orthogonal CAR
returns. In the left action \(m\mapsto U_rm\), the two words produce
\[
m_{01}=U_1U_0m_*,\qquad m_{10}=U_0U_1m_*.
\]
The two underlying affine paths have the identical endpoint
\((I,e_0+e_1)\). Exact full-Fock reduction gives
\[
m_{10}-m_{01}=(2-2p)e_2+(2p-2)e_{12},
\]
where the basis labels are the zero-based occupation-mask coordinates of the
existing sixteen-dimensional carrier. Every other coordinate of the
difference vanishes exactly. Its positive-pairing Euclidean norm is
\[
\|m_{10}-m_{01}\|^2=2(2-2p)^2=16-24p>0,
\qquad p+p^2=1,quad p>0.
\]
Indeed (p<2/3), since (x+x^2) is increasing for (x>0) and
\(2/3+(2/3)^2=10/9>1). The certificate checks the seed against the
existing closed-record-engine owner, all four full16 returns against the
actual CAR record, the two-slot difference, and the exact squared norm.

This demonstrates the user's proposed distinction concretely: the endpoint
sum alone has forgotten order, while the current matter vector after the
ordered returns has not. It does not establish that the D0 transition uses
the affine path to select these returns. The existing autonomous record
engine recomputes its observer from the current first grade; the map from
affine path labels into that engine, joint evolution of \((q,D,b,m)\), and
refinement-compatible preparation remain open. Nor does this one pair prove
that all possible histories are injectively stored or derive a physical
finite-bit capacity law.

The exact checker is
[`a4d_native_affine_path_matter_memory_check.py`](certificates/a4d_native_affine_path_matter_memory_check.py),
with result
[`a4d_native_affine_path_matter_memory_results.json`](certificates/a4d_native_affine_path_matter_memory_results.json).
It runs 26 exact controls, verifies the consumed source hashes, and leaves
physical admission, refinement, source/Ward, and GR flags false. Reproduce
with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_affine_path_matter_memory_check.py
```
