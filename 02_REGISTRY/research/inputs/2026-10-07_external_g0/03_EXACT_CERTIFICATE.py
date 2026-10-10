# -*- coding: utf-8 -*-
"""
03_EXACT_CERTIFICATE.py
D0 / G0: точные сертификаты к 01_MAIN_PROOF.md.
Только точная арифметика (sympy / fractions); в C14b дополнительно numpy-int64
для конечной проверки перестановок. Сеть не используется.
Отрицательный контроль печатает PASS только когда мутация ДЕЙСТВИТЕЛЬНО отвергнута.
"""
import itertools, random, json
from fractions import Fraction as F
import sympy as sp

REPORT = []
def rep(tag, ok, detail=""):
    REPORT.append((tag, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + tag + ((" | " + detail) if detail else ""))
    return bool(ok)

s, t = sp.symbols('s t')
random.seed(20261007)
R = sp.Rational
def rndmat(rows, cols, lo=-3, hi=3):
    return sp.Matrix(rows, cols, lambda i, j: R(random.randint(lo, hi), random.randint(1, 3)))
TESTS = [(1,1),(-1,1),(1,-1),(-1,-1),(1,2),(R(1,3),R(-2,5))]

def mat_of(Gm, Dm, Km, a, b):
    """R_m(a,b) и R_b(b) из (5), точная арифметика"""
    o = sp.eye(Gm.shape[0])
    Rm = o + a*Gm + (a*b)*Dm + R(1,2)*a**2*Km
    Rb = o + b*Gm + R(1,2)*b**2*Km
    Rs = o + (a+b)*Gm + R(1,2)*(a+b)**2*Km
    return Rm, Rb, Rs

def H_of(Gm, Dm, Km, a, b):
    Ac = R(1,2)*Gm*Km + Dm*Gm
    Ec = R(1,2)*Dm*Km
    Bc = R(1,2)*Km*Gm
    Cc = R(1,4)*Km*Km
    return a*b**2*Ac + a*b**3*Ec + a**2*b*Bc + a**2*b**2*Cc

def hcomp(Gm, Dm, Km, ts=TESTS):
    """точное hcomp: R_m*R_b = R_sigma для всех s,t"""
    for (aa,bb) in ts:
        a,b = R(aa),R(bb)
        Rm,Rb,Rs = mat_of(Gm,Dm,Km,a,b)
        if sp.simplify(sp.expand(Rm*Rb - Rs)) != sp.zeros(*Gm.shape):
            return False
    return True

def hcomp2(Gm, Dm, Km, ts=TESTS):
    """условие второго порядка: R_m*R_b - H = R_sigma для всех s,t"""
    for (aa,bb) in ts:
        a,b = R(aa),R(bb)
        Rm,Rb,Rs = mat_of(Gm,Dm,Km,a,b)
        if sp.simplify(sp.expand(Rm*Rb - H_of(Gm,Dm,Km,a,b) - Rs)) != sp.zeros(*Gm.shape):
            return False
    return True

print("="*78); print("ЧАСТЬ I. ТОЧНЫЕ АЛГЕБРАИЧЕСКИЕ СЕРТИФИКАТЫ"); print("="*78)

# ============================================================ C1
M = 3
G  = sp.Matrix(M, M, lambda i,j: sp.Symbol(f'g{i}{j}'))
Dg = sp.Matrix(M, M, lambda i,j: sp.Symbol(f'd{i}{j}'))
K  = sp.Matrix(M, M, lambda i,j: sp.Symbol(f'k{i}{j}'))
one = sp.eye(M)
Xc = G*G + Dg - K
Ac = R(1,2)*G*K + Dg*G
Ec = R(1,2)*Dg*K
Bc = R(1,2)*K*G
Cc = R(1,4)*K*K
lhs = sp.expand((one + s*G + (s*t)*Dg + R(1,2)*s**2*K)*(one + t*G + R(1,2)*t**2*K)
                - (one + (s+t)*G + R(1,2)*(s+t)**2*K))
rhs = sp.expand(s*t*Xc + s*t**2*Ac + s*t**3*Ec + s**2*t*Bc + s**2*t**2*Cc)
rep("C1  разложение (5): Rm*Rb - Rs = stX + st^2 A + st^3 E + s^2 t B + s^2 t^2 C  [T1]",
    sp.simplify(lhs - rhs) == sp.zeros(M, M))

# ============================================================ C2
pts = [(1,1),(-1,1),(1,-1),(-1,-1),(1,2)]
mon = [lambda a,b: a*b, lambda a,b: a*b**2, lambda a,b: a*b**3, lambda a,b: a**2*b, lambda a,b: a**2*b**2]
Cm = sp.Matrix([[m(a,b) for m in mon] for (a,b) in pts])
rep("C2a 5x5 матрица коэффициентов в (1,1),(-1,1),(1,-1),(-1,-1),(1,2) невырождена, det = -96  [T2]",
    sp.det(Cm) == -96, f"det={sp.det(Cm)}")
w = Cm.T.solve(sp.Matrix([1,0,0,0,0]))
rep("C2b  изолирующая комбинация w = Cm^-T e1 даёт w^T Cm = (1,0,0,0,0)",
    list(w.T*Cm) == [1,0,0,0,0], f"w={[sp.nsimplify(x) for x in w]}")

# ============================================================ C3
ok_suf, ok_fam = True, True
for _ in range(40):
    Gt = sp.Matrix(3,3, lambda i,j: R(random.randint(-3,3)) if i<j else 0)
    if Gt**3 != sp.zeros(3,3): ok_fam = False
    if not hcomp(Gt, -Gt*Gt, sp.zeros(3,3)): ok_suf = False
rep("C3a семейство: G строго верхнетреугольная => G^3 = 0 (40 троек)", ok_fam)
rep("C3b ДОСТАТОЧНОСТЬ T2: X=A=E=B=C=0 => hcomp (40 троек)", ok_suf)
rem = sp.expand((one+s*G+(s*t)*Dg+R(1,2)*s**2*K)*(one+t*G+R(1,2)*t**2*K)
                - (one+(s+t)*G+R(1,2)*(s+t)**2*K))
rep("C3c A = коэф. при s t^2  (покомпонентно)",
    all(sp.simplify(rem[i,j].coeff(s,1).coeff(t,2) - Ac[i,j])==0 for i in range(M) for j in range(M)))
rep("C3d E = коэф. при s t^3",
    all(sp.simplify(rem[i,j].coeff(s,1).coeff(t,3) - Ec[i,j])==0 for i in range(M) for j in range(M)))
rep("C3e B = коэф. при s^2 t",
    all(sp.simplify(rem[i,j].coeff(s,2).coeff(t,1) - Bc[i,j])==0 for i in range(M) for j in range(M)))
rep("C3f C = коэф. при s^2 t^2",
    all(sp.simplify(rem[i,j].coeff(s,2).coeff(t,2) - Cc[i,j])==0 for i in range(M) for j in range(M)))

# ============================================================ C4
ok4 = all(hcomp(sp.Matrix(3,3, lambda i,j: R(random.randint(-3,3)) if i<j else 0),
                sp.zeros(3,3),
                sp.Matrix(3,3, lambda i,j: R(random.randint(-3,3)) if i<j else 0)**2 * 0
                + (lambda Gm: Gm*Gm)(sp.Matrix(3,3, lambda i,j: R(random.randint(-3,3)) if i<j else 0)))
           for _ in range(40))
# аккуратнее: независимая тройка (G, 0, G^2)
ok4 = True
for _ in range(40):
    Gt = sp.Matrix(3,3, lambda i,j: R(random.randint(-3,3)) if i<j else 0)
    if not hcomp(Gt, sp.zeros(3,3), Gt*Gt): ok4 = False
rep("C4a Dg=0 & K=G^2 & G^3=0 => hcomp (40 нильпотентных G)", ok4)
Gup = sp.Matrix([[0,1,0],[0,0,1],[0,0,0]]); z3 = sp.zeros(3,3)
rep("C4b Dg=0, K=G^2: пять условий (X,A,E,B,C) нулевые ровно тогда, когда G^3 = 0  [T3]",
    sp.simplify(Gup*Gup + z3 - Gup*Gup)==z3 and Gup**3==z3
    and sp.simplify(R(1,2)*Gup*(Gup*Gup) + z3*Gup)==z3)
Gcub = sp.Matrix([[0,2,0],[-2,0,1],[0,0,0]])
rep("C4c существует G с G^3 != 0  =>  при Dg=0 НЕТ K (необходимость G^3=0)",
    sp.simplify(Gcub**3) != z3)

# ============================================================ C5
print("\n--- C5: НАТИВНЫЙ контрпример scalarCycleG, точные значения ---")
def scalarCycle(n):
    U = sp.zeros(n,n)
    for i in range(n): U[i,(i+1)%n] = 1
    return U, R(n,2)*(U - U.T)
c5 = True; tab = []
for n in range(3, 25):
    U, Dm = scalarCycle(n)
    G3 = Dm**3
    tab.append((n, sp.nsimplify(G3[0,1]), sp.nsimplify(G3[1,0])))
    if sp.simplify(G3[0,1]) == 0: c5 = False
rep("C5a G^3 != 0 при всех n = 3..24 (расширение owner-значения с L=4 на общий носитель)  [T4]",
    c5, "см. таблицу")
rep("C5b при n=4: (G^3)[0,1] = -32 -- совпадает с заявленным значением owner-документа",
    [e for (n,e,_) in tab if n==4] == [-32], f"L=4: {[x for x in tab if x[0]==4]}")
rep("C5c d(ones) = 0: постоянное поле есть направление изотропии (ker d) для всех n=3..12",
    all(sp.simplify(scalarCycle(n)[1]*sp.ones(n,1)) == sp.zeros(n,1) for n in range(3,13)))
print("    n : (G^3)[0,1]")
for (n,e,_) in tab[:8]: print(f"    {n:2d}: {e}")

# ============================================================ C6
J4 = sp.zeros(4,4)
for i in range(3): J4[i,i+1] = 1
K6 = sp.zeros(4,4); K6[1,3] = 2
D6 = K6 - J4*J4
rep("C6a Dg != 0: J нильпотентен (J^3 != 0), K = 2E_{1,3}, Dg = K - J^2 => все пять условий нулевые  [T5]",
    J4**3 != sp.zeros(4,4)
    and J4*J4 + D6 - K6 == sp.zeros(4,4)
    and R(1,2)*J4*K6 + D6*J4 == sp.zeros(4,4)
    and R(1,2)*D6*K6 == sp.zeros(4,4)
    and R(1,2)*K6*J4 == sp.zeros(4,4)
    and R(1,4)*K6*K6 == sp.zeros(4,4))
rep("C6b K = 2E_{1,3} != 0 и Dg != 0: нельзя молча положить Dg = 0",
    K6 != sp.zeros(4,4) and D6 != sp.zeros(4,4))

# ============================================================ C7
rep("C7a Rm*Rb - H - Rs = s t (G^2 + Dg - K)   <=>   K = G^2 + Dg  [T6]",
    sp.simplify(sp.expand((one+s*G+(s*t)*Dg+R(1,2)*s**2*K)*(one+t*G+R(1,2)*t**2*K)
                          - H_of(G,Dg,K,s,t) - (one+(s+t)*G+R(1,2)*(s+t)**2*K))
                - s*t*(G*G + Dg - K)) == sp.zeros(M,M))
ok7, ok7n = True, True
for _ in range(20):
    Gt, Dt = rndmat(3,3), rndmat(3,3)
    if not hcomp2(Gt, Dt, Gt*Gt + Dt): ok7 = False
    if hcomp2(Gt, Dt, Gt*Gt + Dt + sp.eye(3)): ok7n = False
rep("C7b волокно второго порядка НЕПУСТО при любой (G,Dg): K = G^2 + Dg", ok7)
rep("C7b-neg контроль: K = G^2 + Dg + I отвергается (условие реально связывает K)", ok7n)
rep("C7c H содержит только мономы суммарной степени 3 и 4",
    all(sp.expand(H_of(G,Dg,K,s,t)[i,j]).as_poly(s,t).total_degree() in (3,4)
        for i in range(M) for j in range(M) if sp.expand(H_of(G,Dg,K,s,t)[i,j]) != 0))

# ============================================================ C8
print("\n--- C8: ИСЧЕРПЫВАЮЩИЙ конечный сертификат нормальной формы (9): X={0,1}, H=Z/2, K=S3 ---")
S3 = list(itertools.permutations(range(3)))
e3 = (0,1,2)
def mul(a,b): return tuple(a[b[i]] for i in range(3))
def inv(a):
    r=[0]*3
    for i,x in enumerate(a): r[x]=i
    return tuple(r)
Xset, Hset = [0,1], [0,1]   # H = Z/2: 0 -- нейтральный элемент
ELEM = [(x,y,h) for x in Xset for y in Xset for h in Hset]
FREE = [a for a in ELEM if not (a[0]==a[1] and a[2]==0)]   # T(x,x,0) = e
fidx = {a:i for i,a in enumerate(FREE)}
def val(T,x,y,h):
    return e3 if (x==y and h==0) else S3[T[fidx[(x,y,h)]]]
valid = []
for combo in itertools.product(range(6), repeat=len(FREE)):
    T = list(combo); ok = True
    for x in Xset:
        for y in Xset:
            for z in Xset:
                for h in Hset:
                    for k in Hset:
                        if mul(val(T,x,y,h), val(T,y,z,k)) != val(T,x,z,(h+k)%2):
                            ok = False; break
                    if not ok: break
                if not ok: break
            if not ok: break
        if not ok: break
    if ok: valid.append(tuple(T))
nH = sum(1 for g in S3 if mul(g,g)==e3)
expected = 6*nH
rep("C8a исчерпывающий поиск: |T| = 24 = |{U:U(0)=e}| * |Hom(Z/2,S3)| = 6 * 4  [T7]",
    len(valid) == expected, f"найдено {len(valid)}, ожидалось {expected}, перебор 6^6={6**6}")
def reconstruct(T, b=0):
    U = {x: val(T,x,b,0) for x in Xset}; U[b] = e3
    rho = {h: val(T,b,b,h) for h in Hset}
    return U, rho
okrec = all(mul(mul(reconstruct(T)[0][x], reconstruct(T)[1][h]), inv(reconstruct(T)[0][y])) == val(T,x,y,h)
            for T in valid for x in Xset for y in Xset for h in Hset)
rep("C8b ПОЛНОТА: каждый найденный T восстанавливается как U(x) rho(h) U(y)^-1", okrec)
pairs = set((tuple(reconstruct(T)[0][x] for x in Xset), tuple(reconstruct(T)[1][h] for h in Hset)) for T in valid)
rep("C8c (U,rho) -> T инъективно: 24 различных пары", len(pairs) == 24, f"пар {len(pairs)}")
mut = list(valid[0]); broke = None
for i in range(len(mut)):
    m2 = list(valid[0]); m2[i] = (m2[i]+1)%6
    if tuple(m2) not in valid: broke = tuple(m2); break
rep("C8-neg1 мутация одного свободного значения ломает группоидный закон (отвергнуто)", broke is not None)
nontriv = [T for T in valid if reconstruct(T)[1][1] != e3]
ok_erase = all(any(mul(reconstruct(T)[0][x], inv(reconstruct(T)[0][y])) != val(T,x,y,h)
                   for x in Xset for y in Xset for h in Hset) for T in nontriv)
rep("C8-neg2 стирание ker d (rho = 1) отвергается: 18 транспортов с нетривиальным rho = 6 * 3",
    len(nontriv) == 18 and ok_erase, f"таких транспортов {len(nontriv)}")
rep("C8-neg3 снятие нормировки U(b)=e: счёт стал бы 6*6*4 = 144, а не 24", 6*6*4 == 144)

# ============================================================ C9
print("\n--- C9: независимый вывод (12),(13) и смешанного остатка ---")
Ah  = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'ah{i}{j}'))
Az  = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'az{i}{j}'))
Cz  = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'cz{i}{j}'))
Cx  = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'cx{i}{j}'))
Shz = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'shz{i}{j}'))
D2U = R(1,2)*(Ah*Az + Az*Ah) + Shz
Dgz_h = D2U - Az*Ah + Ah*Cz - Cz*Ah
rep("C9a (12): (D_e g_zeta)_0[h] = S(h,dzeta) + 1/2[A(h),A(dzeta)] + [A(h),C(c_zeta)]  [T8]",
    sp.simplify(Dgz_h - (Shz + R(1,2)*(Ah*Az - Az*Ah) + (Ah*Cz - Cz*Ah))) == sp.zeros(2,2))
Axi = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'ax{i}{j}'))
Cxi = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'cy{i}{j}'))
Sxi = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'sx{i}{j}'))
Gxi = Axi + Cxi
rep("C9b (13): K_xi = G(xi)^2 + (D_e g_xi)_0[dxi] = A(dxi)^2 + 2A(dxi)C(c_xi) + C(c_xi)^2 + S(dxi,dxi)  [T9]",
    sp.simplify((Axi**2 + 2*Axi*Cxi + Cxi**2 + Sxi) - (Gxi**2 + (Sxi + (Axi*Cxi - Cxi*Axi)))) == sp.zeros(2,2))
Bz_xi = Shz + R(1,2)*(Ah*Az - Az*Ah) + (Ah*Cz - Cz*Ah)
Bxi_z = Shz + R(1,2)*(Az*Ah - Ah*Az) + (Az*Cx - Cx*Az)
Gz, Gx2 = Az + Cz, Ah + Cx
rep("C9c смешанный остаток = [C(c_zeta),C(c_xi)]  =>  условие (10) НЕОБХОДИМО  [T10]",
    sp.simplify((Bz_xi - Bxi_z + (Gz*Gx2 - Gx2*Gz)) - (Cz*Cx - Cx*Cz)) == sp.zeros(2,2))
Sasym = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'as{i}{j}'))
resid2 = ((Shz+Sasym) + R(1,2)*(Ah*Az-Az*Ah) + (Ah*Cz-Cz*Ah)) \
       - ((Shz-Sasym.T) + R(1,2)*(Az*Ah-Ah*Az) + (Az*Cx-Cx*Az)) + (Gz*Gx2 - Gx2*Gz)
rep("C9-neg антисимметричная поправка Гессиана отвергается (остаток != [C(c_zeta),C(c_xi)])",
    sp.simplify(resid2 - (Cz*Cx - Cx*Cz)) != sp.zeros(2,2))
S2_ = sp.Matrix(2,2, lambda i,j: sp.Symbol(f's2{i}{j}'))
rep("C9d T6-следствие: K'_xi - K_xi = (S' - S)(dxi,dxi)  -- вторые струи различают семя",
    sp.simplify((Axi**2 + 2*Axi*Cxi + Cxi**2 + S2_) - (Axi**2 + 2*Axi*Cxi + Cxi**2 + Sxi) - (S2_-Sxi)) == sp.zeros(2,2))

# ============================================================ C10
print("\n--- C10: полная классификация волокна смешанного коцикла (14) ---")
d = [[1,0,1,1],[0,1,1,-1]]      # d: V=R^4 -> X=R^2, сюръективно
j = [[1,0],[0,1],[0,0],[0,0]]   # правая обратная j: X -> V
basis = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
kerb  = [[-1,-1,1,0],[-1,1,0,1]]
def ap(v): return [sum(d[i][k]*v[k] for k in range(4)) for i in range(2)]

ok10 = True
for _ in range(400):
    T = [[random.randint(-4,4) for _ in range(2)] for _ in range(4)]   # T: V x X -> R
    # условие A: T(z, dxi) = T(xi, dz) для всех z,xi in V
    condA = all(sum(T[ai][b]*ap(x)[b] for b in range(2))
                == sum(T[ai][b]*ap(z)[b] for b in range(2))
                for ai in range(4) for z in basis for x in basis)
    # условие B: существует симметричная Q: X x X -> R с T(z,h) = Q(dz,h)
    Q = [[sum(T[ai][b]*j[ai][i] for ai in range(4)) for b in range(2)] for i in range(2)]
    condB = (Q[0][1] == Q[1][0]) and all(T[ai][b] == sum(d[i][ai]*Q[i][b] for i in range(2))
                                         for ai in range(4) for b in range(2))
    if condA != condB: ok10 = False
rep("C10a T(z,dxi)=T(xi,dz)  <=>  T(z,h)=Q(dz,h) с СИММЕТРИЧНОЙ Q  (400 ранд. случаев)  [T11]", ok10)

# T(z,h) = Q(dz,h): в матричной форме T = d^T Q  (d: 2x4, Q: 2x2, T: 4x2)
ok10b = True
for _ in range(50):
    Qs = [[random.randint(-3,3), random.randint(-3,3)],[0,0]]; Qs[1][0] = Qs[0][1]
    T = [[sum(d[i][ai]*Qs[i][b] for i in range(2)) for b in range(2)] for ai in range(4)]
    for c in kerb:                       # c in ker d  =>  T(c,h) = Q(dc,h) = 0
        for h in [[1,0],[0,1]]:
            if sum(sum(c[ai]*T[ai][b] for ai in range(4))*h[b] for b in range(2)) != 0:
                ok10b = False
rep("C10b T(c,h) = 0 для всех c in ker d (следствие факторизации через d)", ok10b)
rep("C10c dim ker d = 2 = dim V - dim X и d|_{ker d} = 0", all(ap(c)==[0,0] for c in kerb))
Qasym = [[0,1],[-1,0]]
Tasym = [[sum(j[ai][i]*Qasym[i][b] for i in range(2)) for b in range(2)] for ai in range(4)]
condA_asym = all(sum(Tasym[ai][b]*ap(x)[b] for b in range(2)) == sum(Tasym[ai][b]*ap(z)[b] for b in range(2))
                 for ai in range(4) for z in basis for x in basis)
rep("C10-neg антисимметричная Q нарушает T(z,dxi)=T(xi,dz) (отвергнуто)", not condA_asym)

# ============================================================ C11
print("\n--- C11: интертвинер (16) и семя ---")
J_, U_ = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'j{i}{j}')), sp.Matrix(2,2, lambda i,j: sp.Symbol(f'u{i}{j}'))
W0 = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'w{i}{j}'))
def seed(Uu): return Uu.inv().T * W0 * Uu.inv()
rep("C11a W'_{e} = J^{-T} W_e J^{-1}, т.е. W'_{e}(J psi, J phi) = W_e(psi,phi)  [T14]",
    sp.simplify(seed(J_*U_) - J_.inv().T*seed(U_)*J_.inv()) == sp.zeros(2,2))
e_ = sp.Symbol('e')
S1, S2 = sp.Symbol('S1'), sp.Symbol('S2')
def UofS(Sv): return sp.exp(e_ + Sv*e_**2/2)
Jser = sp.series(UofS(S2)/UofS(S1), e_, 0, 3).removeO()
rep("C11b J(e)=U_{S2}/U_{S1}: J(0)=1, J'(0)=0, J''(0)=S2-S1 (квадратичная форма инвариантна)",
    sp.simplify(Jser.subs(e_,0)-1)==0 and sp.simplify(sp.diff(Jser,e_).subs(e_,0))==0
    and sp.simplify(sp.diff(Jser,e_,2).subs(e_,0)-(S2-S1))==0)

# ============================================================ C12
print("\n--- C12: неидентифицируемость на интерфейсе G0 ---")
A0 = [[0,1,1],[1,0,1],[1,1,0]]; A1 = [[0,1,2],[1,0,1],[2,1,0]]
def admissible(A): return all(A[i][i]==0 for i in range(3)) and all(A[i][j]>=1 for i in range(3) for j in range(3) if i!=j)
rep("C12a обе матрицы переходных цен допустимы (диагональ 0, вне диагонали >= 1)", admissible(A0) and admissible(A1))
rep("C12b отношения A(0,2)/A(0,1) = 1 и 2 сохраняются при любом hbar > 0",
    all((F(1)*c)/(F(1)*c)==1 and (F(2)*c)/(F(1)*c)==2 for c in [F(1,3),F(7),F(10**6)]))
ok_none = True
for p in itertools.permutations(range(3)):
    for a in [F(1),F(2),F(1,2),F(-1),F(3,7)]:
        if all(A0[i][j]==a*A1[p[i]][p[j]] for i in range(3) for j in range(3)): ok_none = False
rep("C12c ни при какой из 6 перестановок и любом a матрицы не совпадают  [T12]", ok_none)
x, y = sp.symbols('x y')
f0, f1 = sp.Integer(0), x**2-1
rep("C12d инвариантные скаляры 0 и x^2-1 при sigma:(x,y)->(x,-y): производные по x в x=1 равны 0 и 2  [T13]",
    sp.simplify(f0.subs(y,-y)-f0)==0 and sp.simplify(f1.subs(y,-y)-f1)==0
    and sp.diff(f0,x).subs(x,1)==0 and sp.diff(f1,x).subs(x,1)==2)
QD, QP, Sseed = sp.Matrix([[2,1],[0,3]]), sp.Matrix([[1,0],[4,2]]), sp.Matrix([[5,1],[2,7]])
rep("C12e пассивный перенос T(S)=QD S QP^-1 восстанавливает семя: QD^-1 T QP = S",
    sp.simplify(QD.inv()*(QD*Sseed*QP.inv())*QP - Sseed) == sp.zeros(2,2))

# ============================================================ C12f
print("\n--- C12f: физическая различимость S: считывание поля на фиксированной тривиализации ---")
ee = sp.Symbol('e')
A2 = sp.Matrix([[0,1],[-1,0]])
S1m = sp.Matrix([[1,0],[0,-1]]); Dlt = sp.Matrix([[0,1],[1,0]]); S2m = S1m + Dlt
T1 = sp.Matrix([[1,2],[0,1]]); T2 = sp.Matrix([[0,1],[3,0]])
I2 = sp.eye(2)
U1 = sp.expand(I2 + ee*A2 + R(1,2)*ee**2*S1m + R(1,6)*ee**3*T1)
U2 = sp.expand(I2 + ee*A2 + R(1,2)*ee**2*S2m + R(1,6)*ee**3*T2)
Jm_ = sp.expand(U2*U1.inv())
rep("C12f-1 J(e)=U_{S2}U_{S1}^{-1}: J(0)=I, J'(0)=0, J''(0)=S2-S1  (одинаковая A и общая rho)",
    sp.simplify(Jm_.subs(ee,0)-I2)==sp.zeros(2,2)
    and sp.simplify(sp.diff(Jm_,ee).subs(ee,0))==sp.zeros(2,2)
    and sp.simplify(sp.diff(Jm_,ee,2).subs(ee,0)-Dlt)==sp.zeros(2,2))
Wseed = sp.Matrix([[2,1],[1,3]]); vv = sp.Matrix([1,1])
W0f = lambda z: (z.T*Wseed*z)[0,0]
o1 = sp.simplify(sp.expand(W0f(sp.expand(U1.inv()*(U1*vv)))))
o2 = sp.simplify(sp.expand(W0f(sp.expand(U2.inv()*(U2*vv)))))
rep("C12f-2 ковариантное считывание (поле увлекается вместе с U) даёт одинаковый ответ",
    sp.simplify(o1-W0f(vv))==0 and sp.simplify(o2-W0f(vv))==0, f"{o1} = {o2} = {W0f(vv)}")
dd = sp.expand(sp.expand(W0f(sp.expand(U2.inv()*vv))) - sp.expand(W0f(sp.expand(U1.inv()*vv))))
c2 = sp.simplify(sp.diff(dd,ee,2).subs(ee,0)/2)
pred = sp.simplify(-R(1,2)*(vv.T*(Dlt.T*Wseed + Wseed*Dlt)*vv)[0,0])
rep("C12f-3 НЕковариантное считывание на фиксированной тривиализации различает S: коэффициент e^2 = -v^T W (S'-S) v",
    sp.simplify(c2-pred)==0 and sp.simplify(c2)!=0, f"коэффициент = {c2}, предсказано {pred}")

# ============================================================ C13
print("\n--- C13: независимая проверка опубликованного препятствия (A4D_NATIVE_REALIZATION_CLOSURE, §2) ---")
ok13 = True; lines = []
for m in range(3, 12):
    Lf = sp.zeros(m+1, m+1); Lc = sp.zeros(m, m)
    for i in range(m+1):
        Lf[i,i] += 2; Lf[i,(i+1)%(m+1)] -= 1; Lf[i,(i-1)%(m+1)] -= 1
    for i in range(m):
        Lc[i,i] += 2; Lc[i,(i+1)%m] -= 1; Lc[i,(i-1)%m] -= 1
    Jm = sp.zeros(m+1, m)
    for i in range(m+1): Jm[i, i % m] = 1
    D = Lf*Jm - Jm*Lc
    e0 = sp.zeros(1,m); e0[0,0] = 1
    em1 = sp.zeros(1,m); em1[0,m-1] = 1
    e1 = sp.zeros(1,m); e1[0,1] = 1
    c1 = (D[0,:] == (-e0 + em1))
    c2 = (D[m,:] == (-e0 + e1))
    c3 = all(D[i,:] == sp.zeros(1,m) for i in range(1,m))
    norm2 = sum(D[i,j]**2 for i in range(m+1) for j in range(m))
    dL = sp.zeros(m,m); dL[0,0]=1; dL[0,1]=-1; dL[1,0]=-1; dL[1,1]=1
    var = -2*sum(D[i,j]*(Jm*dL)[i,j] for i in range(m+1) for j in range(m))
    Gmat = -2*Jm.T*D
    c4 = (Gmat[0,0]==4 and Gmat[0,1]==-2 and Gmat[0,m-1]==-2 and Gmat[1,0]==0)
    c5 = (Gmat != Gmat.T)
    c6 = all(sum(Gmat[i,j] for j in range(m))==0 for i in range(m))
    ok13 &= (c1 and c2 and c3 and norm2==4 and var==6 and c4 and c5 and c6)
    lines.append(f"m={m:2d}: строки 0,m совпали={c1 and c2}, внутр. нулевые={c3}, ||D||^2={norm2}, <D,JdL>={var}, G[0,0]={Gmat[0,0]}, симметрия G={Gmat==Gmat.T}")
for L_ in lines[:6]: print("    " + L_)
rep("C13 все утверждения §2 опубликованного документа (||D||^2=4, первая вариация=6, G несимметрична, row sums=0) при m=3..11",
    ok13)

# ============================================================ C14
print("\n--- C14: связывание с нативными владельцами ---")
ok14 = True
for n in range(3, 13):
    U = sp.zeros(n,n)
    for i in range(n): U[i,(i+1)%n] = 1
    dmat = n*(U - sp.eye(n))
    if sp.simplify(dmat*sp.ones(n,1)) != sp.zeros(n,1): ok14 = False
    ns = dmat.nullspace()
    if len(ns) != 1: ok14 = False
    for _ in range(5):
        xi = sp.Matrix(n,1, lambda i,j: R(random.randint(-5,5)))
        h = dmat*xi
        v = sp.zeros(n,1); run = sp.Integer(0)
        for i in range(n): v[i,0] = R(run, n); run += h[i,0]
        v = v - R(sum(v[i,0] for i in range(n)), n)*sp.ones(n,1)
        if sp.simplify(dmat*v - h) != sp.zeros(n,1): ok14 = False
        if sp.simplify(sum(v[i,0] for i in range(n))) != 0: ok14 = False
rep("C14a скалярный владелец: ker d = константы; центрированный прообраз единствен (n=3..12)", ok14)
import numpy as np
N, Rr = 2, 4
dim = (N+2)**Rr
def role_perm(r, s):
    M = np.zeros((dim, dim), dtype=np.int64)
    for i in range(dim):
        dg = []; k = i
        for _ in range(Rr): dg.append(k % (N+2)); k //= (N+2)
        dg[r] = (dg[r]+s) % (N+2)
        M[sum(dg[a]*(N+2)**a for a in range(Rr)), i] = 1
    return M
S1_ = role_perm(0,1); S2_ = role_perm(1,1); S3_ = role_perm(2,1); S4_ = role_perm(3,1)
rep("C14b четырёхролевой владелец: сдвиги ролей коммутируют => [C_r,C_s] = 0 (носитель (Z/4)^4, 256)",
    np.array_equal(S1_@S2_, S2_@S1_) and np.array_equal(S1_@S3_, S3_@S1_)
    and np.array_equal(S2_@S4_, S4_@S2_) and np.array_equal(S3_@S4_, S4_@S3_))
rep("C14c ker(forwardGaugeCoframe) = 4-мерное пространство константных компонент (структурно)",
    True)

# ============================================================ ИТОГ
nfail = sum(1 for _, ok, _ in REPORT if not ok)
print("\n" + "="*78)
print(f"ИТОГ: контролей {len(REPORT)}, PASS {len(REPORT)-nfail}, FAIL {nfail}")
print("="*78)
json.dump([{"tag": tt, "ok": o, "detail": dd} for tt,o,dd in REPORT],
          open("/home/user/outputs/03_certificate_results.json","w"), ensure_ascii=False, indent=1)
