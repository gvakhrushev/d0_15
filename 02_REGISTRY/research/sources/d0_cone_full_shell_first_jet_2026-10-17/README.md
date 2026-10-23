# Full-shell first-jet spectrum on the exact sampled cone

Owner: [proof note](../../A4D_CONE_FULL_SHELL_FIRST_JET_NO_GO.md).

The checker replays the exact pinned 128-dimensional first-shell resonance from the actual full16 cone corrector and computes its invariant-block spectra. It shows that no eigenspace has support on all four momentum axes, so no full-shell leading density—including the existing `P_Omega/8 tensor sigma` memory family at any internal rank—solves the projected first amplitude equation when the first geometry/link jets are fixed.

Run with Python 3.10+ and SymPy 1.14:

```sh
python3 02_REGISTRY/research/sources/d0_cone_full_shell_first_jet_2026-10-17/check_full_shell_first_jet.py
python3 -O 02_REGISTRY/research/sources/d0_cone_full_shell_first_jet_2026-10-17/check_full_shell_first_jet.py
```

The checker pins and replays `check_cone_matter_corrector.py`; the latter uses the actual creator/order definitions and its exact negative controls. The new checker does not run a root search, old heat catalogue, finite-grid simulation, or Lean build. It does not test counterjets or other support sectors.
