# D0 v15 Fractal Continuum and Witness Halting Proof

## Scope
This document integrates Researcher A contributions on the fractal tick continuum envelope and Möbius-Witness topological halting, with the required algebraic corrections for semigroup uniqueness and orbit averaging.

## 1. Fractal Tick Substrate and Continuum Envelope

The stable detector-clock tick is defined by the recurrence

\[
A_{n+1} = q A_n, \qquad B_{n+1} = B_n + (1-q) A_n
\]

with \( q = \varphi^{-1} \), \( 1-q = \varphi^{-2} \).

This is the integer sampling of the continuous semigroup

\[
\frac{dA}{ds} = -\kappa A, \qquad \frac{dB}{ds} = \kappa A, \quad \kappa = \log \varphi.
\]

Solutions:

\[
A(s) = A_0 e^{-\kappa s}, \qquad B(s) = B_0 + A_0 (1 - e^{-\kappa s}).
\]

## 2. Semigroup Uniqueness (Correction)

The functional equation for the envelope must satisfy the corrected multiplicative form for uniqueness under the retained-archive split:

\[
A(s+t) = \frac{A(s) A(t)}{A_0}.
\]

(The naive additive form \(A(s+t)=A(s)+A(t)\) is insufficient; the division by \(A_0\) normalizes the initial substrate so that the exponential solution is the unique continuous semigroup compatible with the fractal ratio \(q\).)

## 3. Möbius-Witness Topological Halting

Let the signed terminal role cycle be \(\Omega_8 = ABCD \times \{+,-\}\).

Let the witness/basepoint be \(\omega_0\). The first addressable graph-birth shell is

\[
V_9 = \Omega_8 \sqcup \{\omega_0\}.
\]

Continuous circulation inside \(\Omega_8\) accumulates the logarithmic trace gradient. A finite event occurs when this circulation closes against \(\omega_0\). This is the halt quotient \(\Omega_8 \to \omega_0\).

## 4. Orbit-Averaged Isotropic Trace Emission (Correction)

Because the trace gradient has traversed the full signed role cycle before halt, the emitted archive trace is an orbit-averaged shell emission over the group \(G_8\) of symmetries of \(\Omega_8\):

\[
E_\Omega = \frac{1}{|G_8|} \sum_{g \in G_8} P_g F_N P_g^\dagger.
\]

For each terminal role symmetry \(g\),

\[
g E_\Omega g^{-1} = E_\Omega.
\]

**Important correction:** This average is invariant under the group action, but it is **not** a scalar multiple of the identity unless irreducibility of the representation on the trace space is separately proved. The isotropy of macroscopic expansion is therefore the orbit-average shadow of a completed terminal detector cycle, subject to the irreducibility proviso.

## 5. Negative Controls / Guardrails
- Semigroup uniqueness fails without the \(A(s+t) = A(s)A(t)/A_0\) normalization.
- Orbit average \(E_\Omega\) cannot be treated as a scalar projector without an explicit irreducibility lemma on the representation.
- Direct promotion of the continuous envelope to a background time coordinate without the discrete tick substrate is forbidden.

## 6. Cert Tokens
- PASS_FRACTAL_TICK_SEMIGROUP_UNIQUENESS (corrected form)
- PASS_WITNESS_HALTING_ORBIT_AVERAGE (with |G8| and irreducibility note)
- FAIL_SCALAR_ORBIT_AVERAGE_WITHOUT_IRREDUCIBILITY
- FAIL_SEMIGROUP_ADDITIVE_FORM_ONLY

## 7. Book Patch Text (for Book 01)
Insert the corrected orbit-average language and the semigroup uniqueness theorem (with the \(A(s+t)=A(s)A(t)/A_0\) form) into the informational-mechanics / fractal tick section. Reference the executable witnesses in the v15 closure cert runner.

## 8. Relation to Existing Material
This document supersedes placeholder language in D0_v15_CONTINUUM_FROM_FRACTAL_TICK.md and D0_v15_TOPOLOGICAL_HALTING_ONION_HORIZON_JET.md for the algebraic details, while preserving the overall scope. The full integration appears in the Grand Synthesis layer.

(Executable support appears in the v15 closure certs: vp_fractal_tick_informational_mechanics.py, vp_continuum_from_fractal_tick.py, vp_mobius_witness_topological_halting.py.)
