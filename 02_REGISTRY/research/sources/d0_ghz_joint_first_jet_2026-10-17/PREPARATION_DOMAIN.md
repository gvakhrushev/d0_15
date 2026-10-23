# Golden preparation domain and the vacuum/top limit

17 October 2026. Same #334. Consumer: the surviving vacuum/top preparation
in the joint first-jet calculation of [amplitude_first_jet.py](amplitude_first_jet.py).
This note establishes its actual preparation-domain interfaces. It does not
select a new gate, initial state, observer, source or physical action.

## 1. Literal full16 words carry an exact charge

Use the existing engine, [adaptive AF owner](../../A4D_NATIVE_ADAPTIVE_AF_RECORD_ENGINE.md)
and [scalar AF preparation](../../A4D_NATIVE_ENGINE_SUPPORTED_PREPARATION_SOURCE.md).
On the reducing preparation subspace E0={masks0,1,14,15}, write

```text
l=(m0,m1), h=(m14,m15),
G=[[a,-p],[p,a]], Z=diag(1,-1), a²=p, p+p²=1,
U_s=diag(G^s,ZG^s), s=+/-1,
S=diag(1,1,-1,-1).                                    (D1)
```

These are restrictions of the literal sixteen-row gates, not a smaller
operator carrier. Both full16 gates commute with the extension of S
that is zero on the other twelve coordinates. Thus they preserve
`||l||²-||h||²`. Every scalar AF trace activation has `h=Zl`; the original
whole-blank seed has `h=-Zl`. Both have zero charge, as does the actual
canonical AF activated seed. The full scalar AF channel is distinct and
retained; no AF norm or price is replaced by its CAR projection.

For a normalized physical density and any full purification/reference,

```text
Tr(S rho)=0 -> Tr(S U_word rho U_word*)=0.               (D2)
```

The same conclusion holds for controlled sign gates and controller-only
unitaries: they commute with S tensor I_reference. Orthogonal recorded
branches, mixtures, and the entire reference128 are kept. Normalization
does not change zero charge. In inherited-settings constructions each
orthogonal actual M2 copy has the same initial zero charge; its permitted
record words preserve it. Tracing only to define the physical density
retains the underlying full state and its complete price.

This is an unconditional conserved quantity. A postselected coherent
history filter can reweight charge sectors and requires its own event and
normalizer; such a filter is not silently included in(D2).

## 2. Exact reachability and closure are different

For the chronological word s1,...,sk, the owned all-word identity is

```text
l_k=G^(Splus)l0,
h_k=Z^k G^(Sminus)h0,
Splus=sum_j s_j, Sminus=sum_j(-1)^(j-1)s_j.
```

If h0=sigma Zl0, sigma=+/-1, then

```text
h_k=sigma Z^(k+1) G^(-2N) l_k,
N=sum_(j odd)s_j.                                     (D3)
```

Nonzero vacuum/top support would require `l_k=(x,0),h_k=(0,y)`.
The initial low norm is nonzero and conserved, so x is nonzero. Equation
(D3) then gives `(G^(2N))00=0`. A rotation with zero cosine has fourth
power I, hence `G^(8N)=I`; N=0 cannot have zero cosine. The existing
golden rotation has infinite order: `Tr G²=4p-2` has conjugate
`-6-4p<-2`, incompatible with all conjugates of a finite rotation trace.
Therefore **no finite such record word reaches nonzero vacuum/top exactly**.

This does not give a distance from that plane. Already the two existing
forward words

```text
W=U_plus U_plus=diag(G²,I),
V=U_minus U_plus=diag(I,G²)                             (D4)
```

commute and independently rotate the two pairs. Infinite order of a
circle rotation makes its nonnegative powers dense. Thus W^m V^n has
dense independent phases, and the equal pair norms permit approximation
of either normalized GHZ sign. From the original seed, W^m alone can
rotate its time component towards vacuum while fixing top.

All gates and recorded controls in(D4) are the existing branch matrices;
no arbitrary onsite unitary, SWAP, CNOT or new phase is introduced. But
an arbitrary prescribed sign word is not the engine's selector
`sign(m1)`. Its controller/preparation and storage must actually be
admitted and retained; matrix availability is not that admission.
No rate, free program length, h-schedule or physical preparation cost
is inferred from density of powers.

For the two particular selected seed orbits, the stronger result is already
known: the original orbit has `|m1|>1/5`; the canonical activated AF orbit
enters a finite nonzero low-pair cycle. Those **fixed selected orbits**
cannot approach vacuum/top. This is not a statement about every accepted
engine input or every conditional record program.

## 3. The density limit and the correct coframe map

If a normalized sequence satisfying(D2) converges to a density on
`H_GHZ=span{vacuum,top}`, then necessarily

```text
sigma_GHZ=[[1/2,z],[conjugate(z),1/2]], |z|<=1/2.        (D5)
```

This holds for arbitrary complex coherence and rank, not only GHZ plus.
It follows by continuity of the bounded charge and positivity/trace1.
Retained reference columns cannot cancel it: the expectation is the sum
of the complete column norms with their charge signs.

Every exterior coframe map preserves degree, fixes vacuum and multiplies
top by its determinant. Thus P1=P3=0 for vacuum/top in both raw and form
coordinates. On the cone `e=sO01(theta)`, `G=s²I`, the **orthonormal**
coordinate-form map is

```text
I_G U_e=Lambda(G^-1/2 e^T eta)=Lambda(O^T eta),
(I_G U_e)|H_GHZ=diag(1,-1).                            (D6)
```

The scale s cancels because the form basis is orthonormal. In unnormalized
coordinate components the separate determinant factor must be retained.
Equation(D6) flips z and exchanges GHZ plus/minus but preserves(D5).
Although it can mix the rest of E0 and momenta, it does not mix the
vacuum/top plane. Equivalently, extend the charge to
`P_grade0+P_grade1-P_grade3-P_grade4`; on E0 it equals S, and it commutes
with every orthonormal coframe lift. No representation loophole changes
the limiting diagonal balance.

The new joint amplitude calculation proves that its projected coefficient
equation has squared residual at least `1/(8s^4)` for every balanced
density(D5), including arbitrary phases and mixtures, under its controlled
real first-field-jet hypotheses. Composing that fact with(D5) obstructs
those particular word-limit preparations on the named cone/first shell.
It does not exclude other preparations, fields, shells, noncontrolled
sequences, actions or all of native D0. In particular, no uniform distance
between the entire executor input domain and vacuum/top follows.

## 4. A genuine accepted ring-input family approaches the boundary

The literal executor domain itself is not separated from GHZ. For every
integer N>=2 set

```text
epsilon_N=p^N,
m_N=vacuum-top+epsilon_N time,
||m_N||²=2+epsilon_N².                                 (D7)
```

All16 slots remain; the six zero guards hold and every raw coefficient
belongs to Z[a]. Every finite N has positive m1. These are explicit
accepted **inputs**, not a claimed compilation from the owned seed.
Their normalized direction tends raw GHZ minus, which(D6) maps to form
GHZ plus. Raw normalization is a reading; the executor still stores its
exact unnormalized ring state.

In fact each input has an indefinitely defined selected orbit. Put
epsilon=epsilon_N in(0,p²]. Before the first sign change the low pair is
G^j(1,epsilon). Its first-grade entries are

```text
y1=p+a epsilon>0, y2=2ap+p³epsilon>0,
y3=4-5p+a(4p-3)epsilon,
y4=4a(2-3p)+(9-16p)epsilon,
y5=45p-28+a(21-36p)epsilon.                            (D8)
```

The elementary golden bounds `3/5<p<31/50`, `3/4<a<1` imply

```text
y3>=6p-3>0,
y4>=31-50p>0,
y5<0.
```

For the first inequality the positive remainder at epsilon=p² is
`(a-1)(4p-3)p²`. For the second it is `(4a-3)(2-3p)`.
The coefficients of epsilon in y3,y4 are negative. Both terms in y5
are negative. Thus the first five gates are plus, then minus returns
the low state5 to state4; plus returns state4 to state5. This proves
indefinite nonzero first-grade pairing, not extrapolation from a replay.
Higher grades keep evolving under the full gates and never affect this
selector. No top-grade rebuild is assumed when a later coefficient vanishes.

As N grows, the initial P1 gap nevertheless tends to zero:
`k_N=epsilon_N²/(2+epsilon_N²)`. There is no uniform P1-normalization
derivative bound. The coefficients of p^N involve Fibonacci integers,
so the exact storage/preparation resource is not bounded for free.
Crucially, its input charge is epsilon_N², not the owned seed's zero;
the preceding charge-preserving words do not generate(D7) from that seed.
Admission of each State by the executor is not an endogenous preparation
law, a source/cost law, or a uniform refinement theorem.

## 5. CAR current is regular, but does not manufacture an observer

For any density supported on vacuum/top and any retained unit observer n,

```text
P_GHZ alpha_n(v)P_GHZ=0 for v perpendicular n,
J=n,  g(J,J)=1, P1=P3=0.                              (D9)
```

This uses the actual full16 CAR current, not the first-grade observer law.
Indeed all proper Lorentz exterior maps fix vacuum and top separately.
Their boost generators annihilate the whole plane, and its complete norm
is constant as the retained observer varies. Norm-centering therefore
has rank0 on GHZ, unlike the earlier balanced four-mask preparation.
A Lorentz-equivariant timelike axis cannot be extracted from a state with
this full stabilizer without an additional already-owned transforming
datum. The correlated reading(D9) consistently uses n; it does not derive
it or make the literal m1=0 engine endpoint executable.

## 6. Bounded evidence

[preparation_domain.py](preparation_domain.py) extracts only actual engine
arithmetic/branch/step definitions and the fixed CAR creators. It checks
the full16 charge/block identities, independent words, coherent controller
conservation, correct coframe/top sign, CAR and boost compressions, the
generic sign certificates, and a few exact ring inputs through their first
cycle. No old engine suite, root or spectrum runs. Its own normal/-O output
and validation are stored as PREPARATION_DOMAIN_RESULTS/VALIDATION.json.
