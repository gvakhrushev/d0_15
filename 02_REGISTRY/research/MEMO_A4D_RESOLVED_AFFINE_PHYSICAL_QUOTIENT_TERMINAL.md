# MEMO A4D — resolved affine physical quotient / TERMINAL inventory (PR #201)

**Task:** `EXP-A4D-RESOLVED-AFFINE-PHYSICAL-QUOTIENT`  
**Execution:** PR #201  
**Status:** REVIEW / OTO upper-wall deliverable complete  
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`  
**Primary memo:** `02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PHYSICAL_QUOTIENT.md`

## EXACT / CERTIFIED (load-bearing OTO upper wall)

| Terminal | Statement | Certificate |
|---|---|---|
| F5 Einstein detector | `K_star,metric(k) = (1/4) K_E_eta(k)` exactly over Q on all ten `k_a k_b` coeffs => `beta_sp = 0` | `a4d_star_qr_einstein_detector_check.py` |
| Q-order control | `R_{2|1} = O(eps^5)` near flat => `Q(R) = O(eps^10)`; flat quadratic Hessian of Q is identically zero | same |
| Trial-family F5 | every `S_trial = S_star + Q(R)` inherits the same pure Einstein ray | same |
| H1 on generic controls | on quotient-complete strata `Crit(S_star+Q)/G_aff ≅ Crit(S_star)/G_Lor` | structural + landed `ker J_L = im D_L` |
| Scoped physical dimensions | on declared generic curved principal stratum `d_A = d_E = d_P,aff,generic = 2` | `a4d_star_qr_physical_survival_check.py` |

## OPEN / DEFERRED (not blocking Ready)

| Item | Status | Owner |
|---|---|---|
| Stationary-auxiliary on graph-closure / rank-changing seam | OPEN | graph-closure seam; feeds #202 |
| Global `d_P,aff,res` across flat rank seam (196 vs 192) | OPEN / stratified | Q dormant at `L=I`; limiting incidence not promoted to gauge |
| Continuum Einstein field equations | NOT CLAIMED | out of scope |
| Nondegenerate curved critical point of star dynamics | OPEN | PR #202 |

## Boxed terminals

- `K_star,metric(k) = (1/4) K_E_eta(k)` with `beta_sp = 0`
- `R_{2|1} = O(eps^5)`, `Q(R) = O(eps^10)`
- `Crit(S_star+Q)/G_aff ≅ Crit(S_star)/G_Lor` on generic quotient-complete strata
- `d_A = d_E = d_P,aff,generic = 2`
- `TERMINAL: A4D-STAR-FLAT-METRIC-HESSIAN-IS-PURE-EINSTEIN-RAY`

No continuum Einstein field equations are claimed.

## Validation (re-run)

```bash
python3 02_REGISTRY/research/certificates/a4d_star_qr_einstein_detector_check.py
python3 02_REGISTRY/research/certificates/a4d_star_qr_physical_survival_check.py
python3 tools/validate_work.py
python3 tools/validate_repo.py
```

Both certificates PASS on tip; guards PASS after retire.
