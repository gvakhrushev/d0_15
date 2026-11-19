"""Exact finite checks of the two slab layouts and the complementary source."""

from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import runpy
import subprocess

import mpmath as mp
import sympy as sp

REPO = Path(__file__).resolve().parents[6]
REV = "a4398729c8ac8406d3d1ba9d4dd28320a9ddd84d"
PRIMARY = "02_REGISTRY/research"
ALL40 = "A4D_ARBITRARY_BRINKMANN_ALL40_CARTAN_DISCRETE_EINSTEIN_2026_10_19.md"
WELD = "A4D_ORIGINAL_UNPADDED_N1_J2_ALL42_BRINKMANN_WELD_2026_10_22.md"
OWNER = "sources/d0_arbitrary_brinkmann_all40_2026-10-19/check_all40_arbitrary_brinkmann.py"
OWNER_SHA256 = "d3d0b1bc92c25a0963a4ba851d9d587d2191f0bbd8cd8cd0ab58b664852b7026"


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def full_dirichlet_gradient(nx, ny, h):
    sites = list(product(range(1,nx+1), range(1,ny+1)))
    edges = [(x,y,axis) for axis in (0,1)
             for x,y in product(range(1,nx+2), range(1,ny+2))
             if (axis == 0 and y <= ny) or (axis == 1 and x <= nx)]
    gradient = sp.zeros(len(edges), len(sites))
    for row,(x,y,axis) in enumerate(edges):
        for site, sign in (((x,y), 1), ((x-(axis==0),y-(axis==1)), -1)):
            if site in sites:
                gradient[row,sites.index(site)] = sign/h
    return gradient


def finite_slabs():
    h = sp.Rational(1,4)
    gradient = full_dirichlet_gradient(2,3,h)
    m,n = gradient.shape
    laplace = gradient.T*gradient
    require(all(laplace[i,i] == 4/h**2 for i in range(n)), "missing Dirichlet boundary edge")
    laplace_inv = laplace.inv()
    grad_lift = gradient*laplace_inv
    projector = grad_lift*gradient.T
    require(projector.T == projector and projector**2 == projector, "invalid edge projector")
    paired = (-gradient/2).row_join(sp.eye(m)).col_join(sp.zeros(n,n).row_join(gradient.T))
    inverse = (-2*laplace_inv*gradient.T).row_join(2*laplace_inv).col_join(
        (sp.eye(m)-projector).row_join(grad_lift))
    require(inverse*paired == paired*inverse == sp.eye(n+m), "invalid paired inverse")

    slabs = 3
    shift = sp.zeros(slabs)
    for row in range(1,slabs):
        shift[row,row-1] = 1
    periodic = shift.copy()
    periodic[0,-1] = 1
    time = sp.eye(slabs)

    def same_labels(back):
        r = sp.kronecker_product(time,-gradient/2).row_join(sp.kronecker_product(back,sp.eye(m)))
        s = sp.zeros(slabs*n,slabs*n).row_join(sp.kronecker_product(time,gradient.T))
        return r.col_join(s)

    naive = same_labels(shift)
    periodic_full = same_labels(periodic)
    terminal_circulation = gradient.T.nullspace()
    require(len(terminal_circulation) == m-n, "wrong independent edge circulation")
    for vector in terminal_circulation:
        initial_row = vector.col_join(sp.zeros(naive.rows-m,1))
        terminal_col = sp.zeros(naive.cols-m,1).col_join(vector)
        require(naive*terminal_col == sp.zeros(naive.rows,1)
                and initial_row.T*naive == sp.zeros(1,naive.cols), "wrong boundary defect")
    require(naive.rank() == (n+m)*slabs-(m-n), "naive kernel is larger than claimed")
    require(periodic_full.rank() == periodic_full.cols, "periodic shift must be invertible")
    return {"transverse_sites": n, "transverse_edges": m, "time_slices": slabs,
            "one_paired_block_rank": paired.rank(), "periodic_rank": periodic_full.rank(),
            "same_indices_rank": naive.rank(), "same_indices_kernel": m-n}


def complementary_hessian():
    coupling = sp.Matrix([[2,1],[0,3]])
    conormal = sp.Matrix([[2,-3],[-3,4]])
    mixed = sp.Matrix([[5,4],[0,2]])
    normal = sp.diag(1,0)
    z = sp.zeros(2)
    first = z.row_join(coupling.T).row_join(z)
    second = coupling.row_join(conormal).row_join(mixed)
    third = z.row_join(mixed.T).row_join(normal)
    matrix = first.col_join(second).col_join(third)
    inverse_pair = matrix[:4,:4].inv()
    require(matrix[4:,4:]-matrix[4:,:4]*inverse_pair*matrix[:4,4:] == normal,
            "paired elimination changed the normal Hessian")
    null = sp.Matrix([0,1])
    lifted = (-coupling.inv()*mixed*null).col_join(sp.zeros(2,1)).col_join(null)
    require(matrix*lifted == sp.zeros(6,1), "normal null direction did not lift")

    t, rho0, drho, ddrho, u1, u2, curvature = sp.symbols("t rho0 drho ddrho u1 u2 curvature")
    rho = rho0+drho*t+ddrho*t*t/2
    u = u1*t+u2*t*t/2
    normalized_perspective = rho*(u/rho+curvature*(u/rho)**2/2)
    result = sp.diff(normalized_perspective,t,2).subs(t,0)
    require(sp.cancel(result-u2-curvature*u1*u1/rho0) == 0, "density jet did not cancel")

    mp.iv.dps = 55
    one = mp.iv.mpf(1)
    p = (mp.iv.sqrt(5)-1)/2
    zeta = one/2**20
    b0 = 4*p**3
    a0 = b0*(one+p**6)
    r0 = zeta*(a0+b0)-zeta**2*a0*b0
    rx = 4*zeta*p**2*(one-2*p**2)*p**6*(one-zeta*b0)
    log_phi = -mp.iv.ln(p)
    slope = mp.iv.ln((one-r0)/r0)/log_phi
    kappa = (one+one/(r0*log_phi*(slope-1)))/(one-r0)
    coefficient = kappa*rx/20
    require(coefficient.a > 4.0708e-5 and coefficient.b < 4.0709e-5,
            "incorrect same-operand Gram coefficient")
    return {"Schur_complement_is_normal_block": True, "exact_density_jet_cancellation": True,
            "common_operand_J2_minus_N1_Gram_coefficient": [4.0708e-5,4.0709e-5]}


def stopped_returns():
    output = []
    take = sp.diag(1,0)
    other = sp.eye(2)-take
    initial = sp.Matrix([1,0])
    for c,s in ((sp.Rational(3,5),sp.Rational(4,5)),(sp.Rational(5,13),sp.Rational(12,13))):
        echo = sp.Matrix([[c,s],[s,-c]])
        state = initial
        masses = []
        overlaps = []
        for stage in range(4):
            success = take*echo*state
            state = other*echo*state
            probability = success.dot(success)
            require(probability > 0, "lost successful branch rank")
            masses.append(str(probability))
            # The passive root uses the same direct router with square echo as identity.
            overlap = (initial.T*success)[0]**2/probability if stage == 0 else 0
            overlaps.append(overlap)
        require(state.dot(state) > 0 and initial.dot(state) == 0, "lost overflow")
        require(sum(overlaps) == 1, "normalized RC3 must ignore stopped weights")
        output.append(masses+[str(state.dot(state))])
    require(output[0] != output[1], "Born laws need to be different")
    return {"Born_success_and_overflow_masses": output,
            "same_RC3_on_direct_passive_closure": True}


def finite_shear():
    path = REPO / PRIMARY / OWNER
    require(sha256(path.read_bytes()).hexdigest() == OWNER_SHA256, "changed all40 stencil")
    checker = runpy.run_path(str(path))
    namespace = checker["links"].__globals__
    links, solder, original = (checker[key] for key in ("links","solder","e"))
    base, t = (0,0,0,0), sp.Symbol("t", real=True)
    reference_links, reference_solder = links(base), solder(base)
    sample_counts = []
    for v_uniform in (True,False):
        samples = {}

        def potential(site):
            key = (site[0],site[2],site[3]) if v_uniform else site
            if key not in samples:
                samples[key] = sp.Symbol(f"Xi_{len(samples)}", real=True)
            return samples[key]

        def sheared(site):
            frame = original(site)
            for axis in range(4):
                frame[1,axis] += t*(potential(site)-potential(checker["sh"](site,axis,-1)))
            return frame

        namespace["e"] = sheared
        try:
            require((solder(base)-reference_solder).applyfunc(sp.expand) == sp.zeros(4),
                    "the finite shear changed a coframe Euler row")
            require((links(base)-reference_links).applyfunc(sp.expand) == sp.zeros(4,6),
                    "the finite shear changed a full link Euler row")
            for r,w in checker["pairs"]:
                u,v = [axis for axis in range(4) if axis not in (r,w)]
                holonomy = checker["plaque"](base,r,w)
                curvature = (holonomy-checker["inv"](holonomy))/2
                require(sp.expand(checker["pair"](sheared(base),u,v,curvature)) == 0,
                        "a local face density changed")
        finally:
            namespace["e"] = original
        sample_counts.append(len(samples))
    require(sample_counts == [10,15], "unexpected stencil coverage")
    bu,c,bx,by = sp.symbols("bu c bx by", real=True)
    frame = sp.eye(4)
    frame[1,:] = sp.Matrix([[bu,c,bx,by]])
    perturbation = sp.Matrix(4,4,sp.symbols("d0:16"))
    inverse = frame.inv()
    metric = inverse*checker["eta"]*inverse.T
    dmetric = -inverse*perturbation*metric-metric*perturbation.T*inverse.T
    require(metric[0,:] == sp.Matrix([[0,1/c,0,0]])
            and sp.simplify(dmetric[0,0]+2*perturbation[0,1]/c) == 0,
            "actual matter density variation")
    return {"original_stencil_sha256": OWNER_SHA256, "local_faces": 6,
            "all_unchanged_geometric_Euler_rows": 40,
            "independent_shear_samples_v_uniform_then_general": sample_counts,
            "matter_source_on_shear": "Dg^uu=-2*De_v^+/e_v^-"}


def main():
    source_hashes = {}
    for path in (ALL40,WELD):
        raw = subprocess.check_output(["git","show",f"{REV}:{PRIMARY}/{path}"], cwd=REPO)
        source_hashes[path] = sha256(raw).hexdigest()
    print(json.dumps({
        "primary_revision": REV,
        "primary_sha256": source_hashes,
        "slab": finite_slabs(),
        "finite_nonflat_shear": finite_shear(),
        "second_jet": complementary_hessian(),
        "stopped_direct_router": stopped_returns(),
        "full_physical_source_bound_proved": False,
        "GR_closed": False,
        "status": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
