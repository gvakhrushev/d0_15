#!/usr/bin/env python3
"""Coherent scalar-unit records and the same complete retained source.

Exact finite graph identities, a periodic 16-site 42-field algebraic test,
and high-precision differentiation of the parent's complete matrix price.
No native circuit, physical selection theorem, PDE solution, or finite GR
stationary root is claimed. The geometric stencil below checks the stated
change-of-variables identity; it is not a replacement of an owned lattice.
"""
from __future__ import annotations
from fractions import Fraction as F
from collections import deque
from pathlib import Path
import hashlib, json, platform
import numpy as np
import sympy as sp
import mpmath as mp
import torch

CHECKS=0

def require(ok:bool,name:str)->None:
    global CHECKS
    CHECKS+=1
    if not bool(ok):raise ArithmeticError(name)

def near(a,b,name:str,tol=2e-10)->float:
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    require(err<tol,name+': '+str(err))
    return err

def potentials(nodes,edges):
    """Recover positive vertex units iff all supplied edge ratios agree."""
    adj={x:[] for x in nodes}
    for x,y,c in edges:
        if c<=0:raise ValueError('positive unit ratios required')
        adj[x].append((y,c));adj[y].append((x,1/c))
    r={}
    for root in nodes:
        if root in r:continue
        r[root]=F(1);todo=deque([root])
        while todo:
            x=todo.popleft()
            for y,c in adj[x]:
                if y not in r:r[y]=r[x]*c;todo.append(y)
                elif r[y]!=r[x]*c:return None
    return r

def exact_graph():
    units=[F(2,3),F(7,5),F(9,8),F(11,7)]
    edge_pairs=[(0,1),(1,2),(2,3),(3,0),(0,2)]
    edges=[(x,y,units[y]/units[x]) for x,y in edge_pairs]
    recovered=potentials(range(4),edges)
    require(recovered is not None,'consistent full finite record graph')
    for x in range(4):require(recovered[x]==units[x]/units[0],'spanning-tree reconstruction')
    k0=F(23,7)
    psi=[[F(2,9),F(-3,11)],[F(1,5),F(4,13)],[-F(2,7),F(7,19)],[F(3,17),-F(2,9)]]
    phi=[[units[x]*v for v in psi[x]] for x in range(4)]
    for x,y,c in edges:
        for a in range(2):
            cov=c*psi[y][a]-psi[x][a]
            require(units[x]*cov==phi[y][a]-phi[x][a],'all finite transported differences')
            require(k0*units[x]**2*cov**2==k0*(phi[y][a]-phi[x][a])**2,'finite kinetic density identity')
    for cyc in ([0,1,2,3,0],[0,2,3,0],[0,1,2,0]):
        h=F(1)
        for a,b in zip(cyc,cyc[1:]):h*=units[b]/units[a]
        require(h==1,'all tested cycle products are exact one')
    bad=edges.copy();x,y,c=bad[-1];bad[-1]=(x,y,F(6,5)*c)
    require(potentials(range(4),bad) is None,'nonintegrable independent edge calibration rejected')
    ring=[(0,1,F(2)),(1,2,F(2)),(2,3,F(2)),(3,0,F(2))]
    require(potentials(range(4),ring) is None,'nontrivial periodic holonomy is not a unit convention')
    try:potentials([0,1],[(0,1,F(0))])
    except ValueError:require(True,'zero unit margin rejected')
    else:require(False,'zero unit margin accepted')
    # Constant physical scalar, varying representation: ordinary difference is wrong.
    raw=[1/x for x in units]
    require(all(c*raw[y]-raw[x]==0 for x,y,c in edges),'constant decoded scalar has zero covariant differences')
    naive=sum((raw[y]-raw[x])**2 for x,y in edge_pairs)
    require(naive>0,'omitting unit transport creates a spurious matter source')
    return {'vertices':4,'directed_report_edges':5,'exact_arithmetic':True,
            'naive_nonzero_energy_for_constant_physical_field':str(naive),
            'full_cycle_condition_required':True,'graph_coupling_used_only_for_test':'23/7'}

def continuum_controls():
    x=sp.symbols('x',real=True)
    r=2+sp.sin(x);psi=1/r
    cov=sp.simplify(sp.diff(psi,x)+sp.diff(sp.log(r),x)*psi)
    require(cov==0,'continuum pure calibration connection')
    require(sp.simplify(sp.diff(psi,x))!=0,'ordinary derivative negative control')
    k,p,g=sp.symbols('k p g',positive=True)
    S=-k*p*p
    require(sp.diff(S,k)==-p*p,'a genuinely bare variable coupling retains its own equation')
    a,rr,ad,rd=sp.symbols('psi r psi_dot r_dot')
    actual=sp.diff((rr+rd*x)*(a+ad*x),x).subs(x,0)
    require(sp.expand(actual-(rr*ad+rd*a))==0,'initial scalar normal derivative must also transform')
    require(sp.simplify(actual-rr*ad)==rd*a,'holding the old momentum fixed is not equivalent Cauchy data')
    return {'connection':'A=d log r, not an independent field',
            'initial_momentum':'Pi_Phi=r Pi_psi+n(r) psi',
            'bare_coupling_not_declared_redundant':True}

def field_lattice():
    torch.set_default_dtype(torch.float64);torch.set_num_threads(1)
    n=16;spacing=.4;eta=torch.diag(torch.tensor([1.,-1.,-1.,-1.]))
    pairs=[(a,b) for a in range(4) for b in range(a+1,4)]
    idx=torch.tensor([[x^(1<<mu) for x in range(n)] for mu in range(4)])
    k0=23.4164067518840749729
    arr=torch.linspace(-.03,.04,n*44).reshape(n,44)
    for x in range(n):
        arr[x,:16]=(torch.eye(4)+.01*torch.sin(torch.arange(16).reshape(4,4)+x)).reshape(-1)
        arr[x,16:40]=.02*torch.sin(torch.arange(24)+x*.3)
        arr[x,40]=.05*torch.sin(torch.tensor(.6*x));arr[x,41]=.04*torch.cos(torch.tensor(.7*x))
        arr[x,42]=.17*torch.sin(torch.tensor(.4*x));arr[x,43]=.13*torch.cos(torch.tensor(.5*x))
    y=arr.clone().requires_grad_(True)
    def pieces(fields):
        e=fields[:,:16].reshape(n,4,4);ei=torch.linalg.inv(e)
        gm=e.transpose(1,2)@eta@e;gi=torch.linalg.inv(gm)
        ws=[]
        for mu in range(4):
            row=[]
            for a in range(4):
                cells=[]
                for b in range(4):
                    if a==b:cells.append(fields[:,0]*0)
                    else:
                        j=pairs.index((min(a,b),max(a,b)))
                        cells.append((1 if a<b else -1)*fields[:,16+6*mu+j]*eta[b,b])
                row.append(torch.stack(cells,1))
            ws.append(torch.stack(row,1))
        ff=fields[:,0]*0
        for mu in range(4):
            for nu in range(4):
                curvature=((ws[nu][idx[mu]]-ws[nu])-(ws[mu][idx[nu]]-ws[mu]))/spacing
                curvature=curvature+ws[mu]@ws[nu]-ws[nu]@ws[mu]
                ff=ff+torch.einsum('xa,xb,xab->x',ei[:,mu,:],ei[:,nu,:],curvature@eta)/2
        return ff,gi
    def action(fields,linked=True):
        ff,gi=pieces(fields)
        psi=fields[:,40:42];sig=torch.exp(fields[:,42]);r=torch.exp(fields[:,43])
        if linked:
            ph=r[:,None]*psi
            dp=torch.stack([(ph[idx[mu]]-ph)/spacing/r[:,None] for mu in range(4)],1)
        else:dp=torch.stack([(psi[idx[mu]]-psi)/spacing for mu in range(4)],1)
        qq=torch.einsum('xmn,xma,xna->x',gi,dp,dp)
        return torch.sum(sig*(ff-k0*r*r*qq))*spacing**4
    def target(fields):
        sig=torch.exp(fields[:,42]);r=torch.exp(fields[:,43])
        ef=fields[:,:16]/torch.sqrt(sig[:,None]);ph=r[:,None]*fields[:,40:42]
        vals=torch.cat((ef,fields[:,16:40],ph,fields[:,42:]),1)
        ff,gi=pieces(vals)
        dp=torch.stack([(ph[idx[mu]]-ph)/spacing for mu in range(4)],1)
        qq=torch.einsum('xmn,xma,xna->x',gi,dp,dp)
        return torch.sum(ff-k0*qq)*spacing**4
    value=action(y);other=target(y)
    ev=near(value.detach(),other.detach(),'entire finite action identity')
    grad=torch.autograd.grad(value,y,retain_graph=True)[0]
    alt=torch.autograd.grad(other,y,retain_graph=True)[0]
    eg=near(grad.detach(),alt.detach(),'all704 finite coordinate source components')
    ward_s=grad[:,42]+.5*torch.sum(y[:,:16]*grad[:,:16],1)
    ward_r=grad[:,43]-torch.sum(y[:,40:42]*grad[:,40:42],1)
    es=near(ward_s.detach(),0.,'all local common-gain Ward rows')
    er=near(ward_r.detach(),0.,'all local scalar-unit Ward rows with neighbor contributions')
    # Large but exact finite linked change; not only first-order invariance.
    us=.14*torch.sin(torch.arange(n)*.2);ur=.11*torch.cos(torch.arange(n)*.3)
    y2=y.detach().clone();y2[:,:16]*=torch.exp(us[:,None]/2)
    y2[:,42]+=us;y2[:,40:42]*=torch.exp(-ur[:,None]);y2[:,43]+=ur
    efinite=near(action(y2).detach(),value.detach(),'finite local unit-orbit invariance')
    # Remove the necessary linked transport and the unit row no longer vanishes.
    naive=action(y,False);gn=torch.autograd.grad(naive,y)[0]
    bad=gn[:,43]-torch.sum(y[:,40:42]*gn[:,40:42],1)
    require(float(torch.max(torch.abs(bad)).detach())>1e-5,'bare local coupling has a nonzero omitted source')
    require(float(torch.linalg.norm(grad).detach())>.1,'off-shell test, no Einstein zero assigned')
    return {'sites':16,'physical_field_coordinates_per_site':42,'calibration_coordinates_per_site':2,
            'total_compared_coordinate_derivatives':704,'action_identity_error':ev,'source_identity_error':eg,
            'common_gain_Ward_error':es,'scalar_unit_Ward_error':er,'finite_orbit_error':efinite,
            'naive_untransported_Ward_residual':float(torch.max(torch.abs(bad)).detach()),
            'off_shell_source_norm':float(torch.linalg.norm(grad).detach()),
            'scope':'finite algebraic Palatini-jet stencil control; not owned holonomy mesh or stationary GR solution'}

def original_report(x,y):
    p=(mp.sqrt(5)-1)/2;zz=mp.mpf(2)**-20
    e=p*p*(1+x);ll=4*e*(1-e);u=p+p*p*y;bb=4*u*u*(1-u*u);aa=ll+(1-ll)*bb
    return zz*(aa+bb)-zz*zz*aa*bb

def retained_source():
    mp.mp.dps=95;p=(mp.sqrt(5)-1)/2;chi=p**7;z=mp.mpf(2)**-20;ready=mp.mpf(17)/50
    rf=mp.diff(lambda x:original_report(x,0),0);rq=mp.diff(lambda y:original_report(0,y),0)
    ast=ready*rf;bst=ready*rq;k0=bst/ast
    K=mp.matrix([[mp.mpf('.53'),mp.mpf('.13')],[mp.mpf('.03'),mp.mpf('.27')]]);A=K.T*K
    eta=p**80
    # 2 current copies. Per copy: 2 coframe scales, 4 scalars, 2 log-unit records,
    # two independent reporter slopes and one common baseline control.
    centres=[list(map(mp.mpf,['1.1','.9','.12','-.09','.07','.11','.12','-.17','.3','-.2','.4'])),
             list(map(mp.mpf,['1.03','.96','.10','-.07','.08','.13','-.11','.21','-.2','.4','-.3']))]
    base=[x for block in centres for x in block]
    def data(v):
        scale=v[:2];psi=[[v[2],v[4]],[v[3],v[5]]];r=[mp.exp(v[6]),mp.exp(v[7])]
        phi=[[r[x]*q for q in psi[x]] for x in range(2)]
        qphi=sum((phi[1][a]-phi[0][a])**2 for a in range(2))
        sa=[1+v[8]/10,1+v[8]/8];sb=[1+v[9]/9,1+v[9]/7]
        sigma=[sa[x]*sb[x] for x in range(2)]
        f=[mp.mpf('.2')/scale[0]**2,mp.mpf('.15')/scale[1]**2]
        qr=[qphi/(r[x]**2*scale[x]**2) for x in range(2)]
        aspect=[k0*r[x]**2 for x in range(2)]
        I=sum(sigma[x]*(f[x]-k0*qphi/scale[x]**2)/2 for x in range(2))
        return f,qr,aspect,sa,sb,I
    def current(v,eps,delta):
        f,qr,ks,sa,sb,_=data(v);total=mp.mpf(0)
        for x in range(2):
            def P(xx,yy):return ready*original_report(sa[x]*xx,sb[x]*yy)+v[10]*mp.mpf('1e-8')
            p0=P(0,0)
            Xi=(P(0,delta)-P(0,-delta))*(P(eps*f[x],0)-p0)
            Xi+=(P(ks[x]*delta,0)-P(-ks[x]*delta,0))*(P(0,-eps*qr[x])-p0)
            total+=chi*(4+Xi)/2
        return total
    result=[]
    for powe in (5,7,9,11):
        eps=mp.mpf(2)**-powe;delta=eps/1024
        def details(allv):
            Q=[current(allv[11*j:11*(j+1)],eps,delta) for j in range(2)]
            cs=[1-2*q for q in Q];s=mp.fprod(c*c for c in cs)
            D=(1-z)*mp.eye(2)+z*eta*s*A;Di=D**-1
            w=z*eta*s*sum((Di*A)[i,i] for i in range(2));L=sum(1/c for c in cs)
            G=8*chi*delta*eps*ast*bst*w*L
            return -mp.log(mp.det(D)),G,[(1/c)/L for c in cs]
        J,G,weights=details(base)
        require(G>0,'actual nonzero retained source gain')
        source=[];expected=[]
        for k in range(22):
            def changed(t):
                v=base.copy();v[k]=t;return details(v)[0]
            derivative=mp.diff(changed,base[k])/G
            block=k//11;coord=k%11
            def target(t):
                v=centres[block].copy();v[coord]=t;return data(v)[5]
            target_source=weights[block]*mp.diff(target,base[k])
            source.append(derivative);expected.append(target_source)
        error=sum(abs(a-b) for a,b in zip(source,expected))
        gauge=[]
        for block in range(2):
            off=11*block
            for site in range(2):
                ix=[off+2+site,off+4+site]
                gv=source[off+6+site]-sum(base[k]*source[k] for k in ix)
                tv=expected[off+6+site]-sum(base[k]*expected[k] for k in ix)
                require(abs(tv)<mp.mpf('1e-80'),'exact target local-unit Ward identity')
                gauge.append(abs(gv))
        baseline=max(abs(source[10]),abs(source[21]))
        require(baseline<mp.mpf('1e-70'),'linked current/reference baseline cancels in full determinant')
        result.append({'epsilon':mp.nstr(eps,12),'delta':mp.nstr(delta,12),
                       'actual_Gamma':mp.nstr(G,28),'all22_source_error_l1':mp.nstr(error,28),
                       'calibration_source_norm':mp.nstr(sum(gauge),28),
                       'baseline_source_max':mp.nstr(baseline,8),
                       'current_weights_sum':mp.nstr(sum(weights),8)})
    require(mp.mpf(result[-1]['all22_source_error_l1'])<mp.mpf(result[0]['all22_source_error_l1'])/30,
            'complete source error converges with epsilon')
    require(mp.mpf(result[-1]['calibration_source_norm'])<mp.mpf(result[0]['calibration_source_norm'])/30,
            'finite independent local-unit sources converge, not declared exactly zero')
    return {'original_kappa':mp.nstr(k0,30),'independent_current_copies':2,
            'tested_independent_variables_per_copy':11,'past_matrix_retained':True,'retention_blocks':80,
            'tests':result,'new_native_word_emitted':False,'new_calibration_scheme_physically_selected':False}

def main():
    out={'input_commit':'689a98adc750f6ad1b36f339696768a039b41022',
         'exact_graph':exact_graph(),'continuum':continuum_controls(),
         'finite_covector':field_lattice(),'complete_price':retained_source()}
    out.update({'checks':CHECKS,'status':'PASS_COHERENT_CALIBRATION_SOURCE_COMPOSITION',
                'unrestricted_D0_GR_closed':False,'native_gate_word_emitted':False,
                'Einstein_PDE_solved':False,'Lean_or_CI_run':False,
                'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'environment':{'python':platform.python_version(),'numpy':np.__version__,
                               'sympy':sp.__version__,'mpmath':mp.__version__,'torch':torch.__version__}})
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':main()
