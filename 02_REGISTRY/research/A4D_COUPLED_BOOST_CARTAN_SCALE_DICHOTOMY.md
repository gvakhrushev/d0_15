# Bounded-source coupled boost: Cartan-scale dichotomy

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.  
Status: analytic corollary of the exact bounded-source temporal-`B` current identity; no task terminal.

## 1. Exact input

On the fixed nonconstant warp
[
S_h(x)=operatorname{diag}(1,1,f(hx_1),f(hx_1)),
qquad
f(y)=1+rac{1-cos(2pi y)}{50},
]
consider the general temporal-(B) family in the real Cayley chart, with
identity spatial links.  The exact current reduction supplied by the
bounded-source checker is
[
(E_{K,0})[B]
=sum_{i=1}^3 D_i^-!left(w_isqrt{1+3z_i^2}ight),
qquad
w=(f^2,f,f),
	ag{1}
]
without a four-phase assumption.  The three real (z_i) are recovered
algebraically from the diagonal stationary-response slots
(Xi_{11},Xi_{22},Xi_{33}).

For an independently prescribed bounded source
[
Xi=h^2	au,qquad
|	au_{m diag}|_inftyle M,
	ag{2}
]
the exact recovery and
(sqrt{1+u}-1le u/2) imply that the source-dependent correction to the
geometric current is (O(h^4M^2)), uniformly sitewise.  Summing the literal
owner norm gives the already checked lower bound
[
oxed{
|E_K|_{mathrm{owner},1}
ge rac{102}{625}L^3-90M^2.
}
	ag{3}
]
The constants in (3) belong to the exact temporal-(B), spatial-identity
calculation.  The argument below only needs the structure
(c_0L^3-C_0M^2) with (c_0>0).

## 2. Allow arbitrary sub-Cartan spatial links

Now keep the same coframe and temporal links, but replace the three spatial
links by arbitrary proper-Lorentz links
[
R_{x,s}=exp A_{x,s},qquad s=1,2,3,
]
in one fixed compact logarithm chart.  Put
[
arepsilon_h=max_{x,s}|A_{x,s}|.
	ag{4}
]

The literal connection Euler map is an analytic finite stencil.  On the
fixed compact coframe/link chart there is therefore a constant (C_g),
independent of (L), the temporal amplitudes allowed by (2), and the
particular spatial field, such that replacing the identity spatial links by
(R) changes every connection Euler row by at most
[
C_garepsilon_h.
	ag{5}
]

There are only a fixed number of owner components per lattice site.
Consequently
[
|E_K(S_h,K_{m temporal},R)
      -E_K(S_h,K_{m temporal},I)|_{mathrm{owner},1}
le C'_g L^4arepsilon_h
	ag{6}
]
for another (L)-independent constant (C'_g).

Combining (3) and (6) gives
[
oxed{
|E_K(S_h,K_{m temporal},R)|_{mathrm{owner},1}
ge
rac{102}{625}L^3-90M^2-C'_gL^4arepsilon_h .
}
	ag{7}
]

Hence
[
arepsilon_h=o(h)=o(L^{-1})
quadLongrightarrowquad
E_K
e0
]
for all sufficiently fine meshes.  In particular an exact bounded-source
rescue of this temporal-(B) class cannot use a spatial correction smaller
than the continuum Cartan scale.

Equivalently, every exact rescue sequence must satisfy, along some
subsequence,
[
oxed{
limsup_{h	o0}rac{arepsilon_h}{h}>0.
}
	ag{8}
]

No Fourier decomposition, period-four reduction, inverse estimate, or
classification of temporal amplitudes is used in this conclusion.

## 3. Combine with the literal smooth-critical theorem

The older first-variation/Cartan argument proves the following conditional
statement for the same naked-star action.  If exact connection-stationary
solutions have
[
L_{h,r}=exp(homega_{h,r})
]
with the rescaled connections precompact with sufficient (C^1) control,
then the literal connection Euler equations give
[
omega_h-omega_{m LC}(S_h)=o(1)
]
(and (O(h)) under the stronger owned (C^2) hypothesis), and the metric
readout converges to the designated Einstein response.

Together with (8) this yields a sharp dichotomy for a putative
bounded-source temporal-(B) counterexample on the fixed curved warp:

1. **sub-Cartan spatial compensation**, (|A_{m sp}|_infty=o(h)):  
   impossible by (7);

2. **Cartan-scale but smooth/precompact compensation**,
   (A_{m sp}=homega_h) with the smooth-critical compactness hypotheses:  
   the connection limit is Levi--Civita and the owned response is Einstein;

3. therefore every surviving non-Einstein candidate must use
   **rough Cartan-scale compensation**:
   [
   |A_{m sp}|_infty=Omega(h)
   ]
   while (A_{m sp}/h) fails exactly the compactness needed to pass the
   first variations to the continuum.

This is substantially narrower than “arbitrary extra spatial links”.
The remaining object is an ultraviolet/rough Cartan-scale compensation
mechanism, not a smaller perturbative correction of the rejected boost.

## 4. Why the scale (h) cannot be removed by a crude perturbation argument

The (O(h)) scale is physically and mathematically necessary: the designated
smooth spin connection itself has logarithm (O(h)), and its contribution to
the connection Euler equation is of the same raw owner-sum order (L^3) as
the geometric coframe current in (3).  Thus (7) must not be misread as an
exclusion of the designated Levi--Civita transport.

A proof beyond this memo must recenter at that (O(h)) transport and control
only the rough remainder.  Replacing it by identity links would reintroduce
the background mismatch that (3) measures.

## 6. Closure consequence

For the temporal-(B) response-memory route, the next honest terminal object
is now:

[
oxed{
	ext{exclude or exactify rough Cartan-scale }O(h)
	ext{ spatial compensation under the fixed smooth source.}
}
]

A positive proof may use compactness derived from the joint equations,
or a direct reduced-current identity after recentering at the designated
connection.  A negative terminal would be an exact sourced sequence in this
rough class with normalized response different from the designated branch.

Verdict:
[
oxed{	exttt{TEMPORAL-B-SUB-CARTAN-RESCUE-EXCLUDED}}
]
conditional only on the exact bounded-source current/lower-bound input (1)--(3)
already checked in this task.

No action modification, selector, Fourier cutoff, connection uniqueness,
BOOK/CORE promotion, or task-level Einstein/no-go terminal is asserted.
