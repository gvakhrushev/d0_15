"""Expand the exact-native-phase readiness amplifier into one paid raw word.

This is a constructor, not a decision that a supplied READY predicate has
scalar success on all protected inputs.  That semantic hypothesis is proved
for the consumed factory programme in READINESS_AMPLIFICATION.md.  The actual
Book input cut still includes the fresh rebit blank; the algorithmic initial
reflection intentionally excludes that rebit and the inaccessible source spin.
Every inverse, phase, source and routing stage is in the returned gate list.
"""

from dataclasses import dataclass, replace

import native_phase as phase

native = phase.native


@dataclass(frozen=True)
class AmplificationPlan:
    execution: native.Execution
    rounds: int
    rebit: int
    report_bit: int
    initial_controls: tuple
    ready_controls: tuple
    phase_certificate: dict
    initial_phase_stages: int
    ready_phase_stages: int
    levels: tuple


def _inventory_row(execution, round_number, bounds):
    inv = native.inventory(execution, **bounds)
    return {"round": round_number, "stages": inv.gate_count,
            "G": inv.g_count, "CX": inv.cx_count,
            "SourceI": inv.source_i_count,
            "weighted_inventory": 5 * inv.g_count + inv.cx_count + inv.source_i_count,
            "full_fibre_dimension": inv.full_dimension,
            "actual_book_input_rank": inv.cut_rank}


def amplify_execution(base: native.Execution, *, ready_controls, rebit: int,
                      report_bit: int, rounds: int, max_qubits: int,
                      max_expanded_stages: int, max_phase_k: int,
                      interval_bits: int = 96) -> AmplificationPlan:
    """Construct A_{j+1}=A_j R_initial A_j^dagger R_READY A_j.

    The list is chronological, so it is emitted in the reverse order of this
    matrix product.  All work is reused coherently; no wire is allocated by
    this function.  The caller must include one fresh blank rebit in base.
    The READY controls are existing genuine flags, excluding the report bit.
    This syntactic separation does not by itself establish their semantics.
    """
    bounds = {"max_qubits": max_qubits,
              "max_expanded_stages": max_expanded_stages}
    native.validate_execution(base, **bounds)
    base = replace(base, gates=tuple(base.gates))
    if base.profile != native.G_CX_SOURCE_I:
        raise native.DomainError("the full amplifier requires the declared exact inverse profile")
    if not base.gates:
        raise native.DomainError("amplification requires a nonempty actual base word")
    if type(rounds) is not int or rounds < 0:
        raise native.DomainError("rounds must be a nonnegative integer")
    forbidden = set(base.old_right) | set(base.source_spin or ())
    if (type(rebit) is not int or rebit not in base.blank_wires
            or rebit in forbidden or rebit == base.source_port):
        raise native.DomainError("the phase rebit must be an existing separate fresh blank")
    if any(rebit in gate.wires for gate in base.gates):
        raise native.DomainError("the base word must leave the new phase rebit untouched")
    if (type(report_bit) is not int or not 0 <= report_bit < base.qubits
            or report_bit in forbidden or report_bit == rebit):
        raise native.DomainError("report_bit must be a separate logical output wire")
    if type(ready_controls) not in (list, tuple):
        raise native.DomainError("READY controls must be a finite tuple/list")
    ready_controls = tuple(ready_controls)
    if (not ready_controls
            or any(type(q) is not int or not 0 <= q < base.qubits
                   for q in ready_controls)
            or len(set(ready_controls)) != len(ready_controls)
            or forbidden.intersection(ready_controls)
            or rebit in ready_controls or report_bit in ready_controls):
        raise native.DomainError("READY needs distinct logical flags and must exclude the report/rebit")

    initial = tuple(q for q in base.blank_wires
                    if q != rebit and q not in (base.source_spin or ()))
    maximum = max(len(initial), len(ready_controls))
    certificate = phase.find_stable_native_phase(maximum, max_phase_k,
                                                  bits=interval_bits)
    k_initial = phase.matched_phase_index(maximum, len(initial), certificate["k"])
    k_ready = phase.matched_phase_index(maximum, len(ready_controls), certificate["k"])
    initial_word = phase.phase_word(base, initial, (0,) * len(initial), rebit,
                                    k_initial, **bounds)
    ready_word = phase.phase_word(base, ready_controls, (1,) * len(ready_controls),
                                  rebit, k_ready, **bounds)

    current = base
    levels = [_inventory_row(current, 0, bounds)]
    for round_number in range(1, rounds + 1):
        inverse = native.inverse_word(current, **bounds)
        total = 2 * len(current.gates) + len(inverse) + len(ready_word) + len(initial_word)
        if total > max_expanded_stages:
            raise native.DomainError("the entire amplified word exceeds its paid stage bound")
        gates = (current.gates + ready_word + inverse
                 + initial_word + current.gates)
        current = replace(base, gates=gates)
        native.validate_execution(current, **bounds)
        row = _inventory_row(current, round_number, bounds)
        phase_weight = (sum(5 if gate.op == "G" else 1
                            for gate in initial_word + ready_word))
        if row["weighted_inventory"] > 5 * levels[-1]["weighted_inventory"] + phase_weight:
            raise ArithmeticError("actual primitive inventory violates the proved recurrence")
        levels.append(row)
    return AmplificationPlan(current, rounds, rebit, report_bit, initial,
                             ready_controls, certificate, len(initial_word),
                             len(ready_word), tuple(levels))

