#!/usr/bin/env python3
"""Read-only replay of the same-history port-cost/source composition packet.

The complete Book price and physical GR terminal are not asserted.
Expected scientific evidence is immutable. Only elapsed_seconds is omitted
when comparing a timed receipt; every scientific result field is compared.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]

INPUTS = ['02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/clock_source_reduction.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/prepared_price_feedback.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/d0_sourced_connection_proof.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/check_paid_port_cost.py',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/check_clock_payment.py',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/check_prepared_price_feedback.py',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/d0_sourced_connection_probe.py',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/check_connection_coframe_review.py',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/PAID_PORT_RESULT.json',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/CLOCK_SOURCE_RESULT.json',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/PREPARED_FEEDBACK_RESULT.json',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/CONNECTION_RESULT.json',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/CONNECTION_COFRAME_RESULT.json',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/SOURCE_PINS.json',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_BOOK_CAR_HOLST_WEYL_BRANSDICKE_EINSTEIN_UNIVERSALITY_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_RELATIONAL_COMPACT_EXECUTION_AND_EXACT_SOURCE_SYNTHESIS_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19/check_two_round_complete_shannon_order_source.py',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/coframe_oracle_transport.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/original_record_source.md',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/price_equivalence2_smooth.py']

PINNED_SHA256 = {'02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md': 'ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/clock_source_reduction.md': '7ca9575697d5de7c78794bc5d2879f6c2292caadb4f75334d0e1479fd1287069',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/prepared_price_feedback.md': '73bf64d8c05b2624e092d851cab5f11019fd886c74d6b332ed97f4d4f4d4d434',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/d0_sourced_connection_proof.md': 'b782f919536002c0099b5286290fcde7b2b2b819e9a185bb118a7f92b206dea3',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/check_paid_port_cost.py': '36a091aff2dc826aeabfac0c60a453a80c5bbfc23ecdaf0fd554b17cd8dd1bf3',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/check_clock_payment.py': '2cd1c74b41685606128291001c72b3b4b576a91755b818e2b60475fe2f8ca0a5',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/check_prepared_price_feedback.py': '9a33002a28f4ea52dc0f35a0417a110c2a40e2b43ed290dfa0670ae57befb619',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/d0_sourced_connection_probe.py': '138e8f952b2f59af6ae600691295b6e34ec58200d83b899d0b93ba7dd96c9c48',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/check_connection_coframe_review.py': '5a9b815788f0caa1d793685ef54e0a07dd34d48c19a06a0af9899b6fc86861ce',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/PAID_PORT_RESULT.json': '6a3bec240300bfc8345dd36f3a2bed7c75d09b18aafe21a3f5f29fc4f9711353',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/CLOCK_SOURCE_RESULT.json': '14736514e03c3945e38e8766d8d06f544859ee2ef4a9a31ea3d1066a4f869a38',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/PREPARED_FEEDBACK_RESULT.json': '795512cb89ca4412b3639714a3224cfa09918dcc7101193e4a85d33c36c8b2ad',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/CONNECTION_RESULT.json': 'c0385b4d59e97e0fe259a9b459452605f3d3dcf7c867c643c87885152f9d7178',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/CONNECTION_COFRAME_RESULT.json': '7cf980c756e89cebeb0dfa2dbc6ed2584b8ec6888f69e50f0b304475579307e6',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/SOURCE_PINS.json': '33a3f178c5e49561ab145de649e429ee021be3a90fd6d6b6bc64d6b144a4beb3',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_BOOK_CAR_HOLST_WEYL_BRANSDICKE_EINSTEIN_UNIVERSALITY_2026_10_20.md': 'c7d1c5adb00ef5f6b17e9f23c5fffe4ec649ea2194bba6d6f5dbd93847a0c7de',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md': '2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md': 'f54810cf9cc16f2282eb602fa606381cdd9622c7f877fef5211e978c55e4956c',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md': 'a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md': 'd92aabf2d46d9ac7d8d9aa3bf5ed66a58f25bb83ca4460d66d25648c62f7e10b',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/A4D_RELATIONAL_COMPACT_EXECUTION_AND_EXACT_SOURCE_SYNTHESIS_2026_10_20.md': 'e9aa39f1b4fa4660b0cd149a728e455ee2318b537745f96dc8a5f957df815e67',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19/check_two_round_complete_shannon_order_source.py': '72ade8304bd29471115ebb9961df5225307229004c07ddc35d7f31221e566bf4',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/coframe_oracle_transport.md': '28a2d3db0545f1bd0dd96e9394a8f350b403db75348df590d75d035db1cc8c65',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/original_record_source.md': '3e038dd9fae47bee12e9df6c27ed2b0816c577a47e0581cf6b9f84e976f3cc0c',
 '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/price_equivalence2_smooth.py': '393c459c5295e3e3af413f6c935b4eb4402cd4b8b714761548b7dbc7e8b0b0c8'}

PACKET = ROOT / '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20'


def verify_inputs():
    if set(INPUTS) != set(PINNED_SHA256):
        raise RuntimeError("Declared input set differs from pins")
    for name, wanted in PINNED_SHA256.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != wanted:
            raise RuntimeError("Frozen input changed: " + name)


def scientific_result(result):
    result = dict(result)
    result.pop("elapsed_seconds", None)
    return result


def replay(checker, receipt, *args):
    proc = subprocess.run(
        [sys.executable, "-O", "-B", "-W", "error", str(PACKET / checker), *args],
        cwd=PACKET, text=True, capture_output=True, check=False, timeout=120,
    )
    if proc.returncode or proc.stderr:
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise RuntimeError("Replay failed: " + checker)
    actual = json.loads(proc.stdout)
    expected = json.loads((PACKET / receipt).read_text())
    if actual.get("status") != "PASS" or scientific_result(actual) != scientific_result(expected):
        raise RuntimeError("Complete scientific result differs: " + checker)
    print("PASS " + checker + " matches the immutable scientific result")


def main():
    verify_inputs()
    replay("check_paid_port_cost.py", "PAID_PORT_RESULT.json", "--root", str(PACKET / "inputs"))
    replay("check_clock_payment.py", "CLOCK_SOURCE_RESULT.json")
    replay("check_prepared_price_feedback.py", "PREPARED_FEEDBACK_RESULT.json")
    replay("d0_sourced_connection_probe.py", "CONNECTION_RESULT.json", "--root", str(PACKET / "inputs"))
    replay("check_connection_coframe_review.py", "CONNECTION_COFRAME_RESULT.json")
    verify_inputs()
    print("PASS all proof, checker, source and expected-result pins are unchanged")
    print("SCOPE: actual paid history/source transport and conditional Fourier connection composition; full Book price and GR remain open.")


if __name__ == "__main__":
    main()
