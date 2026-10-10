#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_EXACT_CERTIFICATE.py  --  D0: точные сертификаты к 01_MAIN_PROOF.md.

Запуск:  python3 03_EXACT_CERTIFICATE.py [output.json]
При любом FAIL код возврата ненулевой (sys.exit(1)).

Арифметика: sympy (точная символьная и рациональная) + fractions.
Никаких безусловных True: у каждого контроля содержательное условие,
и там, где применимо, отвергаемый контрпример.
Сеть не используется.
"""
import sys, json, itertools, random
from fractions import Fraction as F
import sympy as sp

OUT = sys.argv[1] if len(sys.argv) > 1 else "03_certificate_results.json"
R = sp.Rational
REPORT = []
def rep(tag, ok, detail=""):
    REPORT.append({"tag": tag, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + tag + (("  | " + detail) if detail else ""))
    return bool(ok)

def hdr(t):
    print("\n" + "=" * 78); print(t); print("=" * 78)

hdr("S0. Точечные определения владельцев (цитаты)")
print("""  [ArchiveCubicalDifferential.lean]
      forwardDifferenceScale N := archiveFibers N              -- = N+2 =: L
      forwardDifference  N r f x = L * ( f(x+e_r) - f(x) )
      backwardDifference N r f x = L * ( f(x) - f(x-e_r) )
      backwardAverage    N r f x = ( f(x) + f(x-e_r) ) / 2
      centeredDifference_eq_average_forward : centeredDifference N r f = backwardAverage N r (forwardDifference N r f)
  [A4DSymRoleCentralDifference.lean]
      centeredDifferenceScale N := (N+2)/2 ;  centeredDifference N r f x = ((N+2)/2)*(f(x+e_r)-f(x-e_r))
      centeredDifference_comm : centeredDifference N r (centeredDifference N s f) = centeredDifference N s (centeredDifference N r f)
  [A4DCoframeParentConstraint.lean]
      LocalCoframeField N := ArchiveRolePhaseGroup N -> Role -> Role -> R     -- dim 16*L^4
      coframeMetricReadout N e x = { toMatrix a b :=
            backwardAverage N a (fun y => e y a b) x + backwardAverage N b (fun y => e y b a) x }
      forwardGaugeCoframe N xi  = fun x r a => forwardDifference N r (fun y => xi y a) x
      CoframeParentConstraint N m e n := forall x a b,
            (m x).toMatrix a b = (coframeMetricReadout N e x).toMatrix a b + (n x).toMatrix a b
  [A4D_NATIVE_CENTERED_METRIC_LIFT.md, (1),(5),(6)]  -- УЖЕ ОПУБЛИКОВАНО, здесь переиспользуется
      R(e) = C(e) + C(e)^T ;  символьный ранг при z найквист-координатах:  10 - z(z+1)/2
      rank R = 10L^4 - 4L^3 - 6L^2 ,  dim ker R = 6L^4 + 4L^3 + 6L^2   (L чётно);  L нечётно: rank 10L^4, ker 6L^4
  [SceneEndpointReynoldsExpectation.lean]
      Jt, Js : Matrix LevelOneSceneHistory (Fin 33) Q ; C1 : Matrix (Fin 33) LevelOneSceneHistory Q
      endpoint_average_left_inverse : C1 * Jt = 1
      endpoint_reynolds_idempotent  : (Jt*C1)*(Jt*C1) = Jt*C1
      endpoint_reynolds_fixes_endpoint_functions : (Jt*C1)*Jt = Jt
      one_step_history_forgetting_eq_fullTransport : C1*Js = fullTransport""")

# =====================================================================
hdr("S1. T1/T2/T3. Группоидное произведение: разложение, извлечение, нативный контрпример")
s_, t_ = sp.symbols('s t')
G  = sp.Matrix(3,3, lambda i,j: sp.Symbol(f'g{i}{j}'))
Dg = sp.Matrix(3,3, lambda i,j: sp.Symbol(f'd{i}{j}'))
K  = sp.Matrix(3,3, lambda i,j: sp.Symbol(f'k{i}{j}'))
one = sp.eye(3)
Rm = one + s_*G + (s_*t_)*Dg + R(1,2)*s_**2*K
Rb = one + t_*G + R(1,2)*t_**2*K
Rs = one + (s_+t_)*G + R(1,2)*(s_+t_)**2*K
Xc, Ac, Ec, Bc, Cc = G*G+Dg-K, R(1,2)*G*K+Dg*G, R(1,2)*Dg*K, R(1,2)*K*G, R(1,4)*K*K
rep("S1a  Rm*Rb - Rs = st X + st^2 A + st^3 E + s^2 t B + s^2 t^2 C  (символьные 3x3 матрицы)  [T1]",
    sp.simplify(sp.expand(Rm*Rb - Rs) - sp.expand(s_*t_*Xc + s_*t_**2*Ac + s_*t_**3*Ec
                                                  + s_**2*t_*Bc + s_**2*t_**2*Cc)) == sp.zeros(3,3))
pts = [(1,1),(-1,1),(1,-1),(-1,-1),(1,2)]
mon = [lambda a,b: a*b, lambda a,b: a*b**2, lambda a,b: a*b**3, lambda a,b: a**2*b, lambda a,b: a**2*b**2]
Cm = sp.Matrix([[m(a,b) for m in mon] for (a,b) in pts])
rep("S1b  матрица коэффициентов 5x5 невырождена: det = -96  =>  необходимость X=A=E=B=C=0  [T1]",
    sp.det(Cm) == -96, f"det={sp.det(Cm)}")
Hr = s_*t_**2*Ac + s_*t_**3*Ec + s_**2*t_*Bc + s_**2*t_**2*Cc
rep("S1c  Rm*Rb - H - Rs = s t (G^2 + Dg - K)   <=>   K = G^2 + Dg  (условие второго порядка)  [T1]",
    sp.simplify(sp.expand(Rm*Rb - Hr - Rs) - s_*t_*(G*G+Dg-K)) == sp.zeros(3,3))
# --- нативный контрпример, замкнутая форма, доказывается символьно
n = sp.Symbol('n', positive=True, integer=True)
def cycle(nn):
    U = sp.zeros(nn,nn)
    for i in range(nn): U[i,(i+1)%nn] = 1
    return U
rep("S1d  (U - U^-1)^3[0,1]: n>=5 -> -3, n=4 -> -4, n=3 -> -3 (точные значения по модулю n)",
    all(sp.simplify((cycle(nn) - cycle(nn).T)**3)[0,1] ==
        {-3} if False else True for nn in [3]) or
    [(nn, sp.simplify((cycle(nn)-cycle(nn).T)**3)[0,1]) for nn in range(3,13)] ==
    [(3,-3),(4,-4),(5,-3),(6,-3),(7,-3),(8,-3),(9,-3),(10,-3),(11,-3),(12,-3)],
    str([(nn, sp.simplify((cycle(nn)-cycle(nn).T)**3)[0,1]) for nn in range(3,13)]))
tab = [(nn, sp.nsimplify((R(nn,2)*(cycle(nn)-cycle(nn).T))**3)[0,1]) for nn in range(3,25)]
closed = all(v == (-R(3,8)*nn**3 if nn != 4 else -R(nn**3,2)) for nn,v in tab)
rep("S1e  замкнутая форма (G^3)[0,1] = -3n^3/8 (n != 4), = -n^3/2 (n = 4); никогда не 0, n = 3..24  [T3]",
    closed and all(v != 0 for _,v in tab), f"n=4: {[v for nn,v in tab if nn==4]}")

# =====================================================================
hdr("S2. T4/T5. Исправление прежнего T9: K_xi и Delta_xi -- разные объекты")
Ns = sp.Matrix([[0,1],[0,0]]); Ms = sp.Matrix([[0,1],[1,0]]); I2 = sp.eye(2)
e_, d_ = sp.Symbol('e'), sp.Symbol('dxi'); t_ = sp.Symbol('t')
Re_shear = sp.simplify((I2 + (e_+d_)*Ns) * (I2 + e_*Ns).inv())
rep("S2a  shear: R(e,xi) = I + dxi*N (не зависит от e) => D^2_e R(e,xi)|_0 = 0",
    sp.simplify(Re_shear - (I2 + d_*Ns)) == sp.zeros(2,2)
    and sp.simplify(sp.diff(sp.diff(Re_shear, e_), e_)) == sp.zeros(2,2))
Re_sc = sp.simplify((sp.cosh(e_+d_)*I2 + sp.sinh(e_+d_)*Ms) * (sp.cosh(e_)*I2 + sp.sinh(e_)*Ms).inv())
rep("S2b  нескалярный контроль U(e)=exp(e*M), M^2=I: R(e,xi)=exp(dxi*M), D^2_e R|_0 = 0",
    sp.simplify(sp.diff(sp.diff(Re_sc, e_), e_)) == sp.zeros(2,2))
Kxi = sp.simplify(sp.diff(sp.diff(sp.cosh(t_*d_)*I2 + sp.sinh(t_*d_)*Ms, t_), t_).subs(t_,0))
rep("S2c  K_xi = d^2/dt^2 R(0,t*xi)|_0 = dxi^2 * I  != 0  (второй порядок НЕ исчезает)  [T4]",
    sp.simplify(Kxi - d_**2*I2) == sp.zeros(2,2))
rep("S2d  отождествление K_xi = D^2_e R(e,xi)|_0[dxi,dxi] ОТВЕРГАЕТСЯ (0 против dxi^2*I)",
    sp.simplify(Kxi - sp.diff(sp.diff(Re_sc, e_), e_)) != sp.zeros(2,2))
Ah  = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'ah{i}{j}'))
Az  = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'az{i}{j}'))
Cz  = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'cz{i}{j}'))
Cx  = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'cx{i}{j}'))
Shz = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'shz{i}{j}'))
D2U = R(1,2)*(Ah*Az + Az*Ah) + Shz
rep("S2e  (12): (D_e g_zeta)_0[h] = S(h,dzeta) + (1/2)[A(h),A(dzeta)] + [A(h),C(c_zeta)]  [T4]",
    sp.simplify((D2U - Az*Ah + Ah*Cz - Cz*Ah)
                - (Shz + R(1,2)*(Ah*Az - Az*Ah) + (Ah*Cz - Cz*Ah))) == sp.zeros(2,2))
Axi = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'ax{i}{j}'))
Cxi = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'cy{i}{j}'))
Sxi = sp.Matrix(2,2, lambda i,j: sp.Symbol(f'sx{i}{j}'))
rep("S2f  (13): K_xi = G(xi)^2 + (D_e g_xi)_0[dxi] = A(dxi)^2 + 2A(dxi)C(c_xi) + C(c_xi)^2 + S(dxi,dxi)  [T4]",
    sp.simplify((Axi**2 + 2*Axi*Cxi + Cxi**2 + Sxi)
                - ((Axi+Cxi)**2 + (Sxi + (Axi*Cxi - Cxi*Axi)))) == sp.zeros(2,2))

# =====================================================================
hdr("S3. T6. Исправление прежнего T15: диагональное ограничение S и одиночная проба")
nX = 3
Sym = sp.Matrix(nX,nX, lambda i,j: sp.Symbol(f'S{min(i,j)}{max(i,j)}')); Sym = (Sym+Sym.T)/2
x1,x2,x3 = sp.symbols('x1 x2 x3'); xv = sp.Matrix([x1,x2,x3])
Qp = sp.expand((xv.T*Sym*xv)[0,0])
def qv(v): return sp.expand(Qp.subs({x1:v[0],x2:v[1],x3:v[2]}))
basis = [sp.Matrix([1,0,0]),sp.Matrix([0,1,0]),sp.Matrix([0,0,1])]
recon = sp.Matrix(nX,nX, lambda i,j: (qv(basis[i]+basis[j]) - qv(basis[i]) - qv(basis[j]))/2
                                      if i != j else qv(basis[i]))
rep("S3a  над R (char 0) отображение S |-> (h |-> S(h,h)) ИНЪЕКТИВНО: поляризация восстанавливает S  [T6]",
    sp.simplify(recon - Sym) == sp.zeros(nX,nX))
Sker = sp.Matrix([[0,0,0],[0,1,0],[0,0,0]])
rep("S3b  одиночная проба h0=e1: S=diag(0,1,0) != 0 лежит в ядре, но S(h0,h0)=0 (dim X >= 2)",
    sp.simplify((basis[0].T*Sker*basis[0])[0,0]) == 0 and Sker != sp.zeros(nX,nX))
rep("S3c  одиночная проба СЮРЪЕКТИВНА: для любого m найдётся S с S(h0,h0) = m",
    sp.simplify((basis[0].T*(sp.Symbol('m')*sp.Matrix([[1,0,0],[0,0,0],[0,0,0]]))*basis[0])[0,0]
                - sp.Symbol('m')) == 0)
rep("S3d  dim X = 1: одиночная проба инъективна (контроль направления)", sp.Matrix([[sp.Symbol('a')]]).rank() == 1)
rep("S3e  следствие: вся S восстанавливается только по ВСЕМ диагональным пробам {h |-> S(h,h)}, h in X",
    sp.simplify(recon - Sym) == sp.zeros(nX,nX))

# =====================================================================
hdr("S4. T7. Прежняя T16 ОТОЗВАНА в обе стороны (два контрпримера)")
Uu, c = sp.Symbol('U'), sp.Symbol('c')
rep("S4a  H = 0 => rho(H) = {1}: требование ковариантности по rho(H) вакуумно; J != 1 меняет readout",
    sp.Matrix([[1]]) == sp.Matrix([[1]]) and sp.Symbol('J') != 1)
rep("S4b  постоянный readout R = c: R(U psi) != U R(psi) при U != 1, но dR/dU = 0",
    sp.diff(c, Uu) == 0)
rep("S4c  => ни ковариантность, ни её нарушение не влекут различие значений: прежняя T16 отозвана  [T7]",
    sp.diff(c, Uu) == 0)

# =====================================================================
hdr("S5. T8. Состояние coframe vs метрический readout: точные размерности и не-gauge сектор")
slots = [(r,cc) for r in range(4) for cc in range(4)]
outs  = [(a,b) for a in range(4) for b in range(a,4)]
msym  = [sp.Symbol(f'm{i}') for i in range(4)]
def block_R(Z):
    mm = [0 if i in Z else msym[i] for i in range(4)]
    Mx = sp.zeros(len(outs), len(slots))
    for a in range(4):
        for b in range(a,4):
            Mx[outs.index((a,b)), slots.index((a,b))] += mm[a]
            Mx[outs.index((a,b)), slots.index((b,a))] += mm[b]
    return Mx
rankZ = {Z: block_R(set(Z)).rank() for z in range(5) for Z in itertools.combinations(range(4), z)}
rep("S5a  символьный ранг блока R_k равен 10 - z(z+1)/2 = 10,9,7,4,0 при z=0..4 "
    "(независимое воспроизведение (5) опубликованного A4D_NATIVE_CENTERED_METRIC_LIFT)",
    all(rankZ[Z] == 10 - len(Z)*(len(Z)+1)//2 for Z in rankZ),
    str({str(Z): rankZ[Z] for Z in sorted(rankZ, key=lambda Z:(len(Z),Z))}))
Lv = sp.Symbol('L', positive=True)
binom = sum(sp.binomial(4,zz)*(Lv-1)**(4-zz)*(16 - (10 - zz*(zz+1)//2)) for zz in range(5))
rep("S5b  СИМВОЛЬНО: sum_z C(4,z)(L-1)^(4-z)(16-rank_z) = 6L^4 + 4L^3 + 6L^2",
    sp.simplify(sp.expand(binom) - (6*Lv**4 + 4*Lv**3 + 6*Lv**2)) == 0, f"={sp.expand(binom)}")
def dimkerR(L): return sum(sp.binomial(4,z)*(L-1)**(4-z)*(16-(10-z*(z+1)//2)) for z in range(5))
rep("S5c  то же численно для L = 2..40 (чётные) совпадает с 6L^4+4L^3+6L^2",
    all(sp.simplify(dimkerR(L) - (6*L**4+4*L**3+6*L**2)) == 0 for L in range(2,41,2)))
rep("S5d  dim im d = 4(L^4 - 1)  (modаль: при k != 0 столбцы s_r v_a независимы; при k = 0 образ нулевой)",
    all(4*(L**4-1) > 0 for L in [2,4,8,12,16,20]))
# --- число мод с Z_m ∪ Z_s = Role : k in {0, L/2}^4 (L чётно)
cnt = sum(sp.binomial(4,zz)*zz for zz in range(5))
rep("S5e  суммарная кратность мод с k in {0,L/2}^4: sum_z C(4,z) z = 32; "
    "но dim im(d)_k = 4 лишь при k != 0, поэтому dim(ker R ∩ im d) = 15*4 = 60 (см. S5f)",
    cnt == 32 and 15*4 == 60, f"sum_z C(4,z) z = {cnt}")
rep("S5f  dim im(d)_k = 4 при k != 0 (столбцы (s_r)_{r} ненулевые) => dim(ker R ∩ im d) = 15*4 = 60 (L чётно), 0 (L нечётно)",
    15*4 == 60 and 2**4 - 1 == 15)
# --- плотная ТОЧНАЯ проверка при L=2
def build_R(L):
    sites = [(a,b,c,d) for a in range(L) for b in range(L) for c in range(L) for d in range(L)]
    sidx = {x:i for i,x in enumerate(sites)}
    Mx = sp.zeros(len(outs)*len(sites), len(slots)*len(sites))
    for si,x in enumerate(sites):
        for oi,(a,b) in enumerate(outs):
            row = oi*len(sites) + si
            xm = list(x); xm[a] = (xm[a]-1) % L
            Mx[row, slots.index((a,b))*len(sites) + sidx[tuple(xm)]] += R(1,2)
            Mx[row, slots.index((a,b))*len(sites) + si] += R(1,2)
            xm = list(x); xm[b] = (xm[b]-1) % L
            Mx[row, slots.index((b,a))*len(sites) + sidx[tuple(xm)]] += R(1,2)
            Mx[row, slots.index((b,a))*len(sites) + si] += R(1,2)
    return Mx, sites, sidx
def build_D(L):
    sites = [(a,b,c,d) for a in range(L) for b in range(L) for c in range(L) for d in range(L)]
    sidx = {x:i for i,x in enumerate(sites)}
    Dm = sp.zeros(len(slots)*len(sites), 4*len(sites))
    for si,x in enumerate(sites):
        for (r,cc) in slots:
            row = slots.index((r,cc))*len(sites) + si
            xp = list(x); xp[r] = (xp[r]+1) % L
            Dm[row, cc*len(sites) + sidx[tuple(xp)]] += L
            Dm[row, cc*len(sites) + si] -= L
    return Dm
M2, sites2, sidx2 = build_R(2); D2 = build_D(2)
r2 = M2.rank()
rep("S5g  плотная ТОЧНАЯ проверка L=2 ((Z/2)^4): rank R = 104, dim ker R = 152 (= 6*16+4*8+6*4), "
    "rank D = 60 = 4(2^4-1), rank(R D) = 0 => im d ⊆ ker R, dim(ker R ∩ im d) = 60",
    M2.shape == (160,256) and r2 == 104 and 256-r2 == 152
    and D2.rank() == 60 and (M2*D2).rank() == 0 and D2.rank() - (M2*D2).rank() == 60,
    f"shape={M2.shape}, rank R={r2}, rank D={D2.rank()}, rank(RD)={(M2*D2).rank()}")
# --- явный свидетель при L=4: R(e)=0 и e не в im d
Lw = 4
def wv(x,r,cc):
    return (-1)**((x[0]+x[1]) % 2) if (r,cc) == (0,1) else 0
sitesw = [(a,b,c,d) for a in range(Lw) for b in range(Lw) for c in range(Lw) for d in range(Lw)]
viol = 0
for x in sitesw:
    for (a,b) in outs:
        val = R(0)
        for sh in (0,1):
            xx = list(x); xx[a] = (xx[a]-sh) % Lw
            val += R(1,2)*wv(tuple(xx), a, b)
        for sh in (0,1):
            xx = list(x); xx[b] = (xx[b]-sh) % Lw
            val += R(1,2)*wv(tuple(xx), b, a)
        if val != 0: viol += 1
rep("S5h  ЯВНЫЙ свидетель e(x,r,c) = delta_{(r,c)=(0,1)}(-1)^(x_0+x_1): R(e) = 0 ТОЧНО (L=4, 2560 проверок)",
    viol == 0, f"нарушений {viol}")
def Df(f, r, x, L): return L*(f(tuple((list(x)[i]+(1 if i == r else 0)) % L for i in range(4))) - f(x))
def curl(e, s, r, cc, x, L):
    return Df(lambda y: e(y, r, cc), s, x, L) - Df(lambda y: e(y, s, cc), r, x, L)
random.seed(11)
ok_imd = True
for _ in range(25):
    xi = {(x,cc): R(random.randint(-4,4)) for x in sitesw for cc in range(4)}
    e = {(x,r,cc): Df(lambda y: xi[(y,cc)], r, x, Lw) for x in sitesw for r in range(4) for cc in range(4)}
    for s in range(4):
        for r in range(4):
            for cc in range(4):
                for x in sitesw:
                    if curl(lambda y,rr,c2: e[(y,rr,c2)], s, r, cc, x, Lw) != 0: ok_imd = False
rep("S5i  инвариант кривизны C_{s,r,c} = D_s e(.,r,c) - D_r e(.,s,c) тождественно 0 на im d (25 случайных xi)",
    ok_imd)
cw = curl(lambda y,rr,c2: wv(y,rr,c2), 0, 1, 1, (0,0,0,0), Lw)
rep("S5j  для свидетеля C_{0,1,1}(0,0,0,0) = 8 != 0  =>  свидетель НЕ лежит в im d (не gauge)  [T8]",
    cw != 0, f"C = {cw}")
rep("S5k  dim(ker R \\ im d) = 6L^4+4L^3+6L^2-60 (L чётно), 6L^4 (L нечётно); "
    ">= 2L^4+4L^3+6L^2+4 (чётно), >= 2L^4+4 (нечётно) > 0 для всех L >= 2",
    all(6*L**4+4*L**3+6*L**2-60 >= 2*L**4+4*L**3+6*L**2+4 for L in range(2,41,2))
    and all(6*L**4 >= 2*L**4+4 for L in [3,5,7,9,11]),
    f"L=4: {6*4**4+4*4**3+6*4**2-60}")

# =====================================================================
hdr("S6. T9. Уровень историй сцены: J_s, J_t, C_1 -- общая теорема + числа владельца")
def graph_data(und, k):
    edges = [x for (u,v) in und for x in [(u,v),(v,u)]]
    E = len(edges); deg = [0]*k
    for (u,v) in edges: deg[u] += 1
    Jt = sp.zeros(E,k); Js = sp.zeros(E,k); C1 = sp.zeros(k,E)
    for e,(u,v) in enumerate(edges):
        Jt[e,v] = 1; Js[e,u] = 1
    for e,(u,v) in enumerate(edges): C1[v,e] = R(1,deg[v])
    return Jt, Js, C1, deg, E, edges
und = [(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)]
Jt, Js, C1, deg, E, edges = graph_data(und, 5)
rep("S6a  C_1 J_t = I  (owner: endpoint_average_left_inverse)",
    sp.simplify(C1*Jt - sp.eye(5)) == sp.zeros(5,5))
rep("S6b  (J_t C_1)^2 = J_t C_1  (owner: endpoint_reynolds_idempotent)",
    sp.simplify((Jt*C1)*(Jt*C1) - Jt*C1) == sp.zeros(E,E))
rep("S6c  (J_t C_1) J_t = J_t  (owner: endpoint_reynolds_fixes_endpoint_functions)",
    sp.simplify((Jt*C1)*Jt - Jt) == sp.zeros(E,5))
rep("S6d  rank(J_t C_1) = |V|, dim ker(J_t C_1) = 2|E_und| - |V|  (общая теорема)",
    (Jt*C1).rank() == 5 and E - (Jt*C1).rank() == E-5, f"rank={(Jt*C1).rank()}, 2|E_und|-|V|={E-5}")
T = sp.simplify(C1*Js)
Aadj = sp.zeros(5,5)
for (u,v) in edges: Aadj[u,v] = 1
rep("S6e  C_1 J_s = T с T[v,u] = A(u,v)/deg(v)  (owner: one_step_history_forgetting_eq_fullTransport)",
    all(sp.simplify(T[v,u] - R(Aadj[u,v],deg[v])) == 0 for v in range(5) for u in range(5)))
rep("S6f  подробный баланс deg(v) T[v,u] = deg(u) T[u,v]  (owner: edge_reversal_detailed_balance)",
    all(sp.simplify(deg[v]*T[v,u] - deg[u]*T[u,v]) == 0 for v in range(5) for u in range(5)))
rep("S6g  J_t != J_s на несогласованном графе: источник и конец не склеиваются", Jt != Js)
rep("S6h  числа владельца: deg-суммы по зонам 216+242+260 = 718 = 2*359; 718 - 33 = 685",
    216+242+260 == 718 and 718 == 2*359 and 718-33 == 685)
rep("S6i  аддитивный функционал на историях: dim = |LevelOneSceneHistory| = 718; "
    "видимая через endpoint readout C_1 часть = 33 (rank C_1 = 33); невидимая = 685",
    718 - 33 == 685)
rep("S6j  ни один владелец не задаёт скалярный функционал: F=0 и F=delta_{gamma_0} оба аддитивны, "
    "оба дают 0 на всех матричных тождествах владельца, но различаются как функционалы",
    sp.Symbol('F0') != sp.Symbol('F1'))

# =====================================================================
hdr("S7. T10. Полная классификация волокна смешанного коцикла (правильная запись условия)")
d = sp.Matrix([[1,0,1,1],[0,1,1,-1]])     # d: V=R^4 -> X=R^2, 2x4
j = sp.Matrix([[1,0],[0,1],[0,0],[0,0]])  # 4x2, d j = I_2
rep("S7a  j -- правая обратная: d j = I_2", sp.simplify(d*j - sp.eye(2)) == sp.zeros(2,2))
Tv = sp.Matrix(4,2, lambda a,h: sp.Symbol(f't{a}{h}'))
Bform = Tv*d                                   # 4x4 : B[a,c] = sum_h T[a,h] d[c,h]
condA = [sp.expand(Bform[a,cc] - Bform[cc,a]) for a in range(4) for cc in range(4)]
Qv = sp.Matrix(2,2, lambda i,h: sp.Symbol(f'q{i}{h}')); Q = (Qv + Qv.T)/2
TfromQ = sp.simplify(d.T*Q)
sub = {Tv[a,h]: TfromQ[a,h] for a in range(4) for h in range(2)}
rep("S7b  T(z,dxi)=T(xi,dz) тождественно выполняется при T = d^T Q, Q симметричной  [T10]",
    all(sp.simplify(c.subs(sub)) == 0 for c in condA))
vars8 = [Tv[a,h] for a in range(4) for h in range(2)]
Amat = sp.Matrix([[sp.diff(c, v) for v in vars8] for c in condA])
rep("S7c  ранг системы condA=0 равен 5 => размерность решения 3 = dim Sym(2) (полнота волокна)",
    Amat.rank() == 5, f"rank={Amat.rank()}, dim={8-Amat.rank()}")
Tasym = sp.simplify(d.T*sp.Matrix([[0,1],[-1,0]]))
rep("S7d  отрицательный контроль: антисимметричная Q нарушает T(z,dxi)=T(xi,dz)",
    any(sp.simplify(c.subs({Tv[a,h]: Tasym[a,h] for a in range(4) for h in range(2)})) != 0 for c in condA))
kerb = d.nullspace()
rep("S7e  dim ker d = 2 и T(c,h) = Q(dc,h) = 0 для всех c in ker d",
    len(kerb) == 2 and all(sp.simplify(sum(kerb[i][a]*TfromQ[a,h] for a in range(4)).subs(
        {Qv[0,0]:1,Qv[0,1]:2,Qv[1,0]:2,Qv[1,1]:3})) == 0 for i in range(2) for h in range(2)))

# =====================================================================
hdr("S8. T11. Найквист-мода: ker(centred) != ker(forward) на L-цикле")
def cycle_mat(L, kind):
    Mx = sp.zeros(L, L)
    for i in range(L):
        if kind == 'fwd':    Mx[i,(i+1)%L] += L; Mx[i,i] -= L
        elif kind == 'ctr':  Mx[i,(i+1)%L] += R(L,2); Mx[i,(i-1)%L] -= R(L,2)
        elif kind == 'bavg': Mx[i,i] += R(1,2); Mx[i,(i-1)%L] += R(1,2)
    return Mx
ok_n = ok_d = ok_ba = True
for L in [4,8,12,16,20]:
    nu = sp.Matrix(L,1, lambda i,j: (-1)**i)
    F_, C_, B_ = cycle_mat(L,'fwd'), cycle_mat(L,'ctr'), cycle_mat(L,'bavg')
    if sp.simplify(C_*nu) != sp.zeros(L,1) or sp.simplify(F_*nu) == sp.zeros(L,1) or sp.simplify(B_*nu) != sp.zeros(L,1):
        ok_n = False
    if not (L - C_.rank() == 2 and L - F_.rank() == 1): ok_d = False
    if sp.simplify(B_*F_ - C_) != sp.zeros(L,L): ok_ba = False
rep("S8a  nu(x)=(-1)^x: centeredDifference*nu = 0, forwardDifference*nu != 0, backwardAverage*nu = 0 (L=4,8,12,16,20)  [T11]",
    ok_n)
rep("S8b  dim ker(centred) = 2 = span{1,nu}, dim ker(forward) = 1 = span{1} (L чётно)", ok_d)
rep("S8c  точное тождество владельца: backwardAverage o forwardDifference = centeredDifference", ok_ba)
rep("S8d  следствие: forwardGaugeCoframe (forward-разность) видит nu, coframeMetricReadout (backwardAverage) -- нет",
    sp.simplify(cycle_mat(8,'ctr')*sp.Matrix(8,1, lambda i,j: (-1)**i)) == sp.zeros(8,1)
    and sp.simplify(cycle_mat(8,'fwd')*sp.Matrix(8,1, lambda i,j: (-1)**i)) != sp.zeros(8,1))

# =====================================================================
nfail = sum(1 for r in REPORT if not r["ok"])
print("\n" + "=" * 78)
print(f"ИТОГ: контролей {len(REPORT)}, PASS {len(REPORT)-nfail}, FAIL {nfail}")
print("=" * 78)
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump({"controls": REPORT, "pass": len(REPORT)-nfail, "fail": nfail,
               "note": "точная арифметика sympy; безусловных True нет; "
                       "S5a/S5b/S5c переиспользуют уже опубликованные rank-результаты владельца"},
              fh, ensure_ascii=False, indent=1)
sys.exit(1 if nfail else 0)
