"""The complete Born pointer and three heat prices on the fixed-volume manifold."""
from fractions import Fraction as Q
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "round76/geometry"))
import check_invisible_geometry as geometry


def restrict_to_fixed_volume(rows, radii):
    columns = rows.reshape(-1, 32, 4)
    errors = (radii + 1e-15 * np.abs(rows)).reshape(-1, 32, 4)
    # s_i3 = -(s_i0+s_i1+s_i2) preserves the volume exactly at every site.
    restricted = columns[:, :, :3] - columns[:, :, 3, None]
    uncertainty = 1.000001 * (errors[:, :, :3] + errors[:, :, 3, None]) + 1e-290
    return restricted.reshape(-1, 96), uncertainty.reshape(-1, 96)


def main():
    geometry.check_structural_identities()
    d, operators, prepared, _ = geometry.assemble()
    pointer, pointer_error = geometry.pointer_rows(d, operators, prepared)
    (prices, price_error), _ = geometry.heat_rows(d)
    assert pointer.shape == (26, 128) and prices.shape == (3, 128)
    geometry.signed_rank(*restrict_to_fixed_volume(pointer, pointer_error))
    geometry.signed_rank(*restrict_to_fixed_volume(
        np.vstack((pointer, prices)), np.vstack((pointer_error, price_error))))
    # Trace of the first Julia coefficient after summing the uniformly prepared
    # SITE and the complete old RIGHT. At unequal role weights r=sum(gamma*w^2)/2048.
    heat = geometry.heat
    counts = geometry.car.actual_counts(heat.ROOT)
    rho = [heat.I.rational(Q(256 * n, sum(counts))) for n in counts]
    gamma = [Q(1, 2), Q(2), Q(1), Q(1)]
    jets = [-(heat.P * heat.P * heat.P).square() * rho[site] * gamma[role] * Q(1, 1024)
            for site, role in geometry.DIRECTIONS]
    early = np.array([(v.lo + v.hi) / 2 for v in jets])
    early_err = 1.000001 * np.array([max(c-v.lo, v.hi-c) for c,v in zip(early, jets)]) + 1e-290
    assert all(jets[i].lo == jets[i+1].lo and jets[i].hi == jets[i+1].hi
               for i in range(2, 128, 4))
    for values, errors in ((pointer, pointer_error),
                           (np.vstack((pointer, prices[1:])), np.vstack((pointer_error, price_error[1:])))):
        geometry.signed_rank(*restrict_to_fixed_volume(
            np.vstack((values, early)), np.vstack((errors, early_err))))
    print("Adding first Julia bit: rank 27, fibre dimension 69, joint rank 29 with depths 64 and 512.")
    print("Fixed individual volumes: 96 coordinates, pointer rank 26, "
          "level dimension 70, three independent thermal prices.")


if __name__ == "__main__":
    main()
