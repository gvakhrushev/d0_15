#!/usr/bin/env python3
"""Exact whole-stencil C2 audit for a direct Julia readout per plaquette.

Each changed based face receives one instrument T(P)=P/2 with its complete
success/failure flag and all 13 positive Choi/POVM effects retained.  The
face-mapped negative effect is Golden-refined only on that face's success
branch.  This is a conditional price candidate, not a native D0 selection.
"""

from itertools import combinations, product

import sympy as sp

import check_four_gate_commutator_c2 as model


LENGTH = 3
ORIGIN = (0, 0, 0, 0)
SITES = tuple(product(range(LENGTH), repeat=4))
PAIRS = tuple(combinations(range(4), 2))
H = sp.symbols("h", positive=True)
ETA = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                 [0, 0, -1, 0], [0, 0, 0, -1]])
I4 = model.I4
ZERO4 = model.ZERO4

# Original flat-six-face map: face orientation -> negative-pointer index.
FACE_POINTER = {
    (0, 1): model.GENERATOR_NAMES.index("B"),
    (0, 2): model.GENERATOR_NAMES.index("barN2"),
    (0, 3): model.GENERATOR_NAMES.index("barN3"),
    (1, 2): model.GENERATOR_NAMES.index("N2"),
    (1, 3): model.GENERATOR_NAMES.index("N3"),
    (2, 3): model.GENERATOR_NAMES.index("J"),
}
FACE_POINTER = {face: 2 * generator + 1
                for face, generator in FACE_POINTER.items()}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def shift(site, axis, amount=1):
    out = list(site)
    out[axis] = (out[axis] + amount) % LENGTH
    return tuple(out)


def face_edges(site, r, t):
    """Positive-link keys in original based-plaquette factor order."""
    return ((site, r, 1), (shift(site, r), t, 1),
            (shift(site, t), r, -1), (site, t, -1))


def edge_set(site, r, t):
    return frozenset((at, axis) for at, axis, _ in face_edges(site, r, t))


def link_factor_jet(link_key, orientation, marked_links):
    identity = [I4, ZERO4, ZERO4, ZERO4]
    if link_key not in marked_links:
        return tuple(identity)
    variable, generator = marked_links[link_key]
    identity[1 if variable == "a" else 2] = orientation * generator
    return tuple(identity)


def plaquette_jet(site, r, t, marked_links):
    out = (I4, ZERO4, ZERO4, ZERO4)
    for at, axis, orientation in face_edges(site, r, t):
        out = model.jet_product(
            out, link_factor_jet((at, axis), orientation, marked_links)
        )
    return out


def affected_faces(marked_links):
    marked_keys = frozenset(marked_links)
    out = []
    for site in SITES:
        for face in PAIRS:
            if edge_set(site, *face) & marked_keys:
                out.append((site, face))
    return out


def inverse_lorentz_jet(plaquette):
    return tuple(ETA * matrix.T * ETA for matrix in plaquette)


def palatini_face_density_jet(face, plaquette):
    """Original flat-coframe G2(e_u wedge e_v, star R(P)) face density."""
    r, t = face
    u, v = (axis for axis in range(4) if axis not in face)
    inverse = inverse_lorentz_jet(plaquette)
    curvature = tuple((plaquette[k] - inverse[k]) / 2 for k in range(4))
    curvature_dual = tuple(matrix * ETA for matrix in curvature)
    bivector = sp.S.Zero
    for a, b in PAIRS:
        c, d = (axis for axis in range(4) if axis not in (a, b))
        coframe_wedge = H**2 * (
            int(a == u and b == v) - int(b == u and a == v)
        )
        bivector += (sp.LeviCivita(a, b, c, d)
                     * coframe_wedge * curvature_dual[0][c, d])
    scale = sp.LeviCivita(r, t, u, v)
    density = [scale * bivector]
    for index in range(1, 4):
        linear = sp.S.Zero
        for a, b in PAIRS:
            c, d = (axis for axis in range(4) if axis not in (a, b))
            coframe_wedge = H**2 * (
                int(a == u and b == v) - int(b == u and a == v)
            )
            linear += (sp.LeviCivita(a, b, c, d) * coframe_wedge
                       * curvature_dual[index][c, d])
        density.append(scale * linear)
    return tuple(sp.simplify(value) for value in density)


def direct_face_price_jet(plaquette, pointer_index):
    success, failure = model.direct_julia_instrument(plaquette)
    branches = (("success", success), ("failure", failure))
    model.assert_complete_kraus_jets(branches, "direct whole-plaquette Julia map")
    records = model.record_probability_jets(branches, "direct whole-plaquette Julia map")
    fine, selected = model.split_pointer_on_history(
        records, pointer_index, "success"
    )
    require(selected[0] > 0, "success-branch pointer has positive baseline")
    return (
        model.entropy_first_jet(fine, 1),
        model.entropy_first_jet(fine, 2),
        model.entropy_mixed_jet(fine),
    )


def local_totals(marked_links):
    faces = affected_faces(marked_links)
    geometry = [sp.S.Zero] * 4
    price = [sp.S.Zero] * 3
    cache = {}
    for site, face in faces:
        word = plaquette_jet(site, *face, marked_links)
        density = palatini_face_density_jet(face, word)
        geometry = [geometry[k] + density[k] for k in range(4)]

        # Translated faces with the same orientation and word have identical
        # local records; cache the full exact POVM/entropy calculation.
        key = (face, tuple(tuple(x for x in matrix) for matrix in word))
        if key not in cache:
            cache[key] = direct_face_price_jet(word, FACE_POINTER[face])
        face_price = cache[key]
        price = [price[k] + face_price[k] for k in range(3)]
    return faces, tuple(map(sp.simplify, geometry)), tuple(map(sp.simplify, price))


def commutator_links(direction_pair, first_generator, second_generator):
    r, t = direction_pair
    return {
        (ORIGIN, r): ("a", first_generator),
        (shift(ORIGIN, r), t): ("b", second_generator),
        (shift(ORIGIN, t), r): ("a", first_generator),
        (ORIGIN, t): ("b", second_generator),
    }


def check_commutator(name, face, first_generator, second_generator):
    marked = commutator_links(face, first_generator, second_generator)
    faces, geometry, price = local_totals(marked)
    require(len(faces) == 21, f"{name}: all 21 affected based faces are included")
    require(geometry[1:] == (0, 0, -H**2),
            f"{name}: summed original six-face geometry has only mixed -h^2 jet; got {geometry}")
    require(price[0] == 0 and price[1] == 0,
            f"{name}: complete direct product has zero first-a and first-b source; got {price[:2]}")
    require(sp.simplify(price[2] + model.C_SH) == 0,
            f"{name}: full 21-face direct price has mixed source -c_Sh; got {price[2]}")
    require(sp.simplify((H**2 / model.C_SH) * price[2] + H**2) == 0,
            f"{name}: first-jet-fixed scale matches the full mixed geometric jet")
    return faces, geometry, price


def check_six_face_first_jet_scale():
    face_generators = {
        (0, 1): model.B,
        (0, 2): model.BAR_N2,
        (0, 3): model.BAR_N3,
        (1, 2): model.N2,
        (1, 3): model.N3,
        (2, 3): model.J,
    }
    for face, generator in face_generators.items():
        r, t = face
        marked = {(ORIGIN, r): ("a", generator)}
        word = plaquette_jet(ORIGIN, r, t, marked)
        geometry = palatini_face_density_jet(face, word)
        price = direct_face_price_jet(word, FACE_POINTER[face])
        require(geometry == (0, -H**2, 0, 0),
                f"face {face}: original mapped-generator first coefficient is -h^2")
        require(sp.simplify(price[0] + model.C_SH) == 0
                and price[1:] == (0, 0),
                f"face {face}: complete direct success-branch Golden source is -c_Sh")
        require(sp.simplify((H**2 / model.C_SH) * price[0] + H**2) == 0,
                f"face {face}: one common first-jet scale matches the original geometry")


def check_commuting_control():
    marked = {
        (ORIGIN, 0): ("a", model.J),
        # The oriented history is (+J,-J).  These are two adjacent links in
        # the same commuting one-parameter subgroup; reversing the second
        # tangent reverses the mixed price jet but leaves geometric curvature
        # identically zero.
        (ORIGIN, 1): ("b", -model.J),
    }
    faces, geometry, price = local_totals(marked)
    require(len(faces) == 11, "commuting-J control has all 11 affected based faces")
    require(geometry == (0, 0, 0, 0),
            f"commuting-J control has zero complete original geometric jets; got {geometry}")
    require(price[0] == 0 and price[1] == 0,
            f"commuting-J control first price jets vanish; got {price[:2]}")
    p = model.P
    expected = H**2 * sp.sqrt(2) * (
        4 + 10 * sp.log(12) + (sp.sqrt(5) - 5) * sp.log(p) / 2
    ) / ((5 - sp.sqrt(5)) * sp.log(p))
    large_logs = [item for item in price[2].atoms(sp.log)
                  if item.args[0] != p]
    require(len(large_logs) == 1,
            "hostile-control entropy has one non-Golden logarithm")
    large_log = large_logs[0]
    exact_log_argument = (
        2**45 * 3**20 * (2**6 * 3)**sp.sqrt(5)
        * (sp.sqrt(5) - 1)**(-5 + sp.sqrt(5))
        / (2**7 * 3)**sp.sqrt(5)
    )
    require(sp.simplify(large_log.args[0] / exact_log_argument) == 1,
            "hostile-control logarithm has the exact factored argument")
    # Its logarithm is 20 log(12) + (sqrt(5)-5) log(p), by prime
    # factorization and sqrt(5)-1=2p.
    normalized_price = price[2].xreplace({
        large_log: 20 * sp.log(12) + (sp.sqrt(5) - 5) * sp.log(p)
    })
    require(sp.simplify(sp.expand(H**2 / model.C_SH * normalized_price
                                  - expected)) == 0,
            "commuting-J hostile control has the exact predicted spurious mixed source")
    require(1 < sp.sqrt(5) < 3, "1 < sqrt(5) < 3")
    require(sp.simplify(p > 0) is sp.true and sp.simplify(p < 1) is sp.true,
            "Golden p lies strictly between zero and one")
    # Therefore log(p)<0, sqrt(5)-5<0, and their product is positive;
    # log(12)>0. The numerator is strictly positive and the denominator
    # strictly negative, so the displayed exact coefficient is negative.
    require(sp.N(expected / H**2) < 0,
            "commuting-control coefficient has the predicted negative sign")
    return faces, geometry, price, expected


def run():
    check_six_face_first_jet_scale()
    rotation = check_commutator(
        "J commutator", (2, 3), model.N2, model.BAR_N3
    )
    boost = check_commutator(
        "B commutator", (0, 1), model.N2, model.BAR_N2
    )
    control = check_commuting_control()
    print("PASS all six original face/generator first jets: direct complete price -c_Sh and geometry -h^2")
    for label, result in (("J", rotation), ("B", boost)):
        faces, geometry, price = result
        print(f"PASS {label}: {len(faces)} affected based faces; geometry jets={geometry}")
        print(f"PASS {label}: direct price first jets=(0, 0), mixed=-c_Sh={sp.sstr(-model.C_SH)}")
        print(f"PASS {label}: h^2/c_Sh scale matches the all-face mixed source")
    faces, geometry, price, scaled = control
    print(f"PASS commuting-J hostile control: {len(faces)} affected based faces; geometry jets={geometry}")
    print("PASS commuting-J direct price first jets=(0, 0), mixed jet is nonzero")
    print(f"FAILS candidate as required: scaled spurious mixed source={sp.sstr(scaled)}")
    print("SCOPE: conditional direct-per-plaquette Julia/Golden candidate only; no native D0 price selection or whole-core no-go")


if __name__ == "__main__":
    run()
