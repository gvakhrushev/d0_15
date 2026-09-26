# MEMO A4D — physical quotient TERMINAL inventory (PR #201)

**Task:** `EXP-A4D-RESOLVED-AFFINE-PHYSICAL-QUOTIENT`  
**Status:** REVIEW / OTO upper-wall complete  
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`

## Boxed terminals

- `S_STAR-CARRIES-EINSTEIN-SEED (c_sp=0, c_eta!=0)`
- `K_star,metric(k) = (1/4) K_E_eta(k)` on naked `S_star` (all ten `k_a k_b` coeffs over Q)
- `R = O(X^4 t)`, `Q = O(X^8 t^2)`; with `t=O(eps), X=O(eps)`: `R=O(eps^5)`, `Q=O(eps^10)`
- `j^2_flat Q = 0` => `j^2_flat(S_star+Q) = j^2_flat S_star`
- Q is nonlinear completion only; F5 is NOT an (a,b) search
- H1 corrected: integrate out `R=R_*(C)` after `EL_R=0`; NOT `EL_b => R=0`
- Curved roots deferred to #202
- Continuum Einstein field equations: NOT CLAIMED

## Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_star_qr_einstein_detector_check.py
python3 tools/validate_work.py
python3 tools/validate_repo.py
```
