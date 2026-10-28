# Canonical AF stationary family with the original archive and nonscalar continuation

28 October 2026. Existing research PR #334 in `gvakhrushev/d0_15`.
Input `d9ef0b0558fcabbc097ecf2024a10b31ec0b5852`; incoming
`185ab21cb165cbf420291a6d8a2056dc366e5275` is consumed and preserved.

[Full proof in Russian](sources/d0_canonical_stationary_family_2026-10-28/PROOF_RU.md),
[executed checker](sources/d0_canonical_stationary_family_2026-10-28/check_canonical_seed.py),
[actual result](sources/d0_canonical_stationary_family_2026-10-28/result.json).

## Parent application

The prior native five-pulse seed had a whole-unitary zero source but required the
binary boundary with twelve blanks and did not preserve the inherited original
AF label. The incoming7dp builds a real15-CX matched-preparation stationary block,
but keeps its nonzero independent inverse/loop rows. This packet constructs an
alternative mathematical initial seed directly on the canonical AF input that
satisfies BOTH the original archive law and the full endpoint stationarity
criterion. It does not substitute this seed for7dp's executed programme, claim
physical actuation or treat the canonical isometry as a paid binary preparation.

## Exact classification on the original tower

For A_m=M_d0+M_d1, iota(X,Y)=(diag(X,Y),X), tau_m=p^(m+1)Tr X+p^(m+2)Tr Y,
the actual conditional expectation is E(Z)_a=sum_b p^(k+b-a)Tr_copies(Z_b).
For W*=W=W^-1 in A_n, the canonical GNS corner is K=L_(E W).
The previous full-source criterion gives zero H+J endpoint covector precisely
when C=E W satisfies C^3=C, with the usual fixed-clock assumptions.

A prescribed Hermitian C with C^3=C has such a deeper reflection realization
IFF the kernel dimension in EACH old central type is even. Necessity follows
from trace preservation, rational independence of the two Golden weights, and
invertibility modulo2 of the Fibonacci incidence matrix. Sufficiency pairs zero
rows and shifts their actual copy indices cyclically, with the inverse shift on
the paired row. There is no diagonal copy contribution and no fitted trace.
Depth k>=4 suffices for all types. This is a spin-blind finite-algebra theorem,
not a classification of all physical critical points or mixed-spin completions.

For the fixed original A0 archive, the same parity condition must hold separately
inside EACH inherited old-label sector. It is again sufficient. Thus the archive
and stationarity constraints are imposed together, not conflated with mere
information retention. The first usable canonical old level for this construction
is A2=M3+M2, whose labels are(0,1,0) and(0,1).

## Explicit archive-compatible seed and compatible refinement

At A2->A5=M13+M8 choose C=(diag(0,1,0),I2). In the actual recursively ordered
path coordinates the complete left matrices are the permutations

    W0=(0 7)(5 10)(8 2), W1=(0 7)(5 2).

All paired paths carry the same original A0 label. Both full matrices are exact
integer involutions; E(W)=C is checked in Z[p]. Spin4 and oldRIGHT2 remain identity.
All128 original archive matrix units are preserved by exact tensor factorization.
The actual canonical GNS carrier has1864 coordinates and104 input columns;
56 return perfectly and48 escape into retained coordinates. Thus

    J=-48 log(1-zeta)>0,
    w_T=56 zeta T/(1-zeta+zeta T)>0.

There is no binary padding or new pure blank. The five displayed path exchanges
are NOT asserted to be five G/CX/SourceI pulses: no native gate word is emitted.
The source theorem holds for any actually supplied fixed clock length, with all
work/harmonic modes retained; the N5 numerical heat check is structural only.

Passive inclusion W_n=iota_(5,n)W5 gives ONE compatible exact stationary family,
with the same canonical old corner for every n>=5. Checked total dimensions at
n5..9 are1864,4880,12776,33448,87568. This is not a physical spacetime mesh or a
claim of stationarity under changing rank/temperature/clock length. The absolute
heat and its resource changes are not deleted.

## Exact nonscalar future criterion

For a partial-isometry initial corner K0, suppose the actual continuation has
factored cold product A K0. Set M=A* A, Q=K0K0*, a,b>0 and

    B_Q=Q[aI+b Q M Q]^-1 Q.

The complete old-prefix return covector is

    C_prefix=-b i[B_Q,M]i*,
    DJ_prefix=0 on ALL endpoint tangents IFF [M,Q]=0.

This replaces the prior sufficient scalar-future premise by an exact criterion.
For the displayed canonical seed, Q is central in A2 intersect A0', so any actual
future effect from that archive-preserving old algebra satisfies it. Future's
own parameter equations and its heat are NOT thereby zero. Arbitrary future
interference does not imply the factored cold product and is not covered.

## Execution and boundary

1970 explicit checks executed, ordinary/-O/repeat JSON byte-identical. Exact
signed permutations, Z[p] expectation and parity are separated from floating
controls. All243 diagonal patterns of M3+M2 are checked:70 realize the unrestricted
reflection criterion,40 additionally realize the original archive criterion.
All233 complex Lie directions of the actual A5 left algebra are tested. GNS
compression error2.23e-16; full return cotangent0. Nonscalar future source identity
error9.31e-25; a sector-mixing negative control is nonzero. Structural full heat
uses3961000 modes including3345880 harmonic modes, with phase-sum error5.56e-17.

Code SHA256 `21744ce3ea2e55dbd48a74393fd627b209d49b391e9367330858c519eab6ca94`;
Git blob `49d89fa52015c55e7fb0b31dbdef6e158b552e1d`.
Proof Git blob `f8675130936e45d9718781d38ef5b762ebaf0eba`.
Result Git blob `e34f7444fb743d230b0a01b878c927f584d42306`.

A continuous matrix family with unchanged corner and reflection signature is
also retained as a negative control: stationarity alone does NOT select an
Einstein law. No true geometry/source map, native actuation, G/CX/SourceI emission,
all42 physical recovery, Lean, CI, main merge or scientific promotion is claimed.
The previous geometric and binary results remain valid at their stated scopes.
`GR_closed=false`.
