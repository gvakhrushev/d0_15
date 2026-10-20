# Narrow comparison with concurrent retained-record update 1cb164de

Reviewer: `cost_variation`, bounded read-only subtask of existing PR #334.
Date: 20 October 2026. Earlier review pins at f22c1864 are preserved.
No upstream proof, checker, review or expected output was changed here.

## Inputs read

Remote commit: `1cb164de3753f9dbaf214ea140eb9ea21a7b9d90`.

| Artifact | Git blob | Independently computed SHA-256 |
|---|---|---|
| `02_REGISTRY/research/A4D_PROSPECTIVE_STOPPED_GOLDEN_MINIMUM_SOURCE_REVERSAL_2026_10_20.md` | `b3acbdc5bb9e9dc4e4d27504d97fafbad5279642` | `ea2016810eb5b7bbc3e41941faf66900d7c0c0b4d97c064f098275102aafc34e` |
| `02_REGISTRY/research/sources/d0_prospective_stopped_golden_2026-10-20/REVIEW.md` | `46ab0cace8d61d7cdbbb8f3cb6e1c203ea1d1db7` | `c199ff1607f7047180b51810543902927adef4ada4bc96eda496641b5546fa25` |

The owned cleanup input `MINIMAL_GOLDEN_COMPLETE_SOURCE.md` was read at
equations (8)--(13). Its local SHA-256 is
`f6a5724e087c58b4294020a59532b7117f55247013181bcd4fd30d069a649330`,
agreeing with the concurrent review's input pin.

**Verdict:** the new capped-record identities and work-entropy estimate
support the actual full-pointer differentiability/source hypothesis needed
by the all-T, arbitrary-ell extension and its active-branch minimum argument.
No contradiction with those results was found. This conclusion is at fixed
mesh and fixed branch k and retains the stated task and payment assumptions.

## What the new argument supplies

From the owned exact cleanup, for c=cos(k theta), s=sin(k theta),

    q_k(t) = [s(1-2t^2)+2ct(1-t^2)]^2 + c^2 r(t),
    r(t) = 4t^4(1-t^2).

Both the port effects and the non-clean effect are scalar multiples of
identity on the entire logical input. Thus every actual port outcome has
the same probability conditional on arbitrary prior work/logical/reference
history. Port independence does not assert independence of the conditional
logical states and requires no copying or resetting of unknown data.

For a fixed k, q_k(0)>0 and continuity give a neighbourhood with q>=q_min>0.
In that neighbourhood the repeated programme is admissible with finite
expected attempts. The complete capped port words, including the unresolved
word, satisfy

    E N_M=(1-(1-q)^M)/q,
    H_phi(ports_M)=h_phi(q) E N_M,
    C_M=(T_k+1+q) E N_M.

Hence the scalar score factor and derivative in (6a)--(6b) have the stated
signs and include the extra success tick. The geometric derivative bound
controls the fixed-branch port-source limit as M tends to infinity.

For the complete fresh-work pointer, each attempted round has one clean
work label and non-clean mass r. Conditional on any earlier full history,
its additional entropy is at most h_phi(r)+r log_phi(d). The entropy chain
rule and the sum of survival probabilities bound the full additional
conditional information by that quantity divided by q_min. Scalar port
effects are what make this bound compatible with retained data history.

Thus, denoting the actual additional work entropy by E_k(y),

    0<=E_k(y)<=C |t(y)|^4 (1+|log|t(y)||),
    E_k(y_0)=0,  D E_k(y_0)=0   for y_0 in Sigma.

The derivative conclusion follows directly from this nonnegative value
bound: smooth t has |t(y)|<=C'||y-y_0|| near y_0, so E_k(y)/||y-y_0||
tends to zero. A separate derivative bound for E_k off Sigma is not needed.

## Precise interface to the extension and envelope

Under the same fixed linear actual per-attempt ledger T+k ell, the full
specified pointer price in a neighbourhood is

    S_k^actual(y)
       = [T+k ell+D_phi(Bern(q_k(y))||Bern(p^2))]/q_k(y)-E_k(y),

up to any fixed oldRIGHT baseline. The new term is not discarded off
Sigma. At Sigma it has zero value and first derivative, so the previously
reviewed exact minimum over k and every branch multiplier are unchanged.

Consequently the active-branch argument may use F(y)=inf_j S_j^actual(y).
A genuine local minimum of F in the full admissible field neighbourhood
makes each active locally admissible S_k^actual have a local minimum.
Differentiability at y_0, now supplied by the bound above, then gives its
vanishing first source. No uniform neighbourhood over all k and no
differentiability of F are required for that implication.

## Preserved boundaries and concurrent correction

The estimates do not establish C1 regularity of the full work entropy on
an entire off-Sigma neighbourhood, a uniform k/mesh/raw216 bound, a minimum
for a finite cap, or the existence of an actual local minimum. None of
these is needed for the narrowly stated extension. The compulsory native
task, admitted repeated controller, full Book Info, fixed compiled ledger
and every additional moving source remain physical application premises.

The concurrent commit independently changes the erroneous final checker
target from -2/p^(3/2) to -1/p^(3/2), matching the earlier independent
review and the correct proof equations. It also fixes the displayed
cleanup first derivative to 2|1>J Dt, consistently with q'_k=4cs.
Preserve this upstream corrected checker rather than replacing it with
the separately recorded f22 hostile-control variant.

The concurrent REVIEW reports isolated replay and optimized hostile controls.
This comparison did not rerun that checker, the older mathematics suite,
or any expensive certificate; it claims only the narrow analytical review
above. The earlier f22 failure remains a truthful historical input result,
while 1cb164de supplies its independently corrected successor.
