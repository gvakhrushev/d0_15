# Audit of the corpus's external-data (data-gated) cert layer — accurate picture

Enumerated ~40 data-gated certs (read a *_manifest.json → local data, produce *_results/*_summary). Assessed
whether each does REAL analysis vs is a scaffold. (Note: my first crude grep over-classified 8 as "demo-
scaffolds" — spot-checking corrected this; several matched on negative-control words like "faked" or an
OPTIONAL "synthetic" mode. Corrected below.)

ACCURATE classification:
- **Data-gated scaffolds, real-capable** (do genuine analysis when given real data; this repo copy just
  doesn't ship the raw data — git-safe by design): `vp_pdg_strict_passport`, `vp_core13_shell_geometry`,
  `vp_sparc_phason_halo_failure_diagnostics` (RAN on real data → genuine 91%-worse-than-baryon negative),
  `vp_cmb_phason_flip_entropy_passport` (has a `--mode planck_pr3` for real Planck), `vp_ligo_merger_mass_defect`
  (real anomaly detection + negative controls, gated on GWTC), `vp_meson_domain_wall_pdg_passport`, etc.
- **Honestly labelled NOT-a-data-confrontation** (corpus is explicit): `vp_h0_evolving_w` — "reads NO external
  data … UNVERIFIED diagnostic … PROOF-TARGET (data confrontation open)". This matches my DESI finding (the
  DE/thawing reading is a diagnostic, not a passed passport).
- **Genuine placeholder-metric flaw (1)**: `vp_desi_bao_sde_real_data.py` synthesizes a 3-tracer sample AND
  uses placeholder metrics (`dm_rd*0.01`, "ΛCDM baseline = observed for demo"). This is a demo/hard-run
  scaffold, not a real analysis — flag: do not read its PASS as a DESI confirmation. My `test_desi_w0wa.py`
  (real DR2 data + covariance + proper w0waCDM fit) is the genuine DESI analysis.

CONCLUSION: the corpus's external-data layer is **data-gated scaffolding** (manifests + cert structure ready;
raw data not shipped — exactly the git-safe pattern), **largely honestly labelled** (un-confronted ones marked
PROOF-TARGET; SPARC marked failure-diagnostics). It is NOT "mostly fake" (my initial grep over-claimed that).
The substantive external confrontations are the ones I downloaded data for and ran: DESI-w0wa, PMNS/NuFIT,
SPARC, PDG, EW (the SCOREBOARD). One cert (desi_bao_sde_real_data) has placeholder metrics — flagged.
