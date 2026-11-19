"""Verify the instrument, both central characters, and the all-success norm bound."""
from itertools import product
import json
import mpmath as mp
import sympy as sp

a = sp.symbols("a", real=True)
p = a**2
modulus = a**4+a**2-1


def exact(matrix):
    for x in matrix:
        if sp.rem(sp.expand(x),modulus,a) != 0:
            raise ValueError(f"Nonzero polynomial: {x}")


def permutation(wires, action):
    out = sp.zeros(2**wires)
    for bits in product(range(2),repeat=wires):
        def index(sequence):
            return sum(x*2**i for i,x in enumerate(reversed(sequence)))
        out[index(action(*bits)),index(bits)] = 1
    return out


def main():
    j = permutation(2,lambda t,c:(1-t,c^t))
    lift_z = permutation(2,lambda t,c:(t,c^t))
    controlled_j = permutation(3,lambda h,t,c:(h,t^h,c^(h&t)))
    eye = sp.eye(4)
    signed_g = sp.Matrix([[a,-p],[p,a]])
    absolute_g = sp.Matrix([[a,p],[p,a]])
    born = sp.Matrix([a,p])
    first = sp.kronecker_product(born,eye)
    # sqrt(2)*K_f (unnormalized +/- row vector); both raw outcomes retained.
    blocks = [sp.kronecker_product(sp.Matrix([[1,sgn]]),eye)*controlled_j*first
              for sgn in (1,-1)]
    for sign, weighted in zip((1,-1),blocks):
        exact(weighted-(a*eye+sign*p*j))
    exact(sum((b.T*b for b in blocks),sp.zeros(4))-2*eye)
    for tag in (1,-1):
        embedding = sp.kronecker_product(sp.eye(2),sp.Matrix([1,tag]))
        target = absolute_g if tag==1 else signed_g
        diag = sp.diag(1,tag)
        exact(blocks[0]*embedding-embedding*target)
        exact(lift_z*embedding-embedding*diag)
        if tag==-1:
            exact(embedding.T*blocks[0].T*blocks[0]*embedding-2*sp.eye(2))
    ideal_direction = sp.ones(4,1)
    exact(j*ideal_direction-ideal_direction)
    exact((blocks[0]**4)*ideal_direction-(a+p)**4*ideal_direction)
    mp.mp.dps = 70
    native_p = (mp.sqrt(5)-1)/2
    growth = mp.sqrt(native_p)+native_p
    n = 2320
    result = {"gate_head_outcomes":2, "input_tag_signs":[1,-1],
              "number_of_field_rotations":n,
              "log10_all_success_upper_bound":mp.nstr(-2*n*mp.log10(growth),17),
              "log10_uniform_negative_tag_success_explicit_filter":
                  mp.nstr(-n*mp.log10(2),17),
              "field_branch_filtered_ports":"one common attenuation, both tags, all columns",
              "proved_for_unrestricted_Book_memory":False,"GR_closed":False}
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
