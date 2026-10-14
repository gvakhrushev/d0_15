"""A hostile test against a tempting but false pi0-phase numerical root.
This is a diagnostic phase assignment, not an assertion about native D0 holonomies.
"""
from itertools import combinations_with_replacement
from math import factorial
from collections import Counter
from pathlib import Path
import json
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]
def main():
    iv=mp.iv;iv.dps=50;L=8;theta=iv.mpf(12)/5
    re=[L*(iv.cos((2*iv.pi*k+theta)/L)-1)for k in range(L)]
    im=[L*iv.sin((2*iv.pi*k+theta)/L)for k in range(L)]
    def energy(ks):
        # V_sep = (4/5) I + (1/5) 11^T; strictly positive.
        A=sum(re[k]**2+im[k]**2 for k in ks)
        Sre=sum(re[k] for k in ks);Sim=sum(im[k]for k in ks)
        return iv.mpf(4)/5*A+(Sre*Sre+Sim*Sim)/5
    chosen=(0,0,0,7);E0=energy(chosen);modes=0;orbits=0
    for ks in combinations_with_replacement(range(8),4):
        mult=factorial(4)
        for n in Counter(ks).values():mult//=factorial(n)
        modes+=mult;orbits+=1
        if ks==chosen:continue
        if not(energy(ks)-E0>iv.mpf(7)):
            raise AssertionError(('SEPARATING_FUNCTIONAL_GAP',ks,energy(ks)-E0))
    if modes!=4096 or orbits!=330:raise AssertionError('FULL_MODE_COVER')
    out={'status':'PASS','result':'NO_FINITE_GIBBS_MOMENT_ROOT_FOR_THIS_DIAGNOSTIC_SHELL',
        'theta_total_each_of_four_cycles':'12/5','L':8,'mode_count':4096,
        'permutation_orbits_checked':330,'selected_momentum_orbit':'permutations of (0,0,0,7)',
        'separating_positive_matrix':'V=(4/5)I+(1/5)11^T',
        'all_other_modes_gap_strictly_greater_than':7,
        'selected_energy_interval':str(E0),
        'proof':'Selected occupation lies on an exposed face of the moment polytope. Every finite-temperature Gibbs state has positive weights on all remaining modes, hence its V moment is strictly larger. A tiny floating residual is not a root.',
        'native_pi0_assignment_claimed':False}
    (ROOT/'results/pi0_phase_boundary.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS_PI0_HOSTILE_PHASE_TEST',orbits,'orbits cover',modes,'modes; finite-root shortcut rejected')
if __name__=='__main__':main()
