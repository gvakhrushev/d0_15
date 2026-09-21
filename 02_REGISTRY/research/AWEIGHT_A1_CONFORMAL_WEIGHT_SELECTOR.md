# A-WEIGHT — A1 Conformal-Weight Selector

CONTROL disposition: **ACCEPT AS RESEARCH / WEIGHT-SELECTOR-NOGO-TERMINAL**  
Audited repository state: `3c02bac3dd589efce5bad2b5e589f495ab9b3c79`  
Source memo: `MEMO_16_AWEIGHT_A1_CONFORMAL_WEIGHT_SELECTOR.md`

This packet is a durable research summary, not a Lean proof owner.

## Terminal result

For the scene symmetry
[
H=S_9\times S_{11}\times S_{13},
]
an H-fixed positive A1 vertex weight is exactly zone-constant:
[
\rho=(r_9,r_{11},r_{13}),\qquad r_9,r_{11},r_{13}>0.
]

The induced A1 edge metric is block-scalar:
[
W=xI_{9,11}\oplus yI_{9,13}\oplus zI_{11,13},
]
with
[
x=\frac1{r_9r_{11}},\qquad
y=\frac1{r_9r_{13}},\qquad
z=\frac1{r_{11}r_{13}}.
]

Over positive reals this factorisation imposes no relation on ((x,y,z)): every positive block triple occurs uniquely, with
[
r_9=\sqrt{\frac{z}{xy}},\qquad
r_{11}=\sqrt{\frac{y}{xz}},\qquad
r_{13}=\sqrt{\frac{x}{yz}}.
]

## Exact weight-shape count

The common rescaling
[
\rho\mapsto t\rho
]
sends
[
W\mapsto t^{-2}W.
]
It is not a symmetry of bare A1 normalization, but in the full finite action it is exactly degenerate with
[
\kappa_A\mapsto t^2\kappa_A.
]

Therefore the common positive scale is not an additional independent weight modulus beyond the A1 contact normalization. A convenient projective coordinate pair is
[
u=\frac{r_9}{r_{11}},\qquad
v=\frac{r_{13}}{r_{11}}.
]

Thus exactly
[
\boxed{2}
]
genuine A1 weight-shape moduli survive the audited owned constraints.

## Why the current structures do not select the weights

The accepted A1 compensator/Ward construction works for arbitrary positive diagonal (W): finite shift invariance, the off-shell Ward identity, compensator solvability, uniqueness of the projected field, the zone-constant pure-gauge statement and the positivity/sign no-go do not generate equations among the zone weights.

Full H-equivariance reduces the 33 vertex weights to the three zone constants and nothing further.

The literal C1 map is
[
U=I\oplus I\oplus R,
]
where (R) is the Euclidean centered-row reflection on the (11\times13) block. Consequently every positive block-scalar metric
[
xI_{9,11}\oplus yI_{9,13}\oplus zI_{11,13}
]
is preserved by (U). C1 weighted-isometry therefore does not force uniform weight.

The following also do not select the A1 zone ratios:

- `SceneSpectralAction.rho1 = 1`;
- the adjacency Perron profile or degree data;
- `S_min = 1`;
- reciprocity when the correct W-dependent dual/Riesz map is used;
- family naturality across (K(a,b,c));
- the current C' A1 local symmetry structure.

No theorem identifies the A1 (ho) with `SceneSpectralAction.rho1`, the Perron eigenprofile, or an `ActionProtocol` normalization.

## Exact status of W=I

If one adds the stronger metric identification
[
\langle X,Y\rangle_{A1}
=
c\,\langle X,Y\rangle_{Hodge},
]
then the Euclidean Hodge pairing forces
[
W=cI.
]
For positive zone weights this is equivalent to
[
r_9=r_{11}=r_{13}.
]

After that independent uniform-ray selector, the remaining common scale is degenerate with (kappa_A), so (W=I) may be chosen as a normalization representative.

However the A1/Hodge pairing identification is **not owned**. It is a new common-metric/common-parent-action bridge.

Therefore:
[
\boxed{W=I\text{ is conditional, not CORE}.}
]

## Strong negative control

Two explicit surviving backgrounds are
[
\rho_U=(1,1,1),\qquad
\rho_N=(1,2,3).
]
They induce
[
W_U=(1,1,1),\qquad
W_N=\left(\frac12,\frac13,\frac16\right)
]
on the three edge blocks.

Both satisfy positivity, full H-symmetry, the accepted A1 compensator/Ward mechanism and C1 weighted-isometry.

On identical zero-marginal alternating rectangle modes the reduced A1 action triples are
[
S_U=(8,8,8),
]
and
[
S_N=\left(4,\frac83,\frac43\right).
]
Their block ratios (1:1:1) and (3:2:1) cannot be related by one overall action rescaling.

Hence the owned constraint class does not entail a unique A1 weight.

## Relation to A-NORM

A-NORM remains accepted on its declared uniform/unit-weight branch. On the uniform ray
[
\rho=r\mathbf1,
]
the common factor only renormalizes the contact coefficient:
[
m^2_{\rm eff}
=
\frac{4\kappa_A}{r^2\kappa_H},
]
while
[
\gamma=\alpha\kappa_H
]
is unchanged.

For nonuniform weights the A1 contact quadratic form is not already proved to reduce to one scalar (4I) relative to the fixed Euclidean Hodge metric. Therefore the convenient candidate list
[
(m^2,\gamma,u,v)
]
is **not yet promoted as a general modulus theorem**.

The next research obligation is to compute the exact compensator-reduced A1 operator for arbitrary positive block-scalar (W), decompose it on the six H-sectors, and only then quotient the combined Hodge+A1+two-tick dynamics.

## Terminal boundary

Primary classification:
[
\boxed{\text{WEIGHT-SELECTOR-NOGO-TERMINAL}}.
]

The current owned structures leave two projective A1 weight-shape moduli. Killing them requires a genuinely new theorem identifying the A1 metric with the Euclidean Hodge metric, or a stronger common parent action that derives both from one declared edge metric.

No CORE upgrade of `D0-HODGE-LINKS-001` follows from this research packet.
