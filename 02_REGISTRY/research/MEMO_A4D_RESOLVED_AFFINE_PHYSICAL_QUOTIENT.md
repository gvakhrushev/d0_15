# MEMO A4D — resolved affine physical quotient / Einstein detector

**Task:** `EXP-A4D-RESOLVED-AFFINE-PHYSICAL-QUOTIENT`  
**Execution:** PR #201  
**Status:** IN_PROGRESS / durable checkpoint  
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`

## 0A. RESUME CHECKPOINT

### EXACT/CERTIFIED — F5 closes positively

Starting from the accepted flat star-density quadratic form, eliminate the
24 Lorentz-link variables by the exact Schur complement of the invertible
connection block.  Convert the remaining 16 coframe perturbations to the ten
symmetric metric perturbations using

[
delta g = Heta+eta H^T,qquad H=rac12,delta g,eta.
]

Let (k) be a formal small momentum.  The effective star metric Hessian is
quadratic in (k).  Comparing all ten coefficient matrices multiplying

[
k_0^2, k_0k_1,ldots,k_3^2
]

with the independently owned Lorentz response (E_eta) gives

[
oxed{
K_{star,mathrm{metric}}(k)
=
rac14,K_{E_eta}(k)
}
]

exactly over (mathbb Q).

Since the audited Lorentz response class is

[
operatorname{span}{E_eta,E_{m sp}},
]

and these rays are independent, the coefficient of the extra spatial ray is

[
oxed{eta_{m sp}=0}.
]

This is the requested F5 Einstein detector.  No continuum field equation is
imported into this calculation: it is an exact equality between the finite
small-momentum Hessian extracted from the selected star action and the already
owned (E_eta) finite response ray.  The existing normal-jet bridge then
identifies that ray with (-2G+O(arepsilon_N^2)) under its own stated
continuum hypotheses.

Exact certificate:

`02_REGISTRY/research/certificates/a4d_star_qr_einstein_detector_check.py`.

### EXACT/STRUCTURAL — the joint-residual completion cannot spoil F5

For the two-holonomy residual

[
R_{2|1}
=
det(I-P_1)t_2-(I-P_2)operatorname{adj}(I-P_1)t_1,
]

take a flat perturbation with

[
I-P_i=O(epsilon),qquad t_i=O(epsilon).
]

In four dimensions,

[
det(I-P_1)=O(epsilon^4),qquad
operatorname{adj}(I-P_1)=O(epsilon^3),
]

hence

[
oxed{R_{2|1}=O(epsilon^5)}.
]

Every quadratic residual action (Q(R)) therefore begins at

[
oxed{Q(R)=O(epsilon^{10})}.
]

Its flat quadratic Hessian is exactly zero.  Therefore every action in the
declared family

[
S_{m trial}=S_{widehatstar}+Q(R)
]

has the same F5 detector as (S_star):

[
oxed{
K_{m trial,metric}
=
rac14K_{E_eta},
qquad
eta_{m sp}=0.
}
]

The action coefficients in (Q) cannot be tuned to fake this result and cannot
reintroduce the unwanted finite (E_{m sp}) ray at linear order.

## 1. Stationary auxiliary theorem for quotient-complete residuals

The landed joint-holonomy packet gives, on each declared generic homogeneous
curved (L=2) control,

[
ker J_L=operatorname{im}D_L,
qquad
operatorname{rank}J_L=192.
]

Consider a quadratic quotient-complete residual term

[
Q_L(b)=langle J_L b,M_LJ_L bangle
]

with nondegenerate readout on (operatorname{im}J_L), and

[
S(Theta,b,L)
=
S_star(widehatTheta,L)+lambda Q_L(b),
qquad
widehatTheta=Theta-b^lat.
]

At a full stationary point, the (Theta)-equation first gives

[
E_{widehatTheta}S_star=0.
]

The (b)-equation then reduces to

[
E_bQ_L=0.
]

On a quotient-complete stratum this forces

[
binker J_L=operatorname{im}D_L.
]

Thus (b) is a node-translation gauge direction, (J_Lb=0), and the residual
term itself vanishes.  Because (Q_L) factors quadratically through (J_Lb),
its first variation with respect to (L) also vanishes at (J_Lb=0).

Therefore, **on every stratum where the landed quotient-completeness hypothesis
holds**, the residual term repairs the affine quotient but does not manufacture
new physical stationary dynamics:

[
oxed{
operatorname{Crit}(S_star+Q)/mathcal G_{m aff}
cong
operatorname{Crit}(S_star)/mathcal G_{m Lor}
}
]

within the stated relative-solder chart.

This is precisely the H1 branch of the gravity strategy: the quotient
completion is auxiliary on shell.

### Scope

This theorem is not yet promoted across the flat rank seam or every nonlinear
link background.  The graph-closure tangent/conormal geometry must still be
used to compute the final global (d_P).  It does, however, imply that the
curved-vacuum search in PR #202 cannot rely on tuning (Q(R)) to cancel a
failed coframe Euler equation on the generic quotient-complete stratum.

## 2. Consequence for the bidirectional GR strategy

The upper wall has advanced materially:

[
S_star
longrightarrow
E_eta
longrightarrow
-2G+O(arepsilon_N^2)
]

with the first arrow now exact at the finite action-Hessian level and no
(E_{m sp}) contamination.

The remaining load-bearing lower-wall problem is therefore sharper, not
broader:

[
oxed{
	ext{find or exclude a nondegenerate curved critical point of the star
physical dynamics itself.}
}
]

The joint residual is still required to make the affine quotient faithful; it
is not a substitute source for the missing curved stationary solution.

## 3. Next exact gates

1. Extend the stationary-auxiliary theorem from the two generic controls to the
   selected graph-closure carrier, including rank-changing seam strata.
2. Finish (d_A,d_E,d_P) on that resolved carrier without quotienting limiting
   incidence directions by assumption.
3. Feed the now fixed physical action into PR #202 and search the richer
   multi-link stationary sector.


## 4. EXACT/CERTIFIED — scoped physical quotient dimension

The generic curved quotient-complete stratum admits two exact separating
quotient-transverse variations for the declared family
[
S_{m trial}=alpha S_{widehatstar}+eta Q(R).
]

First, on the exact curved star witness, uniform solder scaling keeps the
residual channel zero and gives
[
S_star(lambdaTheta)=-rac23lambda^2,qquad
left.rac{dS_star}{dlambda}ight|_{lambda=1}=-rac43
e0.
]

Second, on the exact nongauge matched edge shift with
(deltaTheta=(delta b)^lat), the relative solder is fixed, hence the star
channel is constant, while
[
R(t)=tleft(-rac{32}{9},-rac{40}{9},rac83,0ight)^T,
qquad
Q_eta(t)=-rac{128}{9}t^2,
]
so
[
left.rac{dQ_eta}{dt}ight|_{t=1}=-rac{256}{9}
e0.
]

Therefore the coefficient-to-Euler map has exact rank two on the declared
generic curved principal stratum. Since both channels are full-affine invariant
and the second variation is explicitly outside (operatorname{im}D_L),

[
oxed{d_A=2,qquad d_E=2,qquad d_{P,mathrm{aff},mathrm{generic}}=2.}
]

Certificate:
`02_REGISTRY/research/certificates/a4d_star_qr_physical_survival_check.py`.

This is deliberately **not** the statement that the flat intrinsic quotient has
dimension 192. At (L=I), (operatorname{rank}D_0=60) and the intrinsic
quotient remains 196-dimensional; the residual channel is dormant at the seam
rather than turning the four limiting incidence directions into gauge.

### Current strongest combined statement

On the generic curved resolved-affine principal stratum the selected
two-channel family survives the true node+Lorentz quotient with
(d_P=2), while its flat quadratic metric response is nevertheless a
**single pure Einstein ray** because (Q(R)) starts at tenth order.

Thus action-family dimension two and flat propagating Einstein-ray dimension
one are compatible: the second channel repairs the affine quotient but is
auxiliary/dormant in the flat linearized dynamics.
