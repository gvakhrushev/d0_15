"""Check which data are shared by the existing A57 finite comparison pair."""
from fractions import Fraction
from pathlib import Path
import sys

sys.dont_write_bytecode = True
DIRECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DIRECT / "round57"))
import full_plane_family as family


def requests_for(field):
    for arm in family.ARMS:
        for axis in (0, 2687):
            yield tuple(family.Request(field, family.LegacyLabel(arm, s, axis))
                        for s in (-1, 1))
        for plane in ((1, 6), (0, (1 << family.CODE_BITS) - 1)):
            yield tuple(family.Request(field, family.PlaneLabel(arm, s, plane))
                        for s in (-1, 1))


def compare_packet_fields(field):
    task = family.FullPlaneTask(field)
    count = 0
    for minus, plus in requests_for(field):
        assert family.Request.decode(minus.encode()) == minus
        assert family.Request.decode(plus.encode()) == plus
        assert minus.encode() != plus.encode()
        left, right = task.packet(minus), task.packet(plus)
        different = {k for k in left if left[k] != right[k]}
        assert different == {"label", "request_sha256"}
        assert left["field_name_sha256"] == right["field_name_sha256"]
        assert left["actual_padded_lengths_hex"] == right["actual_padded_lengths_hex"]
        assert left["late_retention_pairs"] == right["late_retention_pairs"] == 222100
        assert left["same_actual_core_and_post_as_bound_A55"]
        count += 1
    return count


def check_split():
    # Single MG2 coordinate. Exact row/column identities apply separately to all 2688.
    h = Fraction(1, 2)
    connection = (1, -h, h, 0)
    def dot(x, y):
        return sum(a*b for a, b in zip(x, y))
    horizontal = (1, 0, 0, 0)
    kernel = ((h, 1, 0, 0), (-h, 0, 1, 0), (0, 0, 0, 1))
    assert dot(connection, horizontal) == 1
    assert all(dot(connection, z) == 0 for z in kernel)
    for i in range(4):
        original = tuple(int(j == i) for j in range(4))
        visible = dot(original, horizontal)
        independent = tuple(dot(original, z) for z in kernel)
        reconstructed = (visible, independent[0] - h*visible,
                         independent[1] + h*visible, independent[2])
        assert original == reconstructed


if __name__ == "__main__":
    fields = (family.FieldCentre(),
              family.FieldCentre(tuple(Fraction((j % 5)-2, 1 << 36) for j in range(2688))))
    count = sum(compare_packet_fields(field) for field in fields)
    check_split()
    print(f"{count} fixed-centre pairs verified at two centres; full MG2 four-row split is invertible.")
