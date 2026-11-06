"""Bounded numerical replay of exact 7cx identities; no new physical premises.
Literal CAR ordering, mirrored Julia word order, Walsh normalization and K
formulas are copied from the pinned original owner below. Positive Julia
roots are evaluated by Hermitian spectral calculus, not by a new instrument.
Run from the repository root, or pass that root as the only argument.
"""
from pathlib import Path
import hashlib, json, sys
import numpy as np
repo=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
owner_rel='02_REGISTRY/research/sources/d0_original_full128_future_even_algebra_2026-10-22/check_future_even_algebra_modprime.py'
owner_sha='1b1e75a8c46135eac9495bc47f9239b83ed36713c268d118d017ab176b95f3a5'
assert hashlib.sha256((repo/owner_rel).read_bytes()).hexdigest()==owner_sha
I=np.eye(16,dtype=complex); order=(0,2,3,1); creators=[]
for r in range(4):
 c=np.zeros((16,16),complex); before=order[:order.index(r)]
 for bits in range(16):
  if not (bits>>r)&1:
   c[bits|(1<<r),bits]=(-1)**sum((bits>>j)&1 for j in before)
 creators.append(c)
G01=creators[0]@creators[1].conj().T+creators[1]@creators[0].conj().T
p=(np.sqrt(5.)-1)/2; c=p*p; d=16
walsh=np.array([[(-1)**((j&k).bit_count()) for j in range(32)] for k in range(32)])
E=np.zeros((2048,16),complex); E[:16]=I
Pmask=np.zeros(2048,dtype=bool); Pmask[:16]=True
def positive_root(H):
 e,v=np.linalg.eigh((H+H.conj().T)/2)
 if e.min() < -1e-12: raise ArithmeticError('Julia contraction chart failed')
 return (v*np.sqrt(np.maximum(e,0)))@v.conj().T
def native(theta,nu):
 boost=I+np.sinh(theta)*G01+(np.cosh(theta)-1)*(G01@G01)
 words=[]
 for r,cr in enumerate(creators):
  b=nu*cr; operand=b@boost if r==1 else b
  x=(1j,1j,-1,-1j)[r]*operand
  left=positive_root(I-x@x.conj().T); right=positive_root(I-x.conj().T@x)
  left0=positive_root(I-b@b.conj().T); right0=positive_root(I-b.conj().T@b)
  for word in ((x,left),(x.conj().T,right),(-b,-left0),(-b.conj().T,-right0)):
   words.extend((word,word))
 N=np.einsum('ij,jbkl->ibkl',walsh,np.array(words)).reshape(64,16,16)/32
 a=N[0]; A=a.conj().T@a; Ai=np.linalg.inv(A); Z=np.trace(Ai).real; rho=Ai/Z
 K=np.array([k for j,n in enumerate(N) for k in
             ((I if j==0 else 0)-2*p*p*n.conj().T@a,-2*p*np.sqrt(p)*n.conj().T@a)])
 Nrow=np.concatenate(list(N),axis=1)
 L=np.vstack((p*Nrow.conj().T,np.sqrt(p)*Nrow.conj().T))
 def apply_U(X): return X-2*L@(L.conj().T@X)
 UE=apply_U(E); C=UE[:16]; QE=UE.copy(); QE[Pmask]=0
 F=QE.conj().T@QE
 tau=sum(k@rho@k.conj().T for k in K[1::2]); q=np.trace(tau).real
 echo=E.copy(); powers=I.copy(); grams=[]; mus=[]; gram_errors=[]; joint_errors=[]
 for m in range(1,6):
  echo=apply_U(echo)
  echo[Pmask if m%2 else ~Pmask]=0
  gram=echo.conj().T@echo; powers=powers@F
  mu=np.trace(tau@gram).real
  grams.append(gram); mus.append(mu)
  gram_errors.append(float(np.linalg.norm(gram-powers)))
  joint_errors.append(float(abs(mu-q*np.trace(powers).real/d)))
 return dict(N=N,a=a,A=A,Ai=Ai,Z=Z,rho=rho,K=K,Nrow=Nrow,L=L,UE=UE,C=C,F=F,tau=tau,q=q,
             sigma=tau/q,grams=grams,mus=np.array(mus),echo_gram_errors=gram_errors,joint_errors=joint_errors)
base_theta=np.log(1.25); base_nu=.6; h=2e-5
b=native(base_theta,base_nu)
boost=I+np.sinh(base_theta)*G01+(np.cosh(base_theta)-1)*(G01@G01)
at=1j*base_nu*creators[1]@G01@boost; at=(at+at.conj().T)/16
Avs=[at@b['a']+b['a']@at,2*b['A']/base_nu]
Fvs=[2*c*(b['C']@X+X@b['C']) for X in Avs]
drhos=[];dqs=[];dmus=[];sigma_derivatives=[];tau_derivative_errors=[];mu_fd_errors=[]
for idx,((dt,dnu),X) in enumerate(zip(((h,0),(0,h)),Avs)):
 plus=native(base_theta+dt,base_nu+dnu); minus=native(base_theta-dt,base_nu-dnu)
 dz=np.trace(b['Ai']@X@b['Ai']).real
 dr=-b['Ai']@X@b['Ai']/b['Z']+b['Ai']*dz/b['Z']**2
 dq=64*p**3*dz/b['Z']**2
 dmu=[]; power=I.copy()
 for m in range(1,6):
  nextpower=power@b['F']
  dmu.append(dq*np.trace(nextpower).real/d+b['q']*m*np.trace(power@Fvs[idx]).real/d)
  power=nextpower
 dmu=np.array(dmu); drhos.append(dr);dqs.append(dq);dmus.append(dmu)
 sigma_derivatives.append(float(np.linalg.norm((plus['sigma']-minus['sigma'])/(2*h))))
 tau_derivative_errors.append(float(np.linalg.norm((plus['tau']-minus['tau'])/(2*h)-dq*I/d)))
 mu_fd_errors.append(float(np.max(np.abs((plus['mus']-minus['mus'])/(2*h)-dmu))))
ri=np.linalg.inv(b['rho']); Aread=b['q']*ri/(64*p**3)
source_tests=[]
for z,label in ((2.**-20,'existing root diagnostic z=2^-20'),(.25,'structural tail-sensitivity parameter only; not physical selection')):
 R=np.linalg.inv(I-z*b['F']); eig=np.linalg.eigvalsh(b['F'])
 J=float(-np.log1p(-z*eig).sum()); horizon=4
 weights=np.array([z**m/m for m in range(1,6)])
 JL=float(d/b['q']*np.dot(weights[:horizon],b['mus'][:horizon]))
 direct=[];readout=[];joint=[];frozen_q=[];joint_tail_bounds=[]
 for idx,X in enumerate(Avs):
  direct.append(float((4*c*z*np.trace(R@b['C']@X)).real))
  readout.append(float((z/(16*p)*(np.trace(R@b['C']@ri)*dqs[idx]
                    -b['q']*np.trace(R@b['C']@ri@ri@drhos[idx]))).real))
  numerator=float(d/b['q']*np.dot(weights[:horizon],dmus[idx][:horizon]))
  joint.append(numerator-JL/b['q']*dqs[idx]); frozen_q.append(numerator)
  joint_tail_bounds.append(float(d*z**(horizon+1)*np.linalg.norm(Fvs[idx],2)/(1-z)))
 spectral_tail=d*(z*eig.max())**(horizon+1)/((horizon+1)*(1-z*eig.max()))
 roundoff=100*np.finfo(float).eps*max(abs(J),abs(JL),1e-300)
 assert abs(J-JL)<=spectral_tail+roundoff
 assert max(abs(np.array(direct)-np.array(readout)))<1e-12
 assert np.all(np.abs(np.array(direct)-np.array(joint))<=np.array(joint_tail_bounds)+roundoff)
 assert abs(frozen_q[1]-joint[1])>1e-8
 if z==.25: assert J-JL>1e-13
 source_tests.append(dict(z=z,label=label,J=J,joint_J_L4=JL,tail_difference=J-JL,
  spectral_tail_bound=float(spectral_tail),roundoff_allowance=float(roundoff),
  direct_source_theta_nu=direct,observable_source_theta_nu=readout,joint_L4_source_theta_nu=joint,
  derivative_tail_bounds=joint_tail_bounds,frozen_q_prefactor_source_theta_nu=frozen_q,
  omitted_quotient_term_theta_nu=list(map(float,np.array(frozen_q)-np.array(joint)))))
KfromU=np.array([b['UE'].reshape(2,64,16,16)[port,j] for j in range(64) for port in range(2)])
checks=dict(N_row_isometry=float(np.linalg.norm(b['Nrow']@b['Nrow'].conj().T-I)),
 N_column_completeness=float(np.linalg.norm(sum(n.conj().T@n for n in b['N'])-I)),
 L_isometry_full2048_unitarity_certificate=float(np.linalg.norm(b['L'].conj().T@b['L']-I)),
 full128_column_reconstruction=float(np.linalg.norm(KfromU-b['K'])),
 complete_Kraus_normalization=float(np.linalg.norm(sum(k.conj().T@k for k in b['K'])-I)),
 native_stationarity=float(np.linalg.norm(sum(k@b['rho']@k.conj().T for k in b['K'])-b['rho'])),
 odd_full_matrix=float(np.linalg.norm(b['tau']-b['q']*I/d)),
 q_source_normalization=abs(b['q']-64*p**3/b['Z']),
 odd_normalized_state=float(np.linalg.norm(b['sigma']-I/d)),
 A_from_actual_rho_q=float(np.linalg.norm(Aread-b['A'])),
 feedback_from_complete_return=float(np.linalg.norm(b['F']-4*c*b['A']@(I-c*b['A']))))
assert max(checks.values())<1e-11
assert max(sigma_derivatives)<1e-9
assert max(tau_derivative_errors)<1e-9
assert max(mu_fd_errors)<1e-9
assert max(b['echo_gram_errors'])<1e-11
assert max(b['joint_errors'])<1e-14
result=dict(status='PASS',source_owner=owner_rel,source_owner_sha256=owner_sha,
 literal_copied_blocks='owner lines76-99 CAR and boost;125-159 mirrored Julia words;162-183 Walsh/Kraus. Positive roots evaluated numerically.',
 dimension=dict(DATA=16,addresses=64,ports=2,full_unitary=2048),
 carrier='full Ux=x-2L(Ldagger x); Ldagger L=I proves all-column Hermitian unitarity; every128 output retained',
 initial_source=dict(nu=base_nu,boost_theta=base_theta,phases=['i','i','-1','-i'],stationary_port1_probability=b['q']),
 matrix_identity_errors=checks,normalized_odd_state_derivative_norms_theta_nu=sigma_derivatives,
 odd_unnormalized_derivative_errors_theta_nu=tau_derivative_errors,
 echo_m_values=list(range(1,6)),echo_KdaggerK_equals_Fpower_errors=b['echo_gram_errors'],
 joint_mu_m=b['mus'].tolist(),joint_mu_formula_errors=b['joint_errors'],joint_mu_derivative_fd_errors_theta_nu=mu_fd_errors,
 feedback_sources_and_tails=source_tests,
 reference128='Free oldRIGHT spectator multiplies trace J/source by128; it does not multiply normalized rho,q,or joint probabilities. Already written fine archive is spectator.',
 scope='One specified stationary tick, port1 joint event, then fresh query work and alternating U/Udagger Q/P event branch. Not first-success stopping or free postselection. Preparation and full observer costs remain real; no GR, thermal, or compulsory selection claim.')
print(json.dumps(result,indent=2))
