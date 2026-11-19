# Cyclic incidence heat on the faithful recorded native word

[THEOREM.md](THEOREM.md) gives the exact operator contract, proof and limits.
This replaces neither Book03 nor the earlier paired-cut packet. It constructs
an explicit normalized connection-incidence Laplacian on K(9,11,13) x C_m and
computes its full cyclic heat with all original full128 record sectors retained.

The heat first/second sources have a dimension-independent winding-tail bound.
At fixed beta=2phi^-2 its first-source coefficient is <1.120e-33 for m=15 and
<2.430e-36 for m=16, multiplied by the TRUE whole-word derivative norm. A
verified negative control shows why scene-dependent short loops are outside
this bound. The bare reflection's zero source is not substituted for the
nonzero source of the recorded word.

```sh
OPENBLAS_NUM_THREADS=1 python interval_coefficients.py
OPENBLAS_NUM_THREADS=1 python check_scene_heat.py
OPENBLAS_NUM_THREADS=1 python -O check_scene_heat.py
```

The commands print fresh results; they do not overwrite stored receipts.
Dependencies: numpy, scipy, mpmath. General claims are analytical; coefficient
and tail bounds use outward intervals; native matrices are double precision.
105 active controls pass normally and under -O, with byte-identical outputs.

A source-normalized refinement corollary applies under ACTUAL logarithmic
clock growth and polynomial field-jet bounds. It is not permission to pad the
physical clock. No full42 field writer, independent apparatus root, compulsory
scene/cut selection, Lean build, remote CI or GR acceptance is claimed.
The scientific owner remains Draft PR #334; GR_closed=false.
