"""Check the signed Golden preparation and the no-controlled-U determinant readout."""

import itertools
import json
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round132"))
from check_paired_activation_reader import ne, require, gate, PIN


def parity(number):
    return bin(number).count("1") % 2


def permutation_sign(values):
    return (-1)**sum(a > b for i, a in enumerate(values) for b in values[i+1:])


def signed_permutation_columns(rank):
    width = (rank-1).bit_length()
    n = rank*width
    mask = (1 << width)-1
    signs = {}
    for column in range(1 << n):
        labels = tuple((column >> ((rank-1-slot)*width)) & mask for slot in range(rank))
        if set(labels) == set(range(rank)):
            signs[column] = permutation_sign(labels)
    require(len(signs) == sp.factorial(rank), "The compiler lost a permutation")
    expected_weight = sum(bin(i).count("1") for i in range(rank))
    require({bin(col).count("1") for col in signs} == {expected_weight},
            "The Golden input does not have equal permutation amplitudes")
    return n, expected_weight, signs


def gray_coefficients(n, signs):
    gray = [i^(i >> 1) for i in range(1 << n)]
    coefficients = [sum((-1)**parity(g & col)*sign for col, sign in signs.items()) for g in gray]
    for col in range(1 << n):
        angle = sum((-1)**parity(g & col)*c for g, c in zip(gray, coefficients))
        require(angle == (1 << n)*signs.get(col, 0), "The actual Gray exponents changed")
    return gray, coefficients


def verify_literal_rank_two():
    rank = 2
    n, weight, signs = signed_permutation_columns(rank)
    gray, coeffs = gray_coefficients(n, signs)
    flag, spin = n, (n+1, n+2)
    z = [gate("SourceI", flag, *spin)]*2
    word = []
    for i, coefficient in enumerate(coeffs):
        rotation = [gate("G", flag)]*abs(coefficient)
        word += rotation if coefficient >= 0 else z+rotation+z
        bit = (gray[i]^gray[(i+1) % len(gray)]).bit_length()-1
        word.append(gate("CX", n-1-bit, flag))
    execution = ne.Execution(n+3, (), (), tuple(word), ne.G_CX_SOURCE_I, flag, spin)
    literal = ne.word_matrix(execution, max_qubits=5, max_expanded_stages=len(word))
    g = sp.Matrix(ne.G_LOCAL)
    expected = sp.kronecker_product(
        sp.diag(*[g**((1 << n)*signs.get(col, 0)) for col in range(1 << n)]), sp.eye(4)
    )
    require(ne.exact_matrix_equal(literal, expected), "The signed sieve changed a literal protected column")
    p, a = ne.P, ne.A
    v = sp.Matrix([a, p])
    prepared = literal*sp.kronecker_product(v,v,sp.Matrix([1,0]),sp.eye(4)[:,0])
    selected = sp.Matrix([prepared[8*j+4] for j in range(4)])
    signed = sp.Matrix([signs.get(j,0) for j in range(4)])
    require(ne.exact_matrix_equal(selected, (g**(1 << n))[1,0]*a**(n-weight)*p**weight*signed),
            "The actual successful branch is not the signed Slater ray")
    return len(word), weight


def verify_determinant():
    z, ready = sp.symbols("z readiness", positive=True)
    c = sp.Matrix([[sp.Rational(1,2), sp.Rational(1,4), 0],
                   [0, sp.Rational(2,3), sp.Rational(1,5)],
                   [0, 0, sp.Rational(3,4)]])
    f = sp.eye(3) - c.T*c
    effect = ready*(sp.eye(3)-z*f)
    permutations = list(itertools.permutations(range(3)))
    value = sum(permutation_sign(left)*permutation_sign(right)
                *sp.prod(effect[a,b] for a,b in zip(left,right))
                for left,right in itertools.product(permutations,repeat=2))/6
    require(sp.expand(value-ready**3*sp.det(sp.eye(3)-z*f)) == 0,
            "Independent retained flag/readers failed to realize the determinant")
    shared = ready**3*(1-z+z*sp.det(c.T*c))
    require(sp.expand((value-shared).subs(z, sp.Rational(1,2**20))) != 0,
            "A single shared flag passed the determinant test")
    return True


def main():
    stage_count, weight = verify_literal_rank_two()
    n3, weight3, signs3 = signed_permutation_columns(3)
    gray_coefficients(n3, signs3)
    print(json.dumps({
        "status": "PASS",
        "native_gate_sha256": PIN,
        "rank_2_signed_filter_all_matrix_columns": 32,
        "rank_2_signed_filter_literal_stages": stage_count,
        "rank_2_born_permutation_weight": weight,
        "rank_3_gray_control_columns": 1 << n3,
        "rank_3_born_permutation_weight": weight3,
        "rank_3_joint_nonscalar_feedback_determinant": verify_determinant(),
        "shared_flag_rejected": True,
        "conditional_slater_preparation_uses_no_logical_Toffoli_or_Hadamard": True,
        "controlled_copy_of_field_word_required": False,
        "physical_book_work_or_info_selected": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
