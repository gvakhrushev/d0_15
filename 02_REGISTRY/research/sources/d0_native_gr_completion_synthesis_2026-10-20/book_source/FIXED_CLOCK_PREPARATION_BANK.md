# A fixed-duration complete Golden preparation bank

20 October 2026. Consumer extension of
[DETERMINANT_PREPARATION_BANK.md](DETERMINANT_PREPARATION_BANK.md),
Git blob `e7b92fae0d6f3dc3e60499f0dd041c18003da872`, read at
`7620c0a0aa9c3ba2cb638b87360190aa83fae811`.

The owned bank already constructs the coherent resources, retains all
failures, and proves the complete source multiplier greater than 0.195.
This note changes its preparation schedule only. It removes the
READY-transcript-dependent preparation delay identified explicitly in
that owner's Section 3. It does not rederive the parity extractor,
identify an operational tick with physical time, or claim minimality
over all resource preparations. `GR_closed=false`.

## 1. Consumed inputs and the precise clock interface

The native parity preparation and forward inverse echo are consumed from:

| Input | Exact Git blob read |
|---|---|
| [Native coherent Bell/plus preparation](../../../A4D_NATIVE_GOLDEN_COHERENT_BELL64_EXACT_P18_PROGRAMME_AND_BOOK_WORK_2026_10_20.md), Section 1 | `2c9db85f5b3ec66df10d888ab13bc088d2d949cf` |
| [Addressed Golden palette and retained-one echo](../../../A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md), Section 1 | `9de7100f8a3a97aa4b3a46fccc02ef95824cc2c5` |
| [Resource/source boundary](../../../A4D_NATIVE_COMPILER_SOURCE_AND_RESOURCE_BOUNDARY.md), Sections 1–4 | `7e36683f9427fcf2e3574db45d41f7a7aca3d63b` |
| [Two native 8D determinant source](TWO_NATIVE_8D_DETERMINANT_SOURCE.md) | `30c5fbb0eb840e341b33aa66f336eb58b6ac3378` |

Fix N >= 2, m = 42N and a finite cap K before execution. For each
resource reserve K fresh three-wire parity slots, a canonical target,
and sufficient retained routing/work/clock space. The first resource is
a plus resource, also supplying a retained computational-one control.
There are N minus resources and 41N plus resources.

The interface assumptions are explicit. Each actual addressed primitive,
fresh readout, and original report symbol has its held field-independent
clock duration and price. Each pair of address-selected routing words has
the same duration, as do the fully executed reports 00 and 10 under the
declared uniform report-symbol clock. Their separately retained prices
may differ.
Selection between two addressed words of the same length is
performed by an actual, uniformly bounded, fixed-duration paid
classical controller; the READY calculation and its archive are included
in that controller. This is the same measured-address interface used by
the owned bank, strengthened to a fixed schedule. If this controller or
its timing is not admitted, this theorem is conditional on that missing
interface. A coherent AND/OR gate is not supplied by the construction.

The clock has capacity greater than the entire finite schedule; a small
cyclic sample clock cannot be silently reused with wraparound. A held
map from this full operational clock to the sampled physical coordinate
u is a separate input, not a consequence of Golden code length.

## 2. Execute every trial and route in reverse order

For each plus slot execute the existing word: two G rotations,
CX(A,C), CX(B,C), CX(A,B), then read fresh parity C. Its success
probability is s = 2p^3, where p = phi^(-1), and its successful A
state is exactly |+>, with B=C=1. Let r=1-s.

Execute ALL K slots, even after a success. Retain all measured parity
bits and all unused success/failure quantum registers. Use the actual
two-symbol report `10` for success. For failure, execute its original
report `0` and then an additional genuinely written and paid known-zero
symbol `0`. Thus each trial takes two report-symbol ticks. This does
not replace the physical parity law (r,s) by a fictitious normalized
Golden law: the two fixed-length words have Kraft sum 2p^2 < 1.
Their entropy is still exactly h_phi(s), because the extra zero is a
deterministic part of the injective record.

After all K trials, scan j=K,...,1 in that fixed order. If parity j
is 1, perform the three-CNOT SWAP of A_j and the canonical target. If
parity j is 0, perform an actual three-CNOT SWAP on two dedicated blank
dummy wires. Every slot therefore executes three routing gates. The
last successful swap in this reverse scan is the smallest successful
index, so the canonical target is exactly the first successful resource.
Earlier target contents remain in the old slots. Nothing is erased.
If all parities are zero, the target remains its original blank.

For the first plus resource run the same fixed reverse scan on its B
byproducts, using a separate canonical control and dummy routing wires.
The resulting control is 1 iff this seed factory succeeded, and 0
otherwise. It is retained throughout the subsequent preparation.

For every intended minus slot, replace the second G by the same
three-operation word CX(control,B), G(B), CX(control,B). With control
1 this is XGX=G^T; the owned parity gadget then supplies |-> on success.
With control 0 the word still executes, and supplies |+> on success.
The latter branch will have READY=false because the seed failed; it is
retained and never used as a valid minus resource. No supplied basis-one,
outcome-dependent skipped gate, or free inverse is required.

Both signs have the same parity probability s, including conditional
on every earlier seed transcript. Fresh slots therefore give exactly
mK independent Bernoulli(s) parity bits. Continue the whole schedule
after any resource failure. READY holds iff each of the m resources
has at least one successful slot. Its probability is the owned value

    alpha = (1-r^K)^m.

On every READY transcript all canonical resource states are identical
to the original bank's specified inputs. Conditional on that transcript,
the remaining preparation registers are retained pure factors; the
canonical inputs are not entangled with the unused failures.

## 3. Exact deterministic counts and full record entropy

Before separately priced measurement/controller/clock overhead, the
same counts are executed on EVERY transcript, including total failure:

| Operation | Count |
|---|---:|
| G | 2mK = 84NK |
| CNOT | (6m+2N+3)K = (254N+3)K |
| Fresh parity measurements | mK = 42NK |
| Actual report-symbol ticks | 2mK = 84NK |

The CNOT count includes 3mK parity/unentangling gates, 3mK target
routing gates, 2NK inverse-echo gates and 3K seed-control routing gates.
Known-zero dummy SWAPs are counted even though their states do not change.
Storage reservation and address/controller work are additional actual
costs; their field-independent deterministic schedule is not priced as
zero. Under the interface in Section 1, the entire prefix has one
duration D_pre, independent of its parity outcomes. Its actual prefix
price may depend on the transcript when addressed prices differ. C_pre
denotes the full expected prefix price, including that dependence;
it is field independent. The source identity below does not require
constant price on different preparation transcripts.

The measured-address and READY archive are deterministic functions of
the retained parity bits. For the complete classical-quantum preparation
state, whose conditional fresh quantum work is pure,

    H_phi(preparation) = mK h_phi(s),
    S_pre = C_pre - mK h_phi(s).

This is the entropy of the new all-trials schedule. It is not the
geometric stopping-time entropy of the original early-stopped bank.
All initial data and this generated preparation word are held fixed
in the geometric/matter variation; unconstrained initial-state Euler
equations are not eliminated by this statement.

## 4. Common query time and the preserved full source

Launch the owned finite-horizon determinant experiment only on READY,
after the fixed prefix. Under the held operational-clock-to-u map,
its first addressed query occurs at the same physical time for every
READY transcript. A prescribed first-query time can be obtained by
starting this same finite prefix at its corresponding earlier clock
position. This removes the random preparation offset without any free
waiting or branch-dependent relabelling of the field.

There are two separate scope limits. First, this does not identify the
fundamental physical clock. Second, every later detector retry must
still use the original theorem's same addressed field y. If retries
instead sample an evolving field at their current execution times,
the geometric survival law must be recomputed. Likewise, sequential
banks on different lattice sites require their actual global schedule;
equal local preparation lengths alone do not synchronize prior random
detector durations across the lattice.

For the unchanged common post-READY experiment and its complete records,
the cost and entropy chain rules give the exact identity

    S_total(y) = S_pre + alpha S_N(y),
    D S_total = alpha c_N D j.

No conditioning away of abort branches is used. The prefix law is
field independent, and its pure retained complement factors from the
identical READY experiment in each complete classical branch.

Consume the owned estimate r<53/100 and choose finite K so that
m(53/100)^K <= 1/2. Then alpha >= 1/2. With the same integer run-stage
price as the determinant owner, |c_N|>0.39 gives

    |alpha c_N| > 0.195.

For identical local banks on the actual original block copies this is
one common nonzero factor multiplying the entire J2 first source,
including all 16+24+2 rows and the unchanged lambda_minus. There is no
single global all-ready event whose probability decays with the number
of lattice blocks. Physical simultaneous scheduling remains the explicit
interface just stated.

This closes a branch-dependent preparation-clock premise of the existing
conditional source construction. It does not select the compulsory field
query, the literal Book03 Info, moving native query preparation, or the
full H+J+R action. In particular, a fixed-duration bank need not minimize
price among banks allowed to finish at different times.

## 5. Verification scope

`check_fixed_clock_preparation_bank.py` checks the changed scheduling
and complete-leaf identities with exact rational arithmetic on small
finite examples: reverse routing, all-failure retention, seed-dependent
signs, common operation counts, READY mass, and the full unconditional
cost/entropy source factor. It consumes the existing parity gadget and
determinant-source theorem; it is not another Golden extractor checker
or a replay of the historical GR geometry.
