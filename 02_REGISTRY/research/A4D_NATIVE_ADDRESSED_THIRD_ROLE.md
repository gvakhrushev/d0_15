# A4D native addressed third role: complete real memory-actuation family

Status: **constructive operator classification of the complete declared
addressed real family; native apparatus admission and gravity remain open**.
Input SOURCE: `074192ae3c76eb6deb426d395f779e43678044a6`.
Its supported D0 subtree is `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.
No physical action, phase selector, temperature, source/coupling prescription
or physical postulate is installed. This is an additional proof part of #310;
its original fixed-source/raw-owner terminal is unchanged. #202/#317 remain
independent.

## 1. The obstruction and its actual consumer

[A4D_NATIVE_UNIFORM_MEMORY_ACTUATION.md](A4D_NATIVE_UNIFORM_MEMORY_ACTUATION.md)
classified all 256 minimal four-real-coordinate retaining recording/comparison
pairs. The 192 pairs with a column-parity +1 primitive transfer the owned
active angle to old memory in 13 forward operations. For the remaining 64,
both primitives normalize the actual left Q8 frame. That finite invariant
excludes the complete old-memory gate at every word length, and excludes
vanishing-error operator approximation in the declared minimal palette.

That result does not claim completeness of larger addressed processors.
Here an actively addressed third dyad role removes that minimal obstruction,
using addressed copies of the SAME classified recording/comparison family.
The extra role is returned exactly, for every full input state and every
correlation. It need not be blank and its history is not discarded.

**Application boundary:** the ability to represent and address these
operations coherently on the existing native roles is an input to this
construction. A matrix lift is not a proof of its physical availability.
Neither functional Boolean truth nor the supplied-compatible-operator
condensed theorem derives this input. The third tensor role here is not
identified with a particular D0 Role label, a new physical qubit or a clock
register without an owned representation/application map.

## 2. Complete declared class, before choosing a programme

Use three dyad coordinates `(active, old record, additional role)` and the
whole eight-real-coordinate workspace. The native four-coordinate retaining
classes have already been proved complete:

- `F = C diag(d)` is retaining recording;
- `U = R diag(c)` is retaining comparison;
- every column coefficient has square 1;
- each class has exactly 16 coherent sign completions.

`C` and `R` are the already-owned forward/reverse comparison skeletons.
Passive exchange relates their specifications; exchange is not introduced as
an available operation. Let `q(v) = v0 v1 v2 v3`. The actual determinant is
`-q(v)`, so a **proper** four-coordinate primitive has `q(v)=-1`.

The declared two-address class contains four independently completed
primitives: `U01(c)`, `F01(d)`, `F02(e)`, `U02(f)`. There are exactly
`16^4 = 65536` realizations, proved as a cardinality of the classified
functional operator carriers. The address lift acts as identity on the
other role. Full multiplication, transpose, identity, scalar and spectator
conjugation identities are proved in the capsule; this is not a check on
blank basis vectors alone.

Let `J = [[0,-1],[1,0]]`, `X = [[0,1],[1,0]]`, `Z = diag(1,-1)`.
The actual owned rotations are bound to

`G0(a,p) = a I8 + p (J ⊗ I ⊗ I)`,
`G1(a,p) = a I8 + p (I ⊗ J ⊗ I)`.

For the native angle, `p=p0=primitiveRoot`, `a=sqrt(p0)` and
`a²+p²=1`. No new angle or target-memory rotation is inserted into the
primitive palette.

## 3. The five-step route for the proper sector

Suppose `q(c)=q(d)=q(e)=-1`. In chronological order apply

`F02(e), U01(c), F01(d), F02(e), U01(c)`.

The full generator passes through the following tensors. The sign factor in
each row multiplies the preceding one.

| Operation | Complete generator after the operation | Sign factor |
|---|---|---|
| F02(e) | X ⊗ I ⊗ J | e0 e2 |
| U01(c) | X ⊗ Z ⊗ J | c0 c2 |
| F01(d) | X ⊗ X ⊗ J | d0 d2 |
| F02(e) | J ⊗ X ⊗ I | e0 e3 |
| U01(c) | I ⊗ J ⊗ I | c0 c3 |

The matrix product is `S5 = U01 F02 F01 U01 F02`, with the rightmost
operation occurring first. Its orientation is

`σ5=(e0e2)(c0c2)(d0d2)(e0e3)(c0c3)`, `σ5²=1`.

Thus `S5 G0(a,p) S5ᵀ = G1(a,σ5 p)` on the ENTIRE workspace.
All 512 independent proper triples `(c,d,e)` satisfy the same identity;
`U02(f)` is unused in this case. For common hardware `e=d`, this includes
all 64 proper original pairs. In particular, the result is not a special
unsigned completion or a fitted helper state.

Every signed F/U has fourth power I and transpose equal to its third
power. `S5ᵀ` therefore costs 15 forward operations. The full conjugation
uses `5+1+15=21` existing forward primitives, retaining all roles.
The chronological execution of that complete code is the reverse of its
matrix-order list. An inverse primitive or a reset is not assumed.

## 4. All remaining address completions, with a common finite bound

The kernel classifies the whole two-address class by column parities.
It does not extend the five-step route to cases where its hypotheses fail.

| Condition, in this precedence order | Route length | Full forward code length |
|---|---:|---:|
| q(d)=+1 | 3 | 13 |
| q(d)=-1, q(c)=+1 | 3 | 13 |
| q(c)=q(d)=-1, q(e)=-1 | 5 | 21 |
| q(c)=q(d)=-1, q(e)=q(f)=+1 | 6 | 25 |
| q(c)=q(d)=q(f)=-1, q(e)=+1 | 7 | 29 |

The six-step chronological route is
`F02, F01, U02, U01, F02, U01`.
Its generator tensors are
`JII → JIX → XJX → IJX → JXX → JXI → IJI`, with orientation
`σ6=(e0e2)(d0d2)(f0f3)(c0c1)(e0e3)(c0c3)`.

The seven-step chronological route is
`F01, U02, F02, U01, U02, F02, U01`.
Its tensors are
`JII → XJI → XJZ → JJJ → IXJ → JXX → JXI → IJI`, with orientation
`σ7=(d0d2)(f0f2)(e0e2)(c0c3)(f0f1)(e0e3)(c0c3)`.
Both orientations have square 1. Every local identity is proved for
arbitrary unit-column signs satisfying the indicated parity, then lifted
with its full spectator. Generic composition supplies the routes.

A generic compiler replaces the inverse of EVERY route letter by three
copies of that same forward primitive. For route length k it produces
`4k+1` letters, only the four addressed primitives and the single owned
active rotation. All 65536 realizations therefore have a full-state code
of length at most 29. When the same hardware is copied to both addresses,
all 256 pairs need only 13 or 21 letters.

The parity case split is a mathematical compilation theorem for given
primitive realizations. It does not derive physical knowledge of their
completion, an endogenous decoder or a programme-selection mechanism.
No phase completion is selected as the definition of native physics.

## 5. Retained refinement, orientation and physical resource boundary

For every complete programme, literal golden-cylinder inclusion intertwines
each lifted primitive and their full composition. The complete programme
has the same action on every retained golden depth. For normalized cylinder
amplitudes, its full squared error mass equals the original squared error
mass: old histories are neither reset nor diluted.

These statements retain arbitrary correlated eight-coordinate states.
The additional actively addressed role used in the construction differs
from the passive appended cylinder. Passive refinement does not itself
supply permission to address the appended history as a processor.

The orientation ± is retained. The preceding packet proves that an
independently prepared own-angle reference distinguishes the orientations;
preparing that reference by the tested operation erases the distinction.
Moving the operator alone is not whole-apparatus gauge transport. This
packet does not declare the orientation unobservable or silently choose it.

The constant factor 29 preserves the prior CONDITIONAL owned-phi programme
resource inequality: for any fixed A,c, eventually
`29 A m^c 9^m ≤ phi^(5m)`. This is not the native endpoint action, MDL,
full runtime cost, decoder/address allocation or internal complete-word
schedule. Those require their own native admission. No ordinary external
clock is used as their substitute.

## 6. Kernel propositions, exact certificate and hostile controls

The standalone capsule prints **95 new actual propositions** and their
transitive axioms. The inlined prior proof bodies are not recounted. The
only transitive axioms are `Classical.choice`, `Quot.sound`, `propext`.
No placeholder or compiler-trust leaf is used. Actual D0 source imports,
toolchain and all previous proof inputs are SHA pinned.

The exact checker re-derives the retaining basis skeletons, verifies all
signed addressed primitives and their three-forward inverses, and checks
both full matrix coefficients I and J0 for every one of the 65536 hardware
realizations. Its route counts are 32768/16384/8192/4096/4096 in the table's
precedence order. It checks arbitrary-workspace operator identities, not
just a fitted state or postselected fiber. Both orientations occur 32768
times. The 256 common-hardware pairs split as 192 length-13 and 64 length-21.

Hostile controls reject a missing restoring word, replacement of the helper
address by the original address and misuse of the five-step route with a
positive helper completion. The old minimal Q8 certificate is preserved
and pinned. False physical-closure and false exact-result ledgers must be
rejected. The exploratory 28-axis finite orbit is not the terminal proof;
the terminal uses generic quantified identities and all-depth intertwining.

## 7. Next native obligation and gravity consumer

G0b now needs the owned physical representation/application of the complete
apparatus: which existing coherent roles carry these coordinates, which
actual native operations act on both addresses, and how preparation,
independent calibration, decoder/address resources and a full internal
schedule are admitted. Construct these from the kernel or prove a complete
obstruction for the actual admissible class. Do not add a qubit, selector,
angle or physical postulate in place of that proof.

The constructive addressed operator family does not exhaust arbitrary
complex or larger native apparatus. It does not alter the minimal Q8
terminal. The joint Delta/P/U family, full variations and condensed
refinement still retain all 653 complementary histories and BOTH
thermal-memory source defects. Own metric/matter source and Ward identity,
quantitative metric contrast, native stationarity, curved joint roots,
soundness/recovery and physical constraints remain required.
**G0b/G0/positive GR/global closure are not claimed.**

Artifacts: `certificates/a4d_native_addressed_third_role.lean`,
`_output.txt`, `_results.json`, `_check.py`, `_certificate.json`.
