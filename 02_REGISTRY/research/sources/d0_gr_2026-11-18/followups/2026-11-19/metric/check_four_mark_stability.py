"""Four positive normalized marks bound scalar pressure slopes on a fixed axis.

All checks, interpolation coefficients, node readouts, and conservative
continuum bounds use exact rational arithmetic. Python standard library only.
"""
from fractions import Fraction as Q
from math import prod
import json


def check(value, message):
    if not value:
        raise ArithmeticError(message)


def multiply(left, right):
    output = [Q(0)]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i+j] += a*b
    return output


def roots_poly(roots):
    result = [Q(1)]
    for root in roots:
        result = multiply(result, [-root, Q(1)])
    return result


def evaluate(polynomial, x):
    result = Q(0)
    for value in reversed(polynomial):
        result = result*x+value
    return result


def interpolation(nodes):
    check(len(nodes)==len(set(nodes))==4 and all(x>0 for x in nodes),
          "four distinct positive points required")
    common = roots_poly(nodes)
    basis = []
    for i,x in enumerate(nodes):
        others = [y for j,y in enumerate(nodes) if j!=i]
        row = roots_poly(others)
        divisor = evaluate(row,x)
        basis.append([value/divisor for value in row]+[Q(0)])
    for i,row in enumerate(basis):
        check(all(evaluate(row,x)==int(i==j) for j,x in enumerate(nodes)),
              "Lagrange basis")
    check(common[0]==prod(nodes)>0, "positive constant in node polynomial")
    weight_at_zero = [abs(row[0])/common[0] for row in basis]
    # Each column bounds the contribution of one sample residual to coefficient k.
    coefficients = [[abs(row[k])+abs(common[k])*weight_at_zero[i]
                     for i,row in enumerate(basis)] for k in range(5)]
    return common,basis,weight_at_zero,coefficients


def q_of(x):
    return x*x/(1+x*x)


def endpoint_factor(x):
    # |1-2q|/(2 sqrt(q(1-q))) on x>0. It is monotone on either side of x=1.
    return abs(1-x*x)/(2*x)


def decimal_interval(value, digits=14):
    scale=10**digits
    def fmt(k):
        whole,rest=divmod(abs(k),scale)
        return ("-" if k<0 else "")+str(whole)+"."+str(rest).zfill(digits)
    return [fmt((value*scale)//1),fmt(-((-value*scale)//1))]


def response(matrix, x):
    # Unit input sector vectors e0,e1, mutually orthogonal binary output projectors.
    y0=matrix[0][0]+x*matrix[0][1]
    y1=matrix[1][0]+x*matrix[1][1]
    mass=y0*y0+y1*y1
    check(mass>0,"positive mass at this mark")
    z=mass/(1+x*x)
    m=y1*y1/mass
    r=y1*y1-x*x*y0*y0
    check(r==(1+x*x)**2*z*(m-q_of(x)), "normalized mark identity")
    return z,m,r


def coefficient_data(matrix):
    a,b=matrix[0]
    c,d=matrix[1]
    n0,n1=a*a+c*c,b*b+d*d
    cross=a*b+c*d
    r=[c*c,2*c*d,d*d-a*a,-2*a*b,-b*b]
    check(r[0]>=0>=r[4],"endpoint signs")
    check(n1-n0==r[2]-r[4]-r[0] and 2*cross==r[1]-r[3],
          "coefficient identity for the full derivative")
    return n0,n1,cross,r


def full_test(nodes,matrix):
    common,basis,zero_weights,coef=interpolation(nodes)
    B=list(map(sum,coef))
    width=q_of(max(nodes))-q_of(min(nodes))
    beta=max(endpoint_factor(min(nodes)),endpoint_factor(max(nodes)))
    method=lambda v: v[2]+v[4]+v[0]+beta*(v[1]+v[3])
    L=(1+max(nodes)**2)**2*method(B)
    n0,n1,cross,r=coefficient_data(matrix)
    samples=[response(matrix,x) for x in nodes]
    all_r=[s[2] for s in samples]
    cubic=[sum(row[k]*ri for row,ri in zip(basis,all_r)) for k in range(5)]
    check(all(r[k]==cubic[k]+r[4]*common[k] for k in range(5)),
          "four nodes reconstruct the residual up to signed leading coefficient")
    check(cubic[0]>=0 and abs(r[4])<=sum(c*abs(y) for c,y in zip(zero_weights,all_r)),
          "opposite signs control the missing degree of freedom")
    refined=[sum(c*abs(y) for c,y in zip(row,all_r)) for row in coef]
    check(all(abs(x)<=t<=b*max(map(abs,all_r)) for x,t,b in zip(r,refined,B)),
          "all coefficient bounds")
    zmax=max(z for z,_,_ in samples)
    delta=max(abs(m-q_of(x)) for x,(_,m,_) in zip(nodes,samples))
    raw_bound=L*delta*zmax
    # Exact proof for ALL x in the node hull, independently of interior grid diagnostics:
    # Z'_q = n1-n0 + cross*(1-x^2)/x and endpoint_factor bounds the variable term.
    concrete_uniform=abs(n1-n0)+2*abs(cross)*beta
    check(concrete_uniform<=method(refined)<=raw_bound, "uniform derivative inequality")
    loss=width*L*delta
    check(loss<1,"positive integrated lower mass")
    lower=zmax*(1-loss)
    log_bound=L*delta/(1-loss)
    refined_abs=method(refined)
    refined_ratio=refined_abs/(zmax-width*refined_abs)
    check(refined_ratio<=log_bound and concrete_uniform/lower<=log_bound,
          "scale-free uniform log-derivative bound")
    for j in range(65):
        x=min(nodes)+(max(nodes)-min(nodes))*Q(j,64)
        z,_,observed=response(matrix,x)
        check(evaluate(r,x)==observed,"direct residual polynomial")
        derivative=n1-n0+cross*(1-x*x)/x
        # Independent differentiation with respect to the rational axis parameter x.
        numerator=n0+2*cross*x+n1*x*x
        dnumerator=2*cross+2*n1*x
        dzdq=(dnumerator*(1+x*x)-2*x*numerator)/(2*x)
        check(dzdq==derivative and abs(dzdq/z)<=log_bound and z>=lower,
              "normalized input and exact interior sample")
    return dict(B=B,L=L,width=width,beta=beta,delta=delta,loss=loss,
                log_bound=log_bound,refined_ratio=refined_ratio,samples=samples,
                crude_raw=raw_bound,concrete_uniform=concrete_uniform,zmax=zmax)


def phase_control():
    x, eps = Q(5,6), Q(1,1000)
    q = q_of(x)
    check(1-eps**2>0, "Hermitian filter has positive determinant and leading minor")
    # Real/imaginary pairs for A(1,x exp(i phase)) and its derivative at phase zero.
    values = ((1,eps*x),(x,-eps))
    slopes = ((-eps*x,0),(0,x))
    masses = [re*re+im*im for re,im in values]
    z = sum(masses)/(1+x*x)
    mark = masses[1]/sum(masses)
    dz = 2*sum(re*dre+im*dim for (re,im),(dre,dim) in zip(values,slopes))/(1+x*x)
    sqrt_v = x/(1+x*x)
    check(z==1+eps**2 and sqrt_v**2==q*(1-q), "real-axis phase fixture")
    check(abs(mark-q)==eps**2*abs(1-2*q)/(1+eps**2), "quadratic real mark error")
    check(abs(dz)==4*eps*sqrt_v, "linear mass response to phase")
    return dict(x=str(x),epsilon=str(eps),absolute_mark_error=str(abs(mark-q)),
                real_axis_mass=str(z),absolute_phase_mass_derivative=str(abs(dz)))


def main():
    nodes=[Q(4,5),Q(5,6),Q(7,8),Q(9,10)]
    qlow,qhigh=q_of(nodes[0]),q_of(nodes[-1])
    # p^2=(3-sqrt(5))/2; certify these q are all inside the noisy collar.
    check(3-2*qlow>0 and (3-2*qlow)**2<5 and qhigh<Q(1,2),"literal noisy collar")
    eps=Q(1,10**10)
    matrix=[[1+2*eps,3*eps],[3*eps,1-eps]]
    check(matrix[0][0]>0 and matrix[0][0]*matrix[1][1]-matrix[0][1]**2>0,
          "strictly positive rational symmetric filter")
    result=full_test(nodes,matrix)
    scaled=full_test(nodes,[[7*y for y in row] for row in matrix])
    check(all(result[k]==scaled[k] for k in ("L","delta","loss","log_bound","refined_ratio"))
          and scaled["zmax"]==49*result["zmax"],"unobserved constant amplitude scale cancels")
    neutral=full_test(nodes,[[Q(5),Q(0)],[Q(0),Q(5)]])
    check(neutral["delta"]==neutral["log_bound"]==0 and neutral["zmax"]==25,
          "four exactly preserved marks certify a flat log partition along the fixed axis")
    rows=[]
    for x,(z,m,_) in zip(nodes,result["samples"]):
        rows.append(dict(x=str(x),parsed_q=str(q_of(x)),normalized_mark=str(m),
                         mass_for_verification_only=str(z)))
    output=dict(status="PASS",arithmetic="exact rational",
                fixture="A=I+10^(-10)[[2,3],[3,-1]] on a fixed orthonormal two-sector axis",
                nodes=rows,interval_q=list(map(str,[qlow,qhigh])),
                width=str(result["width"]),beta=str(result["beta"]),
                coefficient_bounds=list(map(str,result["B"])),
                L=str(result["L"]),max_normalized_mark_error=str(result["delta"]),
                width_L_delta=str(result["loss"]),
                scale_free_uniform_log_slope_bound=str(result["log_bound"]),
                uniform_log_slope_bound_decimal=decimal_interval(result["log_bound"]),
                improved_bound_with_relative_masses_decimal=decimal_interval(result["refined_ratio"]),
                direct_uniform_raw_slope_upper=str(result["concrete_uniform"]),
                interior_points_checked_per_matrix=65,complete_interval_proof=True,
                complex_phase_control=phase_control(),
                unknown_constant_scale_cancelled=True,unchanged_normalized_marks_case="zero slope",
                scope="The axis, filter, and binary terminal are frozen. A moving scale adds its own log derivative.",
                physical_weighted_marks_supplied=False,GR_closed=False)
    print(json.dumps(output,indent=2))


if __name__=="__main__":
    main()
