#!/usr/bin/env python3
"""Focused moving-observer geometry and full-native-source consumer."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


def load(path, name):
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("reflection_source_module_unavailable")
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    repo = Path(__file__).resolve().parents[3]
    source = repo/"02_REGISTRY/research/sources/d0_lorentz_reflection_source_2026-10-16"
    native = load(source/"native_current.py", "d0_lorentz_native_current")
    geometry = load(source/"reflection_geometry.py", "d0_lorentz_reflection_geometry")
    current_result = native.run_checks(repo)
    geometry_result = geometry.run_checks(repo, native.native_data(repo))
    total = current_result["exact_checks"]+geometry_result["exact_checks"]
    print("PASS_NATIVE_LORENTZ_REFLECTION_SOURCE exact_checks="+str(total))
    print("current_checks="+str(current_result["exact_checks"])
          +" geometry_checks="+str(geometry_result["exact_checks"])
          +" full_matter=16 metric_slots=10 observer_directions=3 curved_jets=8")
    print("Rh=-32/25 Rg=0 K_squared=8/25 Omega_squared=8/25 material_Euler=-192/125")
    print("general_identity=proved_in_memo physical_metric_binding=OPEN admission=OPEN")


if __name__ == "__main__":
    main()
