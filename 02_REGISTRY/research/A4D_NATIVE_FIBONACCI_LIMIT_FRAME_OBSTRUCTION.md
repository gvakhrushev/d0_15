# G0: no coherent four-copy frame in the standard Fibonacci AF limit

Input SOURCE: `1018e73be589ddff07dace06d8872caa54b689be`; existing #310.
Status: **scoped analytic NO-GO for coherent bimodule frames in the standard
AF GNS limit**. The finite record construction at each level remains valid.
This does not close native-sector G0, physical admission, source/Ward or GR.

The finite Fibonacci owner constructs four orthogonal isometric maps
`V_{i,n}: H_n -> H_{n+3}` for every `n`, with `V_{0,n}` the actual inclusion.
It also proves that each detail map intertwines both old left and right matrix
actions. The displayed canonical frames fail the one-step naturality test at
the first levels, with exact defect ranks `6,15,39`; that test alone did not
exclude repair by another allowed bimodule frame. The theorem below closes
that repair question for the full bimodule class.

## The coherent-frame question

Let

```text
A_n = M_{a_n}(C) ⊕ M_{b_n}(C),
iota_n(X,Y) = (diag(X,Y), X),
H_n = L²(A_n, tau_n),
tau_n(X,Y) = p^(n+1) Tr(X) + p^(n+2) Tr(Y),  p + p² = 1.
```

Write `J_{n,m}: H_n -> H_m` for the actual trace-preserving inclusion. A
coherent four-frame in the same standard AF carrier would have to satisfy,
for `i,j in {0,1,2,3}`:

```text
V_{0,n} = J_{n,n+3},
V_{i,n}* V_{j,n} = delta_ij I,
V_{i,n}(a x b) = iota_(n,n+3)(a) V_{i,n}(x) iota_(n,n+3)(b),
J_{n+3,n+4} V_{i,n} = V_{i,n+1} J_{n,n+1}.                 (1)
```

The third line is the full old left/right bimodule covariance of the existing
AF construction. The last line is exact naturality under the actual AF bond,
not equality of dimensions or convergence of the canonical coordinates. In
ordinary notation it is
`J_(n+3,n+4) V_(i,n) = V_(i,n+1) J_(n,n+1)`.

**Theorem.** No family `V_{i,n}` satisfies (1) for all `n`.

**Proof.** The AF trace owner proves that `tau_n` is the unique compatible
normalized trace on the whole tower. The incidence matrix
`M=[[1,1],[1,0]]` has `M²=[[2,1],[1,1]]`, so the AF limit is simple and this
trace is faithful. Let `R` be its tracial GNS von Neumann closure. It is a
factor: if a central projection `z` had `0 < tau(z) < 1`, then
`a -> tau(z a)/tau(z)` would be a second normalized trace on the AF limit.
Uniqueness forces it to equal `tau`; normality extends
`tau(z a)=tau(z)tau(a)` from the dense AF union to all `a in R`. Setting
`a=z` gives `tau(z)=tau(z)^2`, a contradiction.

The trace-preserving Hilbert direct limit of the `H_n` is `L²(R,tau)`. By the
last line of (1), each component induces a well-defined isometry

```text
S_i [x_n] = [V_{i,n} x_n] in L²(R,tau).
```

The first line gives `S_0=I`. The second gives `S_i* S_j=delta_ij I`.
The third, at every finite stage and hence on the dense AF union, makes each
`S_i` an `R`–`R` bimodule endomorphism of `L²(R,tau)`.

Every bounded bimodule endomorphism of the standard correspondence of a
finite factor is scalar. To see the relevant fact directly, let `S` commute
with left and right multiplication and set `xi=S(1)`. On the dense subspace
`R`, the two commutation laws give `S(x)=x xi=xi x`. Boundedness of `S`
forces the affiliated operator `xi` to be bounded: if a spectral projection
`e=1_(c,infinity)(|xi|)` were nonzero for `c>||S||`, then
`||S(e)||_2=||xi e||_2 >= c ||e||_2`, contradicting boundedness. Thus
`xi in R`; it commutes with all of `R` and is scalar because `R` is a factor.
Therefore `S_i=lambda_i I`. For `i>0`, `S_0* S_i=0` forces `lambda_i=0`,
contradicting `S_i* S_i=I`. This proves the theorem. ∎

This covers every levelwise gauge-related frame that remains a bimodule
isometry with the same inherited column. No choice of such finite commutant
unitaries can turn the four-frame into a coherent nested family in the
standard AF GNS limit.

## Exact boundary of the result

The result distinguishes two statements that the finite construction alone
does not identify:

* For every finite input level `n`, the owned three-inclusion record frame
  exists and has a nonzero detail component.
* Those frames cannot be made exactly natural across all levels while they
  remain four orthogonal copies of the full old AF bimodule in the same
  multiplicity-one standard GNS limit.

The contradiction uses the bimodule-intertwining requirement. The broader
finite class stated only by simultaneous conjugation covariance is not
classified here. Nor does it rule out a different refinement map. In fact,
the [Jones record-transport owner](A4D_NATIVE_JONES_RECORD_TRANSPORT.md)
already constructs a level-dependent composite `widehat alpha_n=Ad_(R_n)
alpha` that exactly transports the declared record corner and conditional
vector at every adjacent level. It evades the theorem's ordinary-bond
naturality premise. It does not, by itself, produce a coherent four-frame on
the multiplicity-one standard GNS limit or prove that D0 physically admits
that transition. On `L²(R) ⊗ C⁴`, the four coordinate inclusions also give
orthogonal bimodule isometries; this remains a mathematical control, not a
D0 primitive supplied by the current owner.

Therefore the next G0 step is to test whether the native preparation/action
owners admit the already constructed Jones composite, with its complete
state, readout and transition, and bind that transition to the constrained
`(q,D,b,m)` carrier. If they do not, the remaining task is to derive a
different transition from existing primitives or prove an obstruction for
the complete owned class. The existing scene-history and AF-record owners
have not yet supplied that common physical map. This is an exact obstruction
to ordinary-bond four-frame naturality, not a no-go for the whole core, and
it does not introduce an ancilla, action, selector or physical postulate.

## Verification boundary

The input unique-trace result is proved in
`A4D_NATIVE_AF_TRACE_PREPARATION.md`; its Lean capsule has 16 propositions,
and its exact checker covers the stated finite density/trace controls. The
finite four-frame, its left/right intertwiners and canonical bond defects are
proved and checked in `A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md` and its
companion certificate. The direct-limit factor argument and the scalar
bimodule-endomorphism lemma above are analytic proofs; no Lean compilation of
those operator-algebra steps is claimed. The finite certificates are inputs
to the proof, not substitutes for it.
