# C0 inventory after code transition refactoring

`codeStep_respects_profile` now consumes the prior `stateCode_eq_iff` and `F.profile_step_congr`; its statement and assumptions are unchanged. An independent reviewer compared its type and axioms using isolated compiled caches before and after. No cyclic dependency was found. The narrow module build passed using an existing cache.

On clean `361691711324c1852b6e861837307d21ec37e417`, the six-owner compiled inventory enumerated 482 declarations. Its SHA-256 is `001e026d7b616117aa3ae7f2e47ec37d6baabaf4607e47cea2bd34ddb0639778`. Compared with inventory `7f6b25e9`, declaration names, elaborated types, axioms and type dependencies agree; proof dependencies changed for `codeStep_respects_profile` and source ranges for nine declarations. The existing cache is not fully authenticated.

On `69431c43bd9b164e45c945bf10300cf18655616e`, the three C0 views with this inventory contain 6, 44 and 30 candidates with no technical issues. Historical blob `a4a390673994ecbe7529ebae636ddd3fd6e2db7d` remains pinned; the active version must match exactly that blob, the previous `b4ec8b60a52aaa1bb3e5b1fcc40b57ba1087d43b`, or the new `4ecbb048faabcdd4b2a5a2b50141e86663d731de`. The runtime helper is not authenticated by the selected snapshot. Semantic C0 acceptance was not assessed.

On the same `69431c43` snapshot, cached `D0.All` passed 4,822 jobs, 44 targeted tests passed, and `validate_repo.py` and `generate_lean_views.py --check` passed. The complete build log is preserved byte-for-byte in `lean_final.log.gz`; its uncompressed SHA-256 is in `views_receipt.json`. This is not a cold build or a physical result; `GR_closed=false`.
