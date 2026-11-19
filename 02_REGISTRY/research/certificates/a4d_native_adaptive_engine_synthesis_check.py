#!/usr/bin/env python3
"""Focused adaptive AF/engine, supported preparation and inherited settings."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


def load(path, name):
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("adaptive_engine_synthesis_module_unavailable")
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    repo = Path(__file__).resolve().parents[3]
    folder = repo/"02_REGISTRY/research/sources/d0_native_adaptive_engine_2026-10-16"
    counts = []
    for stem in ("adaptive_engine", "engine_preparation", "inherited_settings"):
        module = load(folder/(stem+".py"), "d0_adaptive_synthesis_"+stem)
        result = module.run(repo=repo)
        count = result.get("exact_checks")
        if type(count) is not int or count <= 0:
            raise RuntimeError("missing_executed_checks:"+stem)
        counts.append((stem, count))
    print("PASS_NATIVE_ADAPTIVE_ENGINE_SYNTHESIS exact_checks="
          +str(sum(count for _, count in counts)))
    print(" ".join(stem+"="+str(count) for stem, count in counts))
    print("scope=actual_AF_signed_engine_and_engine_supported_preparation")
    print("moving_geometry_dynamics=OPEN physical_admission=OPEN GR=OPEN")


if __name__ == "__main__":
    main()
