# The partition-corrected branch information source

Continuation of G0 in existing PR #310, consumed by the native action and
source chain. Status: **exact finite normalization theorem and joint first
variation**. No physical path/readout map, source, or action is added.

The existing branch-information cocycle derives

\[
I_\omega=\log_\varphi\!\frac{q_\omega}{\mu_\omega},
\qquad \mu_\omega=\varphi^{-C_\omega},
\]
when the action weight is already the normalized measured probability
\(q_\omega\). Book III, however, defines the scalar path weight
\(w_\omega=\varphi^{-S_\omega}\) inside a statistical sum, while the finite
Born owner normalizes raw detector responses. These two constructions agree
only after their common history/readout map and the normalization have been
proved. The algebraic correction is now explicit.

For a finite complete outcome set, let \(\mathcal N=\sum_\omega w_\omega>0\)
and let \(q_\omega=w_\omega/\mathcal N\) be the corresponding normalized
Born probabilities. With the Book III decomposition
\(S_\omega=C_\omega-I_\omega\), the code reference
\(\mu_\omega=\varphi^{-C_\omega}\), and \(w_\omega=\varphi^{-S_\omega}\),
the exact identity is

\[
I_\omega
=\log_\varphi\!\frac{q_\omega}{\mu_\omega}
+\log_\varphi\mathcal N.
\]

Consequently every admitted differentiable field variation \(V\) carries

\[
D_V I_\omega
=\frac{D_Vq_\omega/q_\omega+D_V\mathcal N/\mathcal N}{\ln\varphi}.
\]

If a source is the probability-weighted mean of the path action, its value is
\(H_\varphi(q)-\log_\varphi\mathcal N\); its derivative also contains
\(-D_V\mathcal N/(\mathcal N\ln\varphi)\). Thus a unit normalizer at one
configuration is insufficient: the earlier cocycle is the full source only
when \(\mathcal N\equiv1\) on the entire admitted family (or when a separate
owned term cancels the full derivative).

This is not the algebra-valued \(\mathcal Z_D\) of Book III; \(\mathcal N\)
here means the scalar total of raw responses for one fixed finite detector
outcome frame. The positive Born owner proves uniqueness once that raw frame
is fixed. It does not identify the Book history weight with that frame's raw
response. Nor does the current D0 ownership prove \(\mathcal N\equiv1\) for
the full history family. Those two facts remain the exact G0 binding to prove.

The Lean capsule proves positivity and normalization of the finite partition,
the corrected code-minus-action identity, recovery of the old cocycle at the
unit-normalizer base point, the full first derivative, the expected-path-action
partition identity and its joint derivative, and that
\(\log_\varphi\mathcal N\) is a common additive shift across outcomes. Every
zero-sum linear contrast therefore cancels it exactly. This classifies its
outcome-space direction; it does not show that the physical stress/readout is
such a contrast. The exact checker includes the hostile control \(q_\omega\)
constant with \(\mathcal N(t)=1+t\): even though \(\mathcal N(0)=1\), the
source omitted by the uncorrected formula is \(1/\ln\varphi\) at the base
point.

This composes with the conditional Ward/scene result
[`d0_ward_scene_constitutive_closure_2026-10-15/RESULT.md`](sources/d0_ward_scene_constitutive_closure_2026-10-15/RESULT.md),
especially its exact joint scene variation (11). That result derives a
candidate scene source from \(B+R\), then explicitly leaves the native field
map and its identification with full Cost-Info open. If history weights and
Born outcomes are eventually shown to share one finite frame, the partition
theorem requires carrying the shared normalizer jet through the same pullback
before testing the complete source against the Ward hypotheses. The common-
mode cancellation says exactly which balanced contrasts can ignore it and
which source components cannot. No identification of the normalizer
correction with a metric trace, or of (11) with full D0 stress, is made here.

The current complete first-jet instrument-interface witness provides an
exact normalizer control on a real constrained field tangent:
[`A4D_NATIVE_FIELD_TO_INSTRUMENT_JET_BOUNDARY.md`](A4D_NATIVE_FIELD_TO_INSTRUMENT_JET_BOUNDARY.md)
computes, for its fixed event \(A=\{1,2\}\),
\[
P_A=144p-\frac{177}{2},\qquad
D_\xi P_A=\lambda(189p-117),\qquad
D_\xi\log P_A
=\lambda\left(\frac{6}{71}-\frac{54p}{71}\right)\ne0.
\]
Thus the normalizer correction can vary within the complete declared
instrument first-jet family even at fixed reference returns and calibration.
Under the identification of these raw event weights with the Book path
weights, the correction to branch information is
\(D_\xi\log P_A/\ln\varphi\). The first-jet owner does not establish that
physical identification or admit either completion as a D0 solution.

For the probability-weighted path action, the Lean capsule also proves
\[
\mathbb E_q[S]=H_\varphi(q)-\log_\varphi\mathcal N,\qquad
D_V\mathbb E_q[S]=D_VH_\varphi(q)-
  \frac{D_V\mathcal N}{\mathcal N\ln\varphi}.
\]
Under the same event-weight identification, the event normalizer contributes
\[
-\frac{D_\xi\log P_A}{\ln\varphi}
=\lambda\frac{54p-6}{71\ln\varphi}>0
\]
to the expected-action source. This is only the normalizer component; the
entropy derivative remains separate. The exact calculation makes the effect
of the normalizer on this candidate source explicit without identifying it
with physical D0 stress.

Scope remains limited to finite recorded outcomes with positive probabilities.
It does not identify graph paths with instrument outcomes, prove physical
admission of the comparator, supply the joint \((q,D,b,m)\) tangent law,
bind the physical source to balanced or common-mode outcome readouts, derive a
local Ward identity, or close G0/G1, curved solutions, soundness, recovery,
GR, or the original #310/#202/#317 terminals.

Replay:

```sh
cd 03_FORMALIZATION
lake env lean ../02_REGISTRY/research/certificates/a4d_native_partition_corrected_branch_info.lean
cd ..
python3 02_REGISTRY/research/certificates/a4d_native_partition_corrected_branch_info_check.py
```
