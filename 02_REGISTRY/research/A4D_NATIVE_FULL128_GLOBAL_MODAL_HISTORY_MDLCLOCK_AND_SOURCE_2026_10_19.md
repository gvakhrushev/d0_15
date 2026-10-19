# Physical Book MDL consumer: original 128-channel full-history unique modal blank, native clock action and first source

19 October 2026. **EXACT FINITE-H ORIGINAL INSTRUMENT CONDITIONAL MDL THEOREM / scoped continuum first-shell theorem.** For #381 and existing #334; upstream parent pinned at `8d426a8c5c9bd670dd79492bdcf7a046e0d81e34`. **No assumption that the physical Book03 weight equals one normalized detector probability has been discharged here. GR_closed=false.**

### Distinguish Book pathwise MDL from a mean action before calculating GR

Book03 §§03.3.0–03.3.0b fixes `Z_D(k)=sum_(gamma) phi^(-S(gamma))[q(gamma)]`, with `S=Cost−Info`, memory-algebra classes, and its classical-limit minimal-code history stationarity. The [same-history information cocycle](A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md) separately proves that **IF** the complete actual detector q_omega is the physical Book history weight, then `S_omega=-log_phi q_omega`; this is not a theorem identifying the algebra-valued full Book sum with the actual stored 128-output tape. The existing [complete original-record owner](A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md) §§1,6,9 separately computes the normalized POINTER ensemble mean and its C¹ source. **Do not equate that mean with the selected modal history.**

## 1. Literal full128 one-step blank map and fixed-shell spectrum

Use the unchanged original one-round complete map with both Golden ports, all32 labels and both coefficient rows, the reference128 retained, and native `K_(blank,port0)=B=I−2p² A²=I−epsilon Delta_h/2` from the full-record owner §1. Here `p=phi^-1`, `A=hD_h/16`, `epsilon=p²h²/64`. In one original flat Fourier first shell with `Delta_h=lambda_h I16`, `lambda_h>0`, the blank effect is the positive scalar operator
```text
B=b_h I16, b_h=1−epsilon_h lambda_h/2, 0<b_h<1,
q0=b_h².
```
The conditioned B outcome leaves the normalized system shell and all retained RIGHT/reference data unchanged. Repeating the actual identical fresh rounds *without discarding old records* gives precisely `P(0^n)=q0^n). `0` is the single ORIGINAL blank-label **port0** outcome, not a sum of all blanks; blank-label port1 and every other port/label are in the complement.

### Global modal theorem with no 128^n enumeration

Take ANY different full length-n retained history `omega`, and let `j` be the first slot at which it does not have `(blank,port0)`. The full trace-preserving original instrument gives
```text
P(omega) <= P(0^(j-1), nonzero outcome at j)
         <= q0^(j-1)(1−q0) <= 1−q0.
```
This holds even if later state, RIGHT/record entanglement, or individual label probabilities are complicated: subsequent conditional branch probability is ≤1. Therefore
```text
q0^n > 1−q0
  => 0^n is the UNIQUE global maximum among ALL 128^n full histories.
```
The comparison is strict. Every other history is bounded, not omitted or approximated. It does NOT claim uniqueness among `Gamma_D(k)` Book memory classes without a typed history equivalence, nor that an externally postselected rare success is MDL.

## 2. Strong exact instance on the ACTUAL original nontrivial geometric chart

Consume the pinned [original 128 Shannon first-source receipt](sources/d0_native_full128_order_readout_2026-10-19/COMPLETE_SHANNON_SOURCE.json) (original data: L=4, h=1/4, k=(0,0,0,1), flat I16/16 and proper-Lorentz J23 variation). This receipt gives:
```text
lambda=288/25, epsilon=p²/1024,
q0=(5034167+28557sqrt(5))/5120000
  = (1−epsilon lambda/2)² = 0.9957074986784104...,
dot q0=(42633−14157sqrt(5))/5120000
      = −epsilon (1−epsilon lambda/2) dot lambda_tr,
dot lambda_tr=Tr_16(dot Delta)/16 = −144/25.
```
The LAST equality is a **trace-jet identity at scalar background**. The actually varied J23 link need not keep `Delta_h` equal to a scalar matrix. The exact modal path's FIRST SOURCE remains computable anyway, because at the base the blank Kraus `B_0` acts by a scalar on the input shell and is Hermitian; differentiating `Tr[B_t^n rho (B_t^*)^n]` at zero yields `n q0^(n−1) dot q0`, even if `dot B` mixes shell/momentum.

Choose n=1024 actual fresh rounds. Elementary rational enclosures give
```text
9957/10000 < q0 < 9958/10000;
(9957/10000)^1024 > 43/10000 > 1−q0.
```
The integer inequality is checked **exactly**, by cross multiplication of big integers, not floating-point approximation. Hence the ONE modal whole tape is unique, and its values and genuine original J23 first source (conditional on Book/Born history identification) are
```text
P(0^1024)≈0.0122163223023820;
S_MDL,1024=−1024 log_phi(q0)≈9.15393616364622;
D_J23 S_MDL,1024=−1024 dot q0/[q0 ln(phi)]
                   ≈−4.58189384505280.
```
At the SAME one-round input, the complete 128-outcome pointer Shannon source is `−0.0315467843124857...`, and the single selected blank-history surprisal source is `−0.00447450570805938...`. They are distinct physical readouts even on one instrument. Neither equals the full Book source without the compulsory same-history binding.

## 3. Exact modal continuum scaling, no arbitrary coupling or counterterm

For a family of strict original flat first shells with bounded `lambda_h→lambda>0`, and the **native clock** `n_h epsilon_h→beta∈(0,∞)` (integer n fixed during any smooth field tangent at each h), have
```text
q0_h=(1−epsilon_h lambda_h/2)²,
q0_h^n -> exp(−beta lambda)>0,
1−q0_h = epsilon_h lambda_h+O(epsilon_h²)->0.
```
Consequently the actual full-history `0^n` is the **unique global modal word** for all sufficiently fine h (NO new code-length optimisation or choice of z). Its conditional Book/Born MDL cost and smooth field source, for controlled `Dlambda_h→Dlambda` with fixed beta/epsilon under the variation, satisfy
```text
S_MDL,n=−2n log_phi(1−epsilon lambda_h/2)
        -> beta lambda/ln(phi),
D S_MDL,n[V] = beta_h Dlambda_h[V]/
                     (ln(phi)(1−epsilon lambda_h/2))
             -> beta Dlambda[V]/ln(phi).
```
The base is always `phi`; normalization/clock are original, not fitted. On general field tangents moving epsilon, controller or preparation, the missing variations MUST be restored. The actual original owner §6 instead proves normalized **full-pointer ENSEMBLE** entropy `H_pointer=beta_h lambda_h ln(1/epsilon)+O_C1(1)` in natural units, with a logarithmically enhanced source. The modal cost is FINITE; mean entropy has a different refinement scaling. Replacing Book pathwise MDL by a Shannon mean (or by a task-selected binary pressure) is therefore a substantial physical hypothesis, NOT a harmless change of presentation.

## 4. Exact physical implication, without overpromoting GR

This is the strongest original-observation bridge we can obtain from the current book text and original detector **without selecting a new action**:

1. If the already-complete literal 128-tape is an allowed FULL Book history at each clock cut and Book's classical MDL rule applies directly to that tape with `w=q`, the selected path is the BLANK history in this controlled flat-shell continuum regime, and its action is the exact Rayleigh/heat expression above — NOT a selected rare filled-return path, not an ensemble-mean entropy, and not the optional 718-edge Perron pressure. There is no free gravity coefficient.
2. If the actual physical histories are memory-algebra classes, or the verified event is a different conditioned programme (e.g. the ten-Golden Slater filled return) then one must explicitly provide the TYPED map, its native admissibility, boundary/source normalization and same-history Book price. One cannot claim an Einstein-derived action merely by moving between these three sample spaces.
3. Even under the conditional binding the modal Rayleigh response is NOT a full Einstein+matter tensor and is no proof of universal gravity: it computes only an exact original instrument source in one controlled class. Coherent record, code cost, source of ordinary history selection, field/geometric Ward, moving prep/clock, full 40 rows, physical selector and raw #216 remain independent gates. `GR_closed=false`.

Reproduce [`check_full128_global_map_native_history.py`](sources/d0_physical_binary_return_2026-10-19/check_full128_global_map_native_history.py), including integer rational MAP certificate and original J23 first-source reconstruction.


## 5. Flat-source incompatibility for a **bare** modal-detector-to-Palatini identification

The original flat constant-coframe / identity-link finite Palatini vacuum has zero first Lorentz-link Euler source. The **actual** full128 readout's J23 link tangent above, however, has
```text
D_J23[-log_phi P(0^n)] = -n dot q0/(q0 ln phi)
  = [n/(ln phi)](-21519+7200sqrt(5))/2516881
  ≈ -0.004474505708059377... * n != 0,
```
so for n=1024 this is `-4.5818938450528...`. The comparison is a **typed theorem target**: if (a) the original detector J23 variation is the SAME admitted original proper-Lorentz variation on the flat Palatini field carrier, (b) the physical compulsory Book source is precisely this bare normalized full128 modal surprisal at fixed clock, and (c) no separate admissible preparation/controller/work/normalizer term contributes a compensating derivative, then this bare action **cannot equal** the original Palatini action's first source even at a flat vacuum. This is not a no-go for Book03's algebra-valued multi-history sum, for a history test with different physical `Γ_D(k)`, or for the separately owned ten-Golden Slater verification action. None of (a)–(c) has been established as the compulsory original physics.

This is the clearest physical discriminator: to promote the detector to gravity one must now supply at least one of (i) a typed same-history projection which makes the MDL history different from all blank, (ii) an ORIGINAL paid action/counterpart whose J23 source cancels the computed `-4.58189...` at the flat stationary field, or (iii) a native restriction of the tested variation with independent justification. A hand-inserted counterterm or reweighted ensemble is not permitted. An exact residual on this ONE physical tangent can be tested first, before chasing more geometric jets.

Also note that this is **pathwise** MDL and the derivative at a strict finite-n maximum. The full Book path action is algebra/memory-class valued, and there is not yet a proof that its sum is exhausted by the measured tape. Consequently the global physical GR claim remains open.
