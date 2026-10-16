#!/usr/bin/env python3
"""Prove the remaining finite native field inverse on the whole root box.

Fixed decimal choices are read, never regenerated. The only calculation is
the new shared Clifford/moment outward validator, not an old full-symbol
run or root search. Its consumer is the full faithful local critical-locus
theorem. No refinement-uniform or physical-action admission follows.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[3]
HERE = ROOT/"02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16"
PINS = {
    "field_inverse_choice.py": "1fa0f1022301d3eb529d1394a99c41849f193ea0e4980f94936674d29e7d5c8a",
    "uniform_symbol_bounds.py": "53b0d77d2d2102a5960769a2be90b02760defc0602eba8a22430375c909ab4fe",
}


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("native_field_inverse:"+label)


def load(name):
    path = HERE/(name+".py")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[path.name],
            "frozen_new_consumer_source:"+name)
    spec = importlib.util.spec_from_file_location("native_inverse_"+name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    start = time.perf_counter()
    choice_owner, validator = load("field_inverse_choice"), load("uniform_symbol_bounds")
    path = HERE/"FIELD_INVERSE_CHOICES.json"
    raw = path.read_bytes()
    choices = json.loads(raw)
    require(choices["source_sha256"] == PINS["field_inverse_choice.py"]
            and choices["root_box_or_inertia_or_inverse_certified"] is False,
            "untrusted_choices_not_a_prior_certificate")
    representatives, differences = choice_owner.domain()
    require([tuple(row["q"]) for row in choices["choices"]] == representatives,
            "all483_disjoint_spatial_S3_and_negation_representatives_exactly_once")
    shared = validator.prepare_shared(ROOT)
    print("shared full119/7140 interval kernel prepared", file=sys.stderr, flush=True)
    output, covered = [], set()
    positive, negative, dimension = 0, 0, 0
    inverse_bound = 0.0
    for index, choice in enumerate(choices["choices"]):
        q = tuple(choice["q"])
        members = set(choice_owner.orbit(q))
        require(not (members & covered) and not (members & differences), "disjoint_field_domain")
        result = validator.evaluate(q, choice, shared, strict=True)
        require(result["zero"] == 0 and result["dimension"] == 17-2*sum(bool(x) for x in q),
                "complete_field_quotient_nonsingular_at_"+str(q))
        require(choice["real_amplitudes_only"] == all((2*x) % 8 == 0 for x in q),
                "self_conjugate_real_block_not_doubled")
        covered |= members
        positive += len(members)*result["positive"]
        negative += len(members)*result["negative"]
        dimension += len(members)*result["dimension"]
        # A spatial role permutation is orthogonal on the full zero-mean
        # active B_r tuple. Its p-1 contrast coordinates have condition<=p:
        # ||x||²<=sum_active||B_r||²<=p||x||². Thus both coordinate maps
        # have norm<=sqrt(p), and inverse-congruence costs at most p.
        p = sum(bool(x) for x in q)
        inverse_bound = max(inverse_bound, p*result["inverse_native_coefficient_norm_upper"])
        result.pop("seconds")
        result.pop("source_pins")
        result.pop("root_box")
        result["orbit_size"] = len(members)
        output.append(result)
        if (index+1) % 50 == 0 or index+1 == len(representatives):
            print("validated %d/%d field orbits" % (index+1, len(representatives)),
                  file=sys.stderr, flush=True)
    require(len(covered) == 4063 and dimension == positive+negative == 40511,
            "entire_real_field_only_normal_dimension")
    for name, expected in PINS.items():
        require(hashlib.sha256((HERE/name).read_bytes()).hexdigest() == expected,
                "no_concurrent_new_source_mutation")
    require(path.read_bytes() == raw, "fixed_choices_not_mutated")
    maximum = max(output, key=lambda row: row["distance_from_signature_upper"])
    # All shell-transfer KKT blocks are previously owned: 8 axis modes and
    #24 two-axis modes, plus real q0. Their normal contributions are374+/223-.
    # Density annihilators and all genuine representations remain zero.
    inertia = {"positive": positive+374, "negative": negative+223, "zero": 40811}
    require(sum(inertia.values()) == 81919, "whole_reduced_density_field_dimension")
    print("completed in %.3f seconds" % (time.perf_counter()-start), file=sys.stderr, flush=True)
    return {"schema": "d0-native-complete-field-inverse/1", "status": "VALIDATED_ALL_FIELD_ONLY_ORBITS",
            "carrier": {"L": 8, "sites": 4096, "Fock": 16, "reference": 128},
            "field_only_orbits": 483, "field_only_frequencies": 4063,
            "complete_real_field_only_quotient_dimension": dimension,
            "field_only_real_inertia": {"positive": positive, "negative": negative, "zero": 0},
            "maximum_signature_distance_upper": maximum["distance_from_signature_upper"],
            "maximum_signature_distance_q": maximum["q"],
            "all_orbit_mean_slice_inverse_bound_upper": inverse_bound,
            "inverse_norm": "Euclidean canonical mean-slice Fourier coefficients; includes spatial-orbit coordinate condition p<=4",
            "minimum_exact_feature_gap_lower": shared["minimum_pair_gap_lower"],
            "root_box": shared["core"]["root_box"], "root_stationarity_is_owned_hypothesis": True,
            "source_sha256": {**PINS, "FIELD_INVERSE_CHOICES.json": hashlib.sha256(raw).hexdigest()},
            "owned_definition_pins": shared["source_pins"],
            "entrypoint_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "composed_full_reduced_real_KKT_inertia": inertia,
            "composed_normal_rank": positive+negative+597,
            "local_critical_family_dimension": 40811,
            "nonlinear_consumer": "LOCAL_CRITICAL_LOCUS_CONSUMER.md: full faithful local Morse-Bott locus; no nearby additional nonflat roots",
            "refinement_uniform_or_rank8_boundary_or_physical_GR_claim": False,
            "old_full4096x16_symbol_runs_or_root_search_replayed": False,
            "orbits": output}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
