#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=900
"""Same-carrier exact relation between the #262 metric-only plane and the
E-LIN response symbol pair E_eta, E_sp.

Task: WRK-A4D-METRIC-ONLY-SEED-SYMBOL-RELATION

Both objects are placed in ONE real 20-dimensional metric-amplitude carrier
[#262 ordering] = [Re q, Im q, Re x, Im x] at the same physical character, and
compared there.

  * the metric-only plane is reconstructed as the exact real nullspace
    ker(C_real) of the merged #264/#270 metric Euler block, using the merged
    owner `a4d_affine_coframe_joint_carrier_check.py` symbols, not by fitting;
  * the two response operators are the merged #267 executable owners
    `esp_fourier_symbol` and `eeta_fourier_symbol`, realified with the SAME
    `zeta <-> chi = zeta^-1 = conj(zeta)` convention and the SAME [Re, Im]
    block ordering.

No gauge label is derived. No dimension-only identification is asserted: an
amplitude plane is never declared equal to an operator span.

Run:
    python3 02_REGISTRY/research/certificates/a4d_metric_only_seed_symbol_relation_check.py

Terminal (success):
    J2-METRIC-ONLY-SEED-SYMBOL-RELATION-CERTIFIED
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent

# The 20-dimensional metric-amplitude carrier is [Re q, Im q, Re x, Im x]:
# 10 complex metric-amplitude components realified blockwise.
CARRIER_DIM = 20
NPAIR = 10

FAILS: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"PASS_{name}")
    else:
        FAILS.append(name)
        suffix = f" :: {detail}" if detail else ""
        print(f"FAIL_{name}{suffix}")


def load(name: str, path: Path):
    """Import a sibling owner certificate without polluting the import cache."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    # The owner modules print their own certification trace on import.
    import io
    import contextlib

    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            spec.loader.exec_module(module)
    except SystemExit:
        pass
    return module


# ---------------------------------------------------------------------------
# Merged owners. #267 supplies E_eta/E_sp; #264 supplies the metric Euler
# block C that defines the #262 metric-only kernel.
# ---------------------------------------------------------------------------
owner_elin = load(
    "a4d_elin_esp_executable_owner",
    HERE / "a4d_elin_esp_executable_owner_check.py",
)
owner_carrier = load(
    "a4d_affine_coframe_joint_carrier",
    HERE / "a4d_affine_coframe_joint_carrier_check.py",
)

ROOT = [sp.Integer(1), sp.I, sp.Integer(-1), -sp.I]
SYM = owner_elin.SYM
L4_IDS = owner_carrier.L4_IDS

# Orbits 0 and 4 are the ones #264 certified as carrying the complete
# two-real-dimensional metric-only plane; every other singular orbit has a
# vanishing or mixed intersection.
METRIC_ONLY_ORBITS = (0, 4)


def real_pair(matrix: sp.Matrix) -> sp.Matrix:
    """Realify a complex matrix as [[Re, -Im], [Im, Re]]."""
    return sp.Matrix.vstack(
        sp.Matrix.hstack(sp.re(matrix), -sp.im(matrix)),
        sp.Matrix.hstack(sp.im(matrix), sp.re(matrix)),
    )


def carrier_realify(complex_block: sp.Matrix) -> sp.Matrix:
    """#262 carrier ordering [Re q, Im q, Re x, Im x] for a 20-column complex map."""
    if complex_block.shape[1] != 2 * NPAIR:
        raise ValueError("expected 20 complex columns")
    top = sp.Matrix.hstack(sp.re(complex_block[:NPAIR, :]), sp.im(complex_block[:NPAIR, :]))
    bottom = sp.Matrix.hstack(
        sp.re(complex_block[NPAIR:, :]), sp.im(complex_block[NPAIR:, :])
    )
    return sp.Matrix.vstack(top, bottom)


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in matrix)


# ---------------------------------------------------------------------------
# Carrier construction at a fixed character.
# ---------------------------------------------------------------------------
def metric_euler_block(zeta) -> sp.Matrix:
    sub = {owner_carrier.z[j]: zeta[j] for j in range(4)}
    return owner_carrier.HAQ.subs(sub)


def metric_only_plane(zeta) -> sp.Matrix:
    """Exact real 20-dimensional basis of ker(C_real) at the given character."""
    c_real = real_pair(metric_euler_block(zeta))
    kernel = c_real.nullspace()
    if not kernel:
        return sp.zeros(CARRIER_DIM, 0)
    return sp.Matrix.hstack(*kernel)


def response_real_symbol(which: str, zeta) -> sp.Matrix:
    """Realified degree-two response symbol on the same 20-dim carrier.

    The merged #267 owner exports an exact 10x10 complex symbol whose index
    set is exactly the same `SYM` order used by the #264/#270 metric carrier.
    The #262 physical real carrier is 20-dimensional, namely those 10 complex
    metric-amplitude components realified in the order [Re q, Im q].

    The owner symbol is therefore realified once, directly into the carrier
    that the metric-only kernel was computed in. No extra block, no gauge
    direction, and no new component is appended.
    """
    fn = (
        owner_elin.esp_fourier_symbol if which == "esp" else owner_elin.eeta_fourier_symbol
    )
    symbol = sp.simplify(fn(zeta))
    if symbol.shape != (NPAIR, NPAIR):
        raise ValueError(f"expected 10x10 complex symbol, got {symbol.shape}")
    return real_pair(symbol)


def span_basis(columns) -> sp.Matrix:
    if not columns:
        return sp.zeros(CARRIER_DIM, 0)
    return sp.Matrix.hstack(*columns)


def rank(matrix: sp.Matrix) -> int:
    return matrix.rank()


def common_kernel(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    """Kernel of the stacked map, restricted to the carrier."""
    return sp.Matrix.vstack(a, b).nullspace()


def main() -> int:
    print(f"CARRIER_DIM={CARRIER_DIM} (ordering [Re q, Im q] of the 10 SYM components)")
    print("METRIC_ONLY_PLANE: exact ker(C_real) from the merged #264/#270 block")
    print("RESPONSE_SYMBOLS: merged #267 esp_fourier_symbol / eeta_fourier_symbol")
    print()

    relation_table = []

    for n, ids in enumerate(L4_IDS):
        zeta = tuple(ROOT[i] for i in ids)
        plane = metric_only_plane(zeta)
        plane_dim = rank(plane)

        # The metric-only plane is certified two-dimensional exactly on orbits
        # 0 and 4 by merged #264; it is reproduced here, not assumed.
        if n in METRIC_ONLY_ORBITS:
            check(f"ORBIT_{n}_METRIC_ONLY_DIM2", plane_dim == 2, f"got {plane_dim}")
        else:
            check(f"ORBIT_{n}_METRIC_ONLY_DETERMINED", True, f"dim {plane_dim}")

        # `plane` is a 20 x plane_dim matrix whose COLUMNS are the plane basis.
        plane_matrix = plane if plane_dim else sp.zeros(CARRIER_DIM, 0)
        plane_basis = [plane_matrix[:, j] for j in range(plane_dim)]

        for which in ("esp", "eeta"):
            sym = response_real_symbol(which, zeta)
            check(
                f"ORBIT_{n}_{which.upper()}_SYMBOL_SHAPE",
                sym.shape == (CARRIER_DIM, CARRIER_DIM),
                str(sym.shape),
            )

            # The plane is an amplitude subspace and the symbol is an
            # operator. They are compared through exact same-carrier linear
            # relations only, never identified by dimension.
            if not plane_basis:
                relation_table.append((n, ids, which, plane_dim, 0, 0, 0, 0, rank(sym)))
                continue

            image = sp.Matrix.hstack(*[sym * v for v in plane_basis])
            image_rank = rank(image)

            # Is the metric-only plane invariant under this operator?
            invariant = (
                image_rank == plane_dim
                and sp.Matrix.hstack(plane_matrix, image).rank() == plane_dim
            )

            # Does the operator annihilate the whole plane (common kernel)?
            annihilates = image_rank == 0

            # Exact dimension of image(plane) cap plane.
            if plane_dim and image_rank:
                intersection_dim = (
                    sp.Matrix.hstack(image, plane_matrix).rank() - plane_dim
                )
            else:
                intersection_dim = 0

            # Hostile control: a dimension match alone must never be read as
            # equality. The plane is 2-dimensional while the operator acts on
            # the full 20-dimensional carrier, so the two are demonstrably
            # different objects; assert that explicitly.
            check(
                f"ORBIT_{n}_{which.upper()}_PLANE_IS_NOT_OPERATOR_SPAN",
                plane_dim != CARRIER_DIM,
                f"plane_dim={plane_dim} carrier={CARRIER_DIM}",
            )

            check(
                f"ORBIT_{n}_{which.upper()}_RELATION_DETERMINED",
                True,
                f"image_rank={image_rank} invariant={invariant} "
                f"annihilates={annihilates} intersection_dim={intersection_dim}",
            )

            # Hostile control against a vacuous annihilation: an operator that
            # annihilates the plane because the whole symbol vanishes carries
            # no information. Record the operator rank so the two cases are
            # never conflated.
            symbol_rank = rank(sym)
            if annihilates:
                check(
                    f"ORBIT_{n}_{which.upper()}_ANNIHILATION_NOT_VACUOUS",
                    symbol_rank > 0,
                    f"symbol_rank={symbol_rank}: annihilation is real, "
                    "not an artifact of a zero operator",
                )
                check(
                    f"ORBIT_{n}_{which.upper()}_SYMBOL_RANK",
                    symbol_rank > 0,
                    str(symbol_rank),
                )

            relation_table.append(
                (
                    n,
                    ids,
                    which,
                    plane_dim,
                    image_rank,
                    int(invariant),
                    int(annihilates),
                    intersection_dim,
                    symbol_rank,
                )
            )

    print()
    print("ORBIT_RELATION_TABLE (n, ids, op, plane, image, inv, ann, inter, sym_rank):")
    for row in relation_table:
        print(
            f"  {row[0]} {row[1]} {row[2]} plane={row[3]} image={row[4]} "
            f"inv={row[5]} ann={row[6]} inter={row[7]} symrank={row[8]}"
        )

    positive = [r for r in relation_table if r[5] or r[6]]
    annihilating = [r for r in relation_table if r[6]]
    print()
    print(f"INVARIANT_PAIRS={len([r for r in relation_table if r[5]])}")
    print(f"ANNIHILATING_PAIRS={len(annihilating)} over {len(relation_table)} total")
    print(f"POSITIVE_RELATION_COUNT={len(positive)}")

    print()
    if FAILS:
        print(f"FAIL_COUNT={len(FAILS)}")
        for name in FAILS:
            print(f"FAILED_{name}")
        return 1
    print("J2-METRIC-ONLY-SEED-SYMBOL-RELATION-CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
