#!/usr/bin/env python3
"""Exact scope audit for the submitted extra-boost product-plane formula.

In the current owner convention B=K1+K2+K3. If the additional W in the
submitted formula is also K1+K2+K3, then CB(-d) CW(kappa) lies on the same
one-parameter Cayley subgroup and is exactly a reparameterization.
"""
import json
from pathlib import Path
import sympy as sp

OUT=Path(__file__).with_name("a4d_y_boost_cayley_composition_results.json")
I4=sp.eye(4)
B=sp.zeros(4)
for i in (1,2,3):
    B[0,i]=B[i,0]=1

def check(name,ok):
    if not ok:
        raise AssertionError(name)
    print("PASS_"+name,flush=True)

def cayley(a):
    den=4-3*a*a
    return I4+4*a/den*B+2*a*a/den*(B*B)

def run(write=False):
    d,k=sp.symbols("d k",real=True)
    t=sp.factor(4*(k-d)/(4-3*d*k))
    check("SAME_GENERATOR_CAYLEY_COMPOSITION",
          (cayley(-d)*cayley(k)-cayley(t)).applyfunc(sp.factor)==sp.zeros(4))
    old=sp.factor((3*t*t+4)/(3*t*t-4))
    submitted=sp.factor((-(9*d*d+12)*k*k+48*d*k-(12*d*d+16))/((3*d*d-4)*(3*k*k-4)))
    check("SUBMITTED_COEFFICIENT_IS_REPARAMETERIZED_OWNER_ROW",
          sp.factor(old-submitted)==0)
    num=sp.factor(-(9*d*d+12)*k*k+48*d*k-(12*d*d+16))
    disc=sp.factor(sp.discriminant(num,k))
    check("SUBMITTED_DISCRIMINANT",disc==-48*(3*d*d-4)**2)
    result={
      "schema":"a4d-y-boost-cayley-composition-v1",
      "owner_generator":"B=K1+K2+K3",
      "submitted_extra_generator":"W=K1+K2+K3",
      "effective_parameter":"t=4*(kappa-d)/(4-3*d*kappa)",
      "composition_identity":"C_B(-d) C_B(kappa)=C_B(t)",
      "coefficient_identity":"submitted c(d,kappa)=(3*t^2+4)/(3*t^2-4)",
      "discriminant":"-48*(3*d^2-4)^2",
      "conclusion":"under the current owner definitions this is an exact reparameterization of the existing one-dimensional B Cayley subgroup, not an additional independent boost direction",
      "scope_fence":"if a different generator was intended for C_B or W, it must be specified explicitly and this audit must be rerun"
    }
    if write:
      OUT.write_text(json.dumps(result,indent=2)+"\n")
      print("WROTE",OUT,flush=True)
    elif OUT.exists():
      check("RESULTS_MATCH_PINNED_JSON",result==json.loads(OUT.read_text()))
    print("TERMINAL A4D-Y-BOOST-EXTRA-FACTOR-IS-SAME-SUBGROUP-REPARAMETERIZATION",flush=True)
    return result

if __name__=="__main__":
    import sys
    run("--write" in sys.argv[1:])
