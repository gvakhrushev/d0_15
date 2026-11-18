"""Check the physical Slater cofactor weighting and a coherent calibration witness."""

from itertools import permutations
import json
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"round132"))
from check_paired_activation_reader import ne, gate, require, PIN


def sign(word):
    return (-1)**sum(x > y for i,x in enumerate(word) for y in word[i+1:])


def remaining_slot(effect):
    rank = effect.rows
    words = list(permutations(range(rank)))
    result = sp.zeros(rank)
    for left in words:
        for right in words:
            result[left[0], right[0]] += (
                sign(left)*sign(right)*sp.prod(effect[j,i] for i,j in zip(left[1:],right[1:]))
                / sp.factorial(rank)
            )
    return result


def verify_filtered_weights():
    z = sp.Rational(1,2**20)
    c2 = sp.Rational(3,8)
    k = sp.Rational(2,9)
    # A nonnormal real physical block, supported on a true rank 3 input.
    old = sp.Matrix([[sp.Rational(1,2),sp.Rational(1,5),0],
                     [0,sp.Rational(2,3),sp.Rational(1,8)],
                     [0,0,sp.Rational(3,4)]])
    require((sp.eye(3)-old*old.T).is_positive_definite, "Probe old block is not contractive")
    input_m = (1-z)*sp.eye(3)+z*c2*old.T*old
    effect = k*input_m
    residual = remaining_slot(effect)
    require(residual == effect.det()*effect.inv()/3, "The actual one-slot cofactor outcome is wrong")
    old_gram = old*old.T
    omega = old_gram*((1-z)*sp.eye(3)+z*c2*old_gram).inv()
    require(old*residual*old.T == effect.det()*omega/(3*k),
            "The previous returning filter did not produce the actual old resolvent")
    x = sp.diag(1,-1,0)
    require(sp.trace(x) == 0 and sp.trace(omega*x) != 0,
            "Uniform trace accidentally controls a genuinely weighted old row")
    return {"rank": 3, "normalized_remaining_old_input": "omega/Tr omega"}


def verify_backward_tangent():
    t = sp.Rational(3,7)
    root = sp.eye(2)
    v = sp.Matrix.vstack(sp.sqrt(1-t)*root,sp.sqrt(t)*root)
    pi = sp.diag(0,0,1,1)
    h = sp.Matrix([[1,3],[3,-2]])
    dv = (pi*v-t*v)*h/(2*t*(1-t))
    require(sp.simplify(v.T*dv) == sp.zeros(2), "Variation is not tangent to an isometry")
    require(sp.simplify(dv.T*pi*v+v.T*pi*dv) == h,
            "The old comparison cannot realize an arbitrary symmetric first jet")
    return True


def verify_terminal_phase():
    port, spin = 0, (1,2)
    word = tuple([gate("SourceI", port, *spin)]*2)
    execution = ne.Execution(3, (), (), word, ne.G_CX_SOURCE_I, port, spin)
    require(ne.exact_matrix_equal(
        ne.word_matrix(execution, max_qubits=3, max_expanded_stages=2),
        sp.diag(sp.eye(4),-sp.eye(4))
    ), "The old relative phase is not a literal native sign")
    x,y=sp.symbols("x y",positive=True)
    phase0, phase1 = sp.eye(2), sp.diag(1,-1)
    c = x*phase0+y*phase1
    require(((x+y)**2*sp.eye(2)-c.T*c-x*y*(phase0-phase1).T*(phase0-phase1)).applyfunc(sp.expand) == sp.zeros(2),
            "The actual coherent phase deficit identity failed")
    return True


def book00_defect():
    pi,s,t = sp.symbols("pi s t",real=True)
    joint = sp.Matrix([[pi*(1-t),pi*t],[(1-pi)*(1-s),(1-pi)*s]])
    ones = sp.ones(2,1)
    d = joint-(joint*ones)*(ones.T*joint)
    value = sp.trace(d.T*d)
    require(sp.expand(value-4*pi**2*(1-pi)**2*(s-t)**2) == 0,
            "Book00 paired comparator has wrong independence defect")
    return True


def main():
    print(json.dumps({
        "status":"PASS",
        "literal_native_sha256": PIN,
        "exact_nonscalar_old_state": verify_filtered_weights(),
        "real_stiefel_derivative_covers_all_symmetric_reverse_effect_jets": verify_backward_tangent(),
        "native_old_relative_phase_and_coherent_terminal_deficit": verify_terminal_phase(),
        "book00_independence_on_two_actual_loader_labels": book00_defect(),
        "old_truthful_report_alone_forces_no_equality_of_reverse_weights": True,
        "book03_full_work_or_info_selected": False,
        "GR_closed": False,
    },indent=2))


if __name__=="__main__":
    main()
