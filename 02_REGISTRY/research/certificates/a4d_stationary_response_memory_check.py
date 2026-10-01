#!/usr/bin/env python3
"""Literal curvature-memory quotient and its exact hostile controls.

All linear coefficients are derived from the action's 4x4 face matrices.
The all-coframe rank and arbitrary-quotient universal properties are proved
in A4D_STATIONARY_RESPONSE_MEMORY.md, separately from these finite inputs.
No new action, source, or stationary-connection selector is introduced.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import numpy as np
import a4d_identity_quarter_nonlinear_response_check as N
from a4d_warped_quarter_regular_response_check import independent_rows

ETA=np.diag(N.SIG).astype(object)
I=N.I


def face_data(solder):
    q=solder.T@ETA@solder
    qi=N.inverse(q)
    lift=[]
    vertical=[]
    for r,s in N.SYM:
        dq=np.zeros((4,4),dtype=object);dq[r,s]=dq[s,r]=1
        ds=solder@qi@dq*F(1,2)
        assert np.array_equal(ds.T@ETA@solder+solder.T@ETA@ds,dq)
        lift.append(ds.reshape(16))
    for g in N.G:
        ds=g@solder
        assert not np.any(ds.T@ETA@solder+solder.T@ETA@ds)
        vertical.append(ds.reshape(16))
    lift=np.array(lift,dtype=object)
    vertical=np.array(vertical,dtype=object)
    m=np.zeros((16,36),dtype=object)
    w=[];dw=[]
    for face,(r,s) in enumerate(N.PAIRS):
        u,v=[j for j in range(4) if j not in (r,s)]
        sign=N.orient(r,s)
        w.append(sign*N.weight(N.wedge(solder[:,u],solder[:,v])))
        for a in range(4):
            da=I[:,a]
            for leg,area in ((u,N.wedge(da,solder[:,v])),(v,N.wedge(solder[:,u],da))):
                weight=sign*N.weight(area)
                for g in range(6):m[4*a+leg,6*face+g]+=np.sum(weight*N.G[g])
        row=[]
        for ds in lift.reshape(10,4,4):
            row.append(sign*N.weight(N.wedge(ds[:,u],solder[:,v])+N.wedge(solder[:,u],ds[:,v])))
        dw.append(row)
    d=lift@m
    actual=np.array([[np.sum(dw[f][j]*N.G[g]) for f in range(6) for g in range(6)]
                     for j in range(10)],dtype=object)
    assert np.array_equal(d,actual)
    return q,lift,vertical,m,d,np.array(w),np.array(dw)


def tensor_memory(solder,curvatures):
    q,lift,vertical,m,d,w,dw=face_data(solder)
    coords=np.array([matrix[a,b] for matrix in curvatures
                     for a,b in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))],dtype=object)
    # GEN upper entries are exactly the coordinates used above.
    for matrix,part in zip(curvatures,coords.reshape(6,6)):
        assert np.array_equal(matrix,sum((N.G[g]*part[g] for g in range(6)),np.zeros((4,4),dtype=object)))
    solder_current=(m@coords).reshape(4,4)
    x=N.inverse(q)@solder.T@solder_current*F(1,2)
    x=(x+x.T)*F(1,2)
    slots=np.array([(1 if a==b else 2)*x[a,b] for a,b in N.SYM],dtype=object)
    assert np.array_equal(slots,d@coords)
    return slots,coords,solder_current


def plaquettes(links,p):
    return [links[p,r]@links[(p+1)%4,s]@N.jinv(links[(p+1)%4,r][None])[0]
            @N.jinv(links[p,s][None])[0] for r,s in N.PAIRS]


def rational_family(generator,t):
    u=N.inverse(I-t*generator*F(1,2))@(I+t*generator*F(1,2))
    ui=N.jinv(u[None])[0]
    assert np.array_equal(u.T@ETA@u,ETA)
    links=np.array([[I.copy() for r in range(4)] for p in range(4)],dtype=object)
    links[0,0]=u;links[2,0]=ui
    return links


def rows(values):
    assert all(isinstance(x,(int,F,np.integer)) for row in values for x in row)
    return [[str(F(x)) for x in row] for row in values]


def full_boost_polynomial():
    # Clear the SAME D=4-3*t^2 on every link, including identities.
    # Each literal Euler term has four link factors. Degree eight is
    # therefore the complete D^4 numerator, not a truncated Taylor test.
    b=N.G[0]+N.G[1]+N.G[2]
    assert np.array_equal(b@b@b,3*b)
    links=np.array([[N.jconst(4*I,8) for _ in range(4)] for _ in range(4)])
    links[:,:,2]=-3*I
    links[0,0,1]=4*b;links[2,0,1]=-4*b
    links[0,0,2]=links[2,0,2]=2*b@b-3*I
    ek,eq=N.euler_links(links)
    assert not np.any(ek)
    visible=np.array([0,0,0,0,-1,1,1,-1,1,-1],dtype=object)
    expected=np.zeros_like(eq)
    for power,c in ((1,256),(3,-576),(5,432),(7,-108)):
        for p,sign in enumerate((1,1,-1,-1)):expected[power,p]=sign*c*visible
    assert np.array_equal(eq,expected)
    print('PASS_FULL_CAYLEY_BOOST_EULER_NUMERATOR_ALL_DEGREE8_COEFFICIENTS',flush=True)
    return {'denominator':'D=4-3*t^2','link_numerator_degree':2,'full_Euler_numerator_degree_bound':8,
            'all_connection_numerator_coefficients':'zero',
            'metric_numerator':'4*t*D^3*sigma_p*(0,0,0,0,-1,1,1,-1,1,-1)',
            'scalar_nonzero_coefficients':[[1,256],[3,-576],[5,432],[7,-108]],
            'method':'exact literal degree-eight denominator-cleared polynomial, not a Taylor extrapolation'}


def run_checks():
    coframes=[I,np.diag(list(map(F,(2,3,5,7)))),
              np.array([[F(1),F(1,7),0,0],[0,1,F(1,5),0],
                        [F(1,11),0,1,F(1,3)],[0,0,0,1]],dtype=object)]
    boost=I.copy();boost[0,0]=boost[1,1]=F(5,3);boost[0,1]=boost[1,0]=F(4,3)
    assert np.array_equal(boost.T@ETA@boost,ETA)
    coframes.append(boost@coframes[-1])
    ledgers=[]
    for solder in coframes:
        q,lift,vertical,m,d,w,dw=face_data(solder)
        assert len(independent_rows(m.T))==16
        assert len(independent_rows(d.T))==10
        frame=np.concatenate([lift.T,vertical.T],axis=1)
        fi=N.inverse(frame)
        assert np.array_equal(fi@frame,np.eye(16,dtype=object))
        columns=independent_rows(d.T)
        assert len(columns)==10
        right=np.zeros((36,10),dtype=object);right[columns]=N.inverse(d[:,columns])
        assert np.array_equal(d@right,np.eye(10,dtype=object))
        projection=right@d
        assert np.array_equal(projection@projection,projection)
        assert not np.any(d@(np.eye(36,dtype=object)-projection))
        # Reconstruct the full solder current on the stationary Ward
        # annihilator: [metric lifts, verticals]^T H = (Xi,0).
        horizontal=fi.T[:,:10]
        assert np.array_equal(lift@horizontal,np.eye(10,dtype=object))
        assert not np.any(vertical@horizontal)
        action=np.array([np.sum(w[f]*N.G[g]) for f in range(6) for g in range(6)],dtype=object)
        qslots=np.array([q[a,b] for a,b in N.SYM],dtype=object)
        assert np.array_equal(qslots@d,action)
        ledgers.append({'S':rows(solder),'Q':rows(q),'solder_current_rank':16,
                        'metric_memory_rank':10,'curvature_kernel_dimension':26,
                        'right_inverse_columns':columns,'D':rows(d)})
    print('PASS_LITERAL_CURRENT_GRAM_MEMORY_RANK10_AND_WARD_DECOMPOSITION',flush=True)
    # The formula is equivariant under proper Lorentz frames and derived
    # independently as a symmetric tensor, rather than only a matrix row.
    curv=np.array([sum((N.G[g]*F((f+1)*(g-2),13) for g in range(6)),np.zeros((4,4),dtype=object))
                   for f in range(6)])
    first,_,_=tensor_memory(coframes[2],curv)
    transformed=np.array([boost@x@N.jinv(boost[None])[0] for x in curv])
    second,_,_=tensor_memory(coframes[3],transformed)
    assert np.array_equal(first,second)
    print('PASS_INDEPENDENT_SYMMETRIC_TENSOR_AND_LORENTZ_COVARIANCE',flush=True)
    # A scalar density is too small; a literal zero-density direction is
    # distinguished by an already owned metric component.
    _,_,_,_,d,w,_=face_data(I)
    action=np.array([np.sum(w[f]*N.G[g]) for f in range(6) for g in range(6)],dtype=object)
    scalar_bad=next(j for j in range(36) if not action[j] and np.any(d[:,j]))
    assert not action[scalar_bad] and np.any(d[:,scalar_bad])
    print('PASS_SCALAR_ONLY_FORGETTING_RESPONSE_FAILURE',flush=True)
    family_results=[]
    for label,generator in (('response_null_Y',N.G[3]-N.G[4]+N.G[5]),
                            ('response_visible_B',N.G[0]+N.G[1]+N.G[2])):
        for t in (F(-1,7),F(1,5),F(1,4)):
            links=rational_family(generator,t)
            ek,eq=N.euler_links(links[:,:,None])
            assert not np.any(ek)
            memories=[]
            for p in range(4):
                pqs=plaquettes(links,p)
                curvature=np.array([(p-N.jinv(p[None])[0])*F(1,2) for p in pqs])
                memory,coords,current=tensor_memory(I,curvature)
                assert np.array_equal(memory,eq[0,p])
                assert np.any(curvature)
                _,_,vertical,_,_,_,_=face_data(I)
                assert not np.any(vertical@current.reshape(16))
                memories.append(memory)
            assert not np.any(sum(memories))
            if label=='response_null_Y':assert not np.any(memories)
            else:
                factor=4*t/(4-3*t*t)
                visible=np.array([0,0,0,0,-1,1,1,-1,1,-1],dtype=object)
                assert np.array_equal(memories,np.array([sign*factor*visible for sign in (1,1,-1,-1)]))
            family_results.append({'family':label,'t':str(t),'full_connection_Euler':'zero',
                                   'memory':rows(memories),'phase_mean':'zero','curvature':'nonzero'})
    print('PASS_EXISTING_STATIONARY_Y_NULL_AND_B_VISIBLE_FAMILY_CONTROLS',flush=True)
    # Phase forgetting identifies B with I although the full metric
    # memory differs. This is the fiber-criterion failure, not gauge.
    assert not np.any(sum(memories)) and np.any(memories)
    # The minimal readout quotient is not a faithful encoding of the
    # entire Euler theory: it can also identify a nonstationary field
    # with I. Thus no full M1 grammar transfer is silently asserted.
    y=N.G[3]-N.G[4]+N.G[5]
    nonsolution=np.array([[I.copy() for _ in range(4)] for _ in range(4)],dtype=object)
    slow_parameters=(F(1,5),F(1,7),F(1,11),F(1,13))
    for p,t in enumerate(slow_parameters):
        nonsolution[p,0]=N.inverse(I-t*y*F(1,2))@(I+t*y*F(1,2))
    bad_ek,bad_eq=N.euler_links(nonsolution[:,:,None])
    assert not np.any(bad_eq) and np.any(bad_ek)
    print('PASS_SAME_RESPONSE_MEMORY_DIFFERENT_STATIONARITY_CONTROL',flush=True)
    full_family=full_boost_polynomial()
    for L in (8,12,16):
        h=F(1,L);t=h*h;factor=4*t/(4-3*t*t)
        raw_owner=6*L**4*abs(factor)
        assert raw_owner/h**2==24*L**4/(4-3*h**4)
    return {'schema':'a4d-stationary-response-memory-v1',
            'input_head':'909ad048d25de2def8875290c41bf9475e9180e6',
            'arithmetic':'exact Q, literal face products and true Gram lift, no spectral census',
            'curvature':'C_rs=(P_rs-P_rs^(-1))/2 in so(1,3)',
            'minimal_memory':'Xi=pack( sym(Q^(-1)*S^T*H)/2 ), H=literal solder Euler current',
            'coframe_ledgers':ledgers,
            'ambient_dimensions':{'face_curvature':36,'solder_current':16,'Gram_memory':10,
                                  'solder_current_invisible':20,'Gram_invisible':26},
            'stationary_Ward':'six Lorentz vertical current components vanish on EK=0; Xi reconstructs H on that annihilator',
            'scalar_forgetting_witness':{'curvature_column':scalar_bad,'density':'zero','metric_memory':list(map(str,d[:,scalar_bad]))},
            'stationary_controls':family_results,
            'full_boost_family_polynomial':full_family,
            'phase_average_forgetting':'not sufficient for full sitewise metric readout, even on EK=0',
            'stationarity_forgetting_control':{'Role0_Cayley_Y_parameters':list(map(str,slow_parameters)),
                                               'metric_memory':'zero, equal to I',
                                               'connection_Euler_nonzero_components':int(np.count_nonzero(bad_ek)),
                                               'consequence':'response quotient does not by itself preserve and reflect full Euler derivability'},
            'existing_B_refinement_obstruction':{'source':'connection source zero; no smooth joint metric source claimed',
                'amplitude':'t=h^2','sitewise_normalized_q11':'-4/(4-3*h^4) -> -1 at the origin',
                'unweighted_normalized_owner1':'24*L^4/(4-3*h^4)',
                'arbitrary_real_scale':'t=a*h^2 gives normalized origin q11 -> -a for every real a',
                'universal_class_separation':'a!=b implies distinct asymptotic response classes; any sufficient continuum quotient has at least continuum many classes on the full EK=0 domain',
                'same_endpoint':'Q_h=eta and K_h(a)->I for every a; normalized current scale is irreducible approach memory for the full response protocol',
                'weak_phase_mean':'zero; not a counterexample to only weak smooth-test readout'},
            'analytic_consequence':'all-frequency exact response-memory factorization and coarsest sufficient quotient; universal singleton-continuum-quotient no-go on the full EK=0 domain, with a real family of separated normalized-current classes',
            'nonclaims':['no smooth-independent-source joint response no-go',
                         'no proof of one continuum memory class on the admissible joint fiber',
                         'not a minimal quotient for other mandatory holonomy or history observables',
                         'no new M1 formalization or automatic faithful refinement interpretation'],
            'verdict':'STATIONARY_RESPONSE_MEMORY_FACTORIZATION_CERTIFIED; JOINT_CONTINUUM_COLLAPSE_OPEN'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--expect',type=Path)
    args=parser.parse_args();report=run_checks()
    expected=args.expect or (Path(__file__).with_name('a4d_stationary_response_memory_results.json') if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text())==report
        print('PASS_PINNED_LEDGER',flush=True)
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('VERDICT',report['verdict'])
