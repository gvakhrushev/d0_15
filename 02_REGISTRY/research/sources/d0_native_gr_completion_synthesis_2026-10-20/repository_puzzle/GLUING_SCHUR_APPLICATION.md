# Actual old gluing matrices: retain and eliminate the archive

Input: `03_FORMALIZATION/D0/Claims/GluingAnomalyTime.lean` at
`2c592f9b9437cd302fcd39352b85212341bff968`. This is the old three-dimensional
P3 example, not a new model of the 42 GR field directions. Its role is to
fix the meaning of the proposed seam/Schur substitution before transporting
it to any physical action. The original Lean theorem proves two matrix
identities, not a universal time/force assertion about every state.

Use its literal matrices

```text
L = [[1,-1,0],[-1,2,-1],[0,-1,1]],
B = [[1,0],[1,1],[0,1]],     Ln=I2.
```

Then `B^T L B=I2`, whereas
`C=LB-B=[[-1,-1],[0,0],[-1,-1]]` is nonzero. Also
`B^T B=[[2,1],[1,2]]`, so B is not an isometric inclusion with these
ordinary Euclidean pairings. An energy restriction is not automatically
an intertwined dynamical operator.

Choose the complementary archive coordinate `n=(1,-1,1)^T`.
`B^T n=0` and `det[B,n]=3`, so `z=Bx+ny` covers the entire original fine
space. The energy is the original `E(z)=z^T L z/2`; no fitted term is added.
Its full Hessian in these coordinates is

```text
[[1,0,-2],
 [0,1,-2],
 [-2,-2,8]].
```

Thus `F=B^T L n=(-2,-2)^T`, `D=n^T L n=8>0`. The actual archive stationary
point is also its unique minimum at fixed x:

```text
y* = -D^-1 F^T x = (x1+x2)/4,
Hred = I2 - F D^-1 F^T = [[1/2,-1/2],[-1/2,1/2]],
Ered = (x1-x2)^2/4,
DEred = ((x1-x2)/2,(x2-x1)/2).
```

At `x=(a,a)`, `y=a/2`, the complete fine state is `(3a/2)1_3` and
`Lz=0`. It is stationary in all three fine directions and minimizes the
positive semidefinite original energy, although the seam commutator C
remains nonzero. This is not an accidental kernel introduced by discarding
the archive: the complete coordinate map is invertible.

The useful connection is therefore exact: the old seam matrix and the old
Schur theorem already compute a nontrivial correction to the actual reduced
energy. But `C != 0`, a scalar alpha difference, and a nonzero full field
source are different assertions. The specific rank-one matrix here is also
not the distinct rank-two cyclic-seam carrier elsewhere in the repository.
The complete physical source still requires its own matrices and price map.

`check_composition.py` checks these substitutions exactly. The independent
review in `reviews/REVIEW_GLUING_SCHUR.md` also checks the literal Lean input,
the source and the full-state stationary control.
