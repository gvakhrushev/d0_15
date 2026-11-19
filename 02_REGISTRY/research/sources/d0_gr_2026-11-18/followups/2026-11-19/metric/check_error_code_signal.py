"""Independent output-instrument replay of the reversible error code."""
import json
import math
from pathlib import Path
import numpy as np


def main():
    p=(math.sqrt(5)-1)/2; a=math.sqrt(p); r=p*p
    G=np.array([[a,-p],[p,a]])
    nwire=7; dim=1<<nwire
    T,TARGET,N,TN,FLAG,ENV,OUT=range(nwire)
    def one(x,wire,mat):
        y=x.copy()
        for j in range(dim):
            if not ((j>>wire)&1):
                k=j|(1<<wire)
                y[j]=mat[0,0]*x[j]+mat[0,1]*x[k]
                y[k]=mat[1,0]*x[j]+mat[1,1]*x[k]
        return y
    def cx(x,control,target):
        y=x.copy()
        for j in range(dim):
            if (j>>control)&1 and not ((j>>target)&1):
                k=j|(1<<target);y[j],y[k]=x[k],x[j]
        return y
    columns=[]
    for t in (0,1):
      for target in (0,1):
        x=np.zeros(dim);x[(t<<T)|(target<<TARGET)]=1
        for wire in (N,TN,FLAG,ENV,OUT):x=one(x,wire,G)
        x=cx(x,T,N)
        x=cx(x,N,TN);x=one(x,TN,G);x=cx(x,N,TN)
        x=one(x,FLAG,G.T);x=cx(x,N,FLAG)
        x=one(x,ENV,G.T);x=cx(x,FLAG,ENV)
        x=cx(x,FLAG,TARGET)
        x=one(x,TN,G.T);x=cx(x,FLAG,TN)
        x=one(x,TN,G.T);x=cx(x,FLAG,TN)
        x=cx(x,T,FLAG)              # E = N xor T
        x=cx(x,FLAG,OUT);x=one(x,OUT,G);x=cx(x,FLAG,OUT)
        for _ in range(20):x=cx(cx(x,T,TARGET),T,TARGET)
        columns.append(x)
    V=np.array(columns).T
    assert np.max(np.abs(np.einsum('ki,kj->ij',V,V)-np.eye(4)))<1e-12
    indices=np.arange(dim)
    def eff(mask):
        Q=V[mask,:]
        return np.einsum('ki,kj->ij',Q,Q)
    bit=lambda w:((indices>>w)&1)
    error1=eff(bit(FLAG)==1)
    n1=eff(bit(ENV)==1)
    assert np.max(np.abs(error1-r*np.eye(4)))<1e-12
    assert np.max(np.abs(n1-np.diag([r,r,p,p])))<1e-12
    assert np.linalg.norm(V[(bit(N)!=bit(ENV))|((bit(N)^bit(T))!=bit(FLAG)),:])<1e-12
    assert np.linalg.norm(V[(bit(FLAG)==1)&(bit(OUT)==1),:])<1e-12
    for t in (0,1):
      for e in (0,1):
        joint=eff((bit(T)==t)&(bit(FLAG)==e))
        P=np.diag([1,1,0,0]) if t==0 else np.diag([0,0,1,1])
        assert np.max(np.abs(joint-(r if e else p)*P))<1e-12
    # A fresh target initially in |0> ends as N; reading it is a further
    # physical operation and is not assumed to have already been paid.
    target1=eff(bit(TARGET)==1)
    for oldcol in (0,2):
        assert abs(target1[oldcol,oldcol]-n1[oldcol,oldcol])<1e-12
    q=.37;Pn=r+p**3*q
    h=lambda x:-x*math.log(x)-(1-x)*math.log1p(-x)
    mutual_N=h(Pn)-h(r)
    fisher_N=(p**3)**2/(Pn*(1-Pn))
    assert mutual_N>0 and fisher_N>0
    info_joint=h(q) # (N,E) determines old T = N xor E
    receipt=json.loads(Path(__file__).with_name('reversible_error_code_result.json').read_text())
    assert receipt['clock_dimension']==68000 and receipt['physical_0_10_transmitter_and_stop_compiled'] is False
    print(json.dumps({
      'status':'PASS','old_input_columns_checked':4,
      'native_inverse_SourceI_and_full_clock':'referenced reversible_error_code receipt',
      'old_port_spin_and_RIGHT':'tensor extension of checked logical effect',
      'E_one_effect':'p^2 I on all old inputs',
      'N_one_effect':'diag(p^2,p) on old T, identity on other old inputs',
      'd_P_E1_dq':0,'d_P_N1_dq':round(p**3,12),
      'E_and_T_independent':True,'N_and_E_joint_determine_T':True,
      'example_q':q,'example_mutual_information_T_N_nats':round(mutual_N,12),
      'example_mutual_information_T_E_nats':0,
      'example_mutual_information_T_N_E_nats':round(info_joint,12),
      'example_N_fisher_wrt_q':round(fisher_N,12),'E_fisher_wrt_q':0,
      'separate_N_or_T_output_compiled_and_paid':False,
      'full_book_cost_info_identified':False,'GR_closed':False,
    },sort_keys=True,indent=2))


if __name__=='__main__':main()
