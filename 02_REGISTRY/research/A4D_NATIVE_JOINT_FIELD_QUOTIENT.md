# G0: complete joint field coordinates, admissible tangents and source ambiguity

Input: `00aa52091ae004fac6c1dc11964be3fa191b75b8`, existing #310.
Supported owner tree: `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.
Status: **constructive complete quotient of the stated nondegenerate native
kinematic carrier**. No action, field equation, physical state selector or
preferred refinement is installed. G0 and positive GR remain OPEN.

The earlier [nonlinear quotient research](MEMO_A4D_STAR_DENSITY_LORENTZ_NONLINEAR_QUOTIENT.md#11-completeness-of-the-quotient-coordinates)
already classified raw solder and linear links by their Gram and dressed
links. That result is consumed, not rediscovered here. The new consumer adds
all affine shifts and the actual sixteen-component exterior matter fibre,
describes the complete quotient image and tangents, expresses the owned
transported metric on it, and derives the constraint on a legitimate source
variation. This is the joint-data route left open by the
[affine scalar boundary](A4D_NATIVE_AFFINE_HISTORY_SCALAR_BOUNDARY.md).

## 1. Actual carrier and transformation laws

At each site x of `ArchiveRolePhaseGroup N`, retain the full invertible raw
solder `F_x=rawSolderMatrix N e x`. A positive edge e=(x,r), y=x+r, has an
`AffineCartanConnection` value `(U_e,a_e)` with Lorentz linear part and an
unrestricted four-vector shift. Retain an arbitrary real `ArchiveCochain N`
matter value psi_x in all sixteen Fock components. Write rho(F) for the
owned exterior lift on the direct sum of grades 0 through 4.

The precise local **linear Lorentz** action, in the raw row convention, is

```text
F'_x = F_x Lambda_x,
U'_e = Lambda_x^-1 U_e Lambda_y,
a'_e = Lambda_x^-1 a_e,
psi'_x = rho(Lambda_x^-1) psi_x.                            (1)
```

These are the literal `rawFullSolderFrameAction`,
`a4dFiniteLorentzLinkAction`, `affineGauge_shift` with zero node translations,
and `archiveAffineCoChainGauge`, using the same Lambda inverse. The exterior
lift has proved composition and inverse laws. This carrier has no imposed
matter Euler equation or parity-sector restriction.

The actual `IsRoleLorentz` predicate allows O(1,3). When using the proper
orthochronous subgroup, retain the orientation and time-cone component labels
of each F as in the prior quotient proof. Equality of Grams alone does not
fix those labels. Internal affine translations, coordinate diffeomorphisms
and response-null directions are not declared gauge here. In particular the
existing raw-solder frame law does not supply a full affine-origin law.

## 2. Complete joint orbit coordinates and their exact image

Define

```text
q_x = F_x eta F_x^T,
D_e = F_x U_e F_y^-1,
b_e = F_x a_e,
m_x = rho(F_x) psi_x.                                    (2)
```

All are invariant under (1). The q and D maps are the actual `a4dSiteGram`
and `a4dDressedLink`. The b and m readings use the full vector and exterior
representations, not a trace or degree-zero projection. Translations and
nonzero matter are retained, not set to zero in the general theorem.

**Completeness.** Two states have identical (q,D,b,m) if and only if they are
related by a unique transformation (1), with the component-label qualification
above for SO+(1,3).

Proof: set Lambda_x=F_x^-1 F'_x. Equality of q implies
Lambda_x eta Lambda_x^T=eta. Equality of D gives exactly the link law in (1).
Equality of b and invertibility give its shift law. Inverting the exterior
lift in the equality of m gives its matter law. The converse follows by
cancellation. F'_x=F_x Lambda_x also proves uniqueness. The capsule compiles
the matrix reconstruction and Lorentz argument, the complete vector/exterior
inverse statements and the group cancellation. The assembly over arbitrary
finite sites and edges is this explicit analytic proof.

The full image of (2) consists precisely of:

```text
q_x symmetric with inertia (1,3),
D_e q_y D_e^T = q_x,                                      (3)
b_e arbitrary in R^4,       m_x arbitrary in R^16.
```

For sufficiency choose one invertible factor F_x with q_x=F_x eta F_x^T.
Such a factor is obtained by writing the symmetric matrix as an orthogonal
eigenbasis times its diagonal real eigenvalue matrix times the transposed
eigenbasis, putting its single positive eigenvalue first, and multiplying
the basis columns by the square roots of the absolute eigenvalues. Set

```text
U_e=F_x^-1 D_e F_y,   a_e=F_x^-1 b_e,   psi_x=rho(F_x)^-1 m_x.
```

Equation (3) proves U_e is Lorentz. It also forces D_e invertible. These
formulas reconstruct an actual state and show that there are no further
constraints on b or m. Different choices of F are precisely the gauge (1).
For SO+ add the chosen component labels and require D to transport their
orientations/time cones. Without that extra condition the image includes
improper or time-reversing links.

With v=L^4 sites and 4v positive links, including the distinct oriented
slots at L=2, the original carrier has dimension
`16v + (6+4)4v +16v =72v`. Its free local Lorentz quotient has dimension
`66v`. The coordinates above have dimension
`10v +16(4v)+4(4v)+16v =106v`, subject to 10 independent constraints per
edge in (3), giving the same 66v. This is a full kinematic quotient dimension,
not the number of propagating modes or independent physical Euler equations.

## 3. Full tangent image and its kernel

For arbitrary variations put H_x=F_x^-1 delta F_x and let d rho(H) be the
actual exterior first derivative. Differentiating (2) gives

```text
delta q_x = F_x(H_x eta+eta H_x^T)F_x^T,
delta D_e = F_x(H_x U_e+delta U_e-U_e H_y)F_y^-1,
delta b_e = F_x(H_x a_e+delta a_e),
delta m_x = rho(F_x)(d rho(H_x)psi_x+delta psi_x).           (4)
```

The complete tangent image is the set of symmetric delta q and all other
variations satisfying the differentiated edge condition

```text
delta D_e q_y D_e^T + D_e delta q_y D_e^T
  + D_e q_y delta D_e^T - delta q_x = 0.                   (5)
```

For an arbitrary vector satisfying (5), choose

```text
H_x = (1/2) F_x^-1 delta q_x F_x^-T eta,
delta U_e = F_x^-1 delta D_e F_y-H_x U_e+U_e H_y,
delta a_e = F_x^-1 delta b_e-H_x a_e,
delta psi_x = rho(F_x)^-1 delta m_x-d rho(H_x)psi_x.
```

Substitution gives (4). Substituting (5) shows
`delta U_e eta U_e^T + U_e eta delta U_e^T=0`, so every reconstructed link
variation is genuinely tangent to the Lorentz group. This proves surjectivity
onto the entire constrained tangent space; no finite-rank extrapolation is used.

If all four outputs in (4) vanish, H_x is Lorentz-skew and the remaining
equations force

```text
delta F_x=F_x H_x,
delta U_e=-H_x U_e+U_e H_y,
delta a_e=-H_x a_e,
delta psi_x=-d rho(H_x)psi_x.                              (6)
```

Conversely (6) is the actual infinitesimal gauge and annihilates (4).
Thus **only** these 6v directions are removed by this quotient. A null
direction of an action Hessian or another readout is not removed by it.

The exact certificate tests a four-link star with five distinct sites,
nonzero shifts and all sixteen nonzero matter components. It retains all
24 independent Lorentz link directions. The full 210-by-200 Jacobian has
rank 170; its kernel is exactly the rank-30 gauge matrix. The rank-40
constraint differential annihilates the Jacobian, proving equality of the
finite image with the constrained target in this control. The all-size
theorem is the construction above, not that one finite rank.

## 4. The actual transported physical metric in these coordinates

The owned `transportedSolderCenter` uses incoming links:

```text
hat F_r(x) = [F_r(x)+(F_(x-r) U_(x-r,r))_r]/2.
```

Define B_x row by row, retaining the role on its own incoming edge:

```text
(B_x)_(r,a) = [delta_(r,a)+(D_(x-r,r))_(r,a)]/2.
```

Since `F_(x-r) U_(x-r,r)=D_(x-r,r) F_x`, the exact native identities are

```text
hat F_x = B_x F_x,
hat q_x = B_x q_x B_x^T.                                  (7)
```

Both identities are compiled for every N, using the literal transported
center and dressed-link definitions. There is no small-link or smoothness
approximation. Raw nondegeneracy does not guarantee det B_x!=0: even a proper
spatial pi-rotation can make selected centered rows cancel.

On the open class det B_x!=0, `(hat q,D,b,m)` is still a complete quotient
coordinate system, since `q=B^-1 hat q B^-T`. Its variations must use

```text
delta hat q = delta B q B^T+B delta q B^T+B q delta B^T,    (8)
```

and substitute `q=B^-1 hat q B^-T` into (3). Treating hat q and D as
independent arbitrary matrices forgets these genuine constraints.

The centered-frame dressed links
`hat D_e=hat F_x U_e hat F_y^-1=B_x D_e B_y^-1` also obey
`hat D_e hat q_y hat D_e^T=hat q_x`. However replacing D by hat D can lose
information. Here is an exact nondegenerate control at every even L:

```text
chi(x)=(-1)^(x_0),   |t|<1,
F_x=diag(1+t chi(x),-1,-1,-1),   U_e=I,   a=psi=0.
```

The actual center is eta, so hat q=eta and hat D=I for every t. Nevertheless
`q_00=(1+t chi)^2` changes, hence the states with t=0 and t!=0 are not on
the same local Lorentz orbit. All raw and centered determinants remain nonzero
and their component labels agree. Specifically the temporal dressed raw link
has first entry `(1+t chi)/(1-t chi)`, and B_00=1/(1+t chi).
Thus **even the full centered metric and centered-frame link readout cannot
justify discarding the raw Nyquist sector as gauge**. This does not assert
stationarity or a physical observable equation for that sector.

## 5. Action descent and the exact source-variation boundary

For this precisely stated carrier, every gauge-invariant scalar action is a
unique scalar function J on the constrained quotient image (3), with component
labels if needed, and conversely every such J pulls back to an invariant
action. Completeness follows from Section 2: the fibres are exactly orbits.
This classifies the invariance interface. It does not select J or prove that
all other native conditions reduce to invariance.

For any differentiable such action I, differentiating its invariance in the
actual gauge direction at site x gives the full finite local-Lorentz identity

```text
E_Fx[F_x H]
 - sum_(edges out of x) E_Ue[H U_e]
 + sum_(edges into x) E_Ue[U_e H]
 - sum_(edges out of x) E_ae[H a_e]
 - E_psix[d rho(H)psi_x] = 0.                              (9)
```

No matter equation was used in (9). Every source, link and matter term must
be retained before taking an on-shell specialization. This is an internal
Lorentz identity; it is **not** the four-component physical stress-divergence
identity required by the gravity plan.

There is a concrete pitfall in defining a metric source directly from J.
On the quotient, delta q at fixed D is not arbitrary: (5) becomes
`D_e delta q_y D_e^T=delta q_x`. An ambient extension of J away from (3)
is not unique. Adding

```text
sum_e <P_e, D_e q_y D_e^T-q_x>
```

changes ambient partial metric derivatives while leaving the entire native
action and its genuine variations identically unchanged. Its full variation
vanishes by (5), including the delta D terms. The scalar restriction
`J(s,t,d)=d^2 t-s` makes this explicit: the ambient s derivative is -1,
whereas the pulled-back action `J(d^2 t,t,d)` and its actual derivative are
zero. Both **actual derivative statements** are compiled, not represented
by unequal formal symbols or constant success checks.

Therefore a legitimate own source must be the derivative of an independently
specified native action under its specified coframe/metric variation, or an
intrinsic cotangent on (3) with a proved physical splitting. The quotient
does not authorize defining the source by an arbitrary off-constraint
extension or by the residual of an Einstein equation. This also explains why
holding the internal U fixed and holding dressed D fixed are different
background variations: (4) retains their exact difference.

## 6. Composition and refinement compatibility that actually follows

For two consecutive affine links the dressed data compose exactly as

```text
(D_1,b_1)(D_2,b_2)=(D_1 D_2,b_1+D_1 b_2).               (10)
```

Endpoint factors cancel; the linear and affine path laws already owned in
`ArchiveAffineCartanConnection` give the result for every word. The exterior
matter lift composes by rho(D_1D_2)=rho(D_1)rho(D_2). Metric compatibility
(3) is preserved by every such composition.

Thus any independently specified blocking that replaces a coarse edge by a
fine path and retains endpoint frames commutes with these joint readings.
This is a proved compatibility of that construction, not a choice of the
native blocking, its metric/cochain weights or its continuum normalization.
Simple frame averaging without its transported-link correction does not
inherit it. No uniform inverse bound, physical source law, native interlevel
admission or nonlinear recovery theorem is obtained from (10).

## 7. What the gravity chain can now consume

The joint nondegenerate **state quotient, complete constrained tangent image,
exact transported-metric map and action-descent interface** are explicit.
The full raw information and matter representation have been retained.
This removes a coordinate/gauge ambiguity before constructing the field law;
it does not identify response-null directions with gauge or install that law.

The remaining G0 action must be an independently owned J on this constrained
joint carrier, or another explicitly justified carrier, with its actual
admissibility and refinement. Its source must use genuine variations as in
Section 5. The earlier star-insertion quotient result remains a conditional
geometric action result; this construction does not equate it to a selected
primitive native cost. Own physical source/Ward, calibrated contrast,
joint curved solutions, soundness/recovery, positive GR and global closure
remain OPEN. Original #310, #202 and #317 terminals are unchanged.

Evidence is separated into the [Lean capsule](certificates/a4d_native_joint_field_quotient.lean),
[compiler output](certificates/a4d_native_joint_field_quotient_output.txt),
[source receipt](certificates/a4d_native_joint_field_quotient_results.json),
[exact checker](certificates/a4d_native_joint_field_quotient_check.py) and
[immutable ledger](certificates/a4d_native_joint_field_quotient_certificate.json).
The full orbit/tangent/image assembly is analytic; the named matrix, exterior,
center and derivative statements are compiled. No supported owner is modified.

Validation: 15 resolved Lean declarations, 51 transitive D0 source pins and
41 exact controls. The finite star keeps all 24 link variations, every
metric component with its packed dual weight, nonzero affine shifts and all
sixteen matter components. Its joint ranks are 170 for the readout, 30 for
gauge and 40 for constraints. Proper/time-component, false ambient source,
incomplete Ward and centered-readout counterexamples delimit the result.
