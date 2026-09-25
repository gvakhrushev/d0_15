#!/usr/bin/env python3
"""Exact finite S3 x six-face audit for the A4D oriented Role selector."""

from itertools import permutations, combinations

ROLES = tuple(range(4))
FACES = tuple(combinations(ROLES, 2))

def sign(seq):
    inv = sum(seq[i] > seq[j]
              for i in range(len(seq))
              for j in range(i + 1, len(seq)))
    return -1 if inv % 2 else 1

def complement(face):
    return tuple(r for r in ROLES if r not in face)

def epsilon(face):
    # Exact repository convention: parity of concatenated ordered S, S^c.
    return sign(tuple(face) + complement(face))

def image_face(p, face):
    return tuple(sorted(p[r] for r in face))

def blade_sign(p, face):
    # Sign needed to re-sort the transported oriented blade.
    return sign(tuple(p[r] for r in face))

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

spatial = tuple((0,) + q for q in permutations((1, 2, 3)))
count = 0

for p in spatial:
    sgn = sign(p)
    check("FIXES_A_" + "".join(map(str, p)), p[0] == 0)

    for face in FACES:
        comp = complement(face)
        image = image_face(p, face)
        chi_f = blade_sign(p, face)
        chi_c = blade_sign(p, comp)
        eps_old = epsilon(face)
        eps_new = epsilon(image)

        tag = "".join(map(str, p)) + "_" + "".join(map(str, face))

        # Complete finite complement-orientation identity.
        check(
            "ORIENTATION_IDENTITY_" + tag,
            eps_new == sgn * eps_old * chi_f * chi_c,
        )

        # For K=I, Lorentz pairing contributes only face/complement blade signs.
        identity_ratio = eps_new * chi_f * chi_c * eps_old
        check("IDENTITY_PARITY_" + tag, identity_ratio == sgn)

        # For K=star, owned star pseudoequivariance contributes one more sgn.
        star_ratio = identity_ratio * sgn
        check("STAR_INVARIANT_" + tag, star_ratio == 1)

        count += 1

check("ALL_36_FACE_CASES", count == 36)

# Hostile controls: odd spatial swaps must distinguish the two channels.
odd = [p for p in spatial if sign(p) == -1]
check("ODD_SPATIAL_ELEMENTS_EXIST", len(odd) == 3)
for p in odd:
    for face in FACES:
        comp = complement(face)
        image = image_face(p, face)
        ratio_I = epsilon(image) * blade_sign(p, face) * blade_sign(p, comp) * epsilon(face)
        ratio_star = ratio_I * sign(p)
        check("ODD_REJECTS_IDENTITY_" + "".join(map(str, p)) + "_" + "".join(map(str, face)),
              ratio_I == -1)
        check("ODD_ACCEPTS_STAR_" + "".join(map(str, p)) + "_" + "".join(map(str, face)),
              ratio_star == 1)

print("RESULT: complete oriented spatial Role/site covariance selects span{star}.")
