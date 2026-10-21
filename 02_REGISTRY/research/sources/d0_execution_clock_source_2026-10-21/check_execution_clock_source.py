#!/usr/bin/env python3
"""One original full128 execution, four typed contractions, and a forward clock.

Consumes existing full128 Walsh/Julia/Golden formulas and actual complementary
Book cut. Tests do not choose the compulsory active clock cut, full price,
field writer, or Einstein dynamics. No postselection, clock reset or cyclic
wrap is used. The finite clock is embedded into a larger one-way counter.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
import sympy as sp

INPUT_REF = 'd8f5901b32024bef0abd2d219f8f7228be4993e9'
ORDER = (0, 2, 3, 1)
P = (5.0 ** 0.5 - 1.0) / 2.0
OLD_RIGHT = 128
Z = 2.0 ** -20


def require(ok: bool, label: str) -> None:
    if not bool(ok):
        raise ArithmeticError(label)


def adj(x: np.ndarray) -> np.ndarray:
    return x.conj().T


def positive_sqrt(x: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh((x + adj(x)) / 2)
    require(values.min() > 1e-9, 'strict original Julia chart')
    return (vectors * np.sqrt(values)) @ adj(vectors)


def creators() -> list[np.ndarray]:
    out = []
    for role in range(4):
        c = np.zeros((16, 16), dtype=complex)
        earlier = ORDER[:ORDER.index(role)]
        for bits in range(16):
            if not (bits >> role) & 1:
                c[bits + (1 << role), bits] = (-1) ** sum((bits >> j) & 1 for j in earlier)
        out.append(c)
    return out


@dataclass(frozen=True)
class CompleteRound:
    kraus: np.ndarray
    reporting_ticks: np.ndarray
    blank_index: int = 0

    def effects(self) -> np.ndarray:
        return np.einsum('kji,kjl->kil', self.kraus.conj(), self.kraus)

    def validate(self) -> float:
        error = float(np.linalg.norm(self.effects().sum(axis=0) - np.eye(16)))
        require(error < 2e-12, 'all128 complete effects')
        require(self.kraus.shape == (128, 16, 16), 'all128/all16 labels')
        require(np.all(self.reporting_ticks >= 1), 'every retained outcome is paid')
        return error

    def mean_reporting_effect(self) -> np.ndarray:
        return np.einsum('k,kij->ij', self.reporting_ticks, self.effects())

    def heisenberg(self, x: np.ndarray) -> np.ndarray:
        return sum((adj(k) @ x @ k for k in self.kraus), np.zeros_like(x))

    def blank_word(self, rounds: int) -> tuple[np.ndarray, int]:
        require(rounds >= 1, 'positive actual round count')
        return np.linalg.matrix_power(self.kraus[self.blank_index], rounds), int(rounds * self.reporting_ticks[self.blank_index])


def native_round(theta: float) -> tuple[CompleteRound, np.ndarray, np.ndarray]:
    """Original L4 character, one actual proper-link deformation, both defects.

    No auxiliary Choi/Jones measurement is substituted for the full128 rows.
    The clock variable here is the original 0/10 reporting subclock. Other
    primitive durations are separate inputs to any complete physical clock.
    """
    C = creators(); I = np.eye(16, dtype=complex); nu = 3.0 / 5.0
    phases = (1j, 1j, -1.0, -1j)
    X = np.zeros((4, 4)); X[0, 1] = X[1, 0] = 1
    GX = sum((X[i, j] * C[i] @ adj(C[j]) for i in range(4) for j in range(4)), np.zeros((16,16), complex))
    U = expm(theta * GX)
    words = []; dA = np.zeros((16,16), complex)
    for r in range(4):
        fixed = nu * C[r]
        transported = fixed @ (U if r == 1 else I) * phases[r]
        L = positive_sqrt(I - transported @ adj(transported))
        R = positive_sqrt(I - adj(transported) @ transported)
        L0 = positive_sqrt(I - fixed @ adj(fixed))
        R0 = positive_sqrt(I - adj(fixed) @ fixed)
        for pair in ((transported,L),(adj(transported),R),(-fixed,-L0),(-adj(fixed),-R0)):
            words.extend((pair,pair))
        if r == 1:
            dP = fixed @ U @ GX * phases[r]
            dA += (dP + adj(dP))/16
    Q=[]
    for label in range(32):
        for coefficient in range(2):
            Q.append(sum(((-1)**((label & j).bit_count()) * words[j][coefficient] for j in range(32)), np.zeros((16,16),complex))/32)
    A=Q[0]
    require(np.linalg.norm(A-adj(A))<1e-13, 'literal selfadjoint blank SELECT block')
    K=[]
    for j,N in enumerate(Q):
        shared=adj(N)@A
        K.extend(((I if j==0 else np.zeros_like(I))-2*P**2*shared, -2*P*np.sqrt(P)*shared))
    execution=CompleteRound(np.asarray(K),np.tile([1,2],64))
    execution.validate()
    dB=-2*P**2*(A@dA+dA@A)
    require(np.linalg.norm(execution.kraus[0]-(I-2*P**2*A@A))<1e-13,'actual reflection column, not SELECT row')
    port1=execution.effects()[1::2].sum(axis=0)
    require(np.linalg.norm(port1-4*P**3*A@A)<1e-13,'actual all-label port1 effect')
    return execution,A,dB


def forward_clock_corner(width: int, delay: int) -> np.ndarray:
    """P_window S^delay P_window with an open (not cyclic) forward counter."""
    require(width >= 1 and delay >= 1, 'clock-cut contract')
    T=np.zeros((width,width),dtype=complex)
    for t in range(width):
        if t+delay < width:
            T[t+delay,t]=1
    return T


def feedback(A: np.ndarray, dA: np.ndarray | None = None) -> tuple[float,float]:
    C=adj(A)@A; dim=C.shape[0]
    F=np.eye(dim)-C
    ev=np.linalg.eigvalsh((F+adj(F))/2)
    require(ev.min()>-1e-12 and ev.max()<1+1e-12,'complete Book complement positive')
    value=float(-OLD_RIGHT*np.log1p(-Z*ev).sum())
    source=0.0
    if dA is not None:
        dF=-(adj(dA)@A+adj(A)@dA)
        M=np.eye(dim)-Z*F
        source=float(OLD_RIGHT*Z*np.trace(np.linalg.solve(M,dF)).real)
    return value,source


def exact_clock_checks() -> dict:
    # Polynomial determinant of a genuine finite open-clock corner. The
    # general proof uses its singular projections, not these small examples.
    z,t=sp.symbols('z t',real=True)
    D=sp.Matrix([[sp.Rational(1,2),t],[0,sp.Rational(1,3)]])
    width,delay=4,2
    T=sp.zeros(width)
    for k in range(width-delay): T[k+delay,k]=1
    A=sp.kronecker_product(T,D)
    det_full=(sp.eye(8)-z*(sp.eye(8)-A.T*A)).det()
    det_data=(sp.eye(2)-z*(sp.eye(2)-D.T*D)).det()
    require(sp.factor(det_full-(1-z)**4*det_data**2)==0,'exact finite-clock determinant identity')
    require(T**2==sp.zeros(width),'strictly forward corner nilpotent')
    require((sp.eye(8)-z*A).det()==1,'oriented-time loop determinant is NOT Book complement')
    # Same finite source sequence, different clock timings: rank is overlap
    # of the window with its translated copy, not outcome probability.
    for m in (1,3,5,8):
        for d in (1,2,4):
            R=sp.zeros(m)
            for k in range(max(m-d,0)): R[k+d,k]=1
            require(R.rank()==max(m-d,0),'exact surviving-clock multiplicity')
            require(R**m==sp.zeros(m),'no wrapped temporal loop')
    return {'clock_shift_is_forward_and_open':True,
            'complement_determinant_identity':'EXACT_POLYNOMIAL',
            'surviving_clock_rank':'max(width-delay,0)',
            'det_I_minus_z_corner':'1_DOES_NOT_IMPLY_ZERO_BOOK_SOURCE',
            'initial_slice_return':'ZERO_AFTER_POSITIVE_DELAY'}


def numerical_native_checks() -> dict:
    theta=.08
    run,A,dB=native_round(theta)
    completeness=run.validate()
    rho=np.eye(16)/16
    effects=run.effects()
    states=np.array([k@rho@adj(k) for k in run.kraus])
    q2=np.einsum('jab,kba->jk',states,effects).real
    require(abs(q2.sum()-1)<2e-13 and q2.min()>-1e-15,'full16384 retained history law')
    ticks=run.reporting_ticks[:,None]+run.reporting_ticks[None,:]
    direct_cost=float((q2*ticks).sum())
    C=run.mean_reporting_effect()
    effect_cost=float(np.trace(rho@(C+run.heisenberg(C))).real)
    require(abs(direct_cost-effect_cost)<3e-13,'same-execution paid-port effect and full history clock')
    B=run.kraus[0]
    D,delay=run.blank_word(2)
    dD=dB@B+B@dB
    require(abs(q2[0,0]-np.trace(rho@adj(D)@D).real)<1e-13,'real allblank history probability')
    jd,sd=feedback(D,dD)
    require(abs(sd)>1e-9,'native nonzero Book field source')
    # The native signal actually depends on the deformed original link.
    ds=1e-5
    Dp=native_round(theta+ds)[0].blank_word(2)[0]
    Dm=native_round(theta-ds)[0].blank_word(2)[0]
    fd=(feedback(Dp)[0]-feedback(Dm)[0])/(2*ds)
    require(abs(fd-sd)<2e-11,'actual full128 complementary-source derivative')
    # A stopped-unresolved status is orthogonal to the ORIGINAL input blank.
    # An equal no-exit probability does not make its actual active corner D.
    stopped_status_corner=np.zeros_like(D)
    _,stopped_status_source=feedback(stopped_status_corner,np.zeros_like(dD))
    require(stopped_status_source==0,'unresolved status is not an unpaid blank return')
    rows=[]
    for width in (1,2,3,5,8):
        T=forward_clock_corner(width,delay)
        AA=np.kron(T,D); dAA=np.kron(T,dD)
        val,src=feedback(AA,dAA)
        survived=max(width-delay,0);lost=width-survived
        boundary=-OLD_RIGHT*lost*16*np.log1p(-Z)
        require(abs(val-boundary-survived*jd)<3e-13,'absolute boundary term retained')
        require(abs(src-survived*sd)<3e-13,'exact clock-to-data source factor')
        require(np.linalg.norm(np.linalg.matrix_power(T,width))==0,'no periodic clock wrap')
        rows.append({'active_clock_width':width,'blank_reporting_delay':delay,
                     'return_clock_rank':survived,'absolute_feedback':val,
                     'boundary_value':float(boundary),'native_field_source':src})
    # Build the actual one-round clocked output vector, including every
    # Kraus outcome at its own forward reporting time; no postselection.
    psi=np.zeros(16,dtype=complex);psi[0]=1
    maxclock=4
    tensor=np.zeros((maxclock,128,16),complex)
    for j,k in enumerate(run.kraus): tensor[run.reporting_ticks[j],j]=k@psi
    require(abs(np.vdot(tensor,tensor).real-1)<2e-13,'full clock+128 output isometry')
    # Both projectors are legitimate but different: initial time slice
    # never receives a forward outcome; active time window can keep blank.
    initial_norm=float(np.vdot(tensor[0,0],tensor[0,0]).real)
    window_blank=float(np.vdot(tensor[:,0],tensor[:,0]).real)
    require(initial_norm==0 and window_blank>0,'same executed tape different declared active cut')
    require(abs(window_blank-np.vdot(B@psi,B@psi).real)<1e-13,'window return includes advanced blank, not reset clock')
    # Original Golden recombined high-CAR return. Its full Book penalty
    # remains positive; changing clock cut cannot silently negate it.
    J=np.zeros((16,16),complex)
    for bits in (6,10,12,14): J[bits+1,bits]=1;J[bits,bits+1]=-1
    alpha=.2
    H=P*np.eye(16)+P**2*expm(alpha*J)
    DH=D@H
    recombined=feedback(DH)[0]-jd
    require(recombined>0,'recombined Golden return has genuine full-complement penalty')
    T=forward_clock_corner(5,delay)
    clock_difference=feedback(np.kron(T,DH))[0]-feedback(np.kron(T,D))[0]
    require(abs(clock_difference-3*recombined)<3e-13,'same clock relative source/value, boundary cancels but remains paid')
    # A zero Fourier mode carries K00=I in the native original execution.
    # Irrespective of data, window boundary alone is NOT field curvature.
    I=np.eye(16,dtype=complex)
    jzero,_=feedback(np.kron(T,I))
    require(abs(jzero+OLD_RIGHT*delay*16*np.log1p(-Z))<3e-13,'clock-only boundary is field-independent on zero-mode data')
    return {'full128_completeness_error':completeness,
            'retained_two_round_outcomes':int(q2.size),
            'full_two_round_reporting_cost':direct_cost,
            'paid_effect_clock_agreement_error':abs(direct_cost-effect_cost),
            'allblank_probability':float(q2[0,0]),
            'data_feedback':jd,'data_feedback_field_source':sd,
            'source_finite_difference_error':abs(fd-sd),
            'clock_cases':rows,
            'unresolved_status_corner_source':stopped_status_source,
            'one_round_initial_slice_return':initial_norm,
            'one_round_window_blank_return':window_blank,
            'native_golden_recombined_feedback_difference':recombined,
            'clock_times_recombined_difference_error':abs(clock_difference-3*recombined)}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result={'status':'PASS_EXECUTION_CLOCK_BOOK_SOURCE_COMPOSITION',
            'input_ref':INPUT_REF,'exact':exact_clock_checks(),
            'native':numerical_native_checks(),
            'scope':{'new_physical_action':False,'new_detector':False,
                     'same_native_full128_Kraus':True,
                     'clock_model':'FORWARD_OPEN_COUNTER_WITH_SUPPLIED_ACTIVE_WINDOW',
                     'clock_checked':'ORIGINAL_0_10_REPORTING_TICKS',
                     'all_other_primitive_durations_derived':False,
                     'compulsory_active_cut_selected':False,
                     'full_Book_Info_work_selected':False,
                     'Einstein_source_identity_proved':False,
                     'GR_closed':False}}
    text=json.dumps(result,indent=2,ensure_ascii=False)
    print(text)
    if args.json: args.json.write_text(text+'\n',encoding='utf-8')

if __name__=='__main__':main()
