# MEMO A4D — resolved affine physical quotient / Einstein detector

**Task:** `EXP-A4D-RESOLVED-AFFINE-PHYSICAL-QUOTIENT`  
**Execution:** PR #201  
**Status:** REVIEW / OTO upper-wall deliverable complete  
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`

## 0. Strategy lock (this PR)

F5 is a binary gate on the **naked** star action \(S_\star\) only.
Do **not** search coefficients \((a,b)\) in \(S_{\mathrm{trial}}=a S_\star+b Q(R)\) for F5:
near flat, \(Q\) cannot alter the flat quadratic jet of \(S_\star\).

Curved stationary roots are deferred entirely to PR #202.

## 1. EXACT / CERTIFIED — naked \(S_\star\) F5 = binary OTO gate

After exact Schur elimination of the 24 Lorentz-link variables and conversion
of the remaining 16 coframe perturbations to the ten symmetric metric
perturbations, the flat small-momentum metric Hessian of naked \(S_\star\)
satisfies, over \(\mathbb Q\) on all ten \(k_ak_b\) coefficient matrices,

\[
\boxed{K_{\mathrm{star,metric}}(k)=\tfrac14 K_{E_\eta}(k)}.
\]

In the owned two-ray Lorentz response space \(\operatorname{span}\{E_\eta,E_{\mathrm{sp}}\}\)
this is exactly the binary gate

\[
\boxed{c_\eta=\tfrac14\neq 0,\qquad c_{\mathrm{sp}}=0}.
\]

\[
\boxed{\texttt{TERMINAL: S\_STAR-CARRIES-EINSTEIN-SEED (c\_sp=0, c\_eta!=0)}}
\]

No continuum Einstein field equation is imported: this is an exact equality
between the finite flat Hessian of \(S_\star\) and the owned \(E_\eta\) ray.

Certificate: `02_REGISTRY/research/certificates/a4d_star_qr_einstein_detector_check.py`.

## 2. EXACT / CERTIFIED — flat-jet order of \(R\) and \(Q\)

For the two-holonomy residual
\[
R=\det(X)\,t_2-Y\,\operatorname{adj}(X)\,t_1
\]
with connection defects \(X,Y\) in four dimensions,

\[
\det(X)=O(X^4),\qquad \operatorname{adj}(X)=O(X^3),
\]
hence with \(Y=O(X)\)

\[
\boxed{R=O(X^4 t)}.
\]

Any quadratic residual action therefore obeys

\[
\boxed{Q(R)=O(X^8 t^2)}.
\]

In the combined near-flat regime \(X=O(\varepsilon)\), \(t=O(\varepsilon)\),

\[
R=O(\varepsilon^5),\qquad Q=O(\varepsilon^{10}).
\]

Consequently the flat quadratic jet vanishes identically:

\[
\boxed{j^2_{\mathrm{flat}}Q=0
\quad\Rightarrow\quad
j^2_{\mathrm{flat}}(S_\star+Q)=j^2_{\mathrm{flat}}S_\star}.
\]

\(Q\) is a **nonlinear completion only**. It cannot fake or kill the naked
\(S_\star\) Einstein seed at flat quadratic order. Same certificate.

## 3. Corrected H1 — integrate-out, not \(\mathrm{EL}_b\Rightarrow R=0\)

**Incorrect (withdrawn):** \(\mathrm{EL}_b\Rightarrow R=0\) as the load-bearing H1.

**Correct:** write the residual as a structural map
\[
R=R_\star(C,e,\ldots)
\]
with \(R_\star(0)=0\), while \(R_\star\) may be nonzero at finite curvature.
On shell in the residual channel, \(\mathrm{EL}_R=0\) determines
\(R=R_\star(C)\) (or an equivalent solving branch). The effective action

\[
S_{\mathrm{eff}}=S_\star+Q\bigl(R_\star(C)\bigr)
\]

still satisfies

\[
\boxed{j^2_{\mathrm{flat}}S_{\mathrm{eff}}=j^2_{\mathrm{flat}}S_\star}
\]

by the flat-jet order of §2. Thus the quotient completion repairs the affine
quotient / nonlinear sector without contaminating the flat Einstein seed.

Generic quotient-complete controls still support the structural reading that
the residual is auxiliary for the **flat quadratic** OTO gate; they do **not**
by themselves prove a curved Crit-set identity needed for #202.

## 4. Scoped \(d_A/d_E/d_P\) (generic curved stratum only)

On the declared generic curved principal stratum, exact separating variations
give

\[
\boxed{d_A=2,\qquad d_E=2,\qquad d_{P,\mathrm{aff},\mathrm{generic}}=2}.
\]

Certificate: `a4d_star_qr_physical_survival_check.py`.

This is **not** a claim that the flat seam is 192-dimensional: at \(L=I\),
\(\operatorname{rank}D_0=60\) and the intrinsic quotient remains 196-dimensional;
\(Q\) is dormant there. Global seam \(d_P\) stays OPEN / deferred.

## 5. EXACT vs OPEN inventory

### EXACT (this PR — Ready)

| Item | Status |
|---|---|
| Naked \(S_\star\) F5: \(c_\eta=1/4\neq0\), \(c_{\mathrm{sp}}=0\) | CERTIFIED |
| \(R=O(X^4 t)\), \(Q=O(X^8 t^2)\); \(j^2_{\mathrm{flat}}Q=0\) | CERTIFIED |
| \(Q\) = nonlinear completion only (not an F5 dial) | CERTIFIED |
| Corrected H1 flat-jet integrate-out statement | STRUCTURAL + certified jet |
| \(d_{P,\mathrm{aff},\mathrm{generic}}=2\) | CERTIFIED (scoped) |

### OPEN / DEFERRED

| Item | Owner |
|---|---|
| Curved nondegenerate root of star physical dynamics | PR #202 |
| H1 across graph-closure / rank-changing seam | seam lane / #202 |
| Global \(d_{P,\mathrm{aff},\mathrm{res}}\) on flat seam | OPEN / stratified |
| Continuum Einstein field equations | **NOT CLAIMED** |

## 6. Boxed terminals

\[
\boxed{K_{\mathrm{star,metric}}=\tfrac14 K_{E_\eta}\quad(c_\eta\neq0,\;c_{\mathrm{sp}}=0)}
\]

\[
\boxed{R=O(X^4 t),\quad Q=O(X^8 t^2),\quad j^2_{\mathrm{flat}}Q=0}
\]

\[
\boxed{j^2_{\mathrm{flat}}(S_\star+Q)=j^2_{\mathrm{flat}}S_\star}
\]

\[
\boxed{\texttt{S\_STAR-CARRIES-EINSTEIN-SEED (c\_sp=0, c\_eta!=0)}}
\]


## 5. EXACT/DERIVED — seam stabilizers and final resolved quotient accounting

The selected graph-closure result resolves, but does not erase, the rank seam.

Let
[
D_L:C^0(X,V)	o C^1_+(X,V).
]

On the declared generic curved controls,

[
operatorname{rank}D_L=64.
]

The node space also has dimension 64, so

[
ker D_L=0,
qquad
dim(C^1_+/operatorname{im}D_L)=256-64=192.
]

At the exact flat point,

[
operatorname{rank}D_0=60,
qquad
dimker D_0=4,
]
hence the intrinsic affine-edge quotient is

[
dim Q_0=256-60=196.
]

The graph-closure lift stores a limiting 64-plane
(mathcal I_*supset U=operatorname{im}D_0), with

[
G_*=mathcal I_*/U,qquad dim G_*=4.
]

Crucially, the landed graph-closure theorem does **not** promote (G_*) to
endpoint gauge. The true flat gauge image remains (U), and the four constant
node translations remain the flat stabilizer. Therefore no quotient dimension
is silently changed:

[
oxed{Q_{m generic}:192,qquad Q_{m flat}:196.}
]

The two charts are reconciled by the resolved incidence fibre, not identified.

### Stabilizers

- nondegenerate local-Lorentz solder sector: trivial Lorentz stabilizer;
- generic curved affine node action: (ker D_L=0);
- exact flat affine node action: four-dimensional constant-translation
  stabilizer (ker D_0);
- limiting incidence directions (G_*): resolution data, not additional gauge.

### Final action/Euler/physical dimensions for the declared family

The exact separating variations in §4 prove rank two for the
coefficient-to-Euler map on a genuine generic physical quotient chart. Both
channels are gauge invariant and nonconstant on the descended configuration
space. Therefore, for the declared two-channel resolved family,

[
oxed{
d_A=2,qquad
d_E=2,qquad
d_{P,mathrm{aff,res}}=2.
}
]

This is a **global family** statement. It does not say that both channels appear
in every local jet at every stratum. At exact flat holonomy,

[
Q(R)=O(arepsilon^{10}),
]

so the quadratic/linearized physical dynamics has only the star channel:

[
oxed{
d_{P,mathrm{flat,quadratic}}=1,
qquad
K_{mathrm{metric}}=rac14K_{E_eta},
qquad
eta_{m sp}=0.
}
]

Thus the final resolved picture is consistent:

- two physical nonlinear action channels globally;
- one flat quadratic propagating metric channel;
- that channel is exactly the finite Einstein ray;
- the second channel repairs/detects the affine quotient away from the seam
  and is auxiliary at generic stationary points.

### Terminal

[
oxed{
	exttt{RESOLVED-AFFINE-TWO-CHANNEL-PHYSICAL-FAMILY-SURVIVES-WITH-PURE-EINSTEIN-FLAT-RAY}
}
]

No continuum Einstein field equation is claimed here. The continuum
identification still uses the independently landed normal-jet bridge and its
stated hypotheses.
