# Proper parallel paths and the actual raw-link cotangent jet

16 October 2026. Same conditional native operator/source interface. This note
converts two existing source coordinates; it selects no connection, action,
preparation or physical admission rule. In particular a Levi--Civita graph is
a comparison graph, not a consequence of the native link Euler equation.

The raw native forward edge is `C(v_x) Lambda(A_(x<-y)) shift`, in that order;
its full16 representation and genuine endpoint adjoint are owned by
[joint adjoint source](A4D_NATIVE_JOINT_ADJOINT_SOURCE.md) and
[full Lorentz adjoint source](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md),
sections 1--3. The latter uses the entire proper Lorentz link class and
retains observer/normalizer sources. The present conversion does not replace
those sources by a geometric inverse adjoint.

## 1. Exact proper path and its left-trivialized variation

Fix an edge direction `r`, write `x` for that coordinate, and let
`Omega(x) in so(eta)` be a smooth connection in the native vector convention.
The actual backward proper parallel link from `x+h` to `x` is

```text
P_h = exp[h(partial_x+Omega)] exp[-h partial_x],
exp[h(partial_x+Omega)] f(x)=P_h(x)f(x+h).
```

This is a multiplication operator and belongs to the proper Lorentz component
near `h=0`. It is not `I+h Omega`; for nonconstant, noncommuting Omega,

```text
P_h=I+h Omega+h^2/2 (Omega'+Omega^2)
      +h^3/6 (Omega''+Omega' Omega+2 Omega Omega'+Omega^3)+O(h^4).
```

Primes denote endpoint-coordinate derivatives. Their order cannot be frozen
or interchanged. Put

```text
xi_h=(delta P_h)P_h^-1/h,    L X=partial_x X+[Omega,X].
```

The exact variation-of-exponential identity gives, on smooth test fields,

```text
xi_h=B_h delta Omega,
B_h=integral_0^1 exp(t h L)dt
   =I+(h/2)L+(h^2/6)L^2+O(h^3).                         (1)
```

Indeed `[partial_x+Omega,M_X]=M_(LX)`, so conjugating the multiplication
operator `delta Omega` proves (1). This includes every endpoint derivative
and commutator even when Omega varies along the edge. It does not divide by
L at a zero mode. The exterior representation gives exactly

```text
delta Lambda(P_h) Lambda(P_h)^-1 = h Gamma(xi_h),
Gamma([Omega,X])=[Gamma(Omega),Gamma(X)].
```

All16 exterior components remain; the statement applies independently to
all native spatial link slots. A passive basis or observer change also
transforms the cotangent, as required by the existing full source.

## 2. Name the pairing before taking its adjoint

Let the link covector be defined by the invariant bilinear trace pairing

```text
delta S_link=integral mu(x) Tr(ell_h(x) xi_h(x)) dx,
mu>0.
```

On periodic fields, or when boundary terms vanish,

```text
L_star ell=-partial_x ell-[Omega,ell]-(partial_x log mu)ell. (2)
```

For a finite interval the omitted integration-by-parts term is explicitly
`[mu Tr(ell X)]_boundary` and must instead be retained unless it vanishes.
Thus `L_star=-L` holds for constant mu with the stated boundary convention.
The trace pairing is an invariant Lie-algebra cotangent pairing; it is not
the positive Hilbert--Schmidt adjoint of the matter pairing.

For the positive real Hilbert--Schmidt pairing `Tr(ell^T X)` the actual formula is

```text
L_star_HS ell=-partial_x ell+[Omega^T,ell]
                         -(partial_x log mu)ell.          (3)
```

For complex matrices replace transpose by conjugate transpose. Boosts have
`Omega^T != -Omega`, so (2) and (3) cannot be silently identified. A moving
measure contributes its separate `delta mu` row to the complete action;
(2) describes the link cotangent at a fixed background measure only.

## 3. The coefficient conversion and its inverse

Let `j_h` be the smooth connection/path covector, in the same pairing:

```text
delta S_link=integral mu Tr(j_h delta Omega),
j_h=B_h_star ell_h.
```

Use coefficient convention `ell_h=ell0+h ell1+h^2 ell2+...` and similarly
for j, without factorials. At fixed smooth Omega and mu, (1) gives

```text
j0=ell0,
j1=ell1+(1/2)L_star ell0,
j2=ell2+(1/2)L_star ell1+(1/6)L_star^2 ell0.
```

Consequently the actual raw-link coefficients are

```text
ell0=j0,
ell1=j1-(1/2)L_star j0,
ell2=j2-(1/2)L_star j1+(1/12)L_star^2 j0.                 (4)
```

The `1/12` is the coefficient of the inverse averaging map, not `1/6`.
Formula (4) works with either explicitly named adjoint (2) or (3).

If the comparison background itself has `Omega_h=Omega0+h Omega1+...`,
and `log mu_h=log mu0+h b1+...`, write
`L_h_star=L0_star+h L1_star+...`. Then the second line for j2 includes
`+(1/2)L1_star ell0`, and (4) becomes

```text
ell2=j2-(1/2)L0_star j1+(1/12)L0_star^2 j0
                                      -(1/2)L1_star j0.   (5)
```

For (2), `L1_star X=-[Omega1,X]-(partial_x b1)X`; for (3), it is
`[Omega1^T,X]-(partial_x b1)X`. Spatial variation of Omega already appears
inside L0 and is different from this explicit h-dependence.

## 4. What this supplies to the h^-2 source target

The raw native link chart is `delta A=h xi A`. Its covector ell is not the
same coefficient as the smooth parallel-path covector j. Equations (4)--(5)
give the exact jet conversion before testing a normalized h^-2 row. Observer,
coframe, volume and normalized preparation rows still come from their actual
owners; they are not cancelled by this change of link coordinates.

This is a smooth coefficient statement, **not** a uniform all-grid C0 inverse
or a remainder estimate. Such an estimate requires an independent source-density
comparison in the named same-grid dual norm. In particular B_h can have a kernel:
at Omega=0 a perturbation proportional to `exp(2 pi i x/h)` has zero averaged
edge jet. A formal inverse series does not recover arbitrary oscillatory tests.
No native comparison graph or physical selector follows from (4).

The new [exact checker](sources/d0_raw_link_cotangent_2026-10-16/check_raw_link_cotangent.py)
uses a nonconstant, noncommuting four-dimensional Lorentz connection. It checks
the ordered path through h^3, actual inverse and Lorentz metric jets, full16
exterior covariance, both cotangent pairings, a nonconstant positive weight,
the integrated source identity, and explicit h-dependent background corrections.
Hostile controls detect frozen endpoints, reversed trivialization, the wrong
1/6 inverse coefficient, omitted density, and the boost adjoint mismatch.
The [RESULTS](sources/d0_raw_link_cotangent_2026-10-16/RESULTS.json) record only
this bounded algebraic calculation; no old suite, continuum heat limit or
physical admission is replayed or claimed.
