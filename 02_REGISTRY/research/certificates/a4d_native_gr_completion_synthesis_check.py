#!/usr/bin/env python3
"""Read-only exact replay of the whole-family CAR/Book/causal source packet.

Saved evidence is immutable. Only elapsed seconds in the timed execution
receipt are excluded from comparison; every scientific field is compared.
This certificate does not assert full physical GR or primitive admission.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]

INPUTS = ['02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/INPUT_COMMIT_ALIAS.json',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/INPUT_SNAPSHOTS.json',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/INPUTS.json',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/RESULT.json',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_book_source_binding.py',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/causal_boundary_completion.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/INPUTS.json',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/RESULT.json',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/check_return_cost_and_stopping.py',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/INPUTS.json',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/RESULT.json',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/VALIDATION.json',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/check_null_first_source.py',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/arbitrary_brinkmann_all40.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/coframe_oracle_transport.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/literal_null_all40.py',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/native_full128_area.py',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/paid_port_history.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/proof.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL128_PORT_SCORE_SUFFICIENCY_AND_CODE_SOURCE_RECOVERY_2026_10_19.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_RETAINED_HISTORY_READOUT_AND_NORMALIZER.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/clock_source_reduction.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/prepared_price_feedback.md']

PINNED_SHA256 = {'02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/INPUT_COMMIT_ALIAS.json': '60830938e1e1f3e9b6f57be110ca803bc68ffec726f0285d0e4fbdb9d0b47bed',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/INPUT_SNAPSHOTS.json': '208f577fccbc68bfbda78d453888394b0a4b128abefd39580dba1ed72622abca',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md': '2b26bf2f4c1b128731ccf14a17437ba654c046e82b5e42e55113a8b6053494ea',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/INPUTS.json': 'f9ab82645f61ba354628debb36d7eacbc58a9a1731ccce98e5d68d8cc5b5f607',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/RESULT.json': '0db66abfabb8cd5aeae03c14c23a0cb5184816233b0f57c0ba842eb1aaeb7ed2',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_book_source_binding.py': 'a6a34c63b1d2f3259be8bb5572f78d86a4034dd6c99a57544d2fa0f004f4e665',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/causal_boundary_completion.md': '46c08c8295401cb42531ec3b974709638ec5f913dbd1b64c0210efa3b99953ba',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/INPUTS.json': '7b4317c4760d6811de8dc0a9e50e9fa32a221dc377e6acd80a68322877a931e1',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/RESULT.json': '7c83ec07af7fe21921dc7bf635516aba7a0157e8a38c1ca648a6300bd8b851eb',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/check_return_cost_and_stopping.py': 'b06b10c069f4a713dac1888a543ebe5b90a1427d3401f4ee86994c7922561dfb',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md': '29e30b35170c8ab1d4d324dd0f7aaa6e588cb1a32f023ad529947dc8639b9faa',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/INPUTS.json': '1ef335c5b048bf01102f3fda9e43bbb2521d97be1567ea49f8bf3c8e965ea166',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/RESULT.json': 'b762e1e4892bdd7a1895dac18ade765aa6e8c98111a4e5f43c47fc26865646a7',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/VALIDATION.json': 'a5eec36b0b3cb0219e183765efff42e9e42166c078cbe1419e6c7e8092ccc9f5',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/check_null_first_source.py': '2d35486c26415d2b667ebc61acded6d0889049d3d481f0c37f36f3601b478ef4',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/arbitrary_brinkmann_all40.md': '8dbca8ff9a4567a2baf216357b5d3ffa2d217281ced4e5d0e535257db2f5e83e',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/coframe_oracle_transport.md': '28a2d3db0545f1bd0dd96e9394a8f350b403db75348df590d75d035db1cc8c65',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/literal_null_all40.py': 'd3d0b1bc92c25a0963a4ba851d9d587d2191f0bbd8cd8cd0ab58b664852b7026',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/native_full128_area.py': '371855a3967c08f82974328bfddd1346cf1b2c62d167cba4748b34a0c33e47f8',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/paid_port_history.md': 'ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/proof.md': 'b1e7d9cdd81605e0b7d532ac8a3bfc682e42806367ad5e109324a5812d7d9e50',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md': '668fc904b0585cc7fd5175babead5225c22051422c9c64e197d7b0d42d225342',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md': 'dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md': '592bbbb1dae9cc599df2eef9cabf117b19f8566d755ad072b77beb04624271d7',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md': '8dbca8ff9a4567a2baf216357b5d3ffa2d217281ced4e5d0e535257db2f5e83e',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md': '6a14686fcaab0b48b78b8ff4f784d989ea3ead1edf0ee28d48b7c20f76c4a7ed',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md': '2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md': 'c5b2f1021e8da573221f4327bacae67934470a368966456bf328b19fc51555fb',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL128_PORT_SCORE_SUFFICIENCY_AND_CODE_SOURCE_RECOVERY_2026_10_19.md': 'f64e04fa9f3d27a604463561fa3d8c1c997e55d3c55badd91a6b4198ce0f9f4e',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md': 'a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md': 'bd3f1ab51599b0efe17af03e40c59a606200cd1912f801e4bd57e0eb77a6b014',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/A4D_RETAINED_HISTORY_READOUT_AND_NORMALIZER.md': '98b02b22f8678be211f555c2ec0c1d8ac3d2cc43f7dd50b002b8e1424460407b',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md': 'f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/clock_source_reduction.md': '7ca9575697d5de7c78794bc5d2879f6c2292caadb4f75334d0e1479fd1287069',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md': 'ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d',
 '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/prepared_price_feedback.md': '73bf64d8c05b2624e092d851cab5f11019fd886c74d6b332ed97f4d4f4d4d434'}

PACKET = ROOT / "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20"


def verify_inputs():
    if set(INPUTS) != set(PINNED_SHA256):
        raise RuntimeError("Declared input set differs from immutable pins")
    for name, wanted in PINNED_SHA256.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != wanted:
            raise RuntimeError("Frozen scientific input changed: " + name)


def scientific_result(value):
    result = dict(value)
    result.pop("seconds", None)
    return result


def replay(checker, receipt, *args, result_file=None):
    proc = subprocess.run(
        [sys.executable, "-O", "-B", "-W", "error", str(PACKET / checker), *args],
        cwd=ROOT, text=True, capture_output=True, timeout=150, check=False,
    )
    if proc.returncode or proc.stderr:
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise RuntimeError("Targeted replay failed: " + checker)
    actual = json.loads(result_file.read_text() if result_file else proc.stdout)
    expected = json.loads((PACKET / receipt).read_text())
    if actual.get("status") != "PASS" or scientific_result(actual) != scientific_result(expected):
        raise RuntimeError("Complete scientific result differs: " + checker)
    print("PASS " + checker + " matches immutable scientific evidence")


def main():
    verify_inputs()
    replay("geometric_source/check_null_first_source.py", "geometric_source/RESULT.json")
    replay("book_source/check_book_source_binding.py", "book_source/RESULT.json",
           "--root", str(PACKET / "inputs"))
    with tempfile.TemporaryDirectory(prefix="d0-gr-source-replay-") as temporary:
        output = Path(temporary) / "return_result.json"
        replay("execution/check_return_cost_and_stopping.py", "execution/RESULT.json",
               "--root", str(PACKET / "inputs"), "--output", str(output), result_file=output)
    verify_inputs()
    print("PASS immutable input/proof/checker/receipt pins before and after replay")
    print("SCOPE: whole-family known reporter source and conditional full-price composition; physical GR remains open.")


if __name__ == "__main__":
    main()
