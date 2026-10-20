#!/usr/bin/env python3
"""Replay only the frozen native clock / complete price / source packet.

Proofs and receipts remain immutable. Every scientific JSON field is compared;
only prospective.elapsed_seconds is ignored. Numerical finite-cut diagnostics
are controls of its pinned analytic proof, not a universal numerical proof.
No full Book Cost-Info, physical admission, Lean or GR closure is asserted.
"""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]

INPUTS = ['02_REGISTRY/research/A4D_NATIVE_CLOCK_PRESSURE_AND_COMPLETE_PRICE_SYNTHESIS_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/INPUT_SNAPSHOTS.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/README.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/COHERENT_RETURN_PRESSURE_AND_PAID_MOMENTS.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/GEOMETRY_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/INPUTS.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/RESULT.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/STOPPED_CLOCK_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/check_coherent_return_pressure.py',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/check_finite_closed_record.py',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/finite_closed_record.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/BOOK_PRICE_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/CENTRAL_GEOMETRY_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/SOURCE_MOMENT_RESULT.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/check_source_moment_collapse.py',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/source_moment_collapse.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL128_JONES_OBSERVER_SO3_QUOTIENT_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/FULL128_HEAT_PRICE_RECYCLING_BRIDGE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/CENTRAL_COMPOSITION_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/FINITE_CUT_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/INPUTS.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/RESULT.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/STOPPED_CLOCK_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/check_stopped_clock_source.py']

PINNED_SHA256 = {'02_REGISTRY/research/A4D_NATIVE_CLOCK_PRESSURE_AND_COMPLETE_PRICE_SYNTHESIS_2026_10_20.md': '823d527dbe61050a9c3f81109691839e1bc9de0855e5435e08259049db1a06ed',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/INPUT_SNAPSHOTS.json': 'c3bd0f9a64d7bc2a0dfc912de6411f515b680574fa132add5a4056356ecc4b46',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/README.md': '70b05ec1b04c8b4f71d46dcc1b9c99dd76abaf006c3942384796ce0165ee298b',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/COHERENT_RETURN_PRESSURE_AND_PAID_MOMENTS.md': '8001997f869a2ed86e78b6222e881d9ed67014ac0dc18573808df12b3592b7de',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/GEOMETRY_REVIEW.md': 'de105b644d2e5a7458587eddac49393c486d5f14b0c584d534141dd1db75d13e',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/INPUTS.json': '26674fa2e66b3534fe0361c2acdae0994d6d03d2f732210fb92719d6ef7782ae',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/RESULT.json': '163bb6d85e7b7deb626cf56486e0117da9e126d4fcdbf8dbf021c449c8b1f138',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/STOPPED_CLOCK_REVIEW.md': '5f8f459577450c4959fd16b1a460805a394827f80244585dbf38578ca5d56f6a',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/check_coherent_return_pressure.py': 'e3388349e9c6cbba37a05ac3a05b607ad34d2135aaca958e1265c3cca16e8db1',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/check_finite_closed_record.py': 'aa6d603038129139e0d944610d722123b776f01e52d72b3c8178636df4bd7b19',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/finite_closed_record.md': '44e3f7844dc40c99c5218c7223fabc485e63fc251517c53f1d424dab222bfe28',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/BOOK_PRICE_REVIEW.md': '862099aac7349fa31e30546141537420fa817e809b3c636f23b13a92555442a7',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/CENTRAL_GEOMETRY_REVIEW.md': '841683dbcbed32f75ed36a415f91b2c8c511f8bece57da328c2c0605d4d030ae',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/SOURCE_MOMENT_RESULT.json': '283d3f92890644469482f1f4de0c9885d380e9dff2ef8825fea40796400f7c08',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/check_source_moment_collapse.py': 'fd4edf0649492910eecf649fb1c133dafd2eb1b3d4b8df801a6e62a0f30691b8',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/source_moment_collapse.md': '9bfb61897324d438bff3458209f3fda321b2876af41b6178b96fdf04490773c4',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md': 'dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md': '482cf99f280620e7aa6120432cd7b9764671c5ef3fb1c0c3b50d7228d66e08b3',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md': '2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md': 'c5b2f1021e8da573221f4327bacae67934470a368966456bf328b19fc51555fb',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL128_JONES_OBSERVER_SO3_QUOTIENT_2026_10_20.md': '610a6688f8f1ea91c93462d4cedf716eec321dd5032ba35a0d2ffb7262ffca61',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md': 'a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md': 'd92aabf2d46d9ac7d8d9aa3bf5ed66a58f25bb83ca4460d66d25648c62f7e10b',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md': 'bd3f1ab51599b0efe17af03e40c59a606200cd1912f801e4bd57e0eb77a6b014',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md': '29e30b35170c8ab1d4d324dd0f7aaa6e588cb1a32f023ad529947dc8639b9faa',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/FULL128_HEAT_PRICE_RECYCLING_BRIDGE.md': 'a8cdbd52e52275cb7e41aa84b8bd69e9fb36170f75d8481c6568fb3ea1a2bce0',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md': 'ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/CENTRAL_COMPOSITION_REVIEW.md': '73cef0764bf733a340df15835d6add01df6740545acae5d7ec4b3d11778c32dd',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/FINITE_CUT_REVIEW.md': 'e70dae15cbc0ead0565b16464818bc21fabee8583a705d98cf889e39e5142e85',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/INPUTS.json': '8de593a2da6afe859e86f5b42a212b53705dcf5ce3def77ae15c22c02c4ea733',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/RESULT.json': 'b226373c813903af983ac1f438c4b7d6485d81dda32f13f2225284d20d0ee35f',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/STOPPED_CLOCK_SOURCE.md': '75845813d20ecf7b585fb7b7a7bef8b8170a711e94a56bb0df0cc3546622a036',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/check_stopped_clock_source.py': 'bdab1158efc863a8d631c50ae7f30f7c3780df744e74441a88ed298bc059f0c9'}

PACKET = ROOT / "02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20"
SNAPSHOT = PACKET / "inputs"


def verify_inputs():
    if set(INPUTS) != set(PINNED_SHA256):
        raise RuntimeError("Declared inputs differ from immutable pins")
    for name, wanted in PINNED_SHA256.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != wanted:
            raise RuntimeError("Frozen scientific input changed: " + name)
    manifest = json.loads((PACKET / "INPUT_SNAPSHOTS.json").read_text())
    for entry in manifest["inputs"]:
        if PINNED_SHA256.get(entry["snapshot_path"]) != entry["sha256"]:
            raise RuntimeError("Input snapshot and declared owner disagree")


def invoke(checker, *args, optimized=True):
    flags = ["-O", "-B", "-W", "error"] if optimized else ["-B", "-W", "error"]
    proc = subprocess.run(
        [sys.executable, *flags, str(PACKET / checker), *args],
        cwd=ROOT, text=True, capture_output=True, timeout=150, check=False,
    )
    if proc.returncode or proc.stderr:
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise RuntimeError("Targeted replay failed: " + checker)
    return proc.stdout


def replay_json(checker, receipt, *args, result_file=None, timed=False):
    stdout = invoke(checker, *args)
    actual = json.loads(result_file.read_text() if result_file else stdout)
    expected = json.loads((PACKET / receipt).read_text())
    if timed:
        actual.pop("elapsed_seconds", None)
        expected.pop("elapsed_seconds", None)
    if actual.get("status") != "PASS" or actual != expected:
        raise RuntimeError("Complete scientific result differs: " + checker)
    print(f"PASS {checker}: {actual['checks']} exact checks; immutable result agrees")


def replay_finite_cut():
    # This checker intentionally has active assertions and rejects Python -O.
    stdout = invoke("check_finite_closed_record.py", optimized=False)
    lines = stdout.splitlines()
    expected = [
        "exact complete-symmetric derivative identity, through degree 7: PASS",
        "finite positive-occupation value/source cut with dark mode and noncommuting jet: PASS",
        "exact original shell exit-cost insertion, including n paid blank ticks: PASS",
        "original full site x CAR16 x reference128 CONDITIONAL source separation: PASS",
        "complete finite apparatus retains failures and has its own exact source: PASS",
        "finite cap preserves h^-2-normalized closed-pressure source: PASS",
    ]
    if lines[:6] != expected or len(lines) != 9:
        raise RuntimeError("Finite-cut checker did not execute all six control groups")
    samples = [ast.literal_eval(line) for line in lines[6:]]
    if [item["L"] for item in samples] != [4, 8, 16]:
        raise RuntimeError("Finite-cut full-spectrum controls are incomplete")
    print(stdout, end="")


def main():
    verify_inputs()
    replay_json("geometry/check_source_moment_collapse.py", "geometry/SOURCE_MOMENT_RESULT.json",
                "--root", str(SNAPSHOT))
    replay_json("book_price/check_coherent_return_pressure.py", "book_price/RESULT.json",
                "--root", str(SNAPSHOT))
    with tempfile.TemporaryDirectory(prefix="d0-clock-source-") as temporary:
        output = Path(temporary) / "stopped_clock.json"
        replay_json("prospective/check_stopped_clock_source.py", "prospective/RESULT.json",
                    "--root", str(SNAPSHOT), "--output", str(output), result_file=output, timed=True)
    replay_finite_cut()
    verify_inputs()
    print("PASS all immutable input/proof/checker/review/receipt pins before and after replay")
    print("SCOPE: exact retained-clock/pressure/known-price/source composition; full Book selection and physical GR remain open.")


if __name__ == "__main__":
    main()
