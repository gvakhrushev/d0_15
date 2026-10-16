# Quarantined parabolic calculation: wrong Euler placement

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Status: negative control only. The former physical interpretation is withdrawn.

The retained checker uses the wrong-placement `(A;C)` stack imported from
[the quarantined first-slow calculation](A4D_IDENTITY_QUARTER_FIRSTSLOW_INJECTIVITY.md).
At `(1,1,i,i)` it has rank 23, a real first derivative of rank three with
kernel `(0,0,-1,1)`, and the recorded second-order cokernel pairing `-8`.
Those numbers reproduce the algebra of that control, not the literal Euler
operator. Its executable and ledger now mark this distinction explicitly.

The physical stack `(A^T;C)` has an exact polynomial kernel along every
`(a,a,i,i)`, `a in C*`. Hence `(1,1,i,i)` is on an entire physical resonance
circle, and the range-eliminated residual on that circle is identically zero.
Its physical real first derivative at this point has rank two, with kernel
spanned by `(1,1,0,0)` and `(0,0,1,-1)`. The corrected audit does not classify
the higher-order opening transverse to the circle.

See [the physical resonance-circle memo](A4D_IDENTITY_PHYSICAL_RESONANCE_CIRCLES.md)
for exact ranks, kernels, minors and independent literal placement checks.
The former eight-isolated-points premise and the proposed inference of a
global `h^-2` inverse loss are withdrawn. No finite polynomial loss follows
from the retained control.

Replay of the retained negative control:

```sh
python3 02_REGISTRY/research/certificates/a4d_identity_rank23_parabolic_resonance_check.py
```

Control terminal: `A4D-IDENTITY-WRONG-PLACEMENT-PARABOLIC-CONTROL`.
Full four-dimensional continuation and response universality remain open.
