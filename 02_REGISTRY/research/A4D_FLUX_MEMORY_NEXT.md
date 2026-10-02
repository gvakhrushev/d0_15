# Flux memory reading of the commuting B rigidity

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `3a5b0e3f206a8597f8ff4a798188a1d683ef7b4d`.
Status: reading of an owned class theorem. No task terminal.

The periodic commuting `B` theorem already is the laser-spot cut for this class. Arbitrary phase amplitudes `t_p` in the real chart produce plaquettes `exp(delta_p B)` with `sum delta_p = 0`. The Gram response is `gamma(delta_p) m` with `gamma` injective. A phase-common source forces every increment to vanish, so the source image is `{0}` before `E_K=0` is imposed. A smooth sampled source then forces the fast response in this sector to be `O(h^infty)`.

The microscopic pattern is not the transported object. The shared-face current sees only the increments. Even and odd parts must not be confused: `gamma` is odd, so `t` and `-t` share no response class.

The [full-link current theorem](A4D_COMMUTING_B_FULL_LINK_CURRENT_RIGIDITY.md) now retains arbitrary spatial links in the same B subgroup. At eta, the full Ward equations and shared-link conservation make the magnitude of `Xi=z*m` constant; independently prescribed uniformly C5 sources give the unweighted normalized bound `3 M5 h`. On the fixed curved warp, spatial B plaquettes do not enter the three diagonal source slots, so every bounded-source full-B completion is excluded on fine meshes.

What remains is noncommuting spatial compensation, not a new circle census. The same owner derives the exact all-field identity `E_K,0[B]=sum_i D_i^- J_i+sum_i T_i(x-e_i)`, with `T_i` the spatial adjoint-transport torque. The common-subgroup torque is zero and its constitutive current is the owned divergence

```text
E_K,0[B] = sum_i D_i^-(w_i sqrt(1+3 z_i^2))
```

Stationarity is conservation of a flux built from the response slots in that subgroup. Beyond it, both the torque and the response projection must be controlled on the exact joint/source equations; dropping the torque or keeping only a scalar harmonic flux is insufficient.

[The harmonic/sign audit](A4D_SOURCE_IMAGE_COLLAPSE.md#9-audit-of-the-proposed-harmonic-plus-sign-terminal) now fixes the next terminal. At fixed Q, one exact prescribed source fixes Xi, although finer harmonic current memory can vary: the mandatory Y vacuum provides the exact source-null witness. Ordinary divergence also does not control the raw owner norm. The next obligation is one refinement-uniform source-image bound for the full quartic shared-link constraints, or one predeclared admissible source separated from the designated response. A further family certificate does not meet that obligation.

Verdict: the full-link commuting B smooth-source image collapses at eta and is infeasible for bounded sources on the fixed warp. The proposed harmonic/sign terminal implication is invalid; the unrestricted source-image estimate remains open. No Einstein terminal.
