# A4D Y temporal SO(3)-spin product rigidity

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`  
Execution: PR #310  
Status: exact scoped sector result; **not** a task-level terminal.

## Statement

At `z=1`, use the product-plane solder
[
S_f=I+(f-1)P_perp,qquad P_perp=-Y^2/3,
]
and temporal links
[
K_0^{(0)}=C_Y(1)C_B(-d)C_R,qquad
K_0^{(2)}=C_Y(1)^{-1}C_B(d)C_R,
]
with odd temporal phases and all spatial links equal to the identity.  Here
[
R=aJ_{12}+bJ_{13}+cJ_{23}
]
and `C_R` is the real Cayley rotation.

Exact elimination of the three role-0 boost Euler rows gives a linear
combination proportional to the backward Laplacian of `f^2`.  After removal
of Cayley denominators and everywhere-nonzero real factors, its only possible
zero multiplier is
[
M(a,b,c,d)=3d^4(a-b+c+3)^2+4(a-b+c-4)^2.
]

Hence `M>0` for real parameters except
[
d=0,qquad a-b+c=4.
]
Away from this exceptional locus stationarity forces
[
3f_0^2=f_1^2+f_2^2+f_3^2.
]
On a connected periodic spatial carrier the finite maximum principle makes
`f` constant.

On the exceptional locus the nine spatial-role rotation Euler rows lose all
dependence on `a,b,c`.  In variables `(f0,f1,f2,f3)` their coefficient
matrix is
[
{1over3}
\begin{pmatrix}
3&0&-2&-1\\
3&0&-1&-2\\
0&0&1&-1\\
-3&2&0&1\\
0&1&0&-1\\
3&-1&0&-2\\
0&1&-1&0\\
-3&2&1&0\\
-3&1&2&0
\end{pmatrix}.
]
It has exact rank 3 and kernel `span{(1,1,1,1)}`; therefore the exceptional
locus also forces `f1=f2=f3=f0`.

Thus every real temporal `SO(3)` Cayley correction in this ansatz is unable
to support a nonconstant product-plane profile.

## Relation to earlier certificates

This strictly extends the separate `J12/J13/J23` tests: `a,b,c` are
simultaneous and arbitrary.  It also composes with the previously certified
boost-dual amplitude `d`.  The older degree-two normal-jet calculation
already permits all 96 connection coefficients, so regular/smooth spatial
transverse corrections do not remove that formal obstruction.

What remains is narrower: singular or refinement-dependent high-Bloch
spatial-transverse corrections, together with the full nonlinear uniform
range estimate.

## Spectral diagnostic and firewall

A corrected diagnostic must use singular values of the full joint symbol,
not the most negative eigenvalue of the connection Hessian.  Numerical
refinement scouting shows one center singular value closing linearly at the
folded Y-center while the next singular value appears bounded away from zero
(about `0.1128` near the tested folded points).  This is **diagnostic only**:
no all-Bloch lower bound is claimed here.

The next proof target is therefore an exact all-Bloch estimate on the
transverse complement,
[
\sigma_2(\mathcal J_Y(k))\ge c_R>0,
]
after the exact Y-center is separated.  If established with the required
uniform nonlinear remainder bounds, it would reduce the remaining singular
spatial rescue to the already rigid center.

## Replay

From repository root:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_temporal_spin_transport_check.py
```

Pinned machine-readable output:
`02_REGISTRY/research/certificates/a4d_y_temporal_spin_transport_results.json`.

### Scope fence

- exact at `z=1`;
- temporal general real spatial rotation and boost-dual correction;
- spatial links are identity in this certificate;
- no arbitrary nonlinear spatial-transverse-link theorem;
- no all-Bloch spectral theorem;
- no task-level `CLOSED` or global `NOGO`.
