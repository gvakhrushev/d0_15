# Curved tensor16 a4: the actual next source and its principal operator

[Proof and full scope](../../A4D_CURVED_TENSOR_A4_SOURCE_AND_ELLIPTICITY.md).
Existing #334, pinned SOURCE a1ca6f547b9b6876c4e31801665573a1734aa65f.

Consumes the newly proved fixed-positive-time finite/source limit without
calling it a short-time Einstein theorem. Extends the actual a2-blind tensor16
right-Clifford connection to a curved positive principal metric G. The full
Hodge curvature cross term is retained, not replaced by a flat Yang-Mills square.

Results: exact curved a4 and projected connection source; vanishing of that
source and the intrinsic metric a4 variation at torsion zero on an Einstein G;
principal quadratic-energy eigenvalues 4/3 (10) and 4/9 (6); a global quartic
coercive estimate on a flat torus; local isolation of T=0 among all sufficiently
small variable tensor critical fields of this a4, not just constant tensors.

These are coefficient-level statements on the declared natural-measure slice.
G is not automatically the physical Lorentz metric. Actual matter, calibration,
remaining eight torsion directions, higher coefficients and the original raw
source/refinement terminal are not removed or replaced by a fitted stress.

```sh
python 02_REGISTRY/research/sources/d0_curved_tensor_a4_2026-10-16/check_curved_tensor.py
python -O 02_REGISTRY/research/sources/d0_curved_tensor_a4_2026-10-16/check_curved_tensor.py
python 02_REGISTRY/research/sources/d0_curved_tensor_a4_2026-10-16/test_mutations.py
```

The first two runs return identical result.json; the third returns mutations.json.
The script reproduces the actual full16 creator convention directly and does
not import or execute old research suites. The 427 conditions mostly test
component/CAR identities, not 427 independent scientific closure claims.
General elliptic/IFT and Bianchi arguments are in the proof, not inferred from
finite samples. No new Lean, independent review, physical action selection or
GR closure is claimed. Inputs and exact local file hashes are recorded below.
