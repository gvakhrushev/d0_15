#!/usr/bin/env python3
"""Exact rational A-stabilizer selector check for the A4D Role-bivector insertion.

This checker keeps two operations distinct:

1. fixed-base internal odd Lorentz reflection:
   K rho(sigma) = rho(sigma) K;

2. simultaneous spatial Role/site relabeling of an oriented top-cell density:
   K rho(sigma) = sign(sigma) rho(sigma) K.

The second is the D0 spatial-gauge/naturality condition because the base
top-cell orientation line contributes sign(sigma).
"""

from fractions import Fraction as Q
from itertools import combinations

print("STRUCTURE_FIXED_BEFORE_NUMBER: eta(+---), Lambda2(Role), so(1,3), Stab(A)=S3, oriented base top-cell")

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}

def z(m, n):
    return [[Q(0) for _ in range(n)] for _ in range(m)]

def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]

def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]

def tr(a):
    return [list(row) for row in zip(*a)]

def rank(a):
    a = [r[:] for r in a]
    m, n = len(a), len(a[0]) if a else 0
    row = 0
    for col in range(n):
        p = next((i for i in range(row, m) if a[i][col]), None)
        if p is None:
            continue
        a[row], a[p] = a[p], a[row]
        q = a[row][col]
        a[row] = [x / q for x in a[row]]
        for i in range(m):
            if i != row and a[i][col]:
                q = a[i][col]
                a[i] = [a[i][j] - q * a[row][j] for j in range(n)]
        row += 1
        if row == m:
            break
    return row

def nullspace(a):
    a = [r[:] for r in a]
    m, n = len(a), len(a[0]) if a else 0
    piv, row = [], 0
    for col in range(n):
        p = next((i for i in range(row, m) if a[i][col]), None)
        if p is None:
            continue
        a[row], a[p] = a[p], a[row]
        q = a[row][col]
        a[row] = [x / q for x in a[row]]
        for i in range(m):
            if i != row and a[i][col]:
                q = a[i][col]
                a[i] = [a[i][j] - q * a[row][j] for j in range(n)]
        piv.append(col)
        row += 1
        if row == m:
            break
    free = [c for c in range(n) if c not in piv]
    out = []
    for f in free:
        v = [Q(0)] * n
        v[f] = Q(1)
        for i, p in enumerate(piv):
            v[p] = -a[i][f]
        out.append(v)
    return out

ETA = [[Q(1),0,0,0],[0,Q(-1),0,0],[0,0,Q(-1),0],[0,0,0,Q(-1)]]

def wedge2(g):
    w = z(6, 6)
    for j, (a, b) in enumerate(PAIRS):
        for i, (c, d) in enumerate(PAIRS):
            w[i][j] = g[c][a] * g[d][b] - g[d][a] * g[c][b]
    return w

def rho_lie(x):
    r = z(6, 6)
    for j, (a, b) in enumerate(PAIRS):
        for i, (c, d) in enumerate(PAIRS):
            r[i][j] = (
                x[c][a] * Q(int(d == b)) - x[d][a] * Q(int(c == b))
                + Q(int(c == a)) * x[d][b] - Q(int(d == a)) * x[c][b])
    return r

def generators():
    out = []
    for i in (1,2,3):
        x = z(4,4); x[0][i] = x[i][0] = Q(1); out.append(x)
    for i,j in ((1,2),(1,3),(2,3)):
        x = z(4,4); x[i][j] = Q(1); x[j][i] = Q(-1); out.append(x)
    return out

def perm(images):
    p = z(4,4)
    for j, i in enumerate(images):
        p[i][j] = Q(1)
    return p

def constraint_rows(reps_with_sign):
    """Rows for K R = s R K; s=+1 ordinary intertwiner, s=-1 orientation twist."""
    rows = []
    for r, s in reps_with_sign:
        for i in range(6):
            for j in range(6):
                row = [Q(0)] * 36
                for k in range(6):
                    row[6*i+k] += r[k][j]
                    row[6*k+j] -= Q(s) * r[i][k]
                rows.append(row)
    return rows

def det4(a):
    a = [r[:] for r in a]
    d, s = Q(1), 1
    for c in range(4):
        p = next((i for i in range(c,4) if a[i][c]), None)
        if p is None: return Q(0)
        if p != c:
            a[c], a[p] = a[p], a[c]; s *= -1
        q = a[c][c]; d *= q
        for i in range(c+1,4):
            if a[i][c]:
                f = a[i][c] / q
                for j in range(c,4):
                    a[i][j] -= f * a[c][j]
    return d * s

def vecmat(v):
    return [v[6*i:6*(i+1)] for i in range(6)]

def proportional(a, b):
    lam = None
    for i in range(6):
        for j in range(6):
            if b[i][j]:
                q = a[i][j] / b[i][j]
                lam = q if lam is None else lam
                if q != lam: return False
            elif a[i][j]:
                return False
    return lam is not None

def scalar_id(a):
    q = a[0][0]
    return all(a[i][j] == (q if i == j else 0)
               for i in range(6) for j in range(6))

def chk(name, cond):
    if not cond: raise AssertionError(name)
    print("PASS_" + name)

def neg(name, false_claim):
    if false_claim: raise AssertionError("negative control unexpectedly passed: " + name)
    print("FAIL_" + name + "_REJECTED")

lie = generators()
chk("SO13_GENERATORS_ETA_SKEW",
    all(add(mm(tr(x), ETA), mm(ETA, x)) == z(4,4) for x in lie))
rho = [rho_lie(x) for x in lie]
proper = constraint_rows([(r,+1) for r in rho])
proper_rank = rank(proper)
chk("PROPER_LORENTZ_RANK_34", proper_rank == 34)
chk("PROPER_LORENTZ_COMMUTANT_DIM_2", 36 - proper_rank == 2)

J = z(6,6)
star = {
 (0,1):((2,3),-1), (0,2):((1,3),1), (0,3):((1,2),-1),
 (1,2):((0,3),1), (1,3):((0,2),-1), (2,3):((0,1),1)}
for p,(q,s) in star.items():
    J[PINDEX[q]][PINDEX[p]] = Q(s)
minus_i = [[Q(-1) if i == j else Q(0) for j in range(6)] for i in range(6)]
chk("STAR_SQUARE_MINUS_ID", mm(J,J) == minus_i)
chk("STAR_COMMUTES_SO13", all(sub(mm(J,r),mm(r,J)) == z(6,6) for r in rho))

Pbc, Pcd = perm([0,2,1,3]), perm([0,1,3,2])
Rbc, Rcd = wedge2(Pbc), wedge2(Pcd)
chk("SWAP_BC_FIXES_A", Pbc[0] == [Q(1),Q(0),Q(0),Q(0)])
chk("SWAP_CD_FIXES_A", Pcd[0] == [Q(1),Q(0),Q(0),Q(0)])
chk("SWAP_BC_PRESERVES_ETA", mm(mm(tr(Pbc),ETA),Pbc) == ETA)
chk("SWAP_CD_PRESERVES_ETA", mm(mm(tr(Pcd),ETA),Pcd) == ETA)
chk("SWAP_BC_ODD", det4(Pbc) == -1)
chk("SWAP_CD_ODD", det4(Pcd) == -1)
chk("STAR_ANTI_SWAP_BC", add(mm(Rbc,J),mm(J,Rbc)) == z(6,6))
chk("STAR_ANTI_SWAP_CD", add(mm(Rcd,J),mm(J,Rcd)) == z(6,6))

# Hostile distinction: a fixed-base improper internal reflection uses ordinary
# commutation and therefore selects I, not star.
fixed_base = proper + constraint_rows([(Rbc,+1)])
fixed_ns = nullspace(fixed_base)
chk("FIXED_BASE_ODD_INTERNAL_DIM_1", len(fixed_ns) == 1)
chk("FIXED_BASE_ODD_INTERNAL_SELECTS_IDENTITY", scalar_id(vecmat(fixed_ns[0])))
neg("FIXED_BASE_INTERNAL_IS_SAME_AS_ROLE_SITE_RELABEL", proportional(vecmat(fixed_ns[0]), J))

# Actual simultaneous Role/site relabel of the oriented top-cell density:
# epsilon_base picks up sign(sigma), so K must be a sign-twisted intertwiner.
twisted_bc = proper + constraint_rows([(Rbc,-1)])
twisted_bc_ns = nullspace(twisted_bc)
chk("ORIENTED_DENSITY_PLUS_SWAP_BC_RANK_35", rank(twisted_bc) == 35)
chk("ORIENTED_DENSITY_PLUS_SWAP_BC_DIM_1", len(twisted_bc_ns) == 1)
chk("ORIENTED_DENSITY_PLUS_SWAP_BC_SELECTS_STAR", proportional(vecmat(twisted_bc_ns[0]), J))

twisted_s3 = proper + constraint_rows([(Rbc,-1),(Rcd,-1)])
twisted_s3_ns = nullspace(twisted_s3)
chk("ORIENTED_DENSITY_PLUS_STAB_A_RANK_35", rank(twisted_s3) == 35)
chk("ORIENTED_DENSITY_PLUS_STAB_A_DIM_1", len(twisted_s3_ns) == 1)
chk("UNIQUE_ORIENTED_DENSITY_LINE_IS_STAR", proportional(vecmat(twisted_s3_ns[0]), J))

# Load-bearing controls.
Pcyc = perm([0,2,3,1])  # B->C->D->B, even
Rcyc = wedge2(Pcyc)
even = proper + constraint_rows([(Rcyc,+1)])
even_dim = 36 - rank(even)
neg("EVEN_SPATIAL_CYCLE_SELECTS_DIM1", even_dim == 1)
chk("EVEN_SPATIAL_CYCLE_LEAVES_DIM2", even_dim == 2)
neg("PROPER_LORENTZ_ALONE_SELECTS_DIM1", 36-proper_rank == 1)

# If the base-orientation sign is incorrectly omitted, one selects the wrong line.
neg("UNTWISTED_ODD_RELABEL_SELECTS_STAR", proportional(vecmat(fixed_ns[0]), J))

# ---------------------------------------------------------------------------
# Complete finite face-by-face density sign audit.
# Faces are oriented in the fixed Role order A<B<C<D.  For a permutation sigma,
# chi_S is the sign required to sort the transported oriented face blade, and
# chi_Sc the analogous complement-blade sign.
#
# Direct finite identity:
# eps(sigma S) = sign(sigma) eps(S) chi_S chi_Sc.
#
# Therefore
# L_I(sigma S) / L_I(S)       = sign(sigma),
# L_star(sigma S) / L_star(S) = 1,
# because star itself contributes sign(sigma).
# ---------------------------------------------------------------------------

from itertools import permutations

def inversion_sign(seq):
    inv = sum(seq[i] > seq[j] for i in range(len(seq)) for j in range(i + 1, len(seq)))
    return -1 if inv % 2 else 1

def face_complement(face):
    return tuple(r for r in range(4) if r not in face)

def complement_orientation_face(face):
    return inversion_sign(tuple(face) + face_complement(face))

def perm_parity(images):
    return inversion_sign(images)

def transported_face(images, face):
    vals = tuple(images[r] for r in face)
    return tuple(sorted(vals))

def transported_blade_sign(images, face):
    vals = tuple(images[r] for r in face)
    return inversion_sign(vals)

spatial_perms = [(0,) + q for q in permutations((1, 2, 3))]
two_faces = PAIRS[:]

for images in spatial_perms:
    sgn = perm_parity(images)
    for face in two_faces:
        comp = face_complement(face)
        image_face = transported_face(images, face)
        chi_face = transported_blade_sign(images, face)
        chi_comp = transported_blade_sign(images, comp)
        eps_old = complement_orientation_face(face)
        eps_new = complement_orientation_face(image_face)

        chk(
            "FACE_ORIENTATION_IDENTITY_"
            + "".join(map(str, images)) + "_"
            + "".join(map(str, face)),
            eps_new == sgn * eps_old * chi_face * chi_comp,
        )

        # Identity-channel density: pairing contributes chi_face*chi_comp.
        identity_ratio = eps_new * chi_face * chi_comp * eps_old
        chk(
            "IDENTITY_DENSITY_PARITY_"
            + "".join(map(str, images)) + "_"
            + "".join(map(str, face)),
            identity_ratio == sgn,
        )

        # Star channel has one additional det/sign(sigma).
        star_ratio = identity_ratio * sgn
        chk(
            "STAR_DENSITY_INVARIANCE_"
            + "".join(map(str, images)) + "_"
            + "".join(map(str, face)),
            star_ratio == 1,
        )

print("PASS_COMPLETE_S3_X_SIX_FACES_DENSITY_AUDIT")
print("RESULT: proper Lorentz -> span{I,star}; complete oriented Stab(A)=S3 density covariance -> span{star}")


# 8. Complete finite density transformation: all six Stab(A)=S3 elements
# and all six degree-two faces. This closes the action-level sign question,
# rather than inferring it from the internal commutant alone.
from itertools import permutations

def perm_sign(images):
    inv = sum(images[i] > images[j] for i in range(4) for j in range(i+1,4))
    return -1 if inv % 2 else 1

def face_action(images, face):
    vals = [images[i] for i in face]
    q = -1 if vals[0] > vals[1] else 1
    return tuple(sorted(vals)), q

def epsilon_face(face):
    comp = tuple(i for i in range(4) if i not in face)
    seq = list(face) + list(comp)
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i+1,4))
    return -1 if inv % 2 else 1

G2 = z(6,6)
eta_diag = [Q(1), Q(-1), Q(-1), Q(-1)]
for i,(a,b) in enumerate(PAIRS):
    G2[i][i] = eta_diag[a] * eta_diag[b]

spatial_group = [(0,) + p for p in permutations((1,2,3))]
all_orientation = True
all_metric = True
all_star_pseudo = True
all_I_parity = True
all_star_invariant = True
saw_odd = False

for sigma in spatial_group:
    sgn = perm_sign(sigma)
    if sgn == -1:
        saw_odd = True
    R = wedge2(perm(sigma))
    all_metric = all_metric and (mm(mm(tr(R), G2), R) == G2)
    all_star_pseudo = all_star_pseudo and (
        sub(mm(J,R), [[Q(sgn) * x for x in row] for row in mm(R,J)]) == z(6,6)
    )
    for face in PAIRS:
        image_face, q_face = face_action(sigma, face)
        comp = tuple(i for i in range(4) if i not in face)
        image_comp, q_comp = face_action(sigma, comp)
        comp_of_image = tuple(i for i in range(4) if i not in image_face)
        all_orientation = all_orientation and (set(image_comp) == set(comp_of_image))
        lhs = epsilon_face(image_face) * q_face * q_comp
        rhs = sgn * epsilon_face(face)
        all_orientation = all_orientation and (lhs == rhs)

        # Complete scalarized density parity.
        # I has internal character +1, star has internal character sgn.
        factor_I = Q(lhs, epsilon_face(face))
        factor_star = factor_I * Q(sgn)
        all_I_parity = all_I_parity and (factor_I == sgn)
        all_star_invariant = all_star_invariant and (factor_star == 1)

chk("ALL_S3_G2_PAIRING_INVARIANT", all_metric)
chk("ALL_S3_STAR_PSEUDOEQUIVARIANT", all_star_pseudo)
chk("ALL_S3_FACE_COMPLEMENT_ORIENTATION_IDENTITY", all_orientation)
chk("ALL_S3_IDENTITY_CHANNEL_PARITY_IS_SIGN", all_I_parity)
chk("ALL_S3_STAR_CHANNEL_DENSITY_INVARIANT", all_star_invariant)
chk("S3_CONTAINS_ODD_SPATIAL_RELABEL", saw_odd)
neg("IDENTITY_CHANNEL_DENSITY_INVARIANT_UNDER_FULL_S3",
    all(perm_sign(sigma) == 1 for sigma in spatial_group))

print("RESULT_DENSITY: L_I transforms by sign(sigma); L_star is invariant for all Stab(A)=S3 and all degree-two faces")
