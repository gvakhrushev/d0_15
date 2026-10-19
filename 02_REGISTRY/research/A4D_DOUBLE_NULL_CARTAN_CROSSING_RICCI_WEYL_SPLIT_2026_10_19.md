# D0 → GR: двухсторонняя Cartan-связность и точное локальное разделение Ricci/Weyl

19 October 2026. **RESEARCH / EXACT CONTINUUM CARTAN + EXACT POINTWISE METRIC 2-JET / same Draft #334.** Не является решением исходных 40 конечных Euler-строк, физическим выбором D0 action/clock/programme, source-normalized recovery или закрытием GR. Потребляет: [Brinkmann 40→3→1](A4D_ARBITRARY_BRINKMANN_ALL40_CARTAN_DISCRETE_EINSTEIN_2026_10_19.md), [full-Lorentz positive-adjoint interface](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md), [moving-volume golden](A4D_BALANCED_NATIVE_GOLDEN_EXACT_SOURCE_SEAM_LOCAL_TO_VOLUME_MEAN_2026_10_19.md), [nine-null/Bianchi](A4D_TWO_SIDED_NULL_BIANCHI_GLOBAL_COMPLETION.md). Отдельная ограниченная геометрическая лемма без изменения этих владельцев.

## 1. Почему просто добавлять противоположную связь нельзя

Исходный кофрейм: e⁺=du, e⁻=dv+(H/2)du, e²=dx,e³=dy; Lorentz null generators N_i=E_{-,i}+E_{i,+}, opposite M_i=E_{+,i}+E_{i,-}, i=2,3. Если добавить только ω_v=L_i M_i dv при старом кофрейме, то T⁺ содержит L_i dv∧dx^i. Точное отсутствие кручения в этом *ограниченном* новом connection-ansatz вынуждает L_i=0. Это не отрицание расширений исходной полной 24-link системы.

## 2. Минимальная двухсторонняя конфигурация — те же 16 coframe/24 link slots

\[
e^+=du+\frac{J(v,x,y)}2dv,\quad
e^-=dv+\frac{H(u,x,y)}2du,\quad e^{2,3}=dx,dy.
\tag{1}
\]
Функция J — противоположный геометрический профиль, НЕ Book-функционал J₂. Положим Ω=1−HJ/4 ≠0. Точно:
\[
ds^2=Hdu^2+Jdv^2+2(1+HJ/4)dudv-dx^2-dy^2,
\quad \det e=\Omega,\quad\sqrt{|\det g|}=|\Omega|.
\tag{2}
\]
\[
(g^{uu},g^{uv},g^{vv})=\Omega^{-2}(-J,\,1+HJ/4,\,-H).
\tag{3}
\]
При J=0 возвращается исходный pp-coframe и постоянный объём. При J≠0 возникает настоящий moving-volume вход для уже имеющегося PF/quantile-механизма; сам физический выбор этого readout этим не доказан.

## 3. EXACT Levi-Civita Cartan normal form

При Ω>0 обозначим
\[
a_i=\frac{\partial_i H}{2\Omega},\quad
b_i=\frac{\partial_i J}{2\Omega},\quad
c_i=-\frac{H\partial_iJ+J\partial_iH}{8\Omega}
    =\frac12\partial_i\log\Omega,\quad
d_i=\frac{J\partial_iH-H\partial_iJ}{8\Omega}.
\tag{4}
\]
Пусть B=E_{--}−E_{++} (boost). Тогда единственная metric-compatible безкрутильная connection для (1):
\[
\boxed{\omega=\sum_{i=2,3}
[(a_i e^++c_i e^-)N_i+
 (c_i e^++b_i e^-)M_i+
 d_i e^i B].}
\tag{5}
\]

**Доказательство.** Подставить
de⁺=(∂iJ/2)dx^i∧dv,
de⁻=(∂iH/2)dx^i∧du,
du=(e⁺−Je⁻/2)/Ω, dv=(e⁻−He⁺/2)/Ω
в de^a+ω^a{}_b∧e^b=0. Все24 torsion coefficients равны0. При Ω≠0 единственность следует из стандартной Koszul/LC-теоремы. Смешанная связь НЕ вводится как свободный counterterm: c_i — половина производной log физического Jacobian; d_i — ориентированная относительная производная двух null-профилей. При J=0 остаётся ω=(∂iH/2)N_i du. Это **континуальная** Cartan-теорема, не замена точным finite link Euler или принудительного one-u-tick staggering.

## 4. Точная CROSSING-теорема: оба односторонних профиля плоские, совместный — кривой

Возьмём поперечные АФФИННЫЕ профили
\[
H=A_xx+A_yy,\qquad J=B_xx+B_yy,\qquad
d=A_xB_x+A_yB_y,\quad w=A_xB_y-A_yB_x.
\tag{6}
\]
Оба однонаправленных spacetime (J=0 или H=0) точно flat, поскольку все поперечные Hessian равны0. В точке x=y=0 двухсторонней метрики H=J=0, но:
\[
\boxed{
\operatorname{Ric}_{uv}=-d/4,\quad
\operatorname{Ric}_{\mu\nu}=0\ (\mu\nu\ne uv,vu),\quad
R=-d/2,\quad
R^2{}_{3uv}=w/4,\quad
R^+{}_{+xy}=w/4.
}
\tag{7}
\]
И полный скаляр Riemann:
\[
\boxed{R_{\alpha\beta\gamma\delta}R^{\alpha\beta\gamma\delta}
       =(d^2-3w^2)/4.}
\tag{8}
\]
Здесь convention R^ρ{}_{σμν}=∂μΓ^ρ_{νσ}−∂νΓ^ρ_{μσ}
+Γ^ρ_{μλ}Γ^λ_{νσ}−Γ^ρ_{νλ}Γ^λ_{μσ}; Ric_{σν}=R^ρ{}_{σρν}.

**Доказательство с конечным 2-jet.** В точке 0 единственные ненулевые первые metric derivatives: ∂i g_uu=A_i, ∂i g_vv=B_i; вторые: ∂i∂j g_uv=(A_iB_j+A_jB_i)/4. Ненулевые Γⁱ_uu=A_i/2, Γⁱ_vv=B_i/2, Γᵛ_ui=A_i/2, Γᵘ_vi=B_i/2. Отсюда R²_{3uv}=(A_xB_y−B_xA_y)/4. Для Ric_uv derivative-source равен +d/4, а две Γ²-констрикции дают −d/2, т.е. Ric_uv=−d/4. Полный 4×4×4×4 Riemann 2-jet contraction даёт (8). Все dyadic identities проверены bounded checker на независимых базисных/смешанных градиентах, без разностного предела.

Если A·B=0 и w≠0, то **в самой точке** Ricci=0, но R^2{}_{3uv}=w/4≠0 и Kretschmann=−3w²/4≠0. Пример H=ax, J=by: K(0)=−3a²b²/4. Поэтому метрика не локально изометрична VSI Brinkmann pp wave около пересечения. Это **не** глобальная Ricci-flat family: вне пересечения остаётся nonlinear Ricci residual и для GR нужны настоящие coframe corrections.

Компактный комплексный cross-jet, без новой константы:
\[
\mathcal Z=(A_x+iA_y)(B_x-iB_y)=d-iw.
\tag{9}
\]
Re Z фиксирует Ricci overlap, Im Z — ориентированный nonabelian rotation channel. Это геометрическая декомпозиция, а НЕ доказанное чтение обоих каналов native detector.

## 5. Нельзя молча переносить null-matter q=0 и старый линейный price

Для прежней реальной CAR16 scalar/top matter Ψ(u) имеем на (1):
\[
q=g^{\mu\nu}D_\mu\Psi\cdot D_\nu\Psi
=-\frac{J}{\Omega^2}|\partial_u\Psi|^2.
\tag{10}
\]
При J≠0 это НЕ 0. Старый универсальный аргумент «higher action powers vanish on f=q=0» на всём двухстороннем носителе не работает. Также при ∂iJ≠0 e⁺∧de⁺≠0, поэтому объявить dΨ пропорциональным e⁺ без решения eikonal/integrability нельзя.

## 6. One-parent consumer и firewall

**Следующий конкретный шаг в том же Draft #334:** (i) повторить original SIX based plaquettes и все16+24 независимые Euler при двухстороннем coframe, не навязывая (5) до вариации, проверить u/v staggering; (ii) на полном старом LEFT/RIGHT/ref128 carrier прогнать два диагностических адресных поля: A∥B и A⊥B при тех же |A|,|B|, проверить actual native return/source's sensitivity to d и w; (iii) затем связать moving Ω, off-null CAR matter, prep/clock/work, one complete Born/Book law и полный H+J+R с теми же covectors; (iv) только после этого потреблять уже доказанный условный nine-null+Ward theorem и исходный raw #216.

Критическая граница: **полное Lorentz algebra closure и exact continuum Cartan не означают original finite all40 stationarity, native controller admission, Book cost source или GR closed.** Статус GR_closed=false.

Checker: [check_two_null_cartan.mjs](sources/d0_two_null_crossing_2026-10-19/check_two_null_cartan.mjs), запуск node 02_REGISTRY/research/sources/d0_two_null_crossing_2026-10-19/check_two_null_cartan.mjs. Он проверяет 24 torsion slots на нескольких независимых nondegenerate fixtures, все Ricci slots, two oriented curvature slots и полный 256-component Kretschmann contraction в точке пересечения. Старые expensive/Lean/whole-price owners этим не перепроверены.
