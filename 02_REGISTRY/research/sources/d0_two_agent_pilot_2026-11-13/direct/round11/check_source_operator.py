#!/usr/bin/env python3
"""Independent direct CAR matrices and all-coordinate polynomial derivative check."""
from pathlib import Path
from itertools import permutations
import argparse
import hashlib
import json
import numpy as np
from source_operator_dag import evaluate

HERE = Path(__file__).resolve().parent
dag = json.loads((HERE/'SOURCE_TENSOR_DAG.json').read_text())
eta = np.array([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]], dtype=float)
order = (0,2,3,1)
mm = lambda a,b: np.einsum('ij,jk->ik',a,b,optimize=False)


def determinant(m):
    if len(m) == 0:
        return 1
    return sum((-1)**j*m[0,j]*determinant(np.delete(m[1:],j,axis=1)) for j in range(len(m)))


def exterior(m):
    out = np.zeros((16,16),dtype=np.result_type(m.dtype,float))
    indices = [[j for j in order if bits & (1<<j)] for bits in range(16)]
    for i,a in enumerate(indices):
        for j,b in enumerate(indices):
            if len(a)==len(b):
                out[i,j]=determinant(m[np.ix_(a,b)])
    return out


heta = exterior(eta)
creators = []
for i in range(4):
    c = np.zeros((16,16))
    for bits in range(16):
        if not bits & (1<<i):
            c[bits|(1<<i),bits] = (-1)**sum(bool(bits & (1<<j)) for j in order[:order.index(i)])
    creators.append(c)


def sharp(m):
    h = eta if m.shape==(4,4) else heta
    return mm(mm(h,m.T),h)


def projection(m):
    e = mm(sharp(m),m)-np.eye(4)
    return mm(m,np.eye(4)-e/2+3*mm(e,e)/8)


def direct(v, p, omit_last_face=False):
    u = np.array([[v[f'u/{r}/{i}'] for i in range(4)] for r in range(4)])
    cs = [sum(u[r,i]*creators[i] for i in range(4)) for r in range(4)]
    links = {}
    for key in dag['link_nodes']:
        loc,r=key.split('/');r=int(r)
        m=np.array([[v[f'M/{loc}/{r}/{i}/{j}'] for j in range(4)] for i in range(4)])
        links[loc,r]=exterior(projection(m))
    f=0
    for r in range(4):
        for s in range(r+1,4):
            if omit_last_face and (r,s)==(2,3):
                continue
            plaquette=mm(mm(mm(links['base',r],links[f'plus{r}',s]),
                            sharp(links[f'plus{s}',r])),sharp(links['base',s]))
            mixed=mm(cs[r],sharp(cs[s]))-mm(cs[s],sharp(cs[r]))
            f-=np.trace(mm(mixed,plaquette))/8
    metric=mm(mm(u,eta),u.T)/(3/5)**2
    q=0
    for a in (0,15):
        dp=np.array([v[f'X/plus{r}/{a}']-v[f'X/base/{a}'] for r in range(4)])
        q+=np.einsum('i,ij,j->',dp,metric,dp,optimize=False)*256**2/(4*p*(1/4)**2)
    return np.array([f/((3/5)**2*(1/4)**2),q])


def generic_inputs():
    v={}
    for n in dag['nodes']:
        if n['op']!='var':continue
        name=n['name'];parts=name.split('/')
        if parts[0]=='u':
            r,i=map(int,parts[1:]);v[name]=0.6*eta[i,r]+(3*r-i+1)/200
        elif parts[0]=='M':
            loc,r,i,j=parts[1:];r,i,j=map(int,(r,i,j))
            locn=0 if loc=='base' else int(loc[-1])+1
            v[name]=float(i==j)+(1+2*i-3*j+r+locn)/500
        else:
            loc,a=parts[1:];locn=0 if loc=='base' else int(loc[-1])+1
            v[name]=(3*locn+int(a)+1)/10000
    return v


p=(np.sqrt(5.)-1)/2
v=generic_inputs()
calc=evaluate(dag,v,p,gradient=True)
root_names=list(dag['roots'])
expected=direct(v,p)
got=np.array([calc[k]['value'] for k in root_names])
value_error=float(np.max(np.abs(got-expected)))
assert value_error<2e-11
# All 282 independent real moment coordinates, including every normal link entry.
max_derivative_error=0.
for name in v:
    w=dict(v);w[name]+=1e-24j
    derivative=direct(w,p).imag/1e-24
    predicted=np.array([calc[k]['gradient'][name] for k in root_names])
    err=float(np.max(np.abs(derivative-predicted)/(1+np.abs(derivative))))
    max_derivative_error=max(max_derivative_error,err)
assert max_derivative_error<3e-12
assert abs(direct(v,p,omit_last_face=True)[0]-expected[0])>1e-8

# At a genuine proper link the R2 normal differential vanishes. Other links may
# be arbitrary; the source remains insensitive to this link's ten normal rows.
e=np.zeros((4,4));e[1,2]=1;e[2,0]=1
U=np.eye(4)+e/5+mm(e,e)/50
assert np.max(np.abs(mm(mm(U.T,eta),U)-eta))<1e-15
normal_error=0.;normal_count=0
for key in dag['link_nodes']:
    loc,r=key.split('/');r=int(r)
    w=dict(v)
    for i in range(4):
        for j in range(4):w[f'M/{loc}/{r}/{i}/{j}']=U[i,j]
    grad=evaluate(dag,w,p,gradient=True)[root_names[0]]['gradient']
    g=np.array([[grad[f'M/{loc}/{r}/{i}/{j}'] for j in range(4)] for i in range(4)])
    for i in range(4):
        for j in range(i,4):
            sym=np.zeros((4,4));sym[i,j]=1;sym[j,i]=1
            tangent=mm(U,mm(eta,sym))
            normal_error=max(normal_error,abs(float(np.sum(g*tangent))))
            normal_count+=1
assert normal_count==160 and normal_error<1e-10

parser=argparse.ArgumentParser()
parser.add_argument('--b21',type=Path)
args=parser.parse_args()
center_result=None
if args.b21:
    geom=args.b21/'BRINKMANN_L4_CENTRE.jsonl'
    data={tuple(r['site']):r for r in map(json.loads,geom.read_text().splitlines())}
    base=(0,0,1,1)
    shift=lambda r:tuple((x+int(i==r))%4 if i<2 else x+int(i==r) for i,x in enumerate(base))
    cv={};Uco=np.array(data[base]['native_coframe_columns_approx'])
    for r in range(4):
        for i in range(4):cv[f'u/{r}/{i}']=Uco[i,r]
    for key in dag['link_nodes']:
        loc,r=key.split('/');r=int(r);site=base if loc=='base' else shift(int(loc[-1]))
        matrix=np.array(data[site]['U_u_approx']) if r==0 else np.eye(4)
        for i in range(4):
            for j in range(4):cv[f'M/{loc}/{r}/{i}/{j}']=matrix[i,j]
    for loc in ['base']+[f'plus{r}' for r in range(4)]:
        site=base if loc=='base' else shift(int(loc[-1]))
        for a in (0,15):cv[f'X/{loc}/{a}']=2*np.sqrt(p)*float(data[site][f'psi{a}'])/256
    cval=evaluate(dag,cv,p)
    center_result={'site':base,'values_before_inverse_PF':{k:float(x['value']) for k,x in cval.items()},
                   'geometry_sha256':hashlib.sha256(geom.read_bytes()).hexdigest(),
                   'scope':'one true interior stencil; no halo/global completion'}
    assert max(abs(x['value']) for x in cval.values())<1e-10
result={'status':'PASS_ORIGINAL_SOURCE_TENSOR_DAG_DIAGNOSTICS',
        'nodes':len(dag['nodes']),'all_independent_scalar_coordinates':len(v),
        'direct_CAR_matrix_value_error':value_error,
        'all_coordinate_complex_step_relative_error':max_derivative_error,
        'normal_link_directions':normal_count,'normal_source_error':normal_error,
        'hostile_omitted_face_detected':True,'B21_actual_interior':center_result,
        'scope':'numeric identity/derivative diagnostics; exact full-input bound in separate rational certificate',
        'full_H1_native_word_executed':False,'GR_closed':False}
(HERE/'SOURCE_OPERATOR_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
