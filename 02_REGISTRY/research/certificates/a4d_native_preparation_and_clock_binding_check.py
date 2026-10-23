#!/usr/bin/env python3
"""Focused actual preparation Euler and matter-clock comparator binding."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


def load(path, name):
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("native_preparation_binding_module_unavailable")
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    repo = Path(__file__).resolve().parents[3]
    folder = repo/"02_REGISTRY/research/sources/d0_native_preparation_stationary_2026-10-16"
    preparation = load(folder/"preparation.py", "d0_native_stationary_preparation")
    binding = load(folder/"matter_clock_binding.py", "d0_native_matter_clock_binding")
    p = preparation.run_checks(repo)
    b = binding.run_checks(repo)
    print("PASS_NATIVE_PREPARATION_AND_CLOCK_BINDING exact_checks="
          +str(p["exact_checks"]+b["exact_checks"]))
    print("preparation_checks="+str(p["exact_checks"])
          +" binding_checks="+str(b["exact_checks"]))
    print("scope=pure_GNS_preparation_and_declared_comparator_equality_family")
    print("full_AF_instrument_equivalence=OPEN physical_admission=OPEN GR=OPEN")


if __name__ == "__main__":
    main()
