# SPARC rotation-curves test — D0 phason dark-matter halo (real 175-galaxy data)

Data: SPARC mass models, Lelli+2016 (Vizier J/AJ/152/157 table2.dat), 3391 points / 175 galaxies.
SHA256 in manifests/sparc.json; raw data gitignored. Fetch: fetch/fetch_sparc.sh.
Ran the corpus's own data-gated cert: 05_CERTS/vp_sparc_phason_halo_failure_diagnostics.py (now unblocked).

RESULT (real data): **the simple archive-phason halo FAILS.**
- shape-only kernel: FAIL — fits WORSE than baryon-only (no dark matter at all) in **159/175 = 91%** of galaxies
  (a working DM halo must BEAT baryon-only; the phason radial-smoothing kernel makes it worse).
- one-global-scale: 34/175 (19%) worse; aggregate FAIL.
- Failure modes: DISK_DOMINATED 105, GLOBAL_SHAPE 33, GAS_DOMINATED 11, OUTER_TAIL 10, INNER_SLOPE 6.
- Corpus's own recommendation: "Reject simple radial smoothing kernels; next operator must include
  hull-boundary response without per-galaxy halo tuning."

VERDICT: **honest NEGATIVE.** D0's naive phason dark-matter halo does not fit galaxy rotation curves. The
corpus labels this honestly (a failure-diagnostics cert, not a claimed success). Dark-matter front is OPEN:
the simple kernel is rejected on real data; a hull-boundary-response operator is the named (unbuilt) next step.
