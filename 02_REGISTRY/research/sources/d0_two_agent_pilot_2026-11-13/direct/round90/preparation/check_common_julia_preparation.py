"""One common approximate full Julia, exactly protected rational coordinates and paid odd source."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
import math

import mpmath as mp
import numpy as np


mp.mp.dps = 65
ORDER = (0, 2, 3, 1)
D = 65536
ROOT_D = 256
SCALE = 256
ADDRESS_DIM = 32*D
P = (mp.sqrt(5)-1)/2
ELL = -mp.log(P)
THETA = mp.asin(P)
INT_GRID = 25*(1 << 16)


def check(condition, description):
    if not condition:
        raise ValueError(description)


def rat(x):
    return mp.mpf(x.numerator)/x.denominator


def zeros(n):
    return np.full((n, n), F(0), dtype=object)


def identity(n):
    return np.array([[F(int(i == j)) for j in range(n)] for i in range(n)], dtype=object)


def determinant(matrix):
    n = len(matrix)
    if n == 0:
        return F(1)
    return sum((-1)**k * matrix[0, k]*determinant(np.delete(matrix[1:], k, axis=1))
               for k in range(n) if matrix[0, k])


def creator(axis):
    out = zeros(16)
    for s in range(16):
        if not s & (1 << axis):
            prior = sum((s >> j) & 1 for j in ORDER[:ORDER.index(axis)])
            out[s | (1 << axis), s] = F((-1)**prior*(1 if axis in (0, 1) else -1), 2)
    return out


def link(kx, ky):
    n = zeros(4)
    for a, val in [(2, kx), (3, ky)]:
        n[1, a] = n[a, 0] = val
    u = identity(4) + n + (n @ n)*F(1, 2)
    grades = [[j for j in ORDER if mask & (1 << j)] for mask in range(16)]
    exterior = zeros(16)
    for i, row in enumerate(grades):
        for j, col in enumerate(grades):
            if len(row) == len(col):
                exterior[i, j] = F(determinant(u[np.ix_(row, col)]), 2)
    check(exterior[0, 0] == F(1, 2) and exterior[4, 1] == kx/2 and
          exterior[8, 1] == ky/2, "actual vacuum and two one-particle link entries")
    return exterior


def inward_root(block, integer_grid):
    """Floating eigensolver proposes B. Integer residual and positivity certify its interval."""
    den = math.lcm(*(x.denominator for x in block.ravel()))
    raw = np.array([[int(v*den) for v in row] for row in block], dtype=object)
    eye = np.eye(16, dtype=int).astype(object)
    num = den**2*eye - raw @ raw.T
    check(min(num[i,i]-sum(abs(z) for j,z in enumerate(num[i]) if j != i)
              for i in range(16)) > 0, "verified positive radicand")
    ev, vec = np.linalg.eigh(np.asarray(num, dtype=float)/den**2)
    approx = np.einsum("ij,j,kj->ik", vec, np.sqrt(ev), vec)
    scale = 1 << 34
    B = np.rint(scale*(approx+approx.T)/2).astype(np.int64).astype(object)
    check(min(B[i,i]-sum(abs(z) for j,z in enumerate(B[i]) if j != i)
              for i in range(16)) > scale//2, "verified positive root candidate")
    residual = num*scale**2 - (B @ B)*den**2
    error = 2*F(max(sum(abs(z) for z in row) for row in residual), den**2*scale**2)
    check(error < F(1,10**8), "integer Sylvester enclosure")
    def digit(x):
        lower = max(0, F(abs(x), scale)-error)*F(integer_grid, ROOT_D)
        return (1 if x >= 0 else -1)*int(lower)
    return np.array([[digit(x) for x in row] for row in B], dtype=np.int64)


def julia_digits(block, integer_grid):
    upper = np.array([[int(x*integer_grid/ROOT_D) for x in row] for row in block], dtype=np.int64)
    return np.block([[upper, inward_root(block, integer_grid)],
                     [inward_root(block.T, integer_grid), -upper.T]])


def four_squares(value):
    scale = 1
    n = value
    if n == 0:
        return [0]*4
    while not n % 4:
        n //= 4
        scale *= 2
    for a in range(math.isqrt(n), -1, -1):
        rem = n-a*a
        test = rem
        while test and test % 4 == 0:
            test //= 4
        if test % 8 == 7:
            continue
        for b in range(math.isqrt(rem), -1, -1):
            rest = rem-b*b
            for c in range(math.isqrt(rest), -1, -1):
                d = math.isqrt(rest-c*c)
                if c*c+d*d == rest:
                    return [scale*x for x in (a,b,c,d)]
    raise ValueError("missing four square decomposition")


def fields(den):
    return [[(F(a,den), F(b,den)) for a,b in stencil] for stencil in
            (((8,-9), (6,1), (-5,-11)), ((9,2), (10,-3), (4,4)))]


def profile(t, x, y, den):
    if t not in (1,2) or x == 0 or y == 0:
        return F(0), F(0)
    center, east, north = fields(den)[t-1]
    return (center[0]+(x-1)*(east[0]-center[0]),
            center[1]+(y-1)*(north[1]-center[1]))


def certify_full_input():
    # All 256 sites and all eight source roles, including true full compact-link Julia defects.
    grid = INT_GRID
    role_counts = Counter()
    for t, _, x, y in product(range(4), repeat=4):
        role_counts.update([("c", axis) for axis in (1, 0, 2, 3)])
        role_counts.update([("l", F(0), F(0))]*3 + [("l", *profile(t,x,y,100))])
    check(sum(role_counts.values()) == D//32, "full role multiplicities")
    dark_slots = 0
    digit2 = 0
    maximum = 0
    for role, count in role_counts.items():
        block = creator(role[1]) if role[0] == "c" else link(*role[1:])
        data = julia_digits(block, grid)
        if role in (("c",2), ("c",3)):
            check(F(int(data[1 << role[1],0]),grid)==F(-1,512), "negative spatial coframe metric leg")
            expected_zero = np.block([[block == 0, ~np.eye(16, dtype=bool)],
                                      [~np.eye(16, dtype=bool), block.T == 0]])
            check(np.all(data[expected_zero] == 0), "unused original slots are exactly dark")
            dark_slots += count*int(expected_zero.sum())
        if role == ("c",0):
            check(F(int(data[1,0]), grid)==F(1,512), "exact donor")
        elif role == ("c",1):
            check(data[1,0] == 0 and F(int(data[2, 0]), grid)==F(1,512), "true dark role and anchor")
            # Its ideal lower vacuum in this convention is sqrt(3)/2.
            check((identity(16)-block.T @ block)[0,0] == F(3,4), "irrational Julia slot")
        elif role[0] == "l":
            for i,j in ((0,0),(4,1),(8,1)):
                check(F(int(data[i,j]),grid)==block[i,j]/ROOT_D, "exact protected link")
        digit2 += count*sum(int(z)**2 for z in data.ravel())
        maximum = max(maximum, max(map(abs, map(int, data.ravel()))))
    deficit = grid**2 - digit2
    check(0 < deficit < grid**2, "protected rounding has a physical deficit")
    squares = four_squares(deficit)
    check(sum(z*z for z in squares) + digit2 == grid**2, "exact common norm with tagged service slots")
    ticket = 1 << (grid-1).bit_length()
    check(max(SCALE*maximum, max(squares))<=ticket, "physical ticket threshold")
    gate = F(SCALE**2*grid**2, ADDRESS_DIM*ticket**2)
    check(gate==F(625,32768), "absolute successful threshold mass")
    check(dark_slots >= 4*SCALE**2, "all four square groups fit the original Hilbert space")
    for raw in (SCALE*maximum,-SCALE*maximum,*squares):
        check(F(2*ticket-2*(ticket-raw),2*ticket)==F(raw,ticket), "signed real ticket")
    return {"denominator":grid,"distinct_Julia_blocks":len(role_counts),
            "address_count_physical":32*D,"work_zero_mass_given_other_resources":str(gate),
            "squared_padding_norm":str(F(deficit,grid**2)),"available_untouched_dark_slots":dark_slots,"four_square_witness":squares}


def h(q):
    return -(q*mp.log(q)+(1-q)*mp.log1p(-q))/ELL


def rows_and_price(den, step):
    eta = P**3*mp.mpf(5)/256
    b = 2*P**3*(1-mp.mpf(5)/16)
    logg = 2*P**3*mp.mpf('.5')/D * mp.mpf(5497642024880)/2**51
    lam = -(1099527356400+824647876594*P)/68720525311
    e0 = 2*(4*P*mp.sin(448*THETA))**2
    cs = []
    for t in (1,2):
        terms = [16*(profile(t,x,y,den)[0]-profile(t,x+1,y,den)[0]+
                     profile(t,x,y,den)[1]-profile(t,x,y+1,den)[1])
                 for _,x,y in product((1,2),repeat=3)]
        check(len(set(terms))==1,"joint neighboring links on the same 4-torus")
        cs.append(rat(sum(terms)/8))
    rows = [c-2*lam*e for c,e in zip(cs,(e0,2*e0))]
    for mask in [(1,0),(0,1),(1,1)]:
        odd = 0
        for j, (r, energy) in enumerate(zip(cs,(e0,2*e0))):
            pm = b+eta*energy
            for m, prob in ((0,1-pm),(1,pm)):
                s = logg*mask[j]*(r-2*lam*(m-b)/eta)
                q = mp.mpf('.5')+step*s
                qm = mp.mpf('.5')-step*s
                check(abs(q+qm-1)<mp.mpf('1e-55') and 0<q<1 and 0<qm<1,"paid mirror on each terminal")
                odd += prob*((1+q-h(q))-(1+qm-h(qm)))/2
        check(abs(odd/(step*logg) - sum(i*z for i,z in zip(mask,rows)))<mp.mpf('1e-49'),
              "individual or summed full registered source")
    return {"R":[mp.nstr(z,11) for z in cs],"recovered_rows":[mp.nstr(z,12) for z in rows],
            "sum":mp.nstr(sum(rows),12)}


def reflector(v, x):
    v2=sum(a*a for a in v)
    check(v2 > 0, "zero rational reflection")
    coef=2*sum(a*b for a,b in zip(v,x))/v2
    return [b-coef*a for a,b in zip(v,x)]


def rational_column(target, fixed, support, precision):
    free=[i for i in support if i not in fixed]
    radius2=1-sum(z*z for z in fixed.values())
    four=four_squares(radius2.numerator*radius2.denominator)
    base=[F(a,radius2.denominator) for a in four]+[F(0)]*(len(free)-4)
    check(sum(z*z for z in base)==radius2,"rational sphere is populated")
    actual=np.array([target[i] for i in free])
    start=np.array(list(map(float,base)))
    sign=1 if np.linalg.norm(start-actual) >= np.linalg.norm(start+actual) else -1
    direction=[F(round(precision*v),precision) for v in start-sign*actual]
    got=[sign*z for z in reflector(direction,base)]
    full=[F(0)]*32
    for i,z in zip(free,got):
        full[i]=z
    for i,z in fixed.items():
        full[i]=z
    check(sum(z*z for z in full)==1,"exact new column")
    return full


def orthogonal_witness():
    # A nonzero real null connection with both protected one-particle cells.
    original=link(F(8,100),F(-9,100))
    C=np.array(original,dtype=float)
    def sqrt_matrix(block):
        eig,vec=np.linalg.eigh(block)
        return np.einsum("ij,j,kj->ik",vec,np.sqrt(eig),vec)
    J=np.block([[C,sqrt_matrix(np.eye(16)-np.einsum("ij,kj->ik",C,C))],
                [sqrt_matrix(np.eye(16)-np.einsum("ji,jk->ik",C,C)),-C.T]])
    precision=1<<19
    columns=[rational_column(J[:,0],{0:F(1,2)},[0,16,3,5,6,7],precision),
             rational_column(J[:,1],{4:F(8,200),8:F(-9,200)},
                             [1,2,4,8,17,18,20,24,9,10,11,12],precision)]
    check(sum(a*b for a,b in zip(*columns))==0,"two rational columns orthogonal")
    # QR produces candidate normals; the rounded factors are exactly orthogonal over Q.
    reduced=J.copy()
    normals=[]
    for i in range(31):
        v=reduced[i:,i].copy()
        v[0]+=np.copysign(np.linalg.norm(v),v[0])
        v/=np.linalg.norm(v)
        reduced[i:]-=2*np.outer(v,np.einsum("i,ij->j",v,reduced[i:]))
        normals.append([F(0)]*i+[F(round(precision*z),precision) for z in v])
    signs=[int(np.sign(reduced[i,i])) for i in range(32)]
    def apply_previous(j, corrections):
        col=[F(signs[j]*int(i==j)) for i in range(32)]
        for normal in list(reversed(normals))+corrections:
            col=reflector(normal,col)
        return col
    corrections=[]
    for j,desired in enumerate(columns):
        old=apply_previous(j,corrections)
        check(sum(z*z for z in old)==1,"exact rational current column")
        ns=[old,[a+b for a,b in zip(old,desired)]]
        check(reflector(ns[1],reflector(ns[0],old))==desired,"exact corrected protected column")
        if j:
            check(all(sum(a*b for a,b in zip(v,columns[0]))==0 for v in ns),
                  "correction preserves first column exactly")
        corrections.extend(ns)
    R=np.diag(signs).astype(float)
    for coords in list(reversed(normals))+corrections:
        v=np.array([float(z) for z in coords])
        R-=2*np.outer(v,np.einsum("i,ij->j",v,R))/np.dot(v,v)
    err=np.linalg.norm(R-J,ord="fro")
    check(0 < err < .001 and np.max(abs(np.einsum("ji,jk->ik",R,R)-np.eye(32)))<1e-11,
          "full approximate link and reference Gram")
    return {"tested_block_dimension":32,"exactly_corrected_columns":2,"rational_reflections":len(normals)+4,
            "full_link_Frobenius_error_numerical":round(float(err),10),
            "preparation_work_zero_bound":"(1/128,1/32]"}


def former_port():
    """Full Walsh transcripts on a 32-dimensional old input for two signed rational roles."""
    n, C, T = 32, 5, 8
    M=np.zeros((2,n,n),dtype=np.int32)
    for j in range(0,n,2):
        M[0,j:j+2,j:j+2]=[[3,-4],[4,3]]
        M[1,j:j+2,j:j+2]=[[4,3],[3,-4]]
    check(np.array_equal(np.einsum("aji,ajk->aik",M,M),np.tile(C*C*np.eye(n,dtype=int),(2,1,1))),
          "each rational role has complete orthogonal columns")
    def walsh(N):
        return np.array([[(-1)**(bin(k & i).count("1")) for i in range(N)] for k in range(N)])
    mask=np.where(np.arange(2*T)<T-M[...,None],-1,1)
    raw=np.einsum("sa,rija->srij",walsh(2*T),mask)
    check(np.array_equal(raw[0],2*M),"all 2048 signed threshold amplitudes")
    # Physical Hermitian Gram of the first work-zero step while old input i is still present.
    check(np.all(np.sum(raw[0]**2,axis=1)==4*C*C),"first selected coarse effect on every old input")
    old=np.arange(2*n*3,dtype=float).reshape(2,n,3)
    old=np.sin(old+.35)
    old/=np.linalg.norm(old)
    full=0.
    selected=None
    for u in range(2*T):
        for v,phase in enumerate(walsh(n)):
            out=np.einsum("aji,i,air->ajr",raw[u],phase,old)/(2*T*n)
            full+=np.linalg.norm(out)**2
            if u==0:
                check(abs(np.linalg.norm(out)**2-float(F(C,n*T)**2))<1e-15,"all old-input labels")
                if v==0:
                    selected=out
    target=np.einsum("aji,air->ajr",M,old)/C
    check(np.linalg.norm(selected*n*T/C-target)<1e-14 and abs(full-1)<2e-13,
          "returned port on entangled input and all recorded failures")
    return {"dimension_per_role":n,"roles_in_complete_check":2,"external_dimension":3,
            "all_outcome_pairs_checked":2*T*n,"success_probability":str(F(C,n*T)**2),
            "general_work_and_old_input_zero_probability":"(1/4096,1/1024]"}


def generic_errors():
    # Explicit common imperfect pure input; compare both entropy and endpoint shifts.
    ep = .00037
    true = np.array([0., .6, .8])
    perturbed = true*math.cos(ep)+np.array([1.,0.,0.])*math.sin(ep)
    eps = abs(math.sin(ep))
    beta = float(2*P**3)
    out = []
    for d in (1/128,1/1024,1/8192):
        def probabilities(x):
            angle = math.asin(d*32)
            f,e,y = x
            return [0.5+2*beta*(f*math.cos(angle)+s*e*math.sin(angle))*y for s in (-1,1)]
        trueq, appq = probabilities(true), probabilities(perturbed)
        slope = (trueq[1]-trueq[0])/(2*d)
        actual = float(((appq[1]-h(appq[1]))-(appq[0]-h(appq[0])))/(2*d))
        qmin = min(trueq+appq+[1-z for z in trueq+appq])
        bound = 2*32*beta*eps+2*beta*eps*(abs(slope)+2*32*beta*eps)/(float(ELL)*qmin*(1-qmin))
        check(abs(actual-slope) < bound,"common preparation's entropy secant")
        out.append([round(d,8),round(abs(actual-slope),10),round(bound,10)])
    return out


def main():
    n=1
    while True:
        sine = mp.sin((1<<20)*n*THETA)
        if 0 < sine < mp.mpf('.03') and mp.cos((1<<20)*n*THETA) > mp.mpf('.99'):
            break
        n += 1
    d=sine/32
    print(json.dumps({"canonical_geometric_Choi_obtainable_exactly_from_canonical_raw":False,
                      "native_positive_step":{"pattern_controls":20,"coefficient":n,"d":mp.nstr(d,12)},
                      "full_rational_table_preparation":certify_full_input(),
                      "rolewise_orthogonal_witness":orthogonal_witness(),
                      "actual_old_port":former_port(),
                      "original_decimal_stencils":rows_and_price(100,d),
                      "dyadic_stencils":rows_and_price(128,d),
                      "generic_common_preparation_actual_and_bound":generic_errors(),
                      "compulsory_Book03_price_identified":False},sort_keys=True,indent=2))


if __name__=="__main__":
    main()
