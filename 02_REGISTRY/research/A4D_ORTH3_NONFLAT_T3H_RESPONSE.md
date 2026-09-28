# Orth3 on the slow solder: the (t^3h) gate stops at a Fredholm obstruction

**Status:** `ORTH3_T3H_COKERNEL_OBSTRUCTION_PRECEDES_T3H2`
**Certificate:** [`certificates/a4d_orth3_slow_t3h2_check.py`](certificates/a4d_orth3_slow_t3h2_check.py)
**Exact output:** [`certificates/a4d_orth3_slow_t3h2_results.json`](certificates/a4d_orth3_slow_t3h2_results.json)

This is the full 96-row #275 calculation for the selected real-COS Orth3 ray
\(\cos=(1,0,-1,0)\), with the #260 quadratic logarithm correction and the
#241 slow solder \(S_h=I+h(\alpha\eta/2)^T\),
\(\alpha_{12}=\alpha_{21}=1\). It is separate from the 24-row character
matrix \(A(Z)\) and from the joint-invisible \(N_0\) carrier.

The flat connection operator has rank 80 and left-kernel dimension 16. In
the certificate's fixed left-kernel basis the exact projection of the
\(t^3h\) connection source is
\[
P B_{31}=(0,0,0,0,0,0,0,0,
1,-\tfrac34,\tfrac14,1,\tfrac34,-\tfrac14,\tfrac14,-\tfrac34)^T.
\]
It has rank one; row 8 is a left-null witness with pairing 1. Consequently
\(L_0r=-B_{31}\) has no solution. The earlier sparse 12-slot vector pairs
to zero and is a different jet slice; its proposed correction does not solve
the rebuilt full source.

The direct metric Euler coefficient on the same uncorrected connection jet
is nonzero. Its 40 entries have this exact sparse form (all omitted slots
are zero):

| phases | (q_{00}) | (q_{01}) | (q_{02}) | (q_{03}) | (q_{13}) | (q_{23}) | (q_{33}) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0, 1 | (5/24) | (-1/24) | (-1/6) | (5/24) | (-5/12) | (-1/16) | (-17/48) |
| 2, 3 | (-5/24) | (1/24) | (1/6) | (-5/24) | (5/12) | (1/16) | (17/48) |

This establishes a nonzero second-order metric term on the specified slow
solder. It is an off-shell coefficient: because the connection equation
already has a nonzero cokernel class, it is not the response of a
connection-stationary continuation. Thus the zero flat-background
contraction from the separate 24-row character calculation does not kill
this 96-row coefficient, but neither does this coefficient define a
stationary-sheet residue. At exact resonance the range equation
\(L_0r=-B_{31}\) has no solution. A detuned response would need its own
nonflat mixed block and limiting analysis.

The raw \(t^3h^2\) coefficient is recorded for reproducibility only. It is
not a continuation because the preceding \(t^3h\) equation is obstructed.
