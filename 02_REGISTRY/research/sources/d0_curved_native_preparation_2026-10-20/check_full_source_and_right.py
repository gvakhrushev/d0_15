#!/usr/bin/env python3
"""Numerical control of the ORIGINAL full-CAR16 pp-wave R source.

No repository edits, physical admission, whole H/J replay or GR closure.
The code constructs original d and its positive adjoint, not a reconstructed
survival operator.  Fixed-RIGHT stationarity is distinguished from unrestricted
normalized-purification stationarity.
"""
import itertools
import json
import math
import numpy as np


CREATE = []
for j in range(4):
    c = np.zeros((16, 16))
    for mask in range(16):
        if not (mask >> j & 1):
            c[mask | 1 << j, mask] = (-1) ** ((mask & ((1 << j)-1)).bit_count())
    CREATE.append(c)
ANN = [c.T for c in CREATE]
E = np.eye(4)
N = E[:, 1]
ETA = np.array([[0,1,0,0], [1,0,0,0], [0,0,-1,0], [0,0,0,-1.]])
N2 = np.zeros((4,4)); N2[1,2] = N2[2,0] = 1
N3 = np.zeros((4,4)); N3[1,3] = N3[3,0] = 1
FOCK = np.eye(16)
QUARTET = [FOCK[:,0], FOCK[:,2], ANN[1] @ FOCK[:,15], FOCK[:,15]]


def gamma(x):
    return sum(x[i,j] * CREATE[i] @ ANN[j]
               for i in range(4) for j in range(4))


def cv(v):
    return sum(v[i] * CREATE[i] for i in range(4))


def exterior_null_exp(x):
    a = gamma(x); out = np.eye(16); term = np.eye(16)
    for k in range(1, 9):
        term = term @ a / k
        out += term
    assert np.max(abs(term)) < 1e-12
    return out


class Original:
    def __init__(self, sizes=(2,2,2,2), ell=.25, nu=.3, link_scale=1):
        self.sizes, self.ell, self.nu = sizes, ell, nu
        self.coords = list(itertools.product(*(range(l) for l in sizes)))
        self.V = len(self.coords)
        index = {x:i for i,x in enumerate(self.coords)}
        self.U, self.Q, self.v, self.C, self.shift = [], [], [], [], []
        for x in self.coords:
            # H is independent of v; all u/transverse dependence is retained.
            ucoord = x[0] / max(1, sizes[0]-1)
            h = (ucoord + 2*x[2] - x[3]) / 10
            legs = [nu*N, nu*(E[:,0]-h*N/2), nu*E[:,2], nu*E[:,3]]
            xn = link_scale*((x[2]+1)/7*N2 + (x[3]+ucoord+1)/11*N3)
            uu = np.eye(4) + xn + xn @ xn/2
            assert np.max(abs(uu.T @ ETA @ uu - ETA)) < 1e-12
            self.U.append([uu, np.eye(4), np.eye(4), np.eye(4)])
            self.Q.append([exterior_null_exp(xn), np.eye(16), np.eye(16), np.eye(16)])
            self.v.append(legs); self.C.append([cv(v) for v in legs])
            self.shift.append([index[tuple((a+int(i==r)) % sizes[i]
                                                for i,a in enumerate(x))]
                               for r in range(4)])

    def d(self, p):
        out = np.zeros_like(p)
        for x in range(self.V):
            for r in range(4):
                out[x] += self.C[x][r] @ (
                    self.Q[x][r] @ p[self.shift[x][r]] - p[x]) / self.ell
        return out

    def dag(self, p):
        out = np.zeros_like(p)
        for x in range(self.V):
            for r in range(4):
                t = self.C[x][r].T @ p[x] / self.ell
                out[self.shift[x][r]] += self.Q[x][r].T @ t
                out[x] -= t
        return out

    def D(self, p):
        return self.d(p) + self.dag(p)

    def leg_variation(self, p, x, r, v):
        out = np.zeros_like(p); y = self.shift[x][r]
        out[x] += cv(v) @ (self.Q[x][r] @ p[y]-p[x]) / self.ell
        t = cv(v).T @ p[x] / self.ell
        out[y] += self.Q[x][r].T @ t; out[x] -= t
        return out

    def link_variation(self, p, x, r, lie):
        out = np.zeros_like(p); y = self.shift[x][r]
        g = gamma(lie)
        out[x] += self.C[x][r] @ g @ self.Q[x][r] @ p[y] / self.ell
        out[y] += self.Q[x][r].T @ g.T @ self.C[x][r].T @ p[x] / self.ell
        return out

    def uniform_observer_boost(self, t):
        """Whiten the SAME native v,U at h=diag(exp(-2t),exp(2t),1,1).

        Positive-adjoint data transform by L v and L U L^-1, L=sqrt(h).
        This mutates this diagnostic instance only.
        """
        l = np.diag([math.exp(-t),math.exp(t),1,1])
        li = np.diag([math.exp(t),math.exp(-t),1,1])
        for x in range(self.V):
            for r in range(4):
                self.v[x][r] = l @ self.v[x][r]
                self.C[x][r] = cv(self.v[x][r])
                self.U[x][r] = l @ self.U[x][r] @ li
                # Null generator can be recovered exactly from exp(X)=I+X+X²/2.
                a = self.U[x][r]-np.eye(4)
                logu = a-a@a/2
                self.Q[x][r] = exterior_null_exp(logu)


def local_sources():
    op = Original(); vcount, ell, nu = op.V, op.ell, op.nu
    # z=-1. General unit-circle z follows analytically from
    # 2 Re((z^-1-1)z)=|z-1|^2, 2 Re(z^-1-1)=-|z-1|^2.
    psis = [np.array([(-1)**x[0]*v/math.sqrt(vcount) for x in op.coords])
            for v in QUARTET]
    ds = [op.D(p) for p in psis]
    lam = nu**2*4/ell**2
    eigen_error = max(np.max(abs(op.D(t)-lam*p)) for t,p in zip(ds,psis))
    errors = []; probes = 0

    def response(der):
        return np.array([[np.sum(ds[i]*der[j])+np.sum(der[i]*ds[j])
                          for j in range(4)] for i in range(4)])

    for x in [0,7,15]:
        w = np.linalg.inv(op.U[x][0]).T @ N
        for r in range(4):
            for j in range(4):
                got = response([op.leg_variation(p,x,r,E[:,j]) for p in psis])
                low = 2*nu*4/(ell**2*vcount)*N[j] if r == 0 else 0
                high = nu*4/(ell**2*vcount)*(w+N)[j] if r == 0 else 0
                errors.append(np.max(abs(got-np.diag([low,low,high,high])))); probes += 1
            for a,b in itertools.combinations(range(4),2):
                antisym = np.zeros((4,4)); antisym[a,b]=1; antisym[b,a]=-1
                lie = ETA @ antisym
                got = response([op.link_variation(p,x,r,lie) for p in psis])
                wr = np.linalg.inv(op.U[x][r]).T @ N
                high = (-1 if r == 0 else 1)*nu*4/(ell**2*vcount)*wr @ lie @ op.v[x][r]
                errors.append(np.max(abs(got-np.diag([0,0,high,high])))); probes += 1
        # All THREE native observer tangents. Metric and normalization move.
        observer = (E[:,0]+E[:,1])/math.sqrt(2)
        for dn in [(E[:,0]-E[:,1])/math.sqrt(2), E[:,2], E[:,3]]:
            dh = 2*ETA @ (np.outer(dn,observer)+np.outer(observer,dn)) @ ETA
            dg = gamma(dh); deriv = []
            for p in psis:
                gp = np.zeros_like(p); gp[x] = dg @ p[x]
                dd = op.dag(gp); dd[x] -= dg @ op.dag(p)[x]
                deriv.append(dd)
            got = response(deriv)
            for i in range(4):
                for j in range(4):
                    got[i,j] += ds[i][x] @ dg @ ds[j][x] - lam*psis[i][x] @ dg @ psis[j][x]
            want = np.eye(4)*lam*(N @ dh @ N)/vcount
            errors.append(np.max(abs(got-want))); probes += 1
    return {"quartet_eigen_error":float(eigen_error), "source_probes":probes,
            "full_leg_link_observer_and_quartet_offdiagonal_error":float(max(errors)),
            "plane_eigenvalue":lam, "observer_boost_derivative":2*lam,
            "low_grades_link_source":"zero for all24 directions",
            "high_grades_link_source":"nonzero generally; all4 roles included"}


def protected_fixed_right(lu, grades):
    op = Original((lu,2,2,2)); rank = lu*len(grades)
    basis = np.zeros((op.V,16,rank))
    for x,coord in enumerate(op.coords):
        for j,g in enumerate(grades):
            basis[x,:,coord[0]*len(grades)+j] = QUARTET[g]/math.sqrt(8)
    flat = basis.reshape(-1,rank)
    db = op.D(basis); bf = db.reshape(-1,rank)
    internal = flat.T @ bf
    reducing_error = np.max(abs(bf-flat @ internal))
    dc = op.D(db).reshape(-1,rank)
    delta_error = np.max(abs(dc-flat @ internal @ internal))
    gram_error = np.max(abs(flat.T @ flat-np.eye(rank)))
    # M is an actual pure purification with M* M=I_rank/rank.
    # Its physical density P/rank commutes Delta. Full-sphere stationarity
    # need not hold because occupied eigenvalues differ.
    m = flat/math.sqrt(rank); dm = dc/math.sqrt(rank)
    rayleigh = np.sum(m*dm)
    full_sphere_residual = np.linalg.norm(dm-rayleigh*m)
    rng = np.random.default_rng(218)
    a = rng.normal(size=m.shape[0]); b = rng.normal(size=m.shape[0])
    a /= np.linalg.norm(a); b /= np.linalg.norm(b)
    tangent = a[:,None]*(b@m)[None,:] - b[:,None]*(a@m)[None,:]
    right_gram_tangent = m.T @ tangent+tangent.T @ m
    fixed_right_euler = 2*np.sum(tangent*dm)
    contraction = max(np.linalg.norm(op.C[x][r] @ op.Q[x][r], 2)
                      for x in range(op.V) for r in range(4))
    assert contraction < 1
    return {"Lu":lu,"grades":grades,"rank":rank,
            "full_carrier_dimension":16*op.V,
            "basis_orthogonality_error":float(gram_error),
            "D_reducing_subspace_error":float(reducing_error),
            "Delta_reducing_subspace_error":float(delta_error),
            "RIGHT_Gram":"I_rank/rank",
            "random_LEFT_tangent_Gram_error":float(np.max(abs(right_gram_tangent))),
            "fixed_RIGHT_first_R_source":float(fixed_right_euler),
            "strict_forward_C_LambdaU_operator_norm":float(contraction),
            "unrestricted_sphere_residual_not_claimed_zero":float(full_sphere_residual),
            "R":float(rayleigh)}


def real_low_modes_fixed_right(lu, grades, kmax):
    """Fixed rank128, nonzero physical modes with energy bounded as h->0.

    Transverse size2 is only a diagnostic. The algebra uses constant
    transverse functions and therefore holds on any transverse volumes.
    """
    assert 2*kmax < lu
    op = Original((lu,2,2,2),ell=1/lu,link_scale=1/lu)
    rank = 2*kmax*len(grades)
    assert rank == 128
    basis = np.zeros((op.V,16,rank)); spectrum=[]
    for k in range(1,kmax+1):
        lam = 4*op.nu**2*math.sin(math.pi*k/lu)**2/op.ell**2
        for trig in range(2):
            for j,g in enumerate(grades):
                col = ((k-1)*2+trig)*len(grades)+j
                spectrum.append(lam)
                for x,coord in enumerate(op.coords):
                    angle = 2*math.pi*k*coord[0]/lu
                    value = math.cos(angle) if trig == 0 else math.sin(angle)
                    basis[x,:,col] = QUARTET[g]*value*math.sqrt(2/(lu*8))
    flat = basis.reshape(-1,rank)
    db=op.D(basis); bf=db.reshape(-1,rank); normal=flat.T@bf
    reducing_error=np.max(abs(bf-flat@normal))
    delta=op.D(db).reshape(-1,rank)
    spectrum=np.array(spectrum)
    delta_error=np.max(abs(delta-flat*spectrum[None,:]))
    m=flat/math.sqrt(rank); dm=delta/math.sqrt(rank)
    energy=float(np.sum(m*dm)); expected=float(np.mean(spectrum))
    contraction=max(np.linalg.norm(op.C[x][r]@op.Q[x][r],2)
                    for x in range(op.V) for r in range(4))
    assert contraction < 1
    boost=.17
    op.uniform_observer_boost(boost)
    boosted=op.D(op.D(basis)).reshape(-1,rank)
    boost_error=np.max(abs(boosted-flat*spectrum[None,:]*math.exp(2*boost)))
    boost_energy=float(np.sum(flat*boosted)/rank)
    upper=op.nu**2*(2*math.pi*kmax)**2
    assert float(max(spectrum)) <= upper
    return {"Lu":lu,"physical_u_length":1,"h":1/lu,
            "actual_transverse_diagnostic_sizes":[2,2,2],
            "quartet_indices":grades,"cos_sin_modes":[1,kmax],"rank":rank,
            "RIGHT_Gram":"I128/128",
            "basis_Gram_error":float(np.max(abs(flat.T@flat-np.eye(rank)))),
            "D_reducing_subspace_error":float(reducing_error),
            "original_Delta_eigenbasis_error":float(delta_error),
            "R":energy,"expected_R":expected,
            "highest_eigenvalue":float(max(spectrum)),
            "uniform_continuum_energy_upper_bound":upper,
            "strict_forward_C_LambdaU_operator_norm":float(contraction),
            "uniform_observer_boost":boost,
            "boosted_original_Delta_error":float(boost_error),
            "R_boosted_minus_exp2t_R":float(boost_energy-math.exp(2*boost)*energy),
            "all_fixed_RIGHT_preparation_rows":"zero by [Delta,P_modes]=0",
            "all_proper_link_R_rows":"zero" if grades==[0,1] else "generally nonzero",
            "all4D_refinement_replayed":False}


if __name__ == "__main__":
    result = {"local_sources":local_sources(),
              "quartet_fixed_RIGHT":protected_fixed_right(32,[0,1,2,3]),
              "low_two_grade_fixed_RIGHT":protected_fixed_right(64,[0,1]),
              "quartet_real_low_modes":real_low_modes_fixed_right(65,[0,1,2,3],16),
              "low_two_real_modes_Lu65":real_low_modes_fixed_right(65,[0,1],32),
              "low_two_real_modes_Lu129":real_low_modes_fixed_right(129,[0,1],32),
              "scope":{"original_D_not_survival_reconstruction":True,
                       "H_J_sources_replayed":False,"clock_grade14_marginal_preserved":False,
                       "native_preparation_admission_proved":False,"GR_closed":False}}
    assert result["local_sources"]["quartet_eigen_error"] < 1e-11
    assert result["local_sources"]["full_leg_link_observer_and_quartet_offdiagonal_error"] < 1e-11
    for tag in ("quartet_fixed_RIGHT","low_two_grade_fixed_RIGHT"):
        r = result[tag]
        assert r["rank"] == 128
        assert r["D_reducing_subspace_error"] < 1e-11
        assert r["Delta_reducing_subspace_error"] < 1e-11
        assert abs(r["fixed_RIGHT_first_R_source"]) < 1e-11
    for tag in ("quartet_real_low_modes","low_two_real_modes_Lu65","low_two_real_modes_Lu129"):
        r=result[tag]
        assert r["rank"] == 128
        assert r["basis_Gram_error"] < 1e-11
        assert r["D_reducing_subspace_error"] < 1e-8
        assert r["original_Delta_eigenbasis_error"] < 1e-8
        assert r["boosted_original_Delta_error"] < 1e-8
        assert abs(r["R_boosted_minus_exp2t_R"]) < 1e-8
    result["status"] = "PASS"
    print(json.dumps(result,indent=2))
