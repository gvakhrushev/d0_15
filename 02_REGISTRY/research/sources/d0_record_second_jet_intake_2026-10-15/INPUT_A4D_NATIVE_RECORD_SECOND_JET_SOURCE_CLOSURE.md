# A4D_NATIVE_RECORD_SECOND_JET_SOURCE_CLOSURE

**Task:** EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE (PR #310)  
**Label:** NATIVE-RECORD-2JET-SOURCE-GR  
**Date:** 2026-10-15  
**Repository:** gvakhrushev/d0_15  
**Base:** main = fa2b04b9c8aae5a0b8470322d6091712ce56567a  
**Status:** PARTIAL / KINEMATIC GERM VERIFIED / SOURCE-COMPLETENESS PROVEN / THERMAL LIMIT CONFIRMED / NATIVE ADMISSION AND GR CLOSURE OPEN

---

## 1. Executive Summary

This document records the execution of the `NATIVE-RECORD-2JET-SOURCE-GR` research task. Two critical verifications were performed:

1. **Source-completeness of the U(4) second-jet germ:** The kinematic fixture `U(x) = exp(i sum A_mu x^mu + i/2 sum C_{mu nu} x^mu x^nu)` with the specific generator choice from `SYNTHESIS_RU.md` yields a record-metric `q(0) = p^3 I_4` (where `p = (sqrt(5)-1)/2`, `p + p^2 = 1`) whose normal-variation map to metric variations has **full rank 10**. This proves that all ten metric source slots are independently accessible through native record variations.

2. **Thermal window limit at beta = h:** The Hodge/CAR heat functional on the unit torus with the volume-preserving curve `q(t) = diag(4e^{2t}, e^{-2t}/4, 1, 1)` satisfies `lim_{L->infinity} dH/dt|_{t=0} = 15/32` when `beta = 1/L`. This confirms that the shape-source does not vanish even when `beta/h^2 -> infinity`.

**What remains open:** The physical admission of the U(4) germ as a native D0 family; the derivation of the full action source on that family; the quantitative right inverse bound; and the Einstein-response theorem substitution.

---

## 2. Verified: Source-Completeness of the Second-Jet Germ

### 2.1 The Fixture

The recording isometry is:

```
J_U psi = sqrt(p) |0> psi + p |1> U psi,   p + p^2 = 1
P = J_U J_U^
```

The unitary family is:

```
U(x) = exp(i H(x))
H(x) = sum_mu A_mu x^mu + 1/2 sum_{mu,nu} C_{mu nu} x^mu x^nu
```

With the generator labels:
- `A_mu`: (0,1), (0,2), (0,3), (1,0) in the Pauli-product basis
- `C_{mu nu}`: (1,1), (1,2), (1,3), (2,0), (2,1), (2,2), (2,3), (3,0), (3,1), (3,2)

### 2.2 Verified Identities

All checks from `check_record_2jet.py` passed:

| Check | Result |
|---|---|
| Golden normalization `p + p^2 = 1` | PASS |
| Partition identity `4p^3 + p^6 = 1` | PASS |
| First-jet metric `q(0) = p^3 I_4` | PASS |
| Normal second-jet orthogonality | PASS |
| Unitarity second derivative | PASS |
| **Source-completeness rank** `rank(B) = 10` | **PASS** |
| First metric derivative vanishing | PASS |
| Scalar curvature `p^3 R = -6` | PASS |
| Rank-loss negative control (`rank = 9`) | PASS |
| Linear-only normal map (`rank = 0`) | PASS |
| Observer signature reflection (`rank = 10`) | PASS |
| Fibonacci trace-band endpoints | PASS (20 levels) |

### 2.3 The Key Lemma

The source-completeness matrix:

```
B_{(mu <= nu), A} = <b_{mu,nu}, n_A>
```

where `b_{mu,nu}` is the second fundamental form of the immersion `P` and `n_A` are the ten normal directions from `C`-variations, satisfies:

```
B = p^3 I_{10}
```

in the inner product `<X,Y> = (1/8) Re Tr(X^
 Y)` (with `d=4`). Therefore `rank(B) = 10` exactly.

**Consequence:** If the pullback of a metric covector `E^{mu nu}` to all normal variations vanishes, then `E = 0`. This is the source-completeness property required for the Einstein-response theorem.

### 2.4 Negative Controls

Two critical negative controls confirm the necessity of the second jet:

1. **Removing one normal direction:** Setting one column of `B` to zero reduces rank to 9, leaving a non-zero hidden source direction.

2. **Linear-only H(x):** If `C_{mu nu} = 0` (only first-order generators), the normal map `B` becomes the zero matrix. The first jet `dU(0)` and metric `q(0)` are unchanged, but **no metric source is accessible** through normal variations. This proves that first-jet tomography is insufficient.

---

## 3. Verified: Thermal Window Limit

### 3.1 The Test

For the diagonal Hodge/CAR heat functional:

```
H = (1/beta) log(16 sum_{k in (Z/LZ)^4} exp(-beta sum_r 4L^2 sin^2(pi k_r/L) / q_r))
```

with `q(t) = diag(4e^{2t}, e^{-2t}/4, 1, 1)` and `beta = 1/L`:

| L | dH/dt | Diff from 15/32 |
|---|---|---|
| 4 | 3.8144935047 | +3.3457435047 |
| 8 | 8.5848697015 | +8.1161197015 |
| 16 | 16.5423331942 | +16.0735831942 |
| 32 | 28.0005491651 | +27.5317991651 |
| 64 | 18.5654919448 | +18.0967419448 |
| 128 | 1.8547687715 | +1.3860187715 |
| 256 | 0.4745582106 | +0.0058082106 |
| 512 | 0.4707075123 | +0.0019575123 |
| 1024 | 0.4697257395 | +0.0009757395 |
| **Limit** | **0.4687500000** | **0** |

The convergence to `15/32 = 0.46875` is confirmed numerically.

### 3.2 Analytical Proof Sketch

Using the Fourier-Bessel identity:

```
Z_1 = L e^{-x} sum_{m in Z} I_{mL}(x),   x = 2L/q
```

and the Laplace expansion `e^{-x} I_0(x) = (2 pi x)^{-1/2} [1 + 1/(8x) + O(x^{-2})]`, the `m != 0` terms are exponentially suppressed. The leading term gives:

```
log Z_1 = (1/2) log(q/(4 pi beta)) + h^2 q/(16 beta) + O(h^2)
```

At `beta = h = 1/L`, after summing four axes and applying the volume-preserving derivative:

```
dH/dt = (1/16) d/dt(sum q_r) + O(h) = (8 - 1/2)/16 + O(h) = 15/32 + O(h)
```

This proves that `beta -> 0` and `beta/h^2 -> infinity` are **not sufficient** to eliminate the shape-source. A stricter scale law (e.g., `beta = h^alpha` with `0 < alpha < 1`) or a physical `beta(h)` law is required.

---

## 4. What Is Proven vs. What Remains Open

### 4.1 Proven (Kinematic/Analytic)

- The U(4) second-jet germ is non-empty and curved.
- The normal-variation map has full rank 10: all metric equations are accessible.
- The first-jet-only truncation destroys source access (rank drops to 0).
- The thermal shape-source persists at `beta = h` with limit `15/32`.
- The observer-line signature reflection preserves the rank-10 structure.

### 4.2 Remaining Open (Physical/Native)

| Barrier | Status | Next Action |
|---|---|---|
| Physical admission of the U(4) germ | OPEN | Derive `A_mu, C_{mu nu}` from native D0 operations, not as free parameters |
| Full action source on the family | OPEN | Apply `A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md` source formulas to this germ |
| Quantitative right inverse `W_h` | OPEN | Prove uniform bound `||W_h|| <= C h^{-nu}` for the metric variation map |
| Matter/archive equations | OPEN | Verify `E_matter = 0` implies `E_geom = 0` via the full coupled system |
| Einstein-response substitution | OPEN | Substitute into existing theorem once above are closed |
| Lorentzian metric `g` from `q` | OPEN | Derive observer-line `t` from native causal current |

---

## 5. Next Steps

1. **Immediate:** Connect the verified germ to `A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md`. The source-completeness lemma is ready; the remaining work is to show that the full native price `A_h` on this family has the structure:
   ```
   dA_h = (D Pi_h)^* (E_geom + E_matter/archive) + r_h
   ```
   with `r_h` controllable.

2. **Critical:** The cubic channel `Re(chi_1^2 - chi_2^2)` from the resonant synthesis must be checked against the native Cost-Info on this same family. The coefficient `32/49` is a kinematic fact for the naked-star action; its relation to the full native action is the next computation.

3. **Scale law:** Either derive `beta(h)` from the Fibonacci tower structure or prove that the thermal source is physically retained as a matter/archive contribution.

---

## 6. Verification Log

| Script | Status | Key Output |
|---|---|---|
| `check_record_2jet.py` | **PASS** | `second_source_map_rank: 10`, `scalar_curvature_times_p3: -6` |
| `check_heat_window.py` | **PASS** | Convergence to `15/32` confirmed at `L=1024` |

---

*This document is a research artifact for PR #310. It does not claim GR closure or native physical admission. It verifies the kinematic prerequisites for the source-completeness argument.*
