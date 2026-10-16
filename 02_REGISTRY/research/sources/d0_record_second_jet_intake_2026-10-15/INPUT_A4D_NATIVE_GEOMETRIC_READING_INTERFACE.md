# A4D_NATIVE_GEOMETRIC_READING_INTERFACE

**Task:** EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE (PR #310)  
**Label:** NATIVE-RECORD-2JET-SOURCE-GR  
**Date:** 2026-10-15  
**Status:** FORMAL INTERFACE DRAFT — connects verified kinematic germ to source-completeness lemma

---

## 1. The Geometric Reading Interface

This document defines the mathematical interface `Pi_h: Omega_h -> (g_h, chi_h)` that connects native D0 operations to geometric observables. It is constructed from verified components and explicitly marks every item that remains hypothetical.

### 1.1 Carrier Space

**Definition 1.1** (Admissible state space). `Omega_h` is the set of native D0 configurations at scale `h` comprising:
- A finite carrier `X_h` (the recorded state space)
- A smooth family of isometric embeddings `J_h(x): H -> H_hat` for `x in X_h`
- A positive price functional `A_h: Omega_h -> R`
- A readout map `pi_h: Omega_h -> O_h` to observables

**Status:** `Omega_h` is defined constructively for the U(4) germ. Physical admission as a D0-native family remains open.

### 1.2 The Recording Projector

**Definition 1.2** (Recording projector). For each `x in X_h`, the recording projector is:
```
P_h(x) = J_h(x) J_h(x)^
,    J_h(x)^
 J_h(x) = I_H
```

**Verified for the U(4) germ:** With `J_U psi = sqrt(p)|0>psi + p|1>U psi`, we have `J_U^
 J_U = I_4` exactly when `p + p^2 = 1`.

### 1.3 Induced Positive Metric

**Definition 1.3** (Record metric). The induced positive metric on parameter space is:
```
q_{mu nu}(x) = (1/(2d)) Re Tr_{2d}(d_mu P_h(x)  d_nu P_h(x))
            = (p^3/d) Re Tr_d(d_mu U(x)^
  d_nu U(x))
```

**Verified:** At the germ origin, `q(0) = p^3 I_4`.

### 1.4 Levi-Civita Connection

**Definition 1.4** (Induced Levi-Civita connection). The Levi-Civita connection of `q` is:
```
Gamma^rho_{mu nu} = q^{rho sigma} <E_sigma, d_mu d_nu P>
b_{mu nu} = d_mu d_nu P - Gamma^rho_{mu nu} E_rho
```
where `E_sigma = d_sigma P` and `<X,Y> = Re Tr(X^
 Y)`.

**Verified:** `Gamma` is symmetric in `mu,nu` and `b_{mu,nu}` is normal to all tangent directions.

### 1.5 Lorentzian Signature Map

**Definition 1.5** (Observer-line signature). For a timelike observer-line `t(x)`, the Lorentzian metric is:
```
g = 2(qt)(qt)^T / (t^T q t) - q
```

**Properties:**
- `g` has signature `(+---)`
- `g t = q t`
- The inverse map `q = 2(gt)(gt)^T / (t^T g t) - g` has rank-10 differential

**Verified:** The signature reflection preserves the rank-10 source structure.

**Open:** The observer-line `t` must be derived from native causal current, not postulated.

---

## 2. Source-Completeness Lemma (Verified)

### 2.1 Statement

**Lemma 2.1** (Source-completeness). Let `n_A` for `A = 1,...,10` be the normal directions to the immersion `P` at `x = 0` obtained from `C_{mu nu}`-variations. Let:
```
B_{(mu <= nu), A} = <b_{mu nu}, n_A> / (2d)
```

Then `B = p^3 I_{10}` and `rank(B) = 10`.

**Consequence:** If `delta S = integral E^{mu nu} delta q_{mu nu}` for all normal variations `delta P = sum_A f^A n_A`, and `delta S = 0` for all such variations, then `E^{mu nu} = 0`.

### 2.2 Proof Summary

1. The ten normal directions `n_A` are obtained from variations `delta U = i C_A eps` where `C_A` are the ten generators orthogonal to all `A_mu`.
2. The second fundamental form `b_{mu,nu}` is computed via the Gauss formula from the Levi-Civita connection.
3. In the inner product `<X,Y> = (1/(2d)) Re Tr(X^
 Y)`, the matrix `B_{(mu<=nu),A}` evaluates to `p^3 I_{10}` by direct computation.
4. The negative controls confirm necessity:
   - Removing one `C` direction drops rank to 9
   - Setting all `C = 0` drops rank to 0 while preserving `q(0)` and `dU(0)`

### 2.3 Quantitative Bound

The minimal singular value of `B` is `sigma_min(B) = p^3 = (sqrt(5)-1)^3/8 approx 0.236`.

For any metric covector `E`:
```
||E|| <= (2 p^3)^{-1} ||E_normal||
```

where `E_normal` is the pullback to normal variations.

---

## 3. The Full Price Functional

### 3.1 Structure

The full native price on `Omega_h` has the form:
```
A_h = H + J + R + Info + normalizer
```

where:
- `H` = heat/geometry contribution
- `J` = chronological feedback
- `R` = archive/retained matter
- `Info` = coherent record information
- `normalizer` = partition correction

### 3.2 What Is Ready for Substitution

From `A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md`, the following are established:

| Component | Status | Formula Reference |
|---|---|---|
| Full source covector `dR_A` | Ready | Eq. (7) of continuation |
| Costate recursion `C_{n,k}` | Ready | Eq. (6) of continuation |
| Channel generator `G_r` | Ready | Eq. (8) of continuation |
| Moving normalization derivative | Ready | Eq. (3) of continuation |
| Frame lift `L0, L, Theta` | Ready | Eq. (6) of chronological reduction |
| Uniform error transfer | Ready | Eq. (13) of chronological reduction |

### 3.3 What Remains to Connect

| Gap | Blocker |
|---|---|
| `H` on the U(4) germ | Need to define `beta` and `Q` for this family |
| `J` on the U(4) germ | Need `U_n` and `c` for the specific generators |
| `Info` binding | Need `sigma(x)` and `mu` for the germ |
| `chi` (resonant modes) | Need to map U(4) parameters to resonant amplitudes |

---

## 4. Dependency Graph

```
Fibonacci trace preparation (A4D_NATIVE_AF_TRACE_PREPARATION)
    |
    v
Golden recording isometry J_U (verified: p + p^2 = 1)
    |
    v
Second-jet germ U(x) = exp(iH(x)) (verified: rank(B) = 10)
    |
    +--> Metric q = p^3 I (verified)
    +--> Curvature R = -6/p^3 (verified)
    +--> Source-completeness B = p^3 I_10 (verified)
    |
    v
[OPEN BRIDGE] Native action A_h on this family
    |
    +--> Need: H(beta, Q) for germ parameters
    +--> Need: J(z, F) for germ feedback
    +--> Need: Info(sigma, mu) for germ state
    +--> Need: chi resonant amplitudes
    |
    v
Stationary descent: dA_h = 0 on ker(D pi_h)^perp
    |
    v
Source-completeness: E_geom = 0 from B^* E = 0
    |
    v
Einstein-response theorem substitution
```

---

## 5. The Critical Open Question

The verified kinematic germ answers the question: "Can record variations see all metric equations?" The answer is **yes** for this germ.

The remaining question is: "Does the full native price on this family actually produce the right-hand side structure?"

Specifically, for the formula:
```
d A_h = (D Pi_h)^* (E_geom + E_matter/archive) + r_h
```

we need to verify that:
1. `E_geom` is independently defined from the geometric reading `Pi_h`
2. `E_matter/archive` comes from the native action on the same family
3. The residual `r_h` is controllable (goes to 0 with refinement)
4. The right inverse `W_h` satisfies `||W_h|| <= C h^{-nu}`

---

## 6. Recommended Next Computations

### 6.1 Immediate (can be done with current tools)

1. **Compute `J` on the U(4) germ.** Use the two-tick golden block `F = 4p^3 vv^T` and verify `dJ = 0` for the specific generators.

2. **Compute `Info` on the germ.** Use the coherent state `sigma(w)` from the audit and compute `D(sigma||mu)` for variations along `A_mu` and `C_{mu nu}`.

3. **Map to resonant chi.** Express the U(4) generators in terms of the `chi_1, chi_2` amplitudes from the resonant synthesis.

### 6.2 Medium-term (requires additional structure)

1. **Derive `beta(h)` from the Fibonacci tower.** Use the trace-band width `1/(F_{N+1} F_{N+2})` and the refinement schedule to get a scale law.

2. **Construct the right inverse `W_h`.** Use the explicit `B = p^3 I_{10}` to build `W_h = B^{-1}` and estimate its norm under refinement.

3. **Verify the cubic channel.** Compute the full `Cost-Info` contribution to `Re(chi_1^2 - chi_2^2)` and compare with `32/49`.

---

*This interface document is a formal bridge. It does not claim that the U(4) germ is physically admitted by D0. It provides the verified kinematic structure needed for that admission to be tested.*
