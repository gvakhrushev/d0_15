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
unit-normalizer base point, the full first derivative, and that
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
