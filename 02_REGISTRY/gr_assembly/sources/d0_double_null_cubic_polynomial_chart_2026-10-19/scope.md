# Cubic crossed-null polynomial-chart obstruction

For the orthogonal crossed-null background `H=a*x`, `J=b*y` at `h=1`, the
published exact order-`a*b` Cartan correction is retained. At order `a^2*b`,
the checker allows each of the 24 proper-Lorentz link corrections and each of
the 16 coframe corrections to be an independent polynomial of total spatial
degree at most two. Every polynomial is evaluated at its own link or coframe
site, including shifted links in all six based plaquettes.

The 40 original independent Euler rows are expanded symbolically in `x,y`.
Their six possible coefficients against `1,x,y,x^2,x*y,y^2` give 240 exact
rational equations for 240 correction coefficients. The coefficient matrix
has rank 154, while the augmented matrix has rank 155, so no solution exists
in this correction chart.

This is a finite scoped obstruction, not a general no-go for the crossed-null
branch. It does not exclude arbitrary lattice functions, higher-degree or
nonpolynomial corrections, different lower-order coframe branches, an exact
nonlinear root, or physical D0 Cost-Info selection. The checker uses the
adjacent `check_cubic_uniform_control.py` as its exact six-plaquette Jet and
Euler-row implementation; that input is pinned by SHA-256 in the assembly
record.
