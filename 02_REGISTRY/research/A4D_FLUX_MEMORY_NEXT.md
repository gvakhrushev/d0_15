# Flux memory reading of the commuting B rigidity

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input: `3a5b0e3f206a8597f8ff4a798188a1d683ef7b4d`.
Status: retained current interpretation; the source-sequence task has the
exact negative terminal in [Section 10 of the source-image owner](A4D_SOURCE_IMAGE_COLLAPSE.md#10-exact-terminal-prescribed-smooth-limit-sources-defeat-the-raw-owner-norm).

The periodic commuting `B` theorem already is the laser-spot cut for this class. Arbitrary phase amplitudes `t_p` in the real chart produce plaquettes `exp(delta_p B)` with `sum delta_p = 0`. The Gram response is `gamma(delta_p) m` with `gamma` injective. A phase-common source forces every increment to vanish, so the source image is `{0}` before `E_K=0` is imposed. A smooth sampled source then forces the fast response in this sector to be `O(h^infty)`.

The microscopic pattern is not the transported object. The shared-face current sees only the increments. Even and odd parts must not be confused: `gamma` is odd, so `t` and `-t` share no response class.

The [full-link current theorem](A4D_COMMUTING_B_FULL_LINK_CURRENT_RIGIDITY.md) now retains arbitrary spatial links in the same B subgroup. At eta, the full Ward equations and shared-link conservation make the magnitude of `Xi=z*m` constant; independently prescribed uniformly C5 sources give the unweighted normalized bound `3 M5 h`. On the fixed curved warp, spatial B plaquettes do not enter the three diagonal source slots, so every bounded-source full-B completion is excluded on fine meshes.

For the stronger fixed-smooth-source formulation, noncommuting spatial compensation remains unresolved. The same owner derives the exact all-field identity `E_K,0[B]=sum_i D_i^- J_i+sum_i T_i(x-e_i)`, with `T_i` the spatial adjoint-transport torque. The common-subgroup torque is zero and its constitutive current is the owned divergence

```text
E_K,0[B] = sum_i D_i^-(w_i sqrt(1+3 z_i^2))
```

Stationarity is conservation of a flux built from the response slots in that subgroup. Beyond it, both the torque and the response projection must be controlled on the exact joint/source equations; dropping the torque or keeping only a scalar harmonic flux is insufficient.

[The harmonic/sign audit](A4D_SOURCE_IMAGE_COLLAPSE.md#9-audit-of-the-proposed-harmonic-plus-sign-terminal) fixed the correct terminal. At fixed Q, one exact prescribed source fixes Xi, although finer harmonic current memory can vary. Ordinary divergence also does not control the raw owner norm. [The source-first exact inverse](A4D_SOURCE_IMAGE_COLLAPSE.md#10-exact-terminal-prescribed-smooth-limit-sources-defeat-the-raw-owner-norm) now realizes the predeclared source `tau_h=h^4*sigma*m` by exact joint links and gives a normalized raw response gap of exactly 6 from the designated identity comparator at every mesh. Its smooth interpolants tend to zero in C3. This supplies the negative terminal for the selected source-sequence convention.

Verdict: `A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO` for the raw owner norm with independently prescribed sources converging to a smooth limit. The fixed-smooth-source problem and the physical continuum theory are not decided by this topology obstruction. Further carrier certificates are not required to close the selected task.
