# MEMO A4D — resolved curved stationary closure

**Task:** `EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE`  
**Execution:** PR #202  
**Status:** IN_PROGRESS / durable checkpoint  
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`

## 0A. RESUME CHECKPOINT

### EXACT/DERIVED — F4 reduces to the star physical critical set on generic quotient-complete strata

PR #201 has now certified two facts for the selected family

[
S_{\rm trial}(\Theta,b,L)
=
\alpha S_{\widehat\star}(\Theta-b^\flat,L)
+
\beta Q_L(b).
]

On every declared generic curved stratum where the landed joint-residual map is
quotient-complete,

[
\ker J_L=\operatorname{im}D_L.
]

At a full stationary point the \(\Theta\)-equation first imposes

[
E_{\widehat\Theta}S_\star=0.
]

The \(b\)-equation then reduces to \(E_bQ_L=0\), hence

[
b\in\ker J_L=\operatorname{im}D_L,
qquad
J_Lb=0.
]

Therefore the residual energy and its first \(L\)-variation vanish on shell.
Consequently the quotient-completion channel cannot be tuned to cancel a failed
star coframe equation on these strata.

The lower-wall search is therefore reduced to

[
\boxed{
C(L)\neq0,quad
\det\widehat\Theta_x\neq0\ \forall x,quad
E_{\widehat\Theta}S_\star=0,quad
E_LS_\star=0.
}
]

This is the actual F4 target.

### EXACT/CERTIFIED inherited hostile controls

The landed stationary-sector packet already supplies:

1. a one-boost curved control with nondegenerate all-site solder satisfying the
   star solder Euler equation alone, so solder stationarity does **not** force
   flatness or degeneracy;
2. an exact connection-Euler operator of rank 282 on free bivector data, showing
   that joint stationarity is the first real nonlinear compatibility gate;
3. the canonical flat checkerboard quotient-null directions are obstructed at
   cubic order:
   [
   T(z,z,w_0)=-\frac{32}{3}(a^2+b^2),
   ]
   so they do not seed a nearby curved stationary branch from canonical flat
   solder;
4. the historical sparse two-link curved witness has no nondegenerate solder
   stationary representative.

Thus neither “all curved sectors die” nor “a small flat-null branch survives” is
currently supported.

## 1. Search strategy now fixed

The next search must be richer than the killed sparse witnesses.  Use at least
a multi-link / multi-plaquette curved ansatz with:

- exact proper-Lorentz links;
- all-site nondegenerate solder;
- enough link freedom to satisfy both solder and connection Euler equations;
- explicit nonzero curvature certificate;
- quotient/gauge fixing only after the equations are assembled.

Numerical root-finding is allowed only as a scout.  Any survivor must be
rationally reconstructed or converted into an exact algebraic certificate.

## 2. Terminal alternatives

A. Construct one exact nondegenerate curved critical point:
[
\boxed{\texttt{RESOLVED-AFFINE-NONDEGENERATE-CURVED-STATIONARY-WITNESS}}
]

B. Prove an exact no-go for a precisely declared ansatz class.

C. If only numerical roots appear, record them as NUMERICAL/EXPLORATORY and
identify the smallest exact polynomial subsystem needed for certification.

No GR/Einstein conclusion is allowed from F5 alone; F4 remains independently
load-bearing.
