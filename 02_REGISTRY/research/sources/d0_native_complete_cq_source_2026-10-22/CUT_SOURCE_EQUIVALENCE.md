# The actual READY cut heat preserves the complete apparatus source

22 October 2026. Existing Draft #334, `constitutive/native-programme-v1`.
Bounded analytical continuation at published input
`cd7595b0808e47c38147f25e2cabe476ecb508f8`. No new heat selection, native
variation, preparation, field or feedback is introduced. `GR_closed=false`.

## 1. The input and the new substitution

The owned
[`ACTUAL_CUT_APPLICATION.md`, §§0,5](../d0_generated_thermal_source_2026-10-22/ACTUAL_CUT_APPLICATION.md)
constructs `C=(I-P)UP`, its paired heat `L_C=C* C+C C*`, and its complete
trace on the original cost20 READY execution. Its original full work
dimension is `D_w>=50549`; the explicitly untouched RIGHT spectator has
dimension `s=128`. Its cut is rank one before that spectator, its fixed
Book parameter is `z=2^-20`, and `beta>0`. The full carrier dimension is
`s D_w`, not two. Every harmonic work/archive mode remains in the trace.

That owner proves the common-null all42 source survives with gain greater
than two-thirds. The new statement is stronger: **at fixed calibration and
dimension the SAME positive gain relates the entire apparatus cotangent,
on every actual rank-one cut/unitary variation, before restricting to the
42 fields or to the common-null family.** Thus the new cut heat has exactly
the feedback's stationary set, full critical Hessian inertia and normalized
source precision on any supplied generated execution graph. This removes
a separate cut-heat upstream solve; it does not solve the feedback's
existing independent preparation/controller reaction.

Sources are consumed analytically, not replayed:

| Source at the pinned input | Git blob |
|---|---|
| `sources/d0_generated_thermal_source_2026-10-22/ACTUAL_CUT_APPLICATION.md` | `04bd07f4699ef2190aae7f74dfee9238decd8bf4` |
| `A4D_ORIGINAL_GOLDEN_READY_COHERENT_BOOK_FULL42_BRIDGE_2026_10_22.md` | `35134d3a536450442267cda276028ec780329544` |
| `sources/d0_original_golden_ready_coherent_book_2026-10-22/check_native_palindrome_compilation.mjs` | `09b62a47b9530bc56b8c61192000bea3e332fd52` |

The last source supplies the native base word used only as the new
matrix-variation fixture. This checker neither imports nor reruns its
older gate-compilation verification.

## 2. Exact global source equivalence on the actual rank-one carrier

Let `f` be the sole active eigenvalue of `F=C* C` before the spectator.
For any unitary `U` and rank-one orthogonal `P`, `0<=f<=1`, even when
`P` and `U` both move and `U` is not a reflection. The two nonzero
eigenvalues of `L_C` are `f,f`; at `f=0` they also become zero. The whole
trace, original feedback and derived coupled scalar are

\[
 Z_0(f)=D_w-2+2e^{-\beta f},\qquad
 J(f)=-s\log(1-zf),\qquad
 \mathcal B_C(f)=J(f)+\beta^{-1}\log[sZ_0(f)].       \tag{1}
\]

All multiplicities, including the `D_w-2` harmonic complement and the
`s` inside the absolute heat logarithm, are compulsory in (1).

**Theorem.** On every smooth execution map into this same rank-one
apparatus, with `s,D_w,beta,z` fixed,

\[
 \boxed{d\mathcal B_C=R(f)\,dJ,\qquad
 R(f)=1-\frac{2(1-zf)e^{-\beta f}}
 {s z[D_w-2+2e^{-\beta f}]}.}                        \tag{2}
\]

The identity holds for the complete cotangent: coframe, link, matter,
generated preparation, independently admitted input, controller and
clock-gate/cut variables, whenever they belong to that same finite map.
It is not necessary to freeze a moving `P` or diagonalize its derivative.

Indeed `J_f=sz/(1-zf)>0`, and the heat derivative is
`H_f=-2e^-beta f/Z_0`. Dividing the full derivative by `J_f` proves (2).
The moving-frame calculation is already contained in the equality of the
scalars (1), so arbitrary noncommuting `dP,dU` are included. At `f=0,1`
the functions and scalar coefficients are smooth because `0<z<1`;
only realizable one-sided or tangential apparatus derivatives are used.

Writing `t=e^-beta f in (0,1]` gives

\[
 \frac{(1-zf)t}{D_w-2+2t}\le \frac1{D_w},
\]

because `(D_w-2)t<=D_w-2` and `1-zf<=1`. Therefore, on the actual
cost20 carrier and every larger retained carrier with the same `s,z`,

\[
 \boxed{\frac{34165}{50549}
 =1-\frac{16384}{50549}
 \le R(f)<1,\qquad
 \frac{34165}{50549}-\frac23=\frac{1397}{151647}>0.}   \tag{3}
\]

The decimal `0.6758788502245346` is only a rendering of this exact rational
lower bound. The bound is independent of beta, f, the field and the
particular finite unitary word. It is not asserted for a two-dimensional
truncation or a carrier with a different spectator/cut.

## 3. Critical equations, Hessian and refinement precision

Let `E:X -> (P,U)` be any actually supplied smooth execution graph with
the calibration and dimension above. It may have fixed boundaries and
generated states; it may also retain independent upstream coordinates.
Equation (2) immediately gives

\[
 \operatorname{Crit}(\mathcal B_C\circ E)
 =\operatorname{Crit}(J\circ E).                     \tag{4}
\]

In particular no artificial independent thermal-matrix Euler equation is
introduced. Any genuinely independent upstream row of `J` remains a row
of `B_C`, multiplied by the same nonzero factor. The statement applies to
an actual constrained manifold or justified gauge quotient as well; it
does not choose that manifold.

Since `J_f>0`, write `B_C=Phi(J)` on its whole interval. Define
`w=2e^-beta f/Z_0`, so `0<w<1` for the actual `D_w>2`. Then

\[
 R_f=\frac{\beta w(1-w)(1-zf)+zw}{sz}>0,\qquad
 \Phi''(J)=R_f/J_f>0.                               \tag{5}
\]

Consequently, in any chart,

\[
 D^2(\mathcal B_C\circ E)
 =R\,D^2(J\circ E)+\Phi''(J)\,d(J\circ E)^{\otimes2}.\tag{6}
\]

At a stationary point the second term vanishes. The whole critical
Hessian, its kernel and its positive/negative inertia therefore agree
up to the factor R. In particular adding this heat does not turn an
existing saddle into a minimum. Away from criticality its Hessian
correction is positive semidefinite of rank at most one.

For every homogeneous covector norm,

\[
 \frac{34165}{50549}\|d(J\circ E)\|
 \le\|d(\mathcal B_C\circ E)\|\le\|d(J\circ E)\|.    \tag{7}
\]

The same inequality holds after division by the actual common nonzero
source normalization on each mesh. Thus this paired cut heat creates no
additional vanishing gain or loss of refinement precision relative to
the owned READY feedback. Any gain already lost by the reporter remains;
(7) is not an absolute lower bound on that reporter's source.

The owner supplies `D_42 J=a_J Xi_42` on the original common-null family.
Composing that fact with (2) reproduces its all42 result and now covers
every other admitted P/U tangent of the same apparatus. If the real
total price is `J+A`, with an additional already priced term A, this
does **not** imply `d(B_C+A)=R d(J+A)`: the exact difference is

\[
 d(\mathcal B_C+A)=R\,d(J+A)+(1-R)dA.                \tag{8}
\]

No CQ, preparation or work term may be silently absorbed into this
monotone transformation.

## 4. The remaining original preparation reaction is explicit

For the actual READY reflection write
`A=V* Q_click V`, `A^2=A`, normalized input `psi`,
`q=<psi,A psi>`, `f=4q(1-q)`. With fixed V and a freely admitted normalized
input variation, the real tangent gradient is

\[
 \nabla_\psi\mathcal B_C
 =8(1-2q)\,[J_f-w]\,(A-q)\psi,\qquad
 \|(A-q)\psi\|^2=q(1-q).                            \tag{9}
\]

The whole gradient includes both paired heat and feedback. At the actual
common-null report `q_0=a r_0`, with

\[
 a=2F_{21}p^{23},\quad F_{21}=10946,\quad p=\varphi^{-1},
\]
\[
 r_0=z[(1-p^{12})+(1-p^6)]-z^2(1-p^{12})(1-p^6),
\]

one has `0<q_0<1/2` (approximately `6.32459e-7`). Equation (3) makes
(9) nonzero. Its exact norm is

\[
 8(1-2q_0)[J_f(f_0)-w(f_0)]\sqrt{q_0(1-q_0)}>0.     \tag{10}
\]

The actual prescribed programme may generate this state from fixed
blanks; that does not admit a free sphere tangent. If a free normalized
input tangent is independently admitted, the true remaining price or
constraint reaction must cancel (9). A simultaneous conjugation of
`P,U` is an isospectral gauge and gives `df=0`; it cannot remove (9).
At the special `q=1/2`, the reflection polynomial has `f_q=0`, so its
first source vanishes; this is not the original READY report. At `q=0,1`
the normalized-state normal vector vanishes. None of these exceptional
points is a source-preserving replacement for `q_0`.

### The available native boundary is narrower than a free preparation orbit

The original READY owner, §1, already gives the complete normalized
Golden prefix `Psi_G=sum_gamma p^(ell(gamma)/2)|gamma>` from the unchanged
constant p and fixed cost20 stopping/suffix word. Its amplitudes are
field independent; its history and stopping/controller registers are
generated. They are not additional freely variable initial states.
The same owner's native inverse-word application uses the actual fixed
`G^-1=XGX` and H/CNOT phase comparator. Choosing another finite word or
integer cap is a prospective programme comparison, not an infinitesimal
Euler coordinate of the declared word. A supplied fixed initial clock
is likewise a boundary, rather than an extra row created by notation.

This discharges **no additional physical admission**, but it prevents
inventing a preparation/controller obstruction for these already fixed
or generated parts. Equations (2),(4) apply directly to their actual
executed graph, with its genuine boundary.

The source-bearing remainder is distinct: the owner §2 starts with a
supplied fully unitary report `V_y` and prepared `chi_y`; its §5 explicitly
retains the CAR/Choi resource-writer and physical admission boundary.
Neither that input nor the y-dependent report may be frozen while
claiming its known field source. A fixed complete initial state and a
fixed autonomous finite word have a fixed output; any nonconstant y
chart must enter through a real field/input/gate/clock parameter or a
different stored programme. Encoding y into the initial programme does
not leave the complete initial state fixed. The remaining native map
must specify that source-bearing access and its price. It is not a need
to solve an independent Euler equation for every generated work register.

## 5. Moving calibration and discrete work dimension

With beta and z genuinely moving while `s,D_w` remain fixed, the exact
complete identity replaces (2) by

\[
 \boxed{d\mathcal B_C=R\,dJ+H_\beta\,d\beta
                      +(1-R)J_z\,dz,}               \tag{11}
\]

where

\[
 H_\beta=-\frac{\log(sZ_0)}{\beta^2}
         -\frac{2f e^{-\beta f}}{\beta Z_0},\qquad
 J_z=\frac{sf}{1-zf}.                               \tag{12}
\]

These are derivatives of the original absolute heat, not a shifted
ground energy. On the actual large carrier `H_beta<0`; an independently
free beta with no other price therefore has a nonzero row even when
`df=0`. If beta or z is generated by an admitted clock, pull (11) back
through that actual clock map. A fixed native calibration has no such
extra Euler row merely because beta and z occur in the formula.

`D_w` and s are integer dimensions of the retained execution. They have
no smooth Euler derivatives on a fixed chart. Comparing a different
finite cap/work inventory is a different complete value comparison; for
example, holding f and beta fixed while adding one dormant harmonic
mode changes H by exactly

\[
 \Delta H=\beta^{-1}\log\frac{D_w-1+2e^{-\beta f}}
                                     {D_w-2+2e^{-\beta f}}>0.\tag{13}
\]

Hence (2) cannot be used to suppress the absolute work/clock price of a
changed programme. If a spectator ceases to be a genuine unchanged tensor
factor, the scalar formulas must be rederived on its real joint state.

## 6. Verification and parent boundary

`check_cut_source_equivalence.py` consumes the fixed native ten-gate
Golden/H/CNOT/X word as a base matrix and independently differentiates
the entire moving P/U cut complex, including simultaneous noncommuting
preparation and controller directions. It retains all eight base columns,
the exact number of dormant harmonic modes and s=128. Its direct matrix
heat/feedback derivative is compared with (2) and finite differences.
It also checks the exact rational gain bound, the critical Hessian and
off-critical rank-one correction, the genuine input-normal reaction and
the beta/z/dimension controls. Native Golden entries, exponentials and
matrix comparisons are numerical with declared tolerances; this is not
an interval certificate. Assertions remain effective under `python -O`.

The analytical theorem applies to the **already constructed** heat L_C.
The owned default `L913 tensor I` has different rank and spectrum; (2)
does not equate it with L_C. The actual scene/cut admission, full Book03
valuation, source-bearing field writer and independently admitted
preparation/controller laws remain the physical obligations. What is
removed is the separate cut-heat first-source and criticality comparison:
it is now identical to the original feedback problem on the whole fixed
apparatus, with a uniform explicit multiplier.
