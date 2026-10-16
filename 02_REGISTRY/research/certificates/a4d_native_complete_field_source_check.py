#!/usr/bin/env python3
"""Focused full source, Lorentz transport, preparation and actual record heat."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


def load(path, name):
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("complete_field_source_module_unavailable")
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    repo = Path(__file__).resolve().parents[3]
    folder = repo/"02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16"
    counts = []
    for stem in ("record_frame_source", "lorentz_link_transport", "preparation_measure",
                 "record_heat_continuation", "stored_rotational_wave"):
        result = load(folder/(stem+".py"), "d0_complete_field_"+stem).run(repo=repo)
        count = result.get("exact_checks")
        if type(count) is not int or count <= 0:
            raise RuntimeError("missing_executed_checks:"+stem)
        counts.append((stem, count))
    print("PASS_NATIVE_COMPLETE_FIELD_SOURCE exact_checks="
          +str(sum(count for _, count in counts)))
    print(" ".join(stem+"="+str(count) for stem, count in counts))
    print("scope=full_source_and_native_stored_program_with_rotational_wave")
    print("native_spatial_aggregation=OPEN physical_action=OPEN GR=OPEN")


if __name__ == "__main__":
    main()
