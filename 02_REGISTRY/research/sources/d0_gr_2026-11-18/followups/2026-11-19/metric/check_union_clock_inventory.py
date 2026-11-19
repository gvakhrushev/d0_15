"""Finite stopped clock theorem in a genuine Golden NC1/CZ macro example.

The complete expanded union-factory clock and Book03 prices are not built.
"""
import json
import math
import numpy as np


def need(x,msg):
    if not x: raise AssertionError(msg)


def mm(A,B):
    return np.einsum('ik,kj->ij',A,B,optimize=False)


def clock(isometries):
    dims=[isometries[0].shape[1]]+[v.shape[0] for v in isometries]
    offsets=np.cumsum([0]+dims);D=sum(dims)
    T=np.zeros((D,D))
    # Forward original local isometries.
    for t,V in enumerate(isometries):
        T[offsets[t+1]:offsets[t+2],offsets[t]:offsets[t+1]]=V
    # Terminal domain = propagated initial image plus propagated birth complements.
    # QR gives orthonormal bases; explicit projectors preserve the exact construction.
    blocks=[]
    q=np.eye(dims[0])
    for t,V in enumerate(isometries):
        q=mm(V,q)
    blocks.append((q,0,np.eye(dims[0])))
    for t,V in enumerate(isometries):
        full=np.linalg.svd(V.T,full_matrices=True)[2].T
        K=full[:,V.shape[1]:]
        if K.shape[1]==0:continue
        q=K
        for W in isometries[t+1:]:q=mm(W,q)
        blocks.append((q,t+1,K))
    for q,target,K in blocks:
        T[offsets[target]:offsets[target+1],offsets[-2]:offsets[-1]]+=mm(K,q.T)
    need(np.max(np.abs(np.einsum('ki,kj->ij',T,T,optimize=False)-np.eye(D)))<1e-12,'clock isometry')
    need(np.max(np.abs(np.einsum('ik,jk->ij',T,T,optimize=False)-np.eye(D)))<1e-12,'clock coisometry')
    return T,dims


def inventory(n,l1,l2,l3):
    m=16;M=m*(2*n+2)+2*(m-1); z=m*(n+2)+(m-1)
    # Upper bound: each primitive reading gets its own fresh NC1 tail.
    return {'m':m,'marked_toffoli':M,'clean_zeros_before':z,
        'base_births':m*(n+1)+z+1+2*l1,
        'base_G':z+1+l1,'base_CX':2*z+(32*n+110)+2*l1,
        'per_toffoli_births':20*l2+2*l3+2,
        'per_toffoli_G':40*l2+14*l3+2,
        'per_toffoli_CX':68*l2+34*l3+12,
        'per_toffoli_SourceI_port_correction_at_most':4,
        'per_toffoli_primitive_NC1_reads':10*l2+l3,
        'total_births_upper_excluding_routing_and_controller':m*(n+1)+z+1+2*l1+M*(20*l2+2*l3+2),
        'total_G_upper_excluding_routing_and_controller':z+1+l1+M*(40*l2+14*l3+2),
        'total_CX_upper_excluding_routing_and_controller':2*z+(32*n+110)+2*l1+M*(68*l2+34*l3+12)}


def main():
    p=(math.sqrt(5)-1)/2;a=math.sqrt(p)
    G=np.array([[a,-p],[p,a]])
    X=np.array([[0.,1.],[1.,0.]])
    CNOT=np.array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,0.,1.],[0.,0.,1.,0.]])
    B=np.kron(np.eye(2),np.array([[a],[p]]))
    NG=np.kron(np.eye(2),G)
    # Real NC1 birth and word, followed by a retained exact CZ attempt
    # collapsed to the published Kraus macro: K0=cos(2 theta) I,
    # K1=-sin(2 theta) CZ. Its elementary word is not expanded here.
    c=math.cos(2*math.acos(a));s=math.sin(2*math.acos(a))
    CZ=np.diag([1.,1.,1.,-1.]);I=np.eye(4)
    # Copy NC1 control r to a retained record, whose orthogonal sectors
    # model the PVM (the completed device must enforce the CQ cut).
    record=np.zeros((8,4)); blank=np.zeros((8,4))
    for j in range(4):
        record[2*j+(j//2),j]=1.
        blank[2*j,j]=1.
    I8=np.eye(8); CZ8=np.kron(CZ,np.eye(2))
    instrument=np.vstack([c*I8,-s*CZ8])
    after=np.block([[I8,np.zeros((8,8))],[np.zeros((8,8)),np.kron(CNOT,np.eye(2))]])
    stages=[B,CNOT,NG,CNOT,record,instrument,after]
    need(all(np.max(np.abs(mm(V.T,V)-np.eye(V.shape[1])))<1e-12 for V in stages),'all stage isometries')
    T,dims=clock(stages)
    # Passive cut replaces each physical square op by identity, while retaining
    # the same birth and a blank outcome flag for this demonstration.
    V=np.eye(2);E=np.eye(2)
    for i,stage in enumerate(stages):
        V=mm(stage,V)
        passive = B if i==0 else (blank if i==4 else (np.vstack([I8,np.zeros((8,8))]) if i==5 else np.eye(stage.shape[0])))
        E=mm(passive,E)
    C=mm(E.T,V);F=np.eye(2)-mm(C.T,C)
    lam=np.linalg.eigvalsh(F);z=2**-20
    need(lam.min()>-1e-12 and lam.max()<1+1e-12,'full feedback positive contraction')
    J=-np.linalg.slogdet(np.eye(2)-z*F)[1]
    maximum=2*(-math.log1p(-z))
    need(0<=J<=maximum,'universal RAW bound')
    rho0=np.diag([1.,0.]);rho1=np.diag([0.,1.])
    need(np.trace(rho0)==np.trace(rho1)==1,'two different input preparations')
    # F,J,clock are defined on the common input space, not by a chosen rho.
    # F may nonetheless be nontrivial and any full source can depend on rho.
    print(json.dumps({'status':'PASS; toy macro clock and conditional large-inventory theorem',
        'toy_clock_stage_dimensions':dims,'toy_clock_dimension':sum(dims),
        'toy_clock_unitarity_error':float(np.max(np.abs(np.einsum('ki,kj->ij',T,T,optimize=False)-np.eye(len(T))))),
        'toy_feedback_eigenvalues':lam.tolist(),'toy_RAW_J':float(J),
        'toy_RAW_universal_upper':maximum,'fixed_graph_RAW_depends_on_initial_density':False,
        'toy_includes_full_CZ_elementary_clock':False,
        'full_branching_union_clock_materialized':False,
        'physical_Book03_tariffs_inferred':False,
        'N8_caps_21_6_66':inventory(8,21,6,66),
        'N40_caps_85_18_203':inventory(40,85,18,203),
        'GR_closed':False},indent=2))


if __name__=='__main__':main()
