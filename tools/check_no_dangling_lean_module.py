#!/usr/bin/env python3
"""Guard: every registry `lean_module` must point to an existing Lean file.

A `lean_module` naming a module that does not exist on disk is registry rot — it falsely suggests a
Lean module backs the claim. This guard fails on any NEW dangling `lean_module` (a module file that
does not exist). The 19 pre-existing dangling pointers found in the Iter-21 sweep are GRANDFATHERED
(all on PYTHON_CERTIFIED / OPEN rows — none is LEAN_PROVED, so none is an over-claim); the set may only
SHRINK as those rows are cleared or their modules built.

Exit 0 if every non-grandfathered `lean_module` resolves to a file; 1 otherwise.
"""
from __future__ import annotations
import csv
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(REPO, "09_LEAN_FORMALIZATION", "docs", "CLAIM_TO_LEAN_MAP.csv")
LEAN_ROOT = os.path.join(REPO, "09_LEAN_FORMALIZATION")

# Iter-21 sweep baseline: dangling `lean_module` refs on cert-only/OPEN rows (NOT LEAN_PROVED).
# The set may only shrink (clear the row's pointer, or build the module).
GRANDFATHER: set[str] = {
    "D0.Edge.RamificationFromUeEffCompanion",
    "D0.Gravity.HorizonJetAndBaryonPole",
    "D0.Gravity.MeasurementHorizonEquivalence",
    "D0.Gravity.OpticalJetBackreaction",
    "D0.IM.ArchivePressureCoupling",
    "D0.IM.ContinuumFromFractalTick",
    "D0.IM.FractalContinuumAndWitnessHalting",
    "D0.IM.FractalContinuumPredictions",
    "D0.IM.FractalTick",
    "D0.IM.LogdetSecondResponse",
    "D0.IM.SelfSubstrateTrace",
    "D0.IM.StrongLogdetPressure",
    "D0.Matter.BaryonAnonymousPoleSet",
    "D0.Metrology.PSDPurification",
    "D0.Metrology.PhasonBragg",
    "D0.Metrology.Phi2Flux",
    "D0.Metrology.QuantumLimits",
    "D0.Publication.MonographStructure",
    "D0.Topology.WitnessHalting",
}


def module_exists(mod: str) -> bool:
    return os.path.exists(os.path.join(LEAN_ROOT, mod.replace(".", os.sep) + ".lean"))


def find_dangling() -> list[tuple[str, str]]:
    """Return (claim_id, module) for every `lean_module` ref that does not resolve to a file."""
    out: list[tuple[str, str]] = []
    with open(CSV, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            mod_field = (r.get("lean_module") or "").strip()
            if not mod_field:
                continue
            for part in mod_field.split(";"):
                part = part.strip()
                if part.startswith("D0.") and not module_exists(part):
                    out.append((r["claim_id"].strip(), part))
    return out


def main() -> int:
    dangling = find_dangling()
    dangling_mods = {m for _, m in dangling}
    new = sorted({(c, m) for c, m in dangling if m not in GRANDFATHER})
    stale = sorted(GRANDFATHER - dangling_mods)  # grandfathered refs now resolved/cleared (good)
    if new:
        print("FAIL: NEW dangling lean_module reference(s) (module file does not exist):")
        for c, m in new:
            print(f"  {c}: {m}")
        print("Fix: point lean_module to the real sibling, build the module, or clear the field.")
        return 1
    note = ""
    if stale:
        note = f" ({len(stale)} grandfathered dangling ref(s) now resolved -- tighten GRANDFATHER)"
    print(f"RESULT: PASS -- no new dangling lean_module; "
          f"{len(dangling_mods)} dangling ref(s) all grandfathered{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
