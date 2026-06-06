# D0 External Passport Summary

## Counters

- PASS: 4
- FAIL: 2
- SKIP: 5

PASS rows:
- Nuclear shell-contact SRC: PASS_NUCLEAR_SHELL_CONTACT_SRC_NATURE2026
- LIGO merger mass defect - all catalog: PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_ALL
- LIGO merger mass defect - clean BBH: PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_CLEAN_BBH
- SPARC data ingest: PASS_SPARC_DATA_INGEST

FAIL rows:
- SPARC shape_only kernel: FAIL_ARCHIVE_PHASON_HALO_SPARC_SHAPE_ONLY
- SPARC one_global_scale kernel: FAIL_ARCHIVE_PHASON_HALO_SPARC_ONE_GLOBAL_SCALE

SKIP rows:
- IceCube HESE phason decoherence: SKIP_NEUTRINO_PHASON_DECOHERENCE_BASELINE_REQUIRED
- CMB phason flip entropy: SKIP_CMB_PHASON_FLIP_EXTERNAL_DATA_REQUIRED
- BAO S_DE phason flip: SKIP_BAO_SDE_EXTERNAL_DATA_REQUIRED
- CKM holonomy external convention: SKIP_CKM_EXTERNAL_DATA_REQUIRED
- Meson domain-wall PDG: SKIP_PDG_MESON_EXTERNAL_DATA_REQUIRED

SPARC data ingest PASS is a data-ingest PASS only, not a physics PASS.

| Passport | Dataset | Manifest | Hash | Frozen D0 object | Baseline | Metric | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nuclear shell-contact SRC | nature2026_src | 08_PASSPORTS/NuclearSRC/nature2026_src_manifest.json | c94f273c568e843e | same-shell proton-neutron contact selector | A-only / N-Z-only / density proxy | source-data rank ordering | PASS_NUCLEAR_SHELL_CONTACT_SRC_NATURE2026 | Fe54/Ca48 integral=1.493, weighted_mean=1.4741 |
| LIGO merger mass defect - all catalog | gwosc_ligo_merger_mass_defect | 08_PASSPORTS/GWOSC/gwosc_manifest.json | fd7a6bc1912a5614 | finite merger mass-defect operator | mean loss / spin-only negative control | RMSE on all complete catalog rows | PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_ALL | rmse_spin_only_negative_control: 0.011562 |
| LIGO merger mass defect - clean BBH | gwosc_ligo_merger_mass_defect | 08_PASSPORTS/GWOSC/gwosc_manifest.json | fd7a6bc1912a5614 | finite merger mass-defect operator | mean loss / spin-only negative control | RMSE on clean BBH domain | PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_CLEAN_BBH | rmse_spin_only_negative_control: 0.00868605 |
| SPARC data ingest | sparc_archive_phason_halo | 08_PASSPORTS/SPARC/sparc_manifest.json | dfbdbb678ce5ec98 | SPARC mass-model data contract | manifest/hash/table parser | rows and galaxies parsed | PASS_SPARC_DATA_INGEST | galaxies_parsed: 175 |
| SPARC shape_only kernel | sparc_archive_phason_halo | 08_PASSPORTS/SPARC/sparc_manifest.json | dfbdbb678ce5ec98 | naive inner-memory archive-phason kernel | baryon-only residual shape | per-galaxy normalized shape correlation | FAIL_ARCHIVE_PHASON_HALO_SPARC_SHAPE_ONLY | rmse_baryon_only_residual: 10726.5 |
| SPARC one_global_scale kernel | sparc_archive_phason_halo | 08_PASSPORTS/SPARC/sparc_manifest.json | dfbdbb678ce5ec98 | naive inner-memory archive-phason kernel with one global scale | baryon-only residual | global RMSE reduction | FAIL_ARCHIVE_PHASON_HALO_SPARC_ONE_GLOBAL_SCALE | rmse_baryon_only_residual: 10726.5 |
| IceCube HESE phason decoherence | icecube_hese12 | 08_PASSPORTS/IceCube/icecube_manifest.json | 8b3ebbc0a8ad6ea0 | Hurwitz phason decoherence kernel | no-decoherence baseline protocol | HESE event curve generated; baseline statistic required | SKIP_NEUTRINO_PHASON_DECOHERENCE_BASELINE_REQUIRED | baseline_ready: false |
| CMB phason flip entropy | planck_cmb_phason_flip_entropy | 08_PASSPORTS/PlanckCMB/planck_manifest.json | cc006d85b80b24ce | phason-flip entropy operator | LambdaCDM-only residual null | multipole entropy residual | SKIP_CMB_PHASON_FLIP_EXTERNAL_DATA_REQUIRED | missing: cl_spectrum,mask_or_likelihood,multipole_range,sha256,status_READY |
| BAO S_DE phason flip | desi_bao_sde_phason_flip | 08_PASSPORTS/DESI/desi_dr2_manifest.json | 52756a8144355414 | S_DE phason-flip archive transfer | constant-shape BAO baseline | BAO residual/covariance response | SKIP_BAO_SDE_EXTERNAL_DATA_REQUIRED | missing: z_eff,dm_rd,dh_rd,covariance,sha256,status_READY |
| CKM holonomy external convention | ckm_holonomy_external_convention | 08_PASSPORTS/CKM/ckm_manifest.json | 34174e64ab5750e9 | CKM phason holonomy matrix convention | PDG convention table | unitarity/convention residual | SKIP_CKM_EXTERNAL_DATA_REQUIRED | missing: Vud,Vus,Vub,Vcd,Vcs,Vcb,Vtd,Vts,Vtb,sha256,status_READY |
| Meson domain-wall PDG | meson_domain_wall_pdg | 08_PASSPORTS/PDG_Meson/pdg_meson_manifest.json | 75ec023e8e578010 | meson phason domain-wall selector | PDG mass-width table | domain-wall class residual | SKIP_PDG_MESON_EXTERNAL_DATA_REQUIRED | missing: particle_id,mass,width,quantum_numbers,sha256,status_READY |

PASS means a pinned external-data manifest was complete and the declared comparison executed. SKIP means either source data are incomplete or the observable baseline/kernel comparison is not implemented yet; see Notes.
