#!/usr/bin/env python3
"""Exact shared-link first-slow/coframe and quadratic-cone compatibility.

The local finite certificate and analytic regular-branch theorem are scoped in
A4D_WARPED_QUARTER_REGULAR_RESPONSE.md. All arithmetic is Q or Q(i).
"""
from fractions import Fraction as F
from itertools import combinations
import json
import numpy as np
from a4d_designated_full_gap_check import GEN,PAIRS,SIG,SYM,STAR_MAP,orient
from a4d_warped_designated_normal_rescue_check import symbol,inverse

G=np.array(GEN,dtype=object);I=np.eye(4,dtype=object);ETA=np.diag(SIG)
STAR=np.zeros((6,6),dtype=object)
for col,(row,sign) in enumerate(STAR_MAP):STAR[row,col]=sign
G2=np.diag([SIG[a]*SIG[b] for a,b in PAIRS])

def wedge(a,b):return np.array([a[i]*b[j]-a[j]*b[i] for i,j in PAIRS],dtype=object)
def weight(a):
 out=np.zeros((4,4),dtype=object)
 for x,(i,j) in zip(a@G2@STAR,PAIRS):out[i,j]+=x*F(SIG[j],2);out[j,i]-=x*F(SIG[i],2)
 return out
def faceweights(S):
 out=[];dw=[];q=S.T@ETA@S
 qi=np.diag([F(1,x) for x in np.diag(q)])
 for a,b in PAIRS:
  u,v=[j for j in range(4) if j not in (a,b)]
  out.append(orient(a,b)*weight(wedge(S[:,u],S[:,v])))
  dd=[]
  for r,s in SYM:
   dq=np.zeros((4,4),dtype=object);dq[r,s]=dq[s,r]=F(1)
   ds=S@qi@dq*F(1,2)
   dd.append(orient(a,b)*weight(wedge(ds[:,u],S[:,v])+wedge(S[:,u],ds[:,v])))
  dw.append(np.array(dd))
 return np.array(out),np.array(dw)

def transport(S,dS):
 T=[];dT=[]
 for r in range(4):
  a,b,c=[j for j in range(4) if j!=r]
  u,v=S[:,b]-S[:,a],S[:,c]-S[:,a]
  du,dv=dS[:,b]-dS[:,a],dS[:,c]-dS[:,a]
  T.append(np.outer(v,u)@ETA-np.outer(u,v)@ETA)
  dT.append((np.outer(dv,u)+np.outer(v,du)-np.outer(du,v)-np.outer(u,dv))@ETA)
 return np.array(T),np.array(dT)

def jm(a,b):
 c=np.zeros_like(a)
 for h in range(2):
  for t in range(3):
   for j in range(h+1):
    for k in range(t+1):c[h,t]+=a[j,k]@b[h-j,t-k]
 return c
def const(a):
 out=np.zeros((2,3,4,4),dtype=object);out[0,0]=a;return out
def links(c,T,dT,B,offset=0,w2=None,dw2=None,w11=None,cprime=0):
 Z=np.zeros((4,4),dtype=object)
 if w2 is None:w2=Z
 if dw2 is None:dw2=Z
 if w11 is None:w11=Z
 C=c*T;L11=offset*(c*dT+cprime*T)+w11
 out=const(I);out[0,1]=c*T;out[0,2]=c*c*(T@T)*F(1,2)
 out[0,2]+=w2
 out[1,1]=L11
 out[1,2]=offset*dw2+(C@L11+L11@C)*F(1,2)
 bg=const(I);bg[1,0]=B
 return jm(bg,out)
def linv(a):return a.swapaxes(-1,-2)*np.array(SIG)[None,None,:,None]*np.array(SIG)[None,None,None,:]

def setup(f=F(1),fp=F(1)):
 S=np.diag([F(1),F(1),f,f]);dS=np.diag([F(0),F(0),fp,fp])
 W,DW=faceweights(S);T,dT=transport(S,dS)
 r=np.zeros(24,dtype=object)
 for face,(a,b) in enumerate(PAIRS):
  u,v=[j for j in range(4) if j not in (a,b)]
  dW=orient(a,b)*weight(wedge(dS[:,u],S[:,v])+wedge(S[:,u],dS[:,v]))
  for j in range(6):
   force=np.sum(dW*G[j])
   r[6*a+j]+=(b==1)*force;r[6*b+j]-=(a==1)*force
 H=np.array([[x.re for x in row] for row in symbol(1,f)],dtype=object)
 a1=-inverse(H)@r
 B=np.array([sum(a1[6*r+j]*G[j] for j in range(6)) for r in range(4)])
 return S,T,dT,W,DW,B,a1

def euler_jet(amplitudes,data,w2=None,dw2=None,w11=None,spatial=True,background=True,damps=None):
 S,T,dT,W,DW,B,a1=data
 if not background:B=np.zeros_like(B)
 phases=np.array(amplitudes,dtype=object).reshape(2,4)
 phases=np.array([phases[0],phases[1],-phases[0],-phases[1]])
 if damps is None:damps=np.zeros((2,4),dtype=object)
 damps=np.array(damps,dtype=object).reshape(2,4)
 damps=np.array([damps[0],damps[1],-damps[0],-damps[1]])
 zero=np.zeros((4,4,4,4),dtype=object)
 if w2 is None:w2=zero
 if dw2 is None:dw2=zero
 if w11 is None:w11=zero
 dS=np.diag([F(0),F(0),F(1),F(1)])
 dW=[]
 for r,s in PAIRS:
  u,v=[j for j in range(4) if j not in (r,s)]
  dW.append(orient(r,s)*weight(wedge(dS[:,u],S[:,v])+wedge(S[:,u],dS[:,v])))
 EK=np.zeros((4,2,3,24),dtype=object);EQ=np.zeros((4,2,3,10),dtype=object)
 for p in range(4):
  for face,(r,s) in enumerate(PAIRS):
   roles=[r,s,r,s];offs=[0,int(r==1),int(s==1),0];shifts=[0,1,1,0]
   def fac_at(bp,baseoff):
    fac=[]
    for j,rr in enumerate(roles):
     pp=(bp+shifts[j])%4
     # spatial=False is a uniform coframe parameter derivative.
     off=baseoff+offs[j] if spatial else 1
     z=links(phases[pp,rr],T[rr],dT[rr],B[rr],off,w2[pp,rr],dw2[pp,rr],w11[pp,rr],damps[pp,rr])
     fac.append(linv(z) if j>=2 else z)
    return fac
   fac=fac_at(p,0);prod=const(I)
   for z in fac:prod=jm(prod,z)
   for h in range(2):
    for t in range(3):
     for j in range(10):EQ[p,h,t,j]+=np.sum(DW[face,j]*prod[h,t])
   for j,rr in enumerate(roles):
    bp=(p-shifts[j])%4;boff=-offs[j] if spatial else 1
    fac=fac_at(bp,boff if spatial else 0)
    prefix=const(I);suffix=const(I)
    for z in fac[:j]:prefix=jm(prefix,z)
    for z in fac[j+1:]:suffix=jm(suffix,z)
    wt=const(W[face].T);wt[1,0]=boff*dW[face].T
    co=jm(jm(suffix,wt),prefix)
    term=-jm(fac[j],co) if j>=2 else jm(co,fac[j])
    for h in range(2):
     for t in range(3):
      for g in range(6):EK[p,h,t,6*rr+g]+=np.sum(term[h,t].T*G[g])
 return EK,EQ

def coefficient(amplitudes,setup_data,keep_transport=True,keep_background=True):
 S,T,dT,W,DW,B,a1=setup_data
 if not keep_transport:dT=np.zeros_like(dT)
 if not keep_background:B=np.zeros_like(B)
 amps=np.asarray(amplitudes,dtype=object).reshape(2,4)
 phases=np.array([amps[0],amps[1],-amps[0],-amps[1]])
 eq=np.zeros((4,2,3,10),dtype=object)
 for p in range(4):
  for face,(r,s) in enumerate(PAIRS):
   fac=[links(phases[p,r],T[r],dT[r],B[r]),
        links(phases[(p+1)%4,s],T[s],dT[s],B[s],int(r==1)),
        linv(links(phases[(p+1)%4,r],T[r],dT[r],B[r],int(s==1))),
        linv(links(phases[p,s],T[s],dT[s],B[s]))]
   prod=const(I)
   for x in fac:prod=jm(prod,x)
   for h in range(2):
    for t in range(3):
     for j in range(10):eq[p,h,t,j]+=np.sum(DW[face,j]*prod[h,t])
 assert not np.any(np.sum(eq[:,0,2],axis=0))
 return np.sum(eq[:,1,2],axis=0)*F(1,4),eq


"""Shared-link first-slow coefficient on the literal joint range graph."""
from a4d_designated_full_gap_check import QI,flat_symbols,mm,pairing,column,EYE

def qi_inverse(a):
 n=len(a);b=[[QI.of(x) for x in row]+[QI.of(i==j) for j in range(n)] for i,row in enumerate(a)]
 for j in range(n):
  p=next(i for i in range(j,n) if b[i][j]);b[j],b[p]=b[p],b[j]
  v=b[j][j];b[j]=[x/v for x in b[j]]
  for i in range(n):
   if i!=j and b[i][j]:
    v=b[i][j];b[i]=[x-v*y for x,y in zip(b[i],b[j])]
 return np.array([r[n:] for r in b],dtype=object)

def independent_rows(a):
 basis=[];rows=[]
 for j,row in enumerate(a):
  v=[QI.of(x) for x in row]
  for col,b in basis:
   z=v[col];v=[x-z*y for x,y in zip(v,b)]
  col=next((k for k,x in enumerate(v) if x),None)
  if col is not None:
   z=v[col];basis.append((col,[x/z for x in v]));rows.append(j)
 return rows

COLS=[0,1,2,3,4,6,7,8,9,10,12,13,14,15,17,18,19,20,22,23]
A,C=flat_symbols([QI(0,1)]*4)
J=np.concatenate([np.array(A,dtype=object).T,np.array(C,dtype=object)])
ROWS=independent_rows(J[:,COLS]);assert len(ROWS)==20
RINV=qi_inverse(J[np.ix_(ROWS,COLS)])

def matcoords(coef):
 return np.array([[sum(coef[p,6*r+j]*G[j] for j in range(6)) for r in range(4)] for p in range(4)])
def generic_h(phase,f):
 phase=list(map(QI.of,phase));a=[[QI() for _ in range(24)] for _ in range(24)]
 weights=[f*f,f,f,f,f,1]
 for face,(r,s) in enumerate(PAIRS):
  u,v=[i for i in range(4) if i not in (r,s)]
  area=wedge(np.array(column(EYE,u)),np.array(column(EYE,v)))
  roles=(r,s,r,s);direct=(QI.of(1),phase[r],-phase[s],QI.of(-1))
  inv=(QI.of(1),1/phase[r],-1/phase[s],QI.of(-1))
  role=[[QI() for _ in range(4)] for _ in range(4)]
  for i,j in combinations(range(4),2):
   role[roles[i]][roles[j]]+=direct[i]*inv[j]/2
   role[roles[j]][roles[i]]-=inv[i]*direct[j]/2
  for i,xi in enumerate(GEN):
   for j,xj in enumerate(GEN):
    xy,yx=mm(xi,xj),mm(xj,xi)
    bracket=[[xy[k][l]-yx[k][l] for l in range(4)] for k in range(4)]
    val=weights[face]*orient(r,s)*pairing(area,bracket)
    for rr in range(4):
     for ss in range(4):a[6*rr+i][6*ss+j]+=role[rr][ss]*val
 return np.array(a,dtype=object).T
def joint_data(data):
 S,T,dT,W,DW,B,a1=data;f=S[2,2];q=QI(0,1)
 H=generic_h([q]*4,f);C=np.array([[QI() for _ in range(24)] for _ in range(10)],dtype=object)
 for face,(r,s) in enumerate(PAIRS):
  roles=[r,s,r,s];direct=[QI.of(1),q,-q,QI.of(-1)]
  for j in range(10):
   for g in range(6):
    val=np.sum(DW[face,j]*G[g])
    for k,rr in enumerate(roles):C[j,6*rr+g]+=direct[k]*val
 J=np.concatenate([H,C]);rows=independent_rows(J[:,COLS])
 assert len(rows)==20
 return J,rows,qi_inverse(J[np.ix_(rows,COLS)])
def hdata(f,z):
 return np.array([[x.re for x in row] for row in generic_h([z]*4,f)],dtype=object)
def hderivative(f,z):
 a0,a1,a2=[hdata(x,z) for x in map(F,[0,1,2])]
 quad=(a2-2*a1+a0)*F(1,2);linear=a1-a0-quad
 return linear+2*f*quad

def corrections(amplitudes,data):
 ek,eq=euler_jet(amplitudes,data,spatial=False,background=False)
 assert not np.any(ek[:,0,1]) and not np.any(eq[:,0,1])
 f=data[0][2,2]
 w=np.zeros((4,24),dtype=object);dw=np.zeros_like(w)
 for sign in [1,-1]:
  ph=np.array([sign**p for p in range(4)],dtype=object)
  f2=np.sum(ph[:,None]*ek[:,0,2],axis=0)*F(1,4)
  df2=np.sum(ph[:,None]*ek[:,1,2],axis=0)*F(1,4)
  H=hdata(f,sign);HI=inverse(H)
  ww=-HI@f2;dd=-HI@(df2+hderivative(f,sign)@ww)
  w+=ph[:,None]*ww;dw+=ph[:,None]*dd
 assert np.array_equal(ek[2,0,2],ek[0,0,2]) and np.array_equal(ek[3,0,2],ek[1,0,2])
 ek,eq=euler_jet(amplitudes,data)
 source=np.concatenate([ek[:,1,1],eq[:,1,1]],axis=-1)
 assert np.array_equal(source[2],-source[0]) and np.array_equal(source[3],-source[1])
 sc=np.array([QI(x,-y) for x,y in zip(source[0],source[1])],dtype=object)
 wc=np.array([QI() for _ in range(24)],dtype=object);wc[COLS]=-RINV@sc[ROWS]
 w11=np.array([[x.re for x in wc],[-x.im for x in wc],[-x.re for x in wc],[x.im for x in wc]],dtype=object)
 return matcoords(w),matcoords(dw),matcoords(w11),w,dw,w11,sc

def graph_coefficient(amplitudes,data):
 w,dw,w11,coords,dcoords,c11,source=corrections(amplitudes,data)
 ek,eq=euler_jet(amplitudes,data,w,dw,w11)
 assert not np.any(ek[:,0,2])
 src=np.concatenate([ek[:,1,1],eq[:,1,1]],axis=-1)
 assert not np.any(src[:,ROWS])
 return np.sum(eq[:,1,2],axis=0)*F(1,4),{'w2':coords,'dw2':dcoords,'w11':c11,'center_source':src}


from a4d_designated_full_gap_check import elimination
from itertools import product

def reduced_first_slow(data):
 J,rows,rinv=joint_data(data);rest=[j for j in range(34) if j not in rows]
 E=np.eye(8,dtype=object);B=[];D=[]
 for i in range(4):
  for out,a,da in [(B,E[i],np.zeros(8,dtype=object)),(D,np.zeros(8,dtype=object),E[i])]:
   ek,eq=euler_jet(a,data,damps=da)
   source=np.concatenate([ek[:,1,1],eq[:,1,1]],axis=-1)
   sc=np.array([QI(x,-y) for x,y in zip(source[0],source[1])],dtype=object)
   w=-rinv@sc[rows];out.append((sc+J[:,COLS]@w)[rest])
 return np.array(B,dtype=object).T,np.array(D,dtype=object).T

def cone_maps():
 planes=[]
 for parity in (0,1):
  m=np.zeros((8,3),dtype=object)
  for r,v in enumerate([[1,0,0],[0,1,0],[0,0,1],[0,-1,1]]):m[4*parity+r]=v
  planes.append(('temporal_'+str(parity),m))
 for parities in product((0,1),repeat=3):
  m=np.zeros((8,3),dtype=object)
  for r,p in enumerate(parities,1):m[4*p+r,r-1]=1
  planes.append(('spatial_'+''.join(map(str,parities)),m))
 return planes

def strings(a):
 return [[{'re':str(QI.of(x).re),'im':str(QI.of(x).im)} for x in row] for row in a]

def run_checks():
 data=setup()
 # The background is the actual first smooth coefficient, fixed before
 # inserting a center; its first connection residual vanishes in all rows.
 ek,eq=euler_jet(np.zeros(8,dtype=object),data)
 assert not np.any(ek[:,1,0]) and not np.any(eq[:,1,0])
 assert list(data[-1])==[0]*15+[-1,0,0]+[0]*4+[-1,0]
 for z in (QI.of(1),QI.of(-1),QI(0,1)):
  a,c=flat_symbols([z]*4)
  assert np.array_equal(generic_h([z]*4,F(1)),np.array(a,dtype=object).T)
 jd,jrows,jinv=joint_data(data)
 assert np.array_equal(jd,J) and jrows==ROWS
 assert elimination(J.tolist())[0]==20
 det=elimination(J[np.ix_(ROWS,COLS)].tolist())[1]
 assert det==QI.of(4)
 print('PASS_LITERAL_OPPOSITE_PHASE_QUARTER_CHART_AND_SMOOTH_BACKGROUND',flush=True)

 B,D=reduced_first_slow(data)
 dr=independent_rows(D);assert dr==[1,3,9,11]
 di=qi_inverse(D[dr]);K=B-D@di@B[dr]
 assert elimination(B.tolist())[0]==4
 assert elimination(D.tolist())[0]==4
 assert elimination(np.concatenate([B,D],axis=1).tolist())[0]==6
 assert elimination(K.tolist())[0]==2
 # Exact entire compatible amplitude plane, not a sampled direction.
 compat=np.array([[QI.of(1),QI()], [QI(),QI.of(1)],
                  [QI(F(1,2),F(1,2)),QI(F(-1,2),F(1,2))],
                  [QI(F(-1,2),F(-1,2)),QI(F(1,2),F(-1,2))]],dtype=object)
 assert not np.any(K@compat)
 print('PASS_FULL_EIGHT_REAL_CENTER_SHARED_LINK_FIRSTSLOW_COMPATIBILITY',flush=True)

 # alpha=a-i*b; realification agrees with the literal four-phase field.
 real=np.array([[x.re for x in row]+[x.im for x in row] for row in K]+
               [[x.im for x in row]+[-x.re for x in row] for row in K],dtype=object)
 assert elimination(real.tolist())[0]==4
 planes=[]
 for name,m in cone_maps():
  coeff=real@m;rr=independent_rows(coeff)
  assert len(rr)==3
  minor=elimination(coeff[rr].tolist())[1]
  assert minor and not minor.im
  planes.append({'name':name,'map':[[str(x) for x in row] for row in m],
                 'rank':3,'minor_rows':rr,'minor_determinant':str(minor.re)})
 print('PASS_ALL_TEN_REAL_QUADRATIC_CONE_PLANES_TRANSVERSE_TO_COMPATIBILITY',flush=True)

 # Literal normal graph, with every shifted coframe, W2 derivative and
 # first-slow normal correction retained. This off-shell mixed field is
 # on the frozen quadratic cone, but not on the first-slow center equation.
 mixed=np.array([0,1,1,0,0,0,0,0],dtype=object)
 response,info=graph_coefficient(mixed,data)
 expected=list(map(F,['3/8','1/8','-1/8','-1/2','0','0','1/4','0','0','1/8']))
 assert list(response)==expected
 assert np.any(info['center_source'])
 w,dw,w11,*_=corrections(mixed,data)
 ek,eq=euler_jet(mixed,data,w,dw,w11)
 assert not np.any(np.sum(eq[:,0,2]*np.array([1,-1,1,-1])[:,None],axis=0))
 print('PASS_NONZERO_FIRST_BOUNDARY_RESPONSE_ON_REJECTED_MIXED_CENTER',flush=True)

 # Independent metric readout routine omits the connection assembly and
 # agrees on the pure-center boundary coefficient before range solving.
 direct,_=coefficient(mixed,data)
 literal_ek,literal_eq=euler_jet(mixed,data)
 assert np.array_equal(direct,np.sum(literal_eq[:,1,2],axis=0)*F(1,4))
 print('PASS_INDEPENDENT_FACE_READOUT_AND_PINNABLE_EXACT_LEDGER',flush=True)
 return {
  'arithmetic':'Q and Q(i), exact Fraction arithmetic; no floating ranks',
  'scope':'fixed small nonconstant one-coordinate warp; regular integer-h four-phase envelopes',
  'center_convention':'alpha=a-i*b, p=sum(x) mod 4; all four roles retained',
  'first_smooth_log_coefficient':[str(x) for x in data[-1]],
  'quarter_range_columns':COLS,'quarter_range_rows':ROWS,
  'quarter_range_determinant':str(det.re),
  'B_coframe_firstslow':strings(B),'D_envelope_firstslow':strings(D),
  'D_inverse_rows':dr,'K_compatibility':strings(K),
  'B_complex_rank':4,'D_complex_rank':4,'BD_complex_rank':6,
  'K_complex_rank':2,'K_real_rank':4,
  'compatible_alpha_plane':strings(compat),
  'owned_quadratic_cone_planes':planes,
  'nonzero_boundary_control':{
   'amplitudes':list(map(str,mixed)),
   'normal_graph_h_times_amplitude_squared_response':list(map(str,response)),
   'frozen_quadratic_metric_gate_zero':True,
   'firstslow_center_residual_nonzero':True,
   'status':'OFF_SHELL_CONTROL; not a stationary counterexample'},
  'coframe_neighborhood':'existential open neighborhood of f=1, from exact transversality and compactness; no numeric radius asserted',
  'analytic_conclusion':'all regular h-expansion coefficients vanish for exact connection/phase-erased-metric fields on nonconstant small warps; owner-sum comparator difference is O(h^infinity)',
  'nonclaims':['no theorem for nonanalytic or nonuniform refinement families',
               'no all-frequency arbitrary-four-dimensional inverse',
               'no prescribed-source existence for extra branches',
               'no unconditional h*kappa^2 cancellation',
               'no task-level universal Einstein terminal']}

if __name__=='__main__':
 import argparse
 from pathlib import Path
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path)
 parser.add_argument('--expect',type=Path)
 args=parser.parse_args();report=run_checks()
 if args.expect:
  assert json.loads(args.expect.read_text())==report
  print('PASS_PINNED_LEDGER',flush=True)
 if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
 print('RESULT: warped firstslow/quadratic-cone rigidity for regular quarter branches.',flush=True)
