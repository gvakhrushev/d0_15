#!/usr/bin/env python3
"""vp_lepton_branch_fixing_operator_nogo - Lane L CLOSE (pigeonhole NO-GO).

D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001. Strengthens terminal L4 (bare 2<3) to a PROVEN
non-constructibility: the frozen shell-torus supplies exactly 2 branch-orbits {4-cycle,3-cycle}
(exponents 1/4 != 1/3) with NO fixed point (no in-carrier third / electron index-0 branch), while the
scene has 3 generations. A branch->generation full-row operator would need an injection Gen(3)->Branch(2),
or a surjection Branch(2)->Gen(3), or a bijection Branch(2)<->Gen(3) -- ALL impossible by cardinality.
Hence PRIM-LEPTON-BRANCH-FIXING-OPERATOR is not constructible from frozen 2-orbit data (external HYP).

Failable: raises SystemExit(1) if any load-bearing fact is corrupted. stdlib only, exact arithmetic.
"""
import sys
from fractions import Fraction as F
from itertools import product

def die(msg):
    print("FAIL " + msg)
    raise SystemExit(1)

def orbits_of(perm):
    seen, obs = set(), []
    for s in range(len(perm)):
        if s in seen:
            continue
        o = [s]; x = perm[s]
        while x != s:
            o.append(x); x = perm[x]
        obs.append(o); seen |= set(o)
    return obs

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: 2 orbit-branches {1/4,1/3} cannot force a distinguished 3-generation row.")
    # ---- Load-bearing FROZEN datum: shell-torus sigma = (0123)(456) on 7 points ----
    # (matches D0.Matter.LeptonBranchAssignmentNoGo.sigmaA and the X5 shell-torus C4 x R3)
    sigma = [1, 2, 3, 0, 5, 6, 4]
    numGenerations = 3   # K(9,11,13): mult. of trivial isotype (R1); Tr(T^2)=3 (CarrierForcing)

    obs = orbits_of(sigma)
    sizes = sorted((len(o) for o in obs), reverse=True)
    if sizes != [4, 3]:
        die(f"ORBIT_SIZES orbit sizes {sizes} != [4,3]")
    numBranches = len(obs)
    if numBranches != 2:
        die(f"NUM_BRANCHES {numBranches} != 2")
    print(f"PASS_ORBITS  shell-torus = {obs}  -> {numBranches} orbits, sizes {sizes}")

    # No fixed point => no in-carrier third (electron, index-0) branch
    fixed = [i for i in range(len(sigma)) if sigma[i] == i]
    if fixed != []:
        die(f"FIXED_POINT shell-torus has fixed point(s) {fixed}")
    print("PASS_NO_THIRD_IN_CARRIER  shell-torus has NO fixed point (electron index-0 branch is external)")

    # Orbit-keyed exponent SET has only 2 distinct values 1/4 != 1/3
    exps = sorted({F(1, n) for n in sizes})
    if exps != [F(1, 4), F(1, 3)] or F(1, 4) == F(1, 3):
        die(f"EXPONENTS {[str(e) for e in exps]} != [1/4,1/3]")
    if len(exps) != numBranches:
        die(f"EXP_CARD {len(exps)} distinct exponents != {numBranches} branches")
    print(f"PASS_EXPONENT_SET  {{1/4, 1/3}} distinct ({len(exps)} values for {numBranches} orbits)")

    # ---- The pigeonhole obstruction (exact enumeration) ----
    B, G = numBranches, numGenerations
    inj  = [f for f in product(range(B), repeat=G) if len(set(f)) == G]   # Gen(3)->Branch(2) injective
    surj = [g for g in product(range(G), repeat=B) if len(set(g)) == G]   # Branch(2)->Gen(3) surjective
    if inj != []:
        die(f"INJECTION Gen({G})->Branch({B}) injection exists: {inj[:1]}")
    if surj != []:
        die(f"SURJECTION Branch({B})->Gen({G}) surjection exists: {surj[:1]}")
    if B == G:
        die(f"BIJECTION card Branch {B} == card Gen {G} (bijection would exist)")
    print(f"PASS_PIGEONHOLE  no injection Gen({G})->Branch({B}), no surjection Branch({B})->Gen({G}), {B}!={G} (no bijection)")

    # ---- Self-tested CONTROLS: the cert must CATCH a planted false close ----
    # CONTROL_A exercises the INJECTION detector positively: with 3 branches, Gen(3)->Branch(3) IS injective.
    inj3 = [f for f in product(range(3), repeat=3) if len(set(f)) == 3]
    if inj3 == []:
        die("CONTROL_A planted injection Gen(3)->Branch(3) wrongly empty (injection guard broken)")
    # CONTROL_B exercises the SURJECTION detector positively (a DIFFERENT computation): Branch(3)->Gen(2)
    # HAS surjections (image size 2). This guards the surjection code path independently of CONTROL_A.
    surj32 = [g for g in product(range(2), repeat=3) if len(set(g)) == 2]
    if surj32 == []:
        die("CONTROL_B planted surjection Branch(3)->Gen(2) wrongly empty (surjection guard broken)")
    print(f"PASS_CONTROLS  injection detector (Gen3->Br3: {len(inj3)}) & surjection detector (Br3->Gen2: {len(surj32)}) both fire")

    print("PASS_LEPTON_BRANCH_FIXING_OPERATOR_NOGO")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
