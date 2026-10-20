#!/usr/bin/env python3
"""Immutable narrow certificate for native stopped minimality and its source.

Checks stay active under optimization. The historical failed f22 checker is
retained as evidence and is not executed as a passing certificate.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]

INPUTS = ['02_REGISTRY/research/A4D_NATIVE_STOPPED_MINIMUM_TO_J2_SOURCE_2026_10_20.md',
 '02_REGISTRY/research/A4D_PROSPECTIVE_STOPPED_GOLDEN_MINIMUM_SOURCE_REVERSAL_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/CORRECTED_REPRODUCTION.log',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/FINAL_STOPPED_OVERVIEW_ACCEPTANCE.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/PROVENANCE.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/README.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/SHA256SUMS.json',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/SOURCE_INPUTS.json',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_1CB_RETAINED_RECORD_COMPARISON.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_ALL_COST_RESULT.json',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_ALL_COST_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_ALL_PREFIX_REVIEW_ADDENDUM.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_ALL_PREFIX_SECOND_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_GENERAL_GATE_PRICE_REVIEW_ADDENDUM.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_CURRENT_REPLAY.json',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_CURRENT_REPLAY.log',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_REPRODUCTION.json',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_REPRODUCTION.log',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_TARGET_CORRECTION.patch',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/VALIDATION.json',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/check_stopped_all_cost_source.py',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/corrected_check_stopped_source_minimum.py',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/upstream_check_stopped_source_minimum.py',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/upstream_reviewed_stopped_proof.md',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/upstream_stopped_proof.md',
 '02_REGISTRY/research/sources/d0_prospective_stopped_golden_2026-10-20/REVIEW.md',
 '02_REGISTRY/research/sources/d0_prospective_stopped_golden_2026-10-20/check_stopped_source_minimum.py']

PINNED_SHA256 = {'02_REGISTRY/research/A4D_NATIVE_STOPPED_MINIMUM_TO_J2_SOURCE_2026_10_20.md': '6e73ece4f1d4312e241e91860871019689bf28017088ef6431893a3286978b0b',
 '02_REGISTRY/research/A4D_PROSPECTIVE_STOPPED_GOLDEN_MINIMUM_SOURCE_REVERSAL_2026_10_20.md': 'ea2016810eb5b7bbc3e41941faf66900d7c0c0b4d97c064f098275102aafc34e',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md': 'f6a5724e087c58b4294020a59532b7117f55247013181bcd4fd30d069a649330',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/CORRECTED_REPRODUCTION.log': 'ae3868f90b3ace0dd3593de00e8b3831a65ca3330d1dcc0543afb6f5c9017d8d',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/FINAL_STOPPED_OVERVIEW_ACCEPTANCE.md': '298042606edc05c91cb0f25fe86f693b8dc7856632a88db33ebeccdc376333ec',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/PROVENANCE.md': 'd06f00e709af5a420252f32d3abd72684f0f9bfce90023867dccd2d992781d62',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/README.md': '59f4d91ed1643bf3aedbcfb0bd5af854f2b82eddfa6982c4bb037a6176ac5fe9',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/SHA256SUMS.json': 'd480afa570f8f7a525228b5c9772083aad98a341aee82095c6df2e3ee16285c3',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/SOURCE_INPUTS.json': 'e2cb97fa3380a3c0dfa633ca393f3c4c1a8a970b4dcbdd24ae02d45479253564',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_1CB_RETAINED_RECORD_COMPARISON.md': 'a53e06653c8ef656bba32fc7f5e262acff5d5143c311a0d48003dc6b583e1463',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_ALL_COST_RESULT.json': 'b972503e95f0329700e3cc3544e6246cc8c896c5a9ebc3aef41c02ff06b71c6d',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_ALL_COST_SOURCE.md': 'ba7513a46fd7796ce6f5ae6d1ad389d66e51bbcaff3ca8866c0087dc41539eb3',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_ALL_PREFIX_REVIEW_ADDENDUM.md': 'd1ed274cf2696fd65094b4ac398d93b8ba4f8af7f8b7cb4844695d9b7d341979',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_ALL_PREFIX_SECOND_REVIEW.md': 'c9734b128e631226e37e1208adaa930ae8c2d96d28c0b35285c21b32f74c5ea0',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/STOPPED_GENERAL_GATE_PRICE_REVIEW_ADDENDUM.md': 'ce9b85e07d45f5a9c683c0d219c9cc96106e9b5863bb6bbe066c21661128537d',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_CURRENT_REPLAY.json': '4da4e9b9efceb6ce7028dc1333db0e10ab0ea42af9239e51e156651c7956ad22',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_CURRENT_REPLAY.log': 'bf0ae04a772374a8683e261d3daaa1749da6d2541940351973926963dda890b1',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_REPRODUCTION.json': '4eb5320f7ce8fc4e57010ad9933212d337135ffad408c63b47bdd1292a754e90',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_REPRODUCTION.log': '1e58a8f76618a2d733facbeaa23135fc48539450b6157fbcaa48a3af1d2a596c',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/UPSTREAM_TARGET_CORRECTION.patch': 'c08c7806059a61e3cab0372d236882317c7ffe838d9eaf3eaaaf9f9b83257026',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/VALIDATION.json': '4e57ada85f482ae6203fa676bd717faecc2aeffa7f31fbf08a37d985ce02b822',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/check_stopped_all_cost_source.py': '281d67f5668c6ee01d5a6c0e647d6a4806154fa7a20676be871053cca9309dc9',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/corrected_check_stopped_source_minimum.py': 'e6f20aa5c9850635165cdaff08f7c4799cdd441aced84be2d64739ac771f901f',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/upstream_check_stopped_source_minimum.py': 'e022977c672f9c64c9c3ee27d652b009508a2b584b46232ec88c270ff61bbe70',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/upstream_reviewed_stopped_proof.md': 'ea2016810eb5b7bbc3e41941faf66900d7c0c0b4d97c064f098275102aafc34e',
 '02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20/upstream_stopped_proof.md': '1e2815efc4daab717a7b84069607e287330360093d5a6eaedcfb55c080f9681a',
 '02_REGISTRY/research/sources/d0_prospective_stopped_golden_2026-10-20/REVIEW.md': 'c199ff1607f7047180b51810543902927adef4ada4bc96eda496641b5546fa25',
 '02_REGISTRY/research/sources/d0_prospective_stopped_golden_2026-10-20/check_stopped_source_minimum.py': 'a8997f58d3af738a2cf70f4a1d20dd6c9c509274c8e9b2393157a50038e2729d'}

PACKET = ROOT / "02_REGISTRY/research/sources/d0_native_stopped_all_cost_source_2026-10-20"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify_inputs():
    require(set(INPUTS) == set(PINNED_SHA256), "Declared inputs differ from frozen pins")
    for path, expected in PINNED_SHA256.items():
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        require(actual == expected, "Frozen science or evidence changed: " + path)
    producer = json.loads((PACKET / "SHA256SUMS.json").read_text(encoding="utf-8"))
    for name, expected in producer.items():
        path = str((PACKET / name).relative_to(ROOT))
        require(PINNED_SHA256[path] == expected, "Producer manifest mismatch: " + name)
    owners = json.loads((PACKET / "SOURCE_INPUTS.json").read_text(encoding="utf-8"))
    for row in owners["upstream_inputs"]:
        require(PINNED_SHA256[row["path"]] == row["sha256"], "Published owner mismatch")
    require(PINNED_SHA256[owners["primary_overview"]] == owners["primary_overview_sha256"],
            "Reviewed synthesis mismatch")


def run(path):
    result = subprocess.run([sys.executable, "-O", "-B", "-W", "error", str(path)],
                            cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", check=False, timeout=45)
    if result.returncode or result.stderr:
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError("Narrow replay failed: " + str(path.relative_to(ROOT)))
    return result.stdout


def main():
    verify_inputs()
    text = run(PACKET / "check_stopped_all_cost_source.py")
    expected = (PACKET / "STOPPED_ALL_COST_RESULT.json").read_text(encoding="utf-8")
    require(text == expected, "Exact all-cost scientific receipt changed")
    data = json.loads(text)
    require(data.get("status") == "PASS", "All-cost source checker did not pass")
    require(data.get("GR_closed") is False and data.get("full_D0_price_selected") is False,
            "Physical task/Info/price premise must remain explicit")
    print("PASS stopped all-cost source: " + str(data["active_exact_checks"]) +
          " active exact controls; immutable receipt agrees byte-for-byte")
    upstream = json.loads((PACKET / "UPSTREAM_CURRENT_REPLAY.json").read_text(encoding="utf-8"))
    text = run(ROOT / upstream["checker"])
    expected = (PACKET / upstream["stdout_file"]).read_text(encoding="utf-8")
    require(text == expected, "Corrected upstream finite-cap/source output changed")
    require(hashlib.sha256(text.encode("utf-8")).hexdigest() == upstream["stdout_sha256"],
            "Corrected upstream replay hash changed")
    print("PASS corrected 1cb stopped source: complete finite-cap and first-jet output agrees")
    verify_inputs()
    print("PASS " + str(len(INPUTS)) + " immutable proof/input/review/checker/receipt pins before and after")
    print("SCOPE: all fixed T>=5 and ell>=1; every minimizing branch preserves DJ2; actual joint local minimum implies DJ2=0 under the declared task, Info, fixed-price and full-field assumptions.")


if __name__ == "__main__":
    main()
