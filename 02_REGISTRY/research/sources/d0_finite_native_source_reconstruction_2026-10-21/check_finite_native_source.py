#!/usr/bin/env python3
"""Exact, finite native source TEST; no finite-word variational lift.

The full two-query work/OR channel is differentiated by 16 separately
paid native programmes. All 256 work amplitudes are checked for each
slot. Their exact polarization identity proves every density entry,
including coherences retained inside the OR blocks. No sampling or
physical experiment is represented by this algebraic replay.
"""
from fractions import Fraction as Q
from dataclasses import dataclass
from pathlib import Path
import argparse
import json
import math
import mpmath as mp


@dataclass(frozen=True)
class A:
    """Q[a]/(a^4+a^2-1), a=sqrt(phi^-1)."""
    c: tuple

    def __add__(self, other):
        other = number(other)
        return A(tuple(x+y for x,y in zip(self.c, other.c)))
    __radd__ = __add__
    def __neg__(self): return A(tuple(-x for x in self.c))
    def __sub__(self, other): return self + (-number(other))
    def __rsub__(self, other): return number(other) + (-self)
    def __mul__(self, other):
        other = number(other)
        if not any(self.c) or not any(other.c): return ZERO
        v = [Q(0)]*7
        for i,x in enumerate(self.c):
            for j,y in enumerate(other.c):
                if x and y: v[i+j] += x*y
        for k in range(6,3,-1):
            v[k-4] += v[k]
            v[k-2] -= v[k]
        return A(tuple(v[:4]))
    __rmul__ = __mul__
    def __truediv__(self, other):
        if isinstance(other, A): raise TypeError('use explicit algebraic inverse')
        return A(tuple(x/Q(other) for x in self.c))
    def __pow__(self, n):
        if n < 0: raise ValueError('nonnegative powers only')
        out=ONE; base=self
        while n:
            if n&1: out=out*base
            base=base*base; n//=2
        return out
    def numeric(self):
        av=mp.sqrt((mp.sqrt(5)-1)/2)
        return sum((mp.mpf(x.numerator)/x.denominator)*av**i for i,x in enumerate(self.c))
    def data(self): return [str(x) for x in self.c]


def number(v):
    return v if isinstance(v,A) else A((Q(v),Q(0),Q(0),Q(0)))


ZERO=number(0); ONE=number(1)
a=A((Q(0),Q(1),Q(0),Q(0))); p=a*a


def require(ok, label):
    if not bool(ok): raise ArithmeticError(label)


def eye(n): return [[ONE if i==j else ZERO for j in range(n)] for i in range(n)]
def transpose(m): return list(map(list,zip(*m)))
def mm(m,n):
    out=[[ZERO for _ in range(len(n[0]))] for _ in range(len(m))]
    for i,row in enumerate(m):
        for k,x in enumerate(row):
            if x==ZERO: continue
            for j,y in enumerate(n[k]):
                if y!=ZERO: out[i][j]=out[i][j]+x*y
    return out
def kron(m,n):
    return [[m[i][j]*n[k][l] for j in range(len(m[0])) for l in range(len(n[0]))]
            for i in range(len(m)) for k in range(len(n))]


G=[[a,-p],[p,a]]
J=[[ZERO,-ONE],[ONE,ZERO]]
DG=mm(J,G)
G3=mm(mm(G,G),G); GM=transpose(G)
CX=eye(4);CX[2][2]=CX[3][3]=ZERO;CX[2][3]=CX[3][2]=ONE


def query(rotations):
    e1,e2,b1,b2=rotations
    return kron(mm(mm(CX,kron(e2,eye(2))),mm(CX,kron(e1,eye(2)))),mm(b2,b1))


def work_coefficients(rotations):
    """256 entries: coefficient times (sqrt(1-z))^c (sqrt(z))^t.

    The two +/- input factors each carry 1/sqrt(2), so their product
    has rational normalization 1/2. Every efficiency/work output stays.
    """
    up=query(rotations[:4]); um=query(rotations[4:])
    vp=[row[0]+row[2] for row in up]
    vm=[row[0]-row[2] for row in um]
    out=[]
    for i in range(8):
        for f in range(2):
            for j in range(8):
                for g in range(2):
                    ci=i not in (0,2); cj=j not in (0,2)
                    coeff=vp[i]*vm[j]/2
                    if (f and not ci) or (g and not cj): coeff=ZERO
                    cexp=int(ci and not f)+int(cj and not g)
                    texp=f+g
                    out.append((coeff,cexp,texp,int(bool(f or g))))
    return out


def probability(work, bit=None):
    z=Q(1,2**20)
    return sum((w*w * ((1-z)**c*z**t) for w,c,t,b in work
                if bit is None or b==bit), ZERO)


def probability_jet(work, derivative, bit=None):
    z=Q(1,2**20)
    return sum((2*w*dw*((1-z)**c*z**t)
                for (w,c,t,b),(dw,dc,dt,db) in zip(work,derivative)
                if bit is None or b==bit), ZERO)


def exact_replay():
    require(p+p*p==ONE,'Golden field relation')
    require(mm(transpose(G),G)==eye(2),'all native G columns')
    c=p**3; s=2*a*p; sin4=2*c*s
    require(c*c+s*s==ONE,'native double-angle identity')
    require(sin4==4*a*p**4 and sin4!=ZERO,'nonzero exact shift denominator')
    invsin=(a+a**3)*(ONE+p)**4/4
    require(invsin*sin4==ONE,'exact shift inverse')
    # Coherent controlled bypass introduces frequency one; it is outside
    # the unconditional R(t) tensor I / supplied-known-one hypothesis.
    controlled_true=-p/2
    controlled_wrong=-p*(ONE+p)**3/2
    require(controlled_true!=controlled_wrong,'unknown controlled-R counterexample')
    # This is the full controlled-cell identity, including the c=0 block.
    C=eye(4);C[2][2]=C[3][3]=ZERO;C[2][3]=C[3][2]=ONE
    GG=kron(eye(2),G)
    plus=mm(GG,mm(C,C)); minus=mm(C,mm(GG,C))
    require(plus==kron(eye(2),G),'plus cell has both controller columns')
    expected=eye(4)
    for i in range(2):
        for j in range(2): expected[i][j]=G[i][j];expected[i+2][j+2]=GM[i][j]
    require(minus==expected,'minus cell retains controller zero complement')
    for k in (-1,1,3):
        nminus=(3-k)//2;nplus=3-nminus
        word=eye(4)
        for _ in range(nminus): word=mm(minus,word)
        for _ in range(nplus): word=mm(plus,word)
        active={-1:GM,1:G,3:G3}[k]
        expected=eye(4)
        for i in range(2):
            for j in range(2): expected[i][j]=G3[i][j];expected[i+2][j+2]=active[i][j]
        require(word==expected,'literal N=3 controlled word')
    base=work_coefficients([G]*8)
    require(len(base)==256 and probability(base)==ONE,'all256 work normalization')
    r0=probability(base,1)
    thetaE=ZERO;thetab=ZERO
    rows=[]; amplitude_checks=0; probability_checks=0
    for slot in range(8):
        rp=[G]*8;rm=[G]*8;rd=[G]*8
        rp[slot]=G3;rm[slot]=GM;rd[slot]=DG
        wp=work_coefficients(rp);wm=work_coefficients(rm);wd=work_coefficients(rd)
        require(probability(wp)==ONE and probability(wm)==ONE,'all shifted work normalized')
        for b,pp,pm,dd in zip(base,wp,wm,wd):
            w,ec,et,bit=b; xp,xec,xet,xb=pp; xm,mec,met,mb=pm; v,dec,det,db=dd
            require((ec,et,bit)==(xec,xet,xb)==(mec,met,mb)==(dec,det,db),
                    'same actual output/efficiency/OR labels')
            require(xp==c*w+s*v and xm==c*w-s*v,
                    'entire retained output amplitude shift identity')
            amplitude_checks+=2
            require((xp*xp-xm*xm)==sin4*(2*w*v),
                    'all256 outcome first jets including darks')
            probability_checks+=1
        # This checked amplitude identity proves every off-diagonal entry too:
        # (c u+s v)(c U+s V)-(c u-s v)(c U-s V)
        #             =2cs(u V+v U).
        # The same fixed OR dephasing projector preserves the identity.
        dr=probability_jet(base,wd,1)
        qr_p=probability(wp,1); qr_m=probability(wm,1)
        require((qr_p-qr_m)*invsin==dr,'whole OR channel exact derivative')
        require(probability_jet(base,wd)==ZERO,'full density derivative traceless')
        if slot%4<2: thetaE+=dr
        else: thetab+=dr
        rows.append({'slot':slot,'parameter':'E' if slot%4<2 else 'b',
                     'plus_report':qr_p,'minus_report':qr_m,'theta_jet':dr})
    sx=thetaE*a/2;sy=-thetab*a**3
    z=Q(1,2**20);L=4*p**3;M=L*(ONE+p**6);Q0=ONE-z*L;R0=ONE-z*M
    rx=4*z*Q0*p**11;ry=-8*z*p**6*(R0+Q0*p**6)
    require(r0==ONE-Q0*R0,'unchanged finite-z baseline report')
    require(sx==rx and sy==ry,'exact original geometry and matter first sources')
    require(sx!=ZERO and sy!=ZERO,'nonzero slopes without a limiting word')
    wx=(ONE+p)**4/8;wy=(ONE+p)**3/4
    require(wx*8*p**4==ONE and wy*4*p**3==ONE,'original-coordinate source weights')
    # Exact hostile control: the same two-shift rule does NOT differentiate
    # the nonlinear functional r(theta)^2 for r=(1+cos(2theta))/2.
    # Its cos4theta term is 1/8; the frequency-four derivative defect is
    # (1-cos4theta)*sin4theta/2, which is nonzero in Q[a].
    cos4=c*c-s*s
    nonlinear_defect=(ONE-cos4)*sin4/2
    require(nonlinear_defect!=ZERO,'nonlinear price cannot inherit channel shift by substitution')
    return {'work_count':256,'amplitude_identity_checks':amplitude_checks,
            'all_output_probability_checks':probability_checks,
            'density_entries_per_slot_covered_by_polarization':256**2,
            'sin4':sin4,'invsin':invsin,'wx':wx,'wy':wy,'r0':r0,'rx':rx,'ry':ry,
            'nonlinear_exact_defect':nonlinear_defect,'rows':rows}


def numerical_receipt(exact):
    mp.mp.dps=70
    pp=p.numeric();logphi=mp.log(1/pp)
    alpha=(1-(1-2*pp**3)**9)**128
    beta=((1-pp**120)**4*(1-(1-16*pp**9)**20))**43
    h=lambda r:-(r*mp.log(r)+(1-r)*mp.log(1-r))/logphi
    r0=exact['r0'].numeric();hp=mp.log((1-r0)/r0)/logphi
    sx=-alpha*beta*hp*exact['rx'].numeric();sy=-alpha*beta*hp*exact['ry'].numeric()
    naive={'E':mp.mpf(0),'b':mp.mpf(0)}
    variance={'E':mp.mpf(0),'b':mp.mpf(0)}
    printed=[]
    for row in exact['rows']:
        rp=row['plus_report'].numeric();rm=row['minus_report'].numeric()
        require(0<rp<2*mp.mpf(2)**-20 and 0<rm<2*mp.mpf(2)**-20,'positive unconditioned report chart')
        naive[row['parameter']]+=h(rp)-h(rm)
        qp=alpha*beta*rp;qm=alpha*beta*rm
        variance[row['parameter']]+=qp*(1-qp)+qm*(1-qm)
        printed.append({'slot':row['slot'],'parameter':row['parameter'],
                        'plus_report':mp.nstr(rp,28),'minus_report':mp.nstr(rm,28)})
    naive_x=-alpha*beta*exact['wx'].numeric()*naive['E']
    naive_y=alpha*beta*exact['wy'].numeric()*naive['b']
    require(abs(naive_x-sx)>mp.mpf('1e-12') and abs(naive_y-sy)>mp.mpf('1e-12'),
            'actual CQ entropy-value shift is unequal to its first source')
    variance_x=hp**2*exact['wx'].numeric()**2*variance['E']
    variance_y=hp**2*exact['wy'].numeric()**2*variance['b']
    text=lambda v:mp.nstr(v,32)
    return {'decimal_precision':70,'readiness_alpha_beta':text(alpha*beta),
            'baseline_r0':text(r0),'hprime_phi_r0':text(hp),
            'source_x':text(sx),'source_y_sigma_minus':text(sy),'source_ratio':text(sy/sx),
            'incorrect_entropy_shift_x':text(naive_x),'incorrect_entropy_shift_y':text(naive_y),
            'incorrect_entropy_shift_error_x':text(naive_x-sx),
            'incorrect_entropy_shift_error_y':text(naive_y-sy),
            'unconditioned_unbiased_source_variance_x_times_n':text(variance_x),
            'unconditioned_unbiased_source_variance_y_times_n':text(variance_y),
            'test_reports':printed}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path);args=ap.parse_args()
    ex=exact_replay(); num=numerical_receipt(ex)
    out={'status':'PASS_FINITE_NATIVE_SOURCE_RECONSTRUCTION',
         'input_ref':'80d3b1bac1bb9a974f365dbc4c48d3ada539d3a2',
         'exact':{'field':'Q[a]/(a^4+a^2-1), a>0',
                  'all_work_outputs':ex['work_count'],
                  'full_amplitude_identities':ex['amplitude_identity_checks'],
                  'all_outcome_first_jets':ex['all_output_probability_checks'],
                  'density_entries_per_slot_by_proved_polarization':ex['density_entries_per_slot_covered_by_polarization'],
                  'slot_count':8,'separate_paid_programmes':16,
                  'original_r_x':ex['rx'].data(),'original_r_y_sigma_minus':ex['ry'].data(),
                  'exact_nonlinear_functional_counterexample':ex['nonlinear_exact_defect'].data()},
         'cost':{'cells_per_rotation_slot':3,'G_per_test':24,'CNOT_per_test':52,
                 'two_query_unit_ticks_if_reached':76,
                 'query_unit_tick_upper_bound_for_one_launch_each_setting':1216,
                 'abort_can_prevent_query_execution':True,
                 'unconditional_mean_query_charge_identified_with_inventory':False,
                 'preparation_compiler_abort_measurement_readout_costs_additional':True,
                 'optional_baseline_additional':True,'repetitions_not_free':True},
         'numerical':num,
         'scope':{'full_retained_channel_derivative_exact':True,
                  'unconditional_R_tensor_I_or_supplied_known_one_required':True,
                  'coherent_unknown_control_bypass_rule':False,
                  'all_256_work_outputs_and_OR_coherences_retained':True,
                  'source_test_has_bounded_word_depth':True,
                  'actual_CQ_price_source_reconstructed':True,
                  'signed_estimator_equals_physical_price':False,
                  'finite_word_family_has_ordinary_field_derivative':False,
                  'field_to_programme_map_or_tangent_lift_proved':False,
                  'finite_samples_give_exact_source':False,
                  'independent_upstream_sources_zeroed':False,
                  'compulsory_Book03_Info_selected':False,'GR_closed':False}}
    rendered=json.dumps(out,indent=2)+'\n';print(rendered,end='')
    if args.output:args.output.write_text(rendered,encoding='utf-8')


if __name__=='__main__':main()
