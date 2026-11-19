"""Run both address orders on the complete native state; compare every paired gate overlap."""
from itertools import product
from math import sqrt
import json

from check_retained_replicas import Golden, a, p, one, ne, action, phase_word, rotation, decimal


def run(order):
    width=9
    gates=ne.Gate
    swap=(gates("CX",(3,4)),gates("CX",(4,3)),gates("CX",(3,4)))
    # Spin and PORT nonzero. Both sharp rails are retained and restored.
    start=(7<<6)|(order<<5)|((1-order)<<4)
    state={start|(j<<3)|(k<<1):(a,p)[j]*(a,p)[k] for j,k in product(range(2),repeat=2)}
    def advance(word):
        nonlocal state
        result=[]
        for gate in word:
            new=action(state,gate,width)
            inner=sum((v*new.get(i,Golden()) for i,v in state.items()),Golden())
            result.append(inner)
            state=new
        return result
    modes=((2,2),(2,3))
    stages=[]
    for j,t in ((5,6),(7,8)):
        layout=ne.Execution(width,(t,),(),(),ne.G_CX_SOURCE_I,2,(0,1))
        word=tuple(g for k,b in product(range(2),repeat=2) for g in
                   phase_word(layout,(3,j),(k,b),t,modes[k][b],
                              max_qubits=width,max_expanded_stages=500))
        stages.extend((advance(word),advance(swap)))
    assert all((i>>4)==(start>>4) for i in state)
    def bitprob(bit):
        return sum((v*v for i,v in state.items() if (i>>(width-1-bit))&1),Golden())
    expected=[p*rotation(pair[0])[1]*rotation(pair[0])[1]+
              p*p*rotation(pair[1])[1]*rotation(pair[1])[1] for pair in modes]
    assert bitprob(6)==expected[order] and bitprob(8)==expected[1-order]
    # Registers of different lanes are independent at each sharp code.
    for b,c in product(range(2),repeat=2):
        mass=sum((v*v for i,v in state.items() if ((i>>2)&1)==b and (i&1)==c),Golden())
        assert mass==(one-expected[order],expected[order])[b]*(one-expected[1-order],expected[1-order])[c]
    return stages,expected[order]


def main():
    s0,q0=run(0)
    s1,q1=run(1)
    assert s0[0]==s1[2] and s0[2]==s1[0] and s0[1]==s1[3] and s0[3]==s1[1]
    def total(stages):
        return sum(sqrt(max(0.,1-decimal(v)**2)) for row in stages for v in row)
    assert s0[0]!=s1[0] and abs(total([s0[0]])-total([s1[0]]))>.01
    assert .6<decimal(q0)<decimal(q1)<.8
    print(json.dumps(dict(complete_square_gates=sum(map(len,s0)),all_staged_overlaps_exact=True,
                          old_key_restored=True,first_lane_motion=[round(total([row[0]]),9) for row in (s0,s1)],
                          total_square_motion_both=round(total(s0),9),
                          fixed_address_probabilities=[round(decimal(q),12) for q in (q0,q1)],
                          geometry_word_executed=False,GR_closed=False),indent=2))

if __name__=="__main__":
    main()
