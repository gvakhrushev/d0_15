"""Independent-report curvature and finite-menu controls; standard library.

A fixed table C is priced on the retained binary report labels. Additional
quantum reference or old-state prices belong to this theorem only when their
conditional expected fee, given the labels, is such a fixed table.
"""
from fractions import Fraction as F
from itertools import product, permutations
from pathlib import Path
import hashlib
import json
import runpy


PREV = Path(__file__).with_name("check_extra_work.py")
assertion = hashlib.sha256(PREV.read_bytes()).hexdigest()
if assertion != "93d93b4923062bc2aa831afbcfda84b0c2cbab1baeeca49b43538ac5090acc45":
    raise ValueError("unexpected rational arithmetic owner")
owner = runpy.run_path(str(PREV))
span, centre = owner["span"], owner["centre"]


def require(ok, why):
    if not ok:
        raise ArithmeticError(why)


def lng(x):
    if x.lo>1:
        return x.log_positive()
    if x.hi<1:
        return -(1/x).log_positive()
    if x.lo==x.hi==1:
        return span(0)
    raise ValueError("unexpected interval straddling 1")


def base(q,ell):
    return 1+q+(q*lng(q)+(1-q)*lng(1-q))/ell


def slope(q,ell):
    return 1+lng(q/(1-q))/ell


def information_curvature(q,ell):
    return 1/(ell*q*(1-q))


def kl(a,b):
    return a*lng(a/b)+(1-a)*lng((1-a)/(1-b))


def intersects(a,b):
    return a.lo<=b.hi and b.lo<=a.hi


def mean_fee(ps,tab):
    val=F(0)
    for bits,c in tab.items():
        weight=F(1)
        for b,p in zip(bits,ps):
            weight*=p if b else 1-p
        val+=c*weight
    return val


def replace(ps,j,q):
    return ps[:j]+(q,)+ps[j+1:]


def axis_tariff(ps,tab,j):
    return mean_fee(replace(ps,j,F(1)),tab)-mean_fee(replace(ps,j,F(0)),tab)


def compare_rationals():
    m=4
    bits=list(product(range(2),repeat=m))
    ps=(F(41,100),F(2,5),F(7,16),F(3,7))
    tab={b:F(15+5*b[0]-7*b[1]+11*b[2]-8*b[3]+17*b[0]*b[1]
               -19*b[1]*b[2]*b[3]+23*b[0]*b[1]*b[2]*b[3],13) for b in bits}
    l,r,h=F(41,100),F(83,200),F(1,900)
    mid=(l+r)/2
    for j in range(m):
        d=axis_tariff(ps,tab,j)
        fee=lambda q:mean_fee(replace(ps,j,q),tab)
        require(fee(r)-fee(l)==(r-l)*d,"exact arbitrary-table secant")
        require(fee(mid+h)+fee(mid-h)-2*fee(mid)==0,"tariff cancellation")
        for b in bits:
            delta={v:F(int(v==b)) for v in bits}
            v=lambda q:mean_fee(replace(ps,j,q),delta)
            require(v(r)-v(l)==(r-l)*axis_tariff(ps,delta,j),"complete atom basis")
        for k in range(m):
            if k==j:continue
            x=replace(ps,k,r); y=replace(ps,k,l)
            require(axis_tariff(x,tab,j)-axis_tariff(y,tab,j)
                    ==(r-l)*(axis_tariff(replace(ps,k,F(1)),tab,j)
                              -axis_tariff(replace(ps,k,F(0)),tab,j)),"mixed coefficient")
    for order in permutations(range(m)):
        permuted={tuple(b[i] for i in order):c for b,c in tab.items()}
        require(mean_fee(tuple(ps[i] for i in order),permuted)==mean_fee(ps,tab),"relabeling")
    return {"report_count":m,"complete_archive_atoms":len(bits),
            "permutations_checked":24,"exact_affine_secant_and_mixed_identity":True}


def native_target_collar(qstar):
    # §7ef equations SC1-SC7, not an arbitrary continuous G-angle.
    p=(span(5).sqrt()-1)/2
    co,si=p.sqrt(),p
    for _ in range(9):
        co,si=co*co-si*si,2*co*si
    kappa=si*si; z=F(1,2**20)
    ready=2*10946*p**23  # F_21=10946
    def report(x,y):
        e=p**2*(1+x)
        lum=4*e*(1-e)
        u=p+p**2*y
        b=4*u*u*(1-u*u)
        a=lum+(1-lum)*b
        return z*(a+b)-z*z*a*b
    v=4*p**2*(1-p**2)
    a0=v+(1-v)*v
    lum_x=4*p**2*(1-2*p**2)
    b_y=8*p**3*(1-2*p**2)
    rx=z*(1-z*v)*lum_x*(1-v)
    ry=z*(1-z*v)*(1-v)*b_y+z*(1-z*a0)*b_y
    k0=ry/rx
    require(F("23.4164")<k0.lo<k0.hi<F("23.4165"),"real SC1 calibration")
    eps=F(1,64); delta=eps/(2*k0)
    ydiff=report(0,delta)-report(0,-delta)
    r0=report(0,0)
    def endpoint(f):
        # SC4 material coordinate q_m=0, so the second SC7 cross term vanishes.
        return p**2+kappa*p**10*(4+ready**2*ydiff*(report(eps*f,0)-r0))
    lower,upper=endpoint(F(-1,8)),endpoint(F(1,8))
    radius=F(9,10**24)
    require(lower.hi<qstar.lo-radius and qstar.hi+radius<upper.lo,
            "actual canonical seven-call target contains tiny symmetric interval")
    require(intersects(endpoint(F(0)),qstar),"SC7 centre")
    return {"target_input":"SC1-SC7, eps=1/64, delta=eps/(2*k0), matter observable zero, f in [-1/8,1/8]",
            "certified_radius_about_literal_q_star":"9e-24",
            "left_gap_qstar_minus_q_minus":(qstar-lower).fmt(28),
            "right_gap_q_plus_minus_qstar":(upper-qstar).fmt(28),
            "local_anchor_free_floor_for_two_target_slopes":(span(4)*radius/centre()[1]).fmt(29),
            "source":"PR 334 0716b659d, primary lines 113422-113516 and 151345-151359",
            "admission":"The common-clock SC5 compiler approximates each finite list of these continuous canonical preparation targets to arbitrary tolerance on every column. No exact continuum of finite words, specific compiled word for the rational endpoints, or geometric right lift for arbitrary input f is asserted. The wider [.41,.415] is a coordinate illustration, not certified here as the same geometric chart."}


def envelopes(ell):
    l,r=F("0.410"),F("0.415")
    one,two=F("0.411"),F("0.414")
    lines=[(F(3),F(0)),(F(1),2*one),(F(-1),2*one+2*two)]
    cuts={l,r}
    for a,b in lines:
        for c,d in lines:
            if a!=c:
                cut=(d-b)/(a-c)
                if l<cut<r:cuts.add(cut)
    cuts=sorted(cuts)
    cells=[]
    for left,right in zip(cuts,cuts[1:]):
        mid=(left+right)/2
        i=min(range(len(lines)),key=lambda i:lines[i][0]*mid+lines[i][1])
        if cells and cells[-1][2]==i:cells[-1]=(cells[-1][0],right,i)
        else:cells.append((left,right,i))
    require([(a,b) for a,b,_ in cells]==[(l,one),(one,two),(two,r)],"three active affine cells")
    a,b,i=max(cells,key=lambda c:c[1]-c[0])
    L=b-a
    require(L>=(r-l)/len(lines),"long active segment")
    def val(t):
        return base(span(t),ell)+min(v*t+w for v,w in lines)
    m=(a+b)/2
    sep=(val(a)+val(b))/2-val(m)
    floor=span(L*L)/(2*ell)
    universal=span((r-l)**2)/(2*len(lines)**2*ell)
    require(sep.lo>floor.hi and floor.lo>=universal.hi,"oscillation/Jensen floor")
    gain=slope(span(b),ell)-slope(span(a),ell)
    require(gain.lo>(4*span(r-l)/(len(lines)*ell)).hi,"one-sided active slope difference")
    # Infinitely many supporting affine majorants of -P give exactly -P
    # on the whole interval. Their Jensen gap is KL(q||t)/ell.
    def tangent_price(q,t):
        return base(span(q),ell)-base(span(t),ell)-slope(span(t),ell)*(q-t)
    for q in (l,one,two,r):
        for t in (l,one,two,r):
            if q==t:
                require(intersects(tangent_price(q,t),span(0)),"touching")
            else:
                k=kl(span(q),span(t))/ell
                require(k.lo>0 and intersects(tangent_price(q,t),k),"relative entropy identity")
    # Sharpness: N tangent majorants of -P at uniform cell midpoints.
    # Every q is within L/(2N) of one midpoint, so its Bregman gap is at
    # most (sup P'') L^2/(8N^2), and the minimum is zero. On [1/2-L,1/2]
    # sup P'' / (4/ell) = 1/(1-4L^2), arbitrarily close to one.
    small=F(1,1000)
    sharp_ratio=1/(1-4*small*small)
    require(sharp_ratio==F(250000,249999),"asymptotic finite-menu sharpness")
    return {"sharpness_ratio_on_width_1_over_1000":str(sharp_ratio),"menu_size":len(lines),"cells":[[str(a),str(b),i] for a,b,i in cells],
            "universal_oscillation_lower_bound":universal.fmt(13),
            "actual_cell_midpoint_gap":sep.fmt(13),"widest_cell_derivative_gain":gain.fmt(12),
            "infinite_menu":"tangent majorants of -P; equality at t=q; a common fee offset allows nonnegative prices on a compact interval"}


def vertex_control(ell):
    boxes=[(F(".410"),F(".415")),(F(".402"),F(".419")),(F(".400"),F(".412"))]
    labels=list(product(range(2),repeat=3))
    tab={b:F(8+4*b[0]-5*b[1]+2*b[2]+b[0]*b[1]-2*b[1]*b[2]+3*b[0]*b[1]*b[2]) for b in labels}
    corners={b:tuple(boxes[i][x] for i,x in enumerate(b)) for b in labels}
    s={b:sum((base(span(q),ell) for q in ps),span(mean_fee(ps,tab))) for b,ps in corners.items()}
    winning=max(s,key=lambda b:s[b].lo)
    require(all(s[winning].lo>v.hi for b,v in s.items() if b!=winning),"strict maximum")
    require(winning==(1,0,1),"mixed outward orientations")
    ps=corners[winning]; checked=[]
    for i,(l,r) in enumerate(boxes):
        d=(2*winning[i]-1)*(slope(span(ps[i]),ell)+axis_tariff(ps,tab,i))
        floor=2*span(r-l)/ell
        require(d.lo>floor.hi,"simultaneous outward derivative")
        checked.append({"axis":i,"outward":d.fmt(10),"universal_floor":floor.fmt(10)})
    return {"row_count":3,"winning_endpoint_bits":list(winning),"derivatives":checked}


def main():
    q,ell=centre()
    l,r=span(F(".41")),span(F(".415"))
    qmid=(l+r)/2; step=(r-l)/2
    curvature=information_curvature(q,ell)
    delta=lng(r*(1-l)/(l*(1-r)))/ell
    strength=4/ell
    d1=slope(r,ell)-slope(l,ell)
    require(intersects(delta,d1) and delta.lo>(strength*(r-l)).hi,"logit slope separation")
    second=base(l,ell)+base(r,ell)-2*base(qmid,ell)
    breg=(kl(l,qmid)+kl(r,qmid))/ell
    require(intersects(second,breg) and second.lo>(strength*step*step).hi,"three-point identity")
    # Non-symmetric Jensen gap; the complete tariff drops out without centering.
    a=F(2,7); v=a*l+(1-a)*r
    gap=a*base(l,ell)+(1-a)*base(r,ell)-base(v,ell)
    require(intersects(gap,(a*kl(l,v)+(1-a)*kl(r,v))/ell),"arbitrary affine secant")
    d=1-2*q; bas=slope(q,ell); crit=bas/d
    require(intersects(bas-crit*d,span(0)) and 1<crit.lo<crit.hi<2,"fixed zero-slope tariff")
    # One restored report's overlap with another has d/dq_i = -(1-2q_j)
    # and zero second derivative in the very same q_i.
    match2=2*curvature+8
    mismatch2=2*curvature-8
    mismatch5=2*curvature-20
    require(match2.lo>0 and mismatch2.lo>0 and mismatch5.hi<0,"diagonal curvature signs")
    left_fee=slope(l,ell)/d
    right_fee=slope(r,ell)/d
    require(left_fee.hi<crit.lo and crit.hi<right_fee.lo,"two row sign-crossing thresholds")
    constant_tilt=-(slope(l,ell)+slope(r,ell))/2
    require(intersects(slope(l,ell)+constant_tilt,-delta/2) and
            intersects(slope(r,ell)+constant_tilt,delta/2),"sharp endpoint bound")
    known=compare_rationals()
    result={"status":"PASS","scope":"fixed conditional tariff on all binary labels of independently restored scalar-effect reports",
            "q_star":q.fmt(14),"arbitrary_tariff":known,
            "independent_axis":{"P_double_prime_at_q_star":curvature.fmt(),"uniform_floor_4_over_ell":strength.fmt(),
                                "centered_secant_interval":["0.41","0.415"],"complete_secant":second.fmt(14),
                                "universal_centered_secant_floor":(strength*step*step).fmt(14),
                                "exact_logit_slope_gain":delta.fmt(14),
                                "anchor_free_max_abs_slope_floor":(delta/2).fmt(14)},
            "restored_two_report_controls":{"fixed_match_fee_to_zero_one_or_two_equal_point_slopes":crit.fmt(),
                                "fixed_match_fee_2_diagonal_curvature":match2.fmt(),
                                "fixed_mismatch_fee_2_diagonal_curvature":mismatch2.fmt(),
                                "fixed_mismatch_fee_5_diagonal_curvature":mismatch5.fmt(),
                                "critical_mismatch_fee_for_diagonal_curvature":(curvature/2).fmt(),
                                "fixed_partner_qstar_sign_crossing_fee_interval":{"left":left_fee.fmt(),"right":right_fee.fmt()},
                                "match_slope_sign":"at fixed partner q* and fixed fee, the slope increases strictly in its own report probability; it crosses zero inside (l,r) iff the fee is strictly between the two thresholds"},
            "finite_menu":envelopes(ell),"one_table_rectangle":vertex_control(ell),
            "actual_canonical_preparation_collar":native_target_collar(q),
            "formula_scope":"coordinate q_i varies while other rows stay fixed; neither common physical field nor arbitrary continuous chart silently supplies these independent axes",
            "GR_closed":False}
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
