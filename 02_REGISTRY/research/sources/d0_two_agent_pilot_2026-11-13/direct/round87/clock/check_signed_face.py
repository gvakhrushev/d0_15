"""A same-root NC1 comparison of two addressed physical angle words."""
import itertools
import json
import math
from fractions import Fraction

import mpmath as mp
import numpy as np

p = (math.sqrt(5)-1)/2
a = math.sqrt(p)
theta = math.asin(p)
v = np.array([a,p])
G = np.array([[a,-p],[p,a]])
eye = np.eye(4)
eta = eye[[1,0,2,3]] @ np.diag([1,1,-1,-1])
# Ordered logical lines. PORT and both Spin bits may be initially arbitrary.
XCOIN,YCOIN,PAR,PTAIL,Q,R,TAIL,F,E,PORT,SPIN_A,SPIN_B = range(12)
DIMS = [2]*12


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


def close(x,y,label,tol=2e-12):
    require(np.max(np.abs(np.asarray(x)-np.asarray(y)))<tol,label)


def rot(t):
    return np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])


def proper_geometry(alpha,beta):
    nu=.25
    frame=nu*eta.copy()
    frame[:,0]-=nu*math.sin(2*alpha)*eye[:,3]
    link=eye.copy()
    link[2:4,2:4]=rot(2*beta)
    close(link.T@eta@link,eta,'Lorentz')
    close(np.linalg.det(frame),-nu**4,'actual signed determinant')
    fixed=(0,0,0,0)
    def tr(x,r):
        y=list(x);y[r]=(y[r]+1)%3
        return tuple(y)
    lateral=tr(fixed,2)
    def U(x,r):
        return link if x==lateral and r==0 else eye
    values=[]
    for site in itertools.product(range(3),repeat=4):
        V=frame if site==fixed else nu*eta
        for r,s in itertools.combinations(range(4),2):
            plaquette=U(site,r)@U(tr(site,r),s)@U(tr(site,s),r).T@U(site,s).T
            B=(np.outer(V[:,r],V[:,s])-np.outer(V[:,s],V[:,r]))@eta
            val=nu**4/(2*np.linalg.det(V))*np.trace(B@(plaquette-plaquette.T)/2)
            values.append(val)
            if site!=fixed or (r,s)!=(0,2):
                close(val,0,'all other physical plaquettes')
    total=sum(values)
    close(total,nu**2*math.sin(2*alpha)*math.sin(2*beta),'native density')
    # The exact exterior action: modes 2,3 are adjacent in original order
    # (0,2,3,1), so spectator occupations introduce no fermion swap sign.
    action=np.zeros((16,16))
    for col in range(16):
        n2=(col>>1)&1; n3=(col>>2)&1
        parity=n2^n3
        bit=np.eye(2)[:,n2]
        xx=np.array([[0,1],[1,0]]) if parity else np.eye(2)
        result=xx@rot(beta)@xx@rot(-beta)@bit
        for i in (0,1):
            row=(col&~6)|(i<<1)|((parity^i)<<2)
            action[row,col]=result[i]
    compare=np.zeros_like(action)
    k=(0,2,3,1)
    for col in range(16):
        src=[k[j] for j in range(4) if col&(1<<j)]
        for row in range(16):
            dst=[k[j] for j in range(4) if row&(1<<j)]
            if len(src)==len(dst):
                compare[row,col]=np.linalg.det(link[np.ix_(dst,src)]) if src else 1.
    close(action,compare,'all 16 physical exterior columns')
    # Reference 02 shear in the actual common-null orientation.
    null=eye.copy()*0;null[1,2]=null[2,0]=1
    t_s=nu*math.sin(2*alpha)
    k_s=math.sin(2*beta)/4
    other=nu*eta.copy();other[:,0]+=t_s*eye[:,0]
    w=(np.outer(other[:,0],other[:,2])-np.outer(other[:,2],other[:,0]))@eta
    pos=eye+k_s*null+(k_s**2/2)*(null@null)
    neg=eye-k_s*null+(k_s**2/2)*(null@null)
    close(pos.T@eta@pos,eta,'genuine neighboring null link')
    close(nu**4/(2*np.linalg.det(other))*np.trace(w@(neg-pos)/2),
          total/4,'true optional null-face product')
    return total


def swap(c,t):
    return [('C',c,t),('C',t,c),('C',c,t)]


def zgate(q):
    return swap(q,PORT)+[('I',),('I',)]+swap(q,PORT)


def invg(q):
    return zgate(q)+[('G',q)]+zgate(q)


def reflect(q,exp,sign):
    rotation=[('G',q)]*exp
    return rotation+zgate(q) if sign==1 else zgate(q)+rotation


def nc1(head,tail):
    return [('C',head,tail),('G',tail),('C',head,tail)]


def schedules(sign1,sign2):
    prefix=invg(PAR)+[('C',XCOIN,PAR),('C',YCOIN,PAR)]+nc1(PAR,PTAIL)
    local_a=reflect(Q,1,sign1)
    local_b=reflect(R,2,-sign2)
    transfer=swap(Q,R)
    mix=[('C',XCOIN,Q)]
    before=invg(Q)+local_a+mix+transfer+local_b+transfer
    # After reading the central head, f,e remain quantum working wires. PAR was measured.
    mark=nc1(Q,TAIL)+invg(F)+[('C',Q,F)]+invg(E)+[('C',F,E)]
    mark+=invg(TAIL)+[('C',F,TAIL)]+invg(TAIL)+[('C',F,TAIL)]
    after=transfer+local_b+transfer+mix+local_a+[('G',Q)]
    return prefix,invg(PTAIL),before+mark+after,len(before+mark+after)


local_source=np.zeros((8,8))
quat=np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
local_source[:4,:4]=eye
local_source[4:,4:]=quat
perm=np.eye(4)[[0,1,3,2]]
old_index=np.arange(8)


def operate(state, gate):
    what=gate[0]
    axes=gate[1:] if what!='I' else (PORT,SPIN_A,SPIN_B)
    mat={'I':local_source,'C':perm,'G':G}[what]
    trailing=list(range(len(axes)))
    front=np.moveaxis(state,axes,trailing)
    applied=np.einsum('ij,jk->ik',mat,front.reshape(len(mat),-1),optimize=False).reshape(front.shape)
    return np.moveaxis(applied,trailing,axes)


def evolve(state, word, measure_work=False):
    total=0.
    for gate in word:
        nxt=operate(state,gate)
        if measure_work:
            odds=abs(np.vdot(state,nxt))**2
            if abs(1-odds)<1e-12:
                odds=1.
            total+=math.sqrt(max(0,1-odds))
        state=nxt
    return state,total


def projection(state, parity):
    mask=np.ones(DIMS)
    wrong=[slice(None)]*12
    wrong[PAR]=1-parity
    mask[tuple(wrong)]=0
    if parity:
        wrong[PAR]=1;wrong[PTAIL]=1
        mask[tuple(wrong)]=0
    return mask*state


def original(old):
    data=old
    for _ in range(9):
        data=np.kron(v,data)
    return data.reshape(DIMS)


def experiment(s,t,geometry=True):
    prefix,early,late,nwin=schedules(s,t)
    base=proper_geometry(s*theta,t*2*theta) if geometry else None
    q=(1+math.sin(2*s*theta)*math.sin(4*t*theta))/2
    n0=p**2+p**4
    n1=2*p**3
    cold0=p*n0
    cold1=2*p**7*(p-p**3*q)**2
    for old_case in range(9):
        # Eight basis columns plus an arbitrary phase-sensitive full old vector.
        old=(np.eye(8)[:,old_case] if old_case<8 else
             np.exp(.31j*old_index)*(old_index+1)/np.linalg.norm(old_index+1))
        start=original(old)
        with_work=(old_case==0)
        raw,work=evolve(start,prefix,with_work)
        columns=[]
        for par,weight,stages,predicted in ((0,n0,early,cold0),(1,n1,late,cold1)):
            projected=projection(raw,par)
            close(np.vdot(projected,projected),weight,'full actual raw mass')
            returned,paid=evolve(projected/math.sqrt(weight),stages,with_work)
            work+=weight*paid
            # Contract all real new wires against the routed passive columns.
            restricted=projection(original(np.ones(8)),par)
            col=(restricted.reshape(-1,8)*returned.reshape(-1,8)).sum(axis=0)
            pred=math.sqrt(predicted)*old
            close(col,pred,'full passive boundary, including dirty PORT/Spin')
            columns.append(float(np.vdot(col,col).real))
            if par:
                big=[slice(None)]*12; big[E]=1
                close(np.linalg.norm(returned[tuple(big)])**2,q,'retained e gives true response')
        if with_work:
            selected=columns
            square_work=work
    return dict(s=s,t=t,density=base,q=q,h=sum(selected),work=square_work,
                prefix=len(prefix),even=len(early),odd_window=nwin)


def mul_a(vec):
    # a^4=1-a^2, coefficient order 1,a,a^2,a^3.
    return np.stack((vec[...,3],vec[...,0],vec[...,1]-vec[...,3],vec[...,2]),axis=-1)


def exact_move(state,gate):
    if gate[0]=='G':
        data=np.moveaxis(state,gate[1],0)
        out=np.stack((mul_a(data[0])-mul_a(mul_a(data[1])),
                      mul_a(mul_a(data[0]))+mul_a(data[1])))
        return np.moveaxis(out,0,gate[1])
    if gate[0]=='C':
        control,target=gate[1:]
        ss=[slice(None)]*13
        ss[control]=1
        out=state.copy()
        out[tuple(ss)]=np.flip(state[tuple(ss)],axis=target-int(target>control))
        return out
    data=state.reshape(-1,8,4)
    ids=np.argmax(abs(local_source),axis=1)
    signs=local_source[np.arange(8),ids].astype(np.int64)
    return (data[:,ids,:]*signs[None,:,None]).reshape(state.shape)


def certified_work(sign1,sign2):
    basis=[np.array([1,0,0,0],dtype=np.int64)]
    for _ in range(18):
        basis.append(mul_a(basis[-1]))
    state=np.zeros((2**9,8,4),dtype=np.int64)
    for i in range(2**9):
        state[i,0]=basis[9+bin(i).count('1')]
    state=state.reshape(DIMS+[4])
    zero=np.zeros(4,dtype=np.int64)
    def dot(old,new):
        bound=max(int(np.max(abs(old))),int(np.max(abs(new))))
        require(16*4096*bound**2*16<2**62,'exact int64 contractions')
        products=old.reshape(-1,4).T@new.reshape(-1,4)
        return sum((int(products[i,j])*basis[i+j]
                    for i,j in itertools.product(range(4),repeat=2)),zero)
    aa=mp.iv.sqrt((mp.iv.sqrt(5)-1)/2)
    def number(coeff):
        out=mp.iv.mpf(0)
        for n in reversed(coeff):
            out=out*aa+int(n)
        return out
    def run(old,stages):
        norm=dot(old,old)
        work=mp.iv.mpf(0)
        for gate in stages:
            new=exact_move(old,gate)
            overlap=dot(old,new)
            if not(np.array_equal(overlap,norm) or np.array_equal(overlap,-norm)):
                rad=number(norm-overlap)*number(norm+overlap)
                require(rad>0,'positive enclosed radicand')
                work+=mp.iv.sqrt(rad)
            old=new
        return old,work
    pre,even,odd,_=schedules(sign1,sign2)
    raw,cost=run(state,pre)
    for b,stages in ((0,even),(1,odd)):
        proj=projection(np.ones(DIMS,dtype=np.int64),b).astype(np.int64)
        _,spent=run(raw*proj[...,None],stages)
        cost+=spent
    return cost


def native_secants():
    mp.mp.dps=95
    pp=(mp.sqrt(5)-1)/2
    theta0=mp.asin(pp)
    zz=mp.mpf(2)**-20
    nu=mp.mpf(1)/4
    n0=pp**2+pp**4
    def h(q):
        return pp*n0+2*pp**7*(pp-pp**3*q)**2
    at=mp.mpf(1)/2
    exact=(8*4*zz*pp**10*(pp-pp**3*at)
           /((1-zz+zz*h(at))*2*nu**2))
    best=1.
    results=[]
    for m in range(2,12000):
        diff=abs(math.sin(2*m*theta))
        if not diff < best/4:
            continue
        best=diff
        prod=mp.sin(2*m*theta0)*mp.sin(4*theta0)
        q1=(1+prod)/2
        q0=(1-prod)/2
        delta=-8*mp.log1p(zz*(h(q1)-h(q0))/(1-zz+zz*h(q0)))
        slope=delta/(2*nu**2*prod)
        results.append((m,float(abs(slope/exact-1))))
    require(len(results)>=4 and results[-1][1]<1e-13,'genuine native secant convergence')
    # Crude norm lower bound divided into full analytic heat error eventually decays.
    # At m>=2*3^7, consecutive conservative terms (for heat with n=2m)
    # have ratio bounded by 3^14/(11^2*(2m+1)*(2m+2)) < 1/2.
    m0=2*3**7
    require(Fraction(3**14,121*(2*m0+1)*(2*m0+2))<Fraction(1,2),
            'factorial beats the algebraic norm lower bound')
    return float(exact),results


def main():
    rows=[experiment(s,t) for s,t in itertools.product((-1,1),repeat=2)]
    close(rows[0]['h'],rows[3]['h'],'equal signed product')
    close(rows[1]['h'],rows[2]['h'],'equal opposite product')
    z=2**-20
    delta=-math.log1p(z*(rows[0]['h']-rows[1]['h'])/(1-z+z*rows[1]['h']))
    require(delta>0,'cold and actual geometric secant')
    lengths={r['odd_window'] for r in rows}
    require(len(lengths)==1 and min(lengths)>=32,'real square interval')
    # A walk with a changed letter must traverse the whole square interval.
    n=32
    rational_heat=Fraction(528,359)*Fraction(1,11)**n/math.factorial(n)/(1-Fraction(1,11*(n+1)))
    require(rational_heat<Fraction(1,2**200),'full heat on both clock degrees')
    mp.iv.dps=55
    pi=(mp.iv.sqrt(5)-1)/2
    ai=mp.iv.sqrt(pi)
    sine2=2*ai*pi
    sine4=2*sine2*(pi-pi**2)
    require(sine2*sine4>mp.iv.mpf(2)/5,'positive interval for geometric product')
    require(delta>2**-35,'observed common full determinant')
    for row in rows:
        val=certified_work(row['s'],row['t'])
        hundredth=math.floor(row['work']*100)
        require(val>mp.iv.mpf(hundredth)/100 and val<mp.iv.mpf(hundredth+1)/100,
                'rigorous work interval, width 1/100')
        row['work_interval_hundredths']=[hundredth,hundredth+1]
    # Analytic independent lower bound j'(q)>=4 z p^10(p-p³);
    # use p>3/5, product>2/5, p-p³=p²>9/25.
    lower=4*Fraction(1,2**20)*Fraction(3,5)**10*Fraction(9,25)*Fraction(2,5)
    require(lower>Fraction(1,2**29),'exact cold lower bound')
    limiting_slope,examples=native_secants()
    return dict(native_secant_full_limit=limiting_slope,verified_m_relative_cold_errors=examples,
                all_old_PORT_Spin_columns=8,real_primitives_per_prefix=rows[0]['prefix'],
                even_square_stages=rows[0]['even'],odd_square_stages=rows[0]['odd_window'],
                field_scenes=[dict(left=r['s'],right=r['t'],geometric_face=round(r['density'],12),
                      retained_probability=round(r['q'],12),full_RC3_h=round(r['h'],12),
                      honest_square_work_old_PORT_Spin_zero=round(r['work'],10),
                      rigorous_work_interval_hundredths=r['work_interval_hundredths']) for r in rows],
                RC3_contrast_per_old_column=round(delta,18),RC3_full_rank8_contrast=round(8*delta,18),
                DeltaJ_per_column_above_2pow=-29,
                abs_Delta_thermal_below_2pow=-200,extra_terminal_delay=0,
                supplied_full_Julia_bank=False,full_Book_Cost_Info=False,GR_closed=False)


if __name__=='__main__':
    print(json.dumps(main(),indent=2))
