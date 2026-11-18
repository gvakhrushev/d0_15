"""First Julia cut, isochoric field, full primary Fourier input and old pointer."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import sys

import numpy as np
from scipy import linalg
from scipy.linalg.blas import dgemm

DIRECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DIRECT / "round76/geometry"))
sys.path.insert(0, str(DIRECT / "round77/volume"))
import check_invisible_geometry as geom
from check_isochoric_rank import restrict_to_fixed_volume

I = geom.heat.I
car = geom.car


def field_coefficients():
    """Weights are a real scalar field before Fourier compression, divided by 16."""
    counts = car.actual_counts(geom.heat.ROOT)
    p = geom.heat.P
    positive = (I(.25), I(1.), p, p)
    negative = (I(.25), I(1.), p*p, p*p)
    for r, matrix in enumerate(car.ROLE_CREATION):
        # Occupied masks have degrees 1 and 3, so their squared outputs add.
        for op, assumed in ((matrix, positive[r]), (car.transpose(matrix), negative[r])):
            coeff = sum(sum(row[m]**2 for row in op)*w for m,w in ((1,p),(14,p*p)))
            assert (coeff-assumed).contains(0)
    mid = np.zeros((256,128))
    err = np.zeros_like(mid)
    locations = set()
    for j,(x,r) in enumerate(geom.DIRECTIONS):
        front = car.site_index(car.step(car.SITES_LIST[x],r,1))
        mass = (p*p*p).square()*Q(256*counts[x],sum(counts))
        for y, factor in ((x,2*negative[r]+positive[r]),(front,positive[r])):
            z = -2*mass*factor/16
            center = float((z.lo+z.hi)/2)
            rad = max(float(z.hi)-center, center-float(z.lo))
            mid[y,j] = center
            err[y,j] = rad*1.000001+1e-290
            locations.add(y)
    active = sorted(locations)
    assert len(active) == 80
    rows,radii = restrict_to_fixed_volume(mid[active],err[active])
    assert np.all(np.linalg.norm(rows,axis=1)>0)
    return rows,radii,active


def compression():
    fourier = np.asarray(car.fourier_numerators(),dtype=np.int64)
    gram = (fourier @ fourier.T)**2
    coordinates = np.array(car.SITES_LIST,dtype=int)
    difference = (coordinates[:,None,:]-coordinates[None,:,:])%4
    lookup = np.array([car.site_index(tuple(x)) for x in difference.reshape(-1,4)])
    assert np.array_equal(gram,gram[0,lookup].reshape(256,256))
    cs = np.array([1,0,-1,0])
    sn = np.array([0,1,0,-1])
    phases = coordinates @ coordinates.T % 4
    eigenvalues = cs[phases] @ gram[0]
    assert np.all(sn[phases] @ gram[0] == 0)
    assert eigenvalues.min() == 2048
    return int(eigenvalues.max())


def exact_scalar_identities(active):
    # Arithmetic in Q[p], p^2=1-p. Only the radius of the field neighbourhood
    # needs a real number; all recurrences on the true early coefficients are exact.
    import sympy as sp
    p = (sp.sqrt(5)-1)/2
    n = [sp.Rational(1,4),sp.Integer(1),p,p]
    u = [sp.Rational(3,4),sp.Integer(3),2-p,2-p]
    shift = sp.zeros(4)
    for j in range(4):
        shift[j,(j+1)%4] = 1
    transfer = {r: ((u[1]-u[r])*sp.eye(4)+n[1]*shift)/n[r] for r in (0,2,3)}
    for x,y in product(transfer.values(),repeat=2):
        assert (x*y-y*x).applyfunc(sp.simplify)==sp.zeros(4)
    ratios = [13,None,((1+p)**3).expand(),((1+p)**3).expand()]
    for r in (0,2,3):
        assert sp.simplify(u[r]+n[r]*ratios[r]-4)==0
    free = {car.SITES_LIST[i] for i,_ in geom.DIRECTIONS}
    assert len(free)==32
    expected = free | {car.step(site,r,1) for site in free for r in range(4)}
    assert {car.SITES_LIST[i] for i in active} == expected
    # Every site in the three outgoing single faces is reached using only
    # internal vertices before the last step. The expressions for the four
    # values at (u,x,y)=(1,1,1) are literally the four independent inputs.
    triples = {(s[0],s[2],s[3]) for s in expected}
    assert triples == {x for x in product(range(1,4),repeat=3) if sum(z==3 for z in x)<=1}


def certify_full_column_rank(A,E):
    row_scale = np.linalg.norm(A,axis=1)
    Z = A/row_scale[:,None]
    eps = E/row_scale[:,None]+3e-16*np.abs(Z)
    u,s,vt = linalg.svd(Z,full_matrices=False)
    inverse = dgemm(1.,vt.T/s,u,trans_b=1)
    center = dgemm(1.,inverse,Z)
    true = np.abs(center-np.eye(Z.shape[1]))+dgemm(1.,np.abs(inverse),eps)
    true += 3e-14*dgemm(1.,np.abs(inverse),np.abs(Z))
    defect = 1.000001*np.max(np.sum(true,axis=1))+1e-15
    assert defect < 1e-4
    gain = (1-defect)/(1.000001*np.max(np.sum(np.abs(inverse),axis=1)))
    print("106 normalized measurements, 96 coordinates: inverse defect",defect,
          "; guaranteed normalized infinity response at least",gain)
    return gain


def certify_early_with_heat(A,E):
    """A weighted infinity norm for the differently scaled spectral price rows."""
    scale=np.linalg.norm(A,axis=1)[:,None]
    Z=A/scale
    delta=E/scale+4e-14*np.abs(Z)
    u,s,vt=linalg.svd(Z,full_matrices=False)
    candidate=dgemm(1.,vt.T/s,u,trans_b=1)
    center=dgemm(1.,Z,candidate)
    error=np.abs(center-np.eye(len(Z)))+dgemm(1.,delta,np.abs(candidate))
    error=1.000001*error+1e-20
    # Eigenvectors only choose positive test weights. The last explicit
    # componentwise inequality, with roundoff, is the proof of inversion.
    values,vectors=linalg.eig(error)
    k=np.argmax(np.abs(values))
    w=np.abs(vectors[:,k].real)
    w=np.maximum(w,1e-8*np.max(w))
    products=np.sum(error*w,axis=1)
    bound=1.000001*np.max(products/w)+1e-15
    assert bound<.4
    print("76 early rows plus three heat rows: weighted inverse defect",bound)


def main():
    mx = compression()
    early,errors,active = field_coefficients()
    exact_scalar_identities(active)
    d,terms,C,_ = geom.assemble()
    q,dq = restrict_to_fixed_volume(*geom.pointer_rows(d,terms,C))
    gain = certify_full_column_rank(np.vstack((early,q)),np.vstack((errors,dq)))
    assert gain>0.000176
    pivot = linalg.qr(early.T, mode="economic", pivoting=True)[2][:76]
    (g, ge), _ = geom.heat_rows(d)
    g, ge = restrict_to_fixed_volume(g, ge)
    # The exact upper rank 76 was derived by the four commuting transfers.
    certify_early_with_heat(np.vstack((early[pivot], g)), np.vstack((errors[pivot], ge)))
    print("Fourier Gram min/max eigenvalues",2048,mx,
          "; early rank 80-4=76; joint rank 96; all three heat prices locally recovered.")


if __name__=="__main__":
    main()
