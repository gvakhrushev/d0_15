"""Paired S+/S- clocks: native 16-column returns and full Hodge bounds.

Uses the published short-winding heat theorem for both genuine labelled clocks;
physical plus preparation, all external costs and full 42-source are not built.
"""
import json
import math
import numpy as np
from mpmath import iv
from check_local_gibbs_records import mm
from check_source_price import load_control, need

def main():
    ne,digest=load_control();p,a=float(ne.P),float(ne.A);gate=ne.Gate
    source=dict(profile=ne.G_CX_SOURCE_I,source_port=1,source_spin=(2,3))
    def matrix(n,g):
        spec=ne.Execution(n,(),(),(g,),**source)
        return np.array(ne.gate_matrix(spec,g,max_qubits=7,max_expanded_stages=100),dtype=float)
    def birth(V,n):return mm(np.kron(np.eye(1<<n),np.array([[a],[p]])),V)
    g=matrix(5,gate('G',(4,)))
    swap=(gate('CX',(4,1)),gate('CX',(1,4)),gate('CX',(4,1)))
    zword=swap+(gate('SourceI',(1,2,3)),gate('SourceI',(1,2,3)))+swap
    zmat=np.eye(32)
    for op in zword:zmat=mm(matrix(5,op),zmat)
    need(np.max(np.abs(zmat-np.kron(np.eye(16),np.diag([1.,-1.]))))<5e-14,
         'actual SourceI-routed Z on all old inputs')
    spec=ne.Execution(7,(),(),(gate('G',(6,)),),**source)
    inv=ne.inverse_word(spec,max_qubits=7,max_expanded_stages=100)
    old=mm(matrix(5,gate('CX',(0,4))),birth(np.eye(16),4))
    E=birth(birth(birth(np.eye(16),4),5),6)
    def complete(U):
        V=mm(U,old);V=birth(V,5)
        for op in (gate('CX',(4,5)),gate('G',(5,)),gate('CX',(4,5))):V=mm(matrix(6,op),V)
        V=birth(V,6)
        for op in inv:V=mm(matrix(7,op),V)
        V=mm(matrix(7,gate('CX',(4,6))),V)
        need(np.max(np.abs(mm(V.T,V)-np.eye(16)))<1e-11,'full terminal isometry')
        h=(np.arange(128)>>2)&1;env=np.arange(128)&1
        need(np.linalg.norm(V[h!=env])<1e-11,'actual copied NC1 environment')
        return mm(E.T,V),mm(V[h==1,:].T,V[h==1,:])
    iv.dps=90;one=iv.mpf(1);pp=(iv.sqrt(5)-one)/2;aa=iv.sqrt(pp);beta=2*pp**2
    theta=iv.atan2(pp,aa);z=one/(2**20)
    c0=pp**2+aa*pp**3;c1=aa*pp**2+pp**3
    d0=pp**3-aa*pp**2;d1=aa*pp**3-pp**2
    def J(t):return -8*sum(iv.log(one-z*(one-(c*iv.cos(t)+d*iv.sin(t))**2)) for c,d in ((c0,d0),(c1,d1)))
    x=beta/11;L=12;e=2*x**L/(math.factorial(L)*(one-x/(L+1)))
    heat=132*e/(359*beta)
    jprime=-16*z*(c0*d0/(one-z*(one-c0*c0))+c1*d1/(one-z*(one-c1*c1)))
    rows=[]
    for q,m in ((19,2),(66,7),(613,65)):
        gq=np.eye(32)
        for _ in range(q):gq=mm(g,gq)
        wp=mm(zmat,zmat,gq);wm=mm(zmat,gq,zmat)
        center=mm(wm,wp);up=mm(wp,wp);um=mm(wm,wm)
        need(np.max(np.abs(center-np.eye(32)))<1e-11,'matching actual identity word')
        cp,ep=complete(up);cm,em=complete(um)
        epsilon=q*theta-2*iv.pi*m;t=2*epsilon;dq=2*aa*pp*iv.sin(2*t)
        exact_j=(J(t)-J(-t))/dq;err=heat/abs(dq)
        need(exact_j-err>iv.mpf('0.00000222') and exact_j+err<iv.mpf('0.00000224'),'full H+J bounded')
        ef=float(dq.mid);tm=float(t.mid)
        need(np.max(np.abs(ep-em-ef*np.eye(16)))<2e-11,'all-column descriptor response')
        c0f=float(c0.mid);c1f=float(c1.mid);d0f=float(d0.mid);d1f=float(d1.mid)
        ecplus=np.diag([c0f*math.cos(tm)+d0f*math.sin(tm)]*8+[c1f*math.cos(tm)+d1f*math.sin(tm)]*8)
        ecminus=np.diag([c0f*math.cos(tm)-d0f*math.sin(tm)]*8+[c1f*math.cos(tm)-d1f*math.sin(tm)]*8)
        need(np.max(np.abs(cp-ecplus))<2e-11 and np.max(np.abs(cm-ecminus))<2e-11,'matched full return')
        rows.append({'q':q,'turns':m,'epsilon_interval':str(epsilon),'delta_q_interval':str(dq),
                     'bootstrap_secant_lower_interval':str(exact_j-err),'bootstrap_secant_upper_interval':str(exact_j+err),
                     'clock_dimension_no_padding':1872+32*(2*q+32)})
    print(json.dumps({'status':'PASS','cut':'original fixed rank-16 old-input cut',
      'scene':'K(9,11,13), both Hodge degrees','clock_dimension':'1872+32(2q+32)+256*m_pad',
      'full_heat_secant_error':'<=132 e_(12+2*m_pad)/(359 beta |delta_q|)',
      'exact_limit_Jprime_over_2ap_interval':str(jprime/(2*aa*pp)),
      'all16_literal_logical_columns_checked':True,'results':rows,
      'full_plus_preparation_clock_and_all32_matter_copies_built':False,
      'independent_full_covector_Book03_and_GR_closed':False,'native_control_digest':digest},indent=2))

if __name__=='__main__':main()
