"""Three-letter balanced pointer, readout errors and the passive-reference instrument."""
from itertools import product
from math import sqrt

import numpy as np


def main():
    p=(sqrt(5)-1)/2
    a=sqrt(p)
    v=np.array([a,p])
    G=np.array([[a,-p],[p,a]])
    X=np.array([[0,1],[1,0]])
    states=[G@v,X@G@X@v]
    assert np.allclose(states[1],[1,0]) and np.allclose(states[0][0],p**3)
    assert all(abs(v@eta-a)<1e-14 for eta in states)
    assert abs(states[0]@states[1]-p**3)<1e-14
    for k in (1,2,5):
        wrong=p**(6*k)
        bits=list(product((0,1),repeat=3))
        channel=np.array([[np.prod([((1-wrong) if y==0 else wrong) if x==0 else int(y==1)
                                    for x,y in zip(src,dst)]) for src in bits] for dst in bits])
        assert np.allclose(channel.sum(axis=0),1)
        assert np.allclose(np.linalg.norm(channel-np.eye(8),1),2*(1-(1-wrong)**3))
        print("copies per label",k,"worst case total variation",1-(1-wrong)**3)


if __name__=="__main__":
    main()
