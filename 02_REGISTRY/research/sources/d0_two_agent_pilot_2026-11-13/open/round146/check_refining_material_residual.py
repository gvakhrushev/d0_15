"""Check the exact full-RIGHT coefficients in the refining material test."""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


RESEARCH = Path(__file__).resolve().parents[4]
SOURCES = (
    "sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
    "PRIMARY_CAR_PREPARATION_SOURCE.md",
    "sources/d0_paid_moment_field_writer_2026-10-21/moments/"
    "EXACT_MOMENT_SOURCE_CONSTRUCTION.md",
    "A4D_ORIGINAL_GOLDEN_PF_DISCRETE_C2_REGULARITY_2026_10_22.md",
    "sources/d0_two_agent_pilot_2026-11-13/direct/round73/matter/"
    "check_matter_root.py",
)
VEC = ((Q(1, 2), Q(-1, 2), 0, 0), (1, 1, 0, 0),
       (0, 0, -1, 0), (0, 0, 0, -1))
QUARTER = Q(1, 4)
WIDTH = Q(3, 4)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def base_overlaps():
    base = 4
    pairs = [mode for mode in product(range(base), repeat=4)
             if mode < tuple(-k % base for k in mode)][:64]
    cos = (1, 0, -1, 0)
    return tuple(Q(sum(cos[mode[axis]] for mode in pairs), len(pairs))
                 for axis in range(4))


def profile(u):
    return u * (u - QUARTER)


def layer_density(index, length, overlap):
    block_size = length // 4
    h = Q(1, length)
    value = profile(index * h)
    result = Q(0)
    for neighbour in (index - 1, index + 1):
        weight = 1 if neighbour // block_size == index // block_size else overlap
        result += weight * (value - profile(neighbour * h))
    return result / h**2


def seam_terms(overlap):
    terms = []
    for seam in (QUARTER, 2 * QUARTER, 3 * QUARTER):
        slope = 2 * seam - QUARTER
        pole = (1 - overlap) * slope
        terms.append((seam, -1, pole, overlap - 3))
        if seam < WIDTH:
            terms.append((seam, 0, -pole, -(1 + overlap)))
    return terms


def verify_mesh(length, overlap, terms):
    h = Q(1, length)
    free = range(1, 3 * length // 4)
    seam_density = {int(seam * length) + offset: pole / h + regular
                    for seam, offset, pole, regular in terms}
    density = [layer_density(index, length, overlap) for index in free]
    require(density == [seam_density.get(index, -2) for index in free],
            f"Nested seam density at L={length}")
    scaled_norm_sq = h**2 * (WIDTH - h)**2 * sum(value**2 for value in density)
    exact_norm_sq = (WIDTH - h)**2 * (
        sum((pole + h * regular)**2 for _, _, pole, regular in terms)
        + 4 * h**2 * (len(free) - len(terms))
    )
    require(scaled_norm_sq == exact_norm_sq, f"Weighted layer count at L={length}")
    require(all(layer_density(index, length, Q(1)) == -2 for index in free),
            f"Unit u-overlap density at L={length}")
    return scaled_norm_sq


def main():
    gram = tuple(tuple(sum(left * right for left, right in zip(v, w))
                       for w in VEC) for v in VEC)
    diagonal = (Q(1, 2), Q(2), Q(1), Q(1))
    require(gram == tuple(tuple(value if row == column else 0 for column in range(4))
                          for row, value in enumerate(diagonal)), "REST leg Gram")
    overlaps = base_overlaps()
    require(overlaps == (Q(7, 16), Q(3, 16), Q(1, 16), Q(0)),
            "Inherited RIGHT128 base overlaps")
    terms = seam_terms(overlaps[0])
    nested_limit = WIDTH**2 * sum(pole**2 for _, _, pole, _ in terms)
    recomputed_limit = 4 * WIDTH**3
    require(nested_limit == Q(32805, 65536), "Nested leading squared norm")
    require(recomputed_limit == Q(27, 16), "Recomputed limiting squared norm")
    samples = {length: verify_mesh(length, overlaps[0], terms)
               for length in (16, 32, 64, 128, 256, 512)}
    for length in (256, 512):
        # These are the first 64 nonselfconjugate pairs in lexicographic
        # order, already reached without leaving the fourth axis.
        require(64 < length - 64, "First 64 positive y modes are representatives")
    print(json.dumps({
        "GR_closed": False,
        "finite_check": "exact rational coefficients and layer count; limits proved in B146",
        "constant_density_leg_norms_squared": [str(value) for value in diagonal],
        "inherited_RIGHT128_nearest_overlaps_at_L4": [str(value) for value in overlaps],
        "inherited_limit_h_times_physical_minimum_squared": str(nested_limit),
        "recomputed_reference_limit_physical_minimum_squared": str(recomputed_limit),
        "inherited_uniform_pf_samples_h_times_physical_norm_squared":
            {str(length): str(norm_sq) for length, norm_sq in samples.items()},
        "original_full_book_cost_info_transferred": False,
        "source_sha256": {path: sha256((RESEARCH / path).read_bytes()).hexdigest()
                          for path in SOURCES},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
