# Complete monitored return entropy: uniform first source without probability floors

21 October 2026. Bounded mathematical continuation of existing Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, on input
`dfc0275eea67ebc21ffe539de9b6ea96713863a5`. Phase: native realization / source
composition. This note supplies the nonlinear retained-record entropy part of
the finite-cap source limit left explicitly open by the existing literal-clock
return theorem. It changes no native primitive, action, information convention,
field map, physical admission, assembly acceptance, or lifecycle.

## 1. Inputs, common objects and exact parent substitution

The existing owner
`A4D_NATIVE_CLOCK_WORK_RETURN_SOURCE_SYNTHESIS_2026_10_21.md` derives the literal
Golden/quaternion sixteen-transition monodromy on arm2 x record2 x spin4. On
the four-dimensional arm/record part, in its fixed prepared coordinate
`j=(1,0,0,0)^T`, the matrix is

```
M(c) = [[ c, 0,-k, 0],
        [ 0, c, 0,-k],
        [ 0,-k, 0,-c],
        [-k, 0,-c, 0]],       k=sqrt(1-c^2).
```

The literal native value is `c0=sqrt(5)-2=p^3`, `p=phi^(-1)`. The spin and
actual correlated spectator reference are untouched. The owner's monitored
completion checks `P=jj*` after each complete cycle, retains every yes/no
status, and continues after no. It is a separately declared monitored
completion of the literal word; this note does not prove its physical
admission. The original fifteen-step trial, the sixteen-step closure, and
this monitored repetition remain distinct executions.

The owner proves, on a real open neighborhood of `M(c0)` in the full unitary
group U(4), with P fixed,

```
V=(I-P)U,       ||V^4||^2 <= 3/4.                       (1)
```

One sufficient radius is
`||U-M(c0)|| < epsilon0 = 318299/33554432`.
It comes from the exact four-step reachability Gram bound
`eta0=1366875/4194304>1/4` and four-power telescoping. The neighborhood is
not restricted to a scalar c variation or commuting tangent. This established
bound and the exact literal matrix are inputs; the old native gate/clock
certificate is not rerun or duplicated here.

The other consumed result is the complete leaf-amplitude / Gram-spectrum
identity of `A4D_ORIGINAL_STOPPED_RECORD_INFORMATION_SOURCE_2026_10_21.md`.
That owner treats the original all128 apparatus. Only its general finite
Gram identity and the distinction between coherent and pointer/CQ cuts are
used here, on the actual four-dimensional return apparatus. No all128
Kraus, CAR16 source, preparation, price or clock is imported.

The missing parent premise now supplied is: the complete entropy of the
retained stopping record, including unresolved mass, has a uniform C1
cap-to-infinity limit throughout (1), despite probability zeros. Consequently
the existing linear cost tail and the new nonlinear entropy tail can be
combined for ONE specified compatible monitored CQ valuation. The actual
primary all128/cap2 field map and its physical Info choice remain separate.

## 2. The complete law and two genuinely different record entropies

Let U be any unitary in (1). For n>=1 and N>=1 define

```
v_N=V^N j,
a_n=j* U V^(n-1)j,
p_n=|a_n|^2,
s_N=||v_N||^2.
```

Unitarity gives `p_n=s_(n-1)-s_n`, `s_0=1`. Thus
`sum_(n=1)^N p_n+s_N=1` and (1) gives `s_N->0`. The complete stopped
record has N resolved labels and its genuine unresolved label:

```
H_N = -[sum_(n=1)^N p_n ln p_n + s_N ln s_N]/ln(phi),
H_infinity = -sum_(n>=1) p_n ln p_n/ln(phi),             (2)
```

with `0 ln 0=0`. No success event, failure prefix, stop time or abort mass is
deleted. The monitored history is `no^(n-1),yes`, or `no^N,unresolved`.
For its full CQ cut, the conditional arm work is pure at every leaf. With
a fixed arbitrary correlated spin/reference state rho, the total CQ entropy
is exactly `H_N+S_phi(rho)`. Conditional entropy relative to this same
spectator is H_N. A moving spectator contributes its actual `dS_phi(rho)`;
it is not declared source-neutral by the matrix factorization.

There is also a useful exact spectral statement, separate from the monitored
physical valuation. The corresponding coherent leaf amplitudes are
`a_1 j,...,a_N j,v_N`. Since `v_N in j^perp`, their work Gram is

```
sigma_N=(1-s_N)P+v_N v_N*.
```

Its two possible nonzero eigenvalues are `1-s_N,s_N`; therefore the coherently
retained flag's entropy is exactly

```
S_phi(flag_coherent)=h_phi(s_N).                         (3)
```

All resolved return amplitudes remain coherent, and at infinite return they
form a pure flag vector. Hence (3) tends to zero, whereas (2) generally does
not. Their difference is `H_N-h_phi(s_N)>=0`, the actual record-coherence
term on these amplitudes. This spectral identity does NOT license use of
the coherent entropy with the monitored expected clock: a coherent padded
implementation must pay its own executed clock and controller/work.

## 3. Rational power and amplitude bounds on the full unitary neighborhood

Use the fixed rational constants

```
r=31/32,       R=r^2=961/1024,       C=7/6.
```

They satisfy `r^8>3/4` and `C r^3>1`. Writing n=4q+t, 0<=t<=3,
(1), contraction of V and these inequalities give

```
||V^n|| <= (3/4)^(q/2) <= r^(4q) <= C r^n.             (4)
```

For any C1 field or parameter map U(y) into this neighborhood and any tangent
delta y, write `B=||dU[delta y]||`. P and j are held fixed in this theorem.
No commutativity is assumed. The ordered product rule gives

```
||dV^n|| <= sum_(l=0)^(n-1) ||V^l|| B ||V^(n-1-l)||
          <= n C^2 r^(n-1) B,
|a_n| <= C r^(n-1),
|da_n| <= C^2 n r^(n-2) B,
||dv_N|| <= N C^2 r^(N-1) B.                            (5)
```

These are uniform over the full neighborhood. If an actual admitted field
map has an h-dependent derivative budget B_h, that budget is retained.
If P or j moves, (5) must instead include the genuine dP,dj sources or be
applied in an actually justified moving frame; no such terms are erased.

## 4. Entropy differentiation through dark amplitudes

For a scalar or vector amplitude z, put
`h(z)=-||z||^2 ln(||z||^2)/ln(phi)`, with h(0)=0. Direct differentiation
away from zero yields

```
dh(z)[dz] = -2 Re<z,dz> [ln(||z||^2)+1]/ln(phi).        (6)
```

Since `t |ln t|->0`, its derivative extends continuously as zero at z=0.
Thus h is C1 in the amplitude coordinates, including probability zeros.
There is no positive probability/eigenvalue floor and no division by a
dark probability. A second derivative need not extend at a rank birth.

For `0<=t<=A<=1`, writing t=A u gives the elementary bounds

```
t(1+|ln t^2|) <= A[1+2 ln(1/A)+2/e],
t^2 ln(1/t^2) <= A^2[2 ln(1/A)+1/e].                  (7)
```

They use `u ln(1/u)<=1/e` and apply at t=0 by continuity. For n>=6,
`A_n=C r^(n-1)<=1`; for N>=5, `C r^N<=1`. The inequalities
`ln(phi)>2/5`, `1+2/e<2`, and `-ln(r)<1/31`, together with (5)-(7), imply

```
|d[-p_n ln p_n/ln(phi)]|
   <= 10 C^3 B r^(-3) (n+n^2/31) R^n,     n>=6,        (8)

|d[-s_N ln s_N/ln(phi)]|
   <= 10 C^3 B r^(-1) (N+N^2/31) R^N,     N>=5.        (9)
```

Both estimates remain valid when the respective amplitude is zero.
For example, in (8) one first bounds
`|a_n|(1+|ln p_n|) <= C r^(n-1)(2+2n/31)` and then uses (5).
This order of bounds is essential: `|dp_n| |ln p_n|` may not be bounded by
postulating a uniform lower probability, which need not exist.

## 5. Explicit uniform C1 tail, including the actual unresolved event

For N>=5 define the exact rational sums

```
T0(N)=R^(N+1)/(1-R),
T1(N)=R^(N+1)[(N+1)/(1-R)+R/(1-R)^2],
T2(N)=R^(N+1)[(N+1)^2/(1-R)
                +2(N+1)R/(1-R)^2+R(1+R)/(1-R)^3].
```

They are respectively `sum_(n>N) R^n`, `sum_(n>N)nR^n`, and
`sum_(n>N)n^2R^n`. The value estimate from (7) gives

```
0 <= H_infinity-H_N
   <= (5/2) C^2 r^(-2) [T0(N)+(2/31)T1(N)].            (10)
```

The lower bound is entropy monotonicity under splitting the unresolved mass;
the upper bound follows by bounding the omitted entropy sum and dropping
the nonnegative entropy of the one unresolved event.

Uniform summability of (8), including its continuous zero-amplitude
extension, proves that H_infinity is C1 on every finite-dimensional C1
parameter chart and that its derivative is the convergent termwise series.
One can prove this directly by integrating the uniformly convergent
derivative series along a small chart segment. No uncontrolled derivative
of a little-o remainder or exchange of nonuniform limits is used.

Combining (8) and (9) yields the complete source estimate

```
|dH_infinity-dH_N|
 <= E_N B,

E_N=10 C^3 { r^(-3)[T1(N)+T2(N)/31]
              +r^(-1)(N+N^2/31)R^N }.                 (11)
```

The second term is the source of the ACTUAL unresolved mass. Omitting it
would prove a statement about an unnormalized truncated entropy sum, not
the complete cap-N law. Equations (10)-(11) give O(N R^N) value and
O(N^2 R^N) full first-source convergence, uniformly through probability
births. They do not assert C2 convergence.

For (3), the small-eigenvalue term is already bounded by (9). Once
`s_N<=1/2`, the other term `-(1-s_N)ln(1-s_N)` has derivative at most
`|ds_N|`, because `|ln(1-s_N)+1|<=1` there. Equation (5) therefore gives
uniform C1 convergence `h_phi(s_N)->0` with the same O(N^2 R^N) rate.
For example N>=16 suffices from `C^2 R^N<1/2`. This is a separate
coherent-cut spectral limit, with no monitored/coherent clock identification.

## 6. One complete compatible CQ price and its actual source

Retain the preceding owner's supplied one-cycle expected price effect
C_cycle(y), compatible with the monitored process. Its finite-cap cost is
exactly

```
L_N=Tr[C_cycle(I-V^N(V*)^N)],
L_infinity=Tr C_cycle.                                  (12)
```

The identity follows from
`sum_(j=0)^(N-1) V^j P(V*)^j=I-V^N(V*)^N` and eventual return. No price
effect is chosen to force a geometric source. A physically separate cap
abort price must be included if present; (12) alone does not price it.

Using the exact same monitored CQ cut and the explicit ENTROPY-Info
valuation, the complete specified contribution is

```
A_N=B_setup+L_N-H_N,
A_infinity=B_setup+Tr C_cycle-H_infinity,
dA_infinity=dB_setup+Tr(dC_cycle)-dH_infinity.            (13)
```

A fixed spectator entropy can be subtracted as a constant; a moving one
retains its derivative. Any further nonlinear work, independently selectable
preparation, monitor/control record, reference or clock charge stays as its
own actual term. The other Book Info convention is not silently substituted.

For `K=||C_cycle||`, `K1=||dC_cycle||` and B from (5), the cost difference
can also be bounded on this same chart:

```
|dL_N-dL_infinity|
 <= 4 C^2 R^N K1 + 8 N C^3 r^(-1) R^N K B.             (14)
```

Indeed, `||V^N(V*)^N||<=C^2R^N` and its derivative has norm at most
`2N C^3 r^(2N-1) B`; trace on the actual four-dimensional arm/record
space introduces the factor 4. Add (11) to (14) for the full specified
entropy-price source. No full all128 carrier is replaced by this dimension.

For the already specified status code, success costs 1, failure costs 2,
so `C_status=2I-U*PU`, `Tr C_status=7`. If a scalar supplied complete-cycle
cost g is added, the total is `4g+7` at infinite return. Both mean cycle
count 4 and this constant trace are exact throughout the cyclic
neighborhood, but the complete entropy source need not vanish:

```
dA_infinity=4 dg-dH_infinity                            (15)
```

when setup is field-independent and this is the whole declared contribution.
Equality of mean clocks therefore does not remove the nonlinear Info source.

## 7. Native-point first source: an interval sign certificate, not gate admission

For the analytic family M(c), the inherited first-return generating function
is

```
sum_(n>=1) a_n q^n
 = [c q-c^2 q^2-c q^3+q^4]/[1-cq-c^2q^2+cq^3].        (16)
```

Hence

```
a1=c, a2=0, a3=c^3-c, a4=(1-c^2)^2,
a_n=c a_(n-1)+c^2 a_(n-2)-c a_(n-3), n>=5.
```

Its derivative is obtained by the ordinary product rule, retaining all
three derivative terms. The exact structural dark return at n=2 is zero
for every c and has zero derivative. For `|c|<=1/4`,
`||M'(c)||=1/sqrt(1-c^2)<=4/sqrt(15)<16/15`; use the rational budget
`B=16/15`. The owner's four-step Gram estimate applies throughout this
family as well.

The accompanying standard-library checker evaluates the first 320 terms
with directed, outward-enlarged Decimal intervals. Each sqrt and logarithm
endpoint is enlarged by an adjacent representable number; every elementary
operation is enclosed. The omitted infinite derivative is bounded by the
EXACT RATIONAL quantity

```
10 C^3 (16/15) r^(-3)[T1(320)+T2(320)/31]
 = 0.0016992528732010191... .                            (17)
```

The complete cap-320 source is independently computed with its unresolved
mass, and the full cap error (11) is `0.0017941494851150778...` after
inserting B. The resulting enclosures give

```
10.61 < dH_infinity/dc at c0=sqrt(5)-2 < 10.62.          (18)
```

The stronger unaggregated-tail enclosure is approximately
`[10.61386406567719548,10.61726257142359752]`. The finite resolved-sum
source is `10.61556331855039649960329924142...`; this is not an assertion
of the infinite source to all those digits. Likewise the finite cap entropy
is `1.79456497802954442316697600603...`, while the conservative rigorous
infinite-value enclosure is
`[1.794564978029544423...,1.794566858204362461...]`.
The interval operations and rational tail, not extrapolation of finite
decimal digits, establish (18).

The derivative in (18) is on the declared analytic unitary chart at the
actual native matrix. It is NOT proof of an independently admitted native
gate-angle or coframe writer. If an admitted field map realizes that tangent,
its nonzero contribution enters (13); without that map, (18) is an exact
source control that rejects a blanket source-neutrality inference from
the constant mean clock. The checker also checks an independent
noncommuting rotation tangent by direct matrix jets against centered
finite differences; that auxiliary floating check is not the interval sign
certificate and admits no new primitive.

## 8. Gain-aware refinement consumer and remaining boundary

On any actual primary-source application that has a proven map into this
same monitored return neighborhood, (11) and (14) retain the actual signal
gain g_h. If the relevant derivative/cost budgets divided by g_h grow at
most like `h^(-q)`, choose an integer

```
N_h >= a ln(1/h),       a > q/|ln R|.
```

Then the complete specified truncation source divided by g_h tends to zero
as `O(h^(a|ln R|-q) ln(1/h)^2)`. This supplies the nonlinear Info portion
of the previous gain-aware tail consumer with logarithmic cap growth.
The exact magnitude/sign of the nontruncated entropy source remains in
the equation; it is not made small by taking a larger cap.

This proof removes the cap-to-infinity C1 entropy-tail premise for this
one actual monitored apparatus. It does not establish the actual all42
field dictionary, its upstream independent stationary equations, forced
Book03 Info, the primary full128/cap2 identification, physical elapsed-time
selection, or GR closure. In particular, the nonzero infinite entropy source
must be included when testing a complete source match; one cannot replace
it by the constant occupation trace or coherent delay `2phi`.

No unchanged all128, geometric, Lean or old gate suite is rerun. Source pins
bind the consumed literal-word and complete-record owners. The new
calculation and the analytical estimate are the decisive checks.
