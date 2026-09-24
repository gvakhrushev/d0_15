"""Runtime-output helpers for D0 certificates.

Certificate code and immutable inputs live in ``04_CERTIFICATES``. Anything
produced by executing a certificate belongs under ignored ``.build`` so a
certificate run cannot create a second source of truth in the release tree.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

JSON_FLOAT_REL_TOL = 1.0e-12
JSON_FLOAT_ABS_TOL = 1.0e-12


def output_dir(script_file: str | Path) -> Path:
    d = ROOT / ".build" / "cert_outputs" / Path(script_file).stem
    d.mkdir(parents=True, exist_ok=True)
    return d


def output_path(script_file: str | Path, name: str) -> Path:
    return output_dir(script_file) / name


def _json_mismatch(path: str, actual: Any, expected: Any, why: str) -> AssertionError:
    return AssertionError(
        f"tracked canonical artifact mismatch at {path}: {why}; "
        f"tracked={actual!r}, computed={expected!r}"
    )


def _assert_json_value_matches(actual: Any, expected: Any, path: str) -> None:
    if expected is None or isinstance(expected, (bool, str, int)):
        if type(actual) is not type(expected) or actual != expected:
            raise _json_mismatch(path, actual, expected, "exact value/type mismatch")
        return

    if isinstance(expected, float):
        if not isinstance(actual, float):
            raise _json_mismatch(path, actual, expected, "expected float")
        if not math.isfinite(actual) or not math.isfinite(expected):
            if actual != expected:
                raise _json_mismatch(path, actual, expected, "non-finite float mismatch")
            return
        if not math.isclose(
            actual, expected, rel_tol=JSON_FLOAT_REL_TOL, abs_tol=JSON_FLOAT_ABS_TOL
        ):
            raise _json_mismatch(
                path, actual, expected,
                f"float mismatch beyond rel={JSON_FLOAT_REL_TOL:g}, abs={JSON_FLOAT_ABS_TOL:g}",
            )
        return

    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise _json_mismatch(path, actual, expected, "list shape mismatch")
        for index, (a_item, e_item) in enumerate(zip(actual, expected)):
            _assert_json_value_matches(a_item, e_item, f"{path}[{index}]")
        return

    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise _json_mismatch(path, actual, expected, "expected object")
        if set(actual) != set(expected):
            missing = sorted(set(expected) - set(actual))
            extra = sorted(set(actual) - set(expected))
            raise _json_mismatch(
                path, actual, expected, f"object keys differ missing={missing} extra={extra}"
            )
        for key in expected:
            _assert_json_value_matches(actual[key], expected[key], f"{path}.{key}")
        return

    raise TypeError(f"unsupported JSON value at {path}: {type(expected).__name__}")


def assert_json_artifact_matches(path: str | Path, expected: Any) -> None:
    """Require a tracked JSON artifact to match deterministic semantic output.

    Structure and non-floating values match exactly. Float fields use the fixed
    repository tolerance above to ignore only platform-level numerical roundoff.
    """
    artifact = Path(path)
    if not artifact.is_file():
        raise AssertionError(f"missing tracked canonical artifact: {artifact}")
    try:
        actual = json.loads(artifact.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(
            f"tracked canonical artifact is not valid JSON: {artifact}: {exc}"
        ) from exc
    _assert_json_value_matches(actual, expected, "$")
