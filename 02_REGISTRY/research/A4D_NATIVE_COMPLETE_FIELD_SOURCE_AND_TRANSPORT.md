# Полный полевой источник: record, лоренцев перенос и мера подготовки

2026-10-16. SOURCE #310. Вычисляется источник уже заданной record-программы
на **полном** raw chart, а не произвольное продолжение цены с matching
graph. Все16 matter,10 positive-metric и6 orthogonal-frame координат
сохраняются. Физический закон агрегации, допуска и полной динамики не выбран.

## 0. Совместная стационарность и действительный операторный вход

[BOOK03 §03.8](../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md#038-finite-equations-of-motion)
задаёт конечную совместную стационарность, а §03.25 — bootstrap

```text
B=beta^−1 log Tr exp(−beta Delta)−log det(I−z Feedback).
dB=−Tr(rho_beta dDelta)+z Tr[(I−z Feedback)^−1 dFeedback],
rho_beta=exp(−beta Delta)/Tr exp(−beta Delta).
```

Здесь beta,z фиксированы, Delta положительна на её собственном полном
носителе и I−z Feedback>0. rho_beta — вес дифференциала, а не ещё один
закон физической подготовки. Общая вариационная задача не требует, чтобы
один tick вспомогательного record-engine выдавал следующее q. Лемма §3.1
остаётся точным тестом одного предложенного повторного чтения engine-output;
она сама по себе не определяет форму метрических уравнений действия.

На уже вычисленном [матричном интерфейсе](A4D_NATIVE_JOINT_ADJOINT_SOURCE.md#9-joint-covector-the-gram-contribution-and-internal-ward)
G>0, Dirac=d+d^dagger_G, Pi²=Pi=Pi^dagger_G и U^dagger_G U=I
полный первый отклик той же heat/feedback цены имеет вид

```text
Y=rho_beta Dirac, K=G^−1 dG,
dB=−4 Re Tr(Y dd)+Tr(C_G K)
       +Tr(C_Pi dPi)+Tr(J_U U^−1 dU),
C_G=−2[Y,d^dagger_G]=2[Y,d].
```

C_Pi,J_U — именно полные resolvent-covectors владельца, с сохранённым
feedback, а не новые sources. Они должны пройти через тот же actual
native map, как G и d. При наличии ambient covectors A_x=dS/dq_x и
B_e=dS/dD_e положим M_e=B_e(q_s^−1 D_e)ᵀ. На базовом geometric carrier
D_e q_t D_eᵀ=q_s собственные строки стационарности равны

```text
sym[A_x+sum_(s(e)=x) M_e/2
        −sum_(t(e)=x) D_eᵀ M_e D_e/2]=0,
skew M_e=0, E_b=0, E_m=0, E_preparation=0.       (0)
```

Это [существующий constrained pullback](A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md#1-all-joint-variations-and-their-intrinsic-covector),
со всеми10 metric slots/site,6 link slots/edge, shifts и всеми16 matter
компонентами. Дополнительные native-связи требуют ограничения на реальные
совместно допустимые кривые; (0) не позволяет независимо занулить запрещённые
ambient directions. В §4.1 ниже вычислен её нелинейный второй отклик.

Здесь важна точная область уже имеющегося Dirac. Для literal stored
оператора archiveSolderedDirac=d+ell и Lorentz links реализация heat как
квадрата selfadjoint stored Dirac требует одновременно
A_xyᵀ h_x A_xy=h_y и A_xy v_r(y)=v_r(x).
В этом классе positive polar factor link равен I. Ненулевой boost-диагностик
§4 не является дополнительным членом его positive heat по определению.
Общий adjoint completion d+d^dagger_G — отдельный матричный интерфейс;
он не заменяет stored operator без native owner. Аналогично независимый
unit observer в нём не отождествляется автоматически с full-CAR current,
а counting-site trace — с geometric volume.

Следующий физический шаг — один общий native pullback от q,D,b,m,
подготовки и retained observer/reference к операторам и всем членам того
же S, с его производными на допустимых кривых. Ни сумма разных цен,
ни fitted q′, ни замена Dirac его adjoint completion здесь не выбираются.

## 1. Actual endpoint-price и все16 rest-source компонент

Используется ровно двенадцатиканальный прибор из
[matter-clock owner](A4D_NATIVE_MATTER_CLOCK_RECORD_BINDING.md), с его
`λ=1`, упорядоченным `k_(ij,±)` и общим retained `C²⁴`:

```text
m0=rho(F)^−1 m,
w_a=p²+(m0_a−m*_a), a=0,...,11,
X^A=m0_(12+A)−m*_(12+A), A=0,...,3,
theta_a=k_a·X,
W_a=[[sqrt(1−w_a),−sqrt(w_a)e^(−i theta_a)],
     [sqrt(w_a)e^(i theta_a),sqrt(1−w_a)]].
```

Полный comparator — `C_yx=W_y*W_x`; feedback и counting logdet-price
принадлежат [price/metric owner](A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md).
Для одного канала обозначим `w=w_a(x)`, `u=w_a(y)`,
`δ=k_a·(X(x)−X(y))`, `v(s)=s(1−s)`. На открытой области
`0<w,u<1/2`, `1−zf_a>0`, при фиксированном allowed `z`,

```text
f_a=w+u−2wu−2sqrt[v(w)v(u)]cosδ,
J_z(x,y)=−Σ_a log(1−z f_a).                         (1)
```

Второй mode каждого канала имеет нулевой leakage и сохранён в полном
определителе; (1) не является postselection. Непосредственная вариация
той же цены даёт

```text
A_a=1−2u−(1−2w)sqrt[v(u)/v(w)]cosδ,
B_a=1−2w−(1−2u)sqrt[v(w)/v(u)]cosδ,
C_a=2sqrt[v(w)v(u)]sinδ,
dJ_z=Σ_a z/(1−z f_a)
       [A_a dw_a(x)+B_a dw_a(y)+C_a k_a·(dX(x)−dX(y))].       (2)
```

Это все16 endpoint-source слотов: первые12 — amplitude derivatives,
последние4 — суммы `k_a C_a` с противоположными знаками на концах.
Фазы не заморожены, matter normalizer не назначен константой и никакие
компоненты `m0` не исключены. Если сам `z` или другие настройки меняются,
их отдельные derivatives также входят в полную цену; (2) относится к
фиксированному `z`.

У actual endpoint-программы оба конца сравниваются в одном заданном
retained instrument frame. В неё не добавлен native spacetime transport.
Иное сравнение с field-dependent transport между концами является
другой программой и требует собственного закона и его source.

## 2. Off-shell raw pullback: десять transverse costates вычислены

В [полном raw chart](A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md#8-a-complete-native-kinematic-lift-of-a-prescribed-positive-metric)
`(h,m0,O)` переменные `h>0`, `m0` strict-timelike и `O∈O(4)` независимы.
Здесь `m*=-2ap e_mask0+(2p−1)e_mask1+e_mask13+e_mask14`, `a=√p`.
Пусть `A=rho(F)` и `R_F[δF]=D rho(F)[δF]m0`. Тогда тождественно

```text
δm0=A^−1[δm−R_F(δF)].                              (3)
```

Для фиксированных endpoints их price (1) зависит только от `m0(x),m0(y)`.
Тот же вывод относится к любому уже определённому функционалу этой
программы и её spatial jets, **если** его measure/weights/reference
также зависят только от `m0` или фиксированы. Обозначим его полный
rest Euler-ковектор после всех integration-by-parts через `e0`.
Из (3) следуют точные raw covectors

```text
E_m=A^−T e0,
E_F=−R_F* E_m,
P_F:=E_F+R_F*E_m=0,
E_h=0, E_O=0.                                      (4)
```

Звёздочка в (4) — cotangent adjoint с полными matrix/packed conventions.
Все10 symmetric `h`-направлений и все6 `O`-направлений включены.
При compact test fields boundary terms исчезают; иначе переносится и
полный boundary operator. Зависимость `e0` от пространственных
производных не теряется: при `δm0(x)≡0` неизменны сам `W(x)` и все его
производные. Поэтому никакая скрытая derivative-frame сила не появляется
в уже заданном `W_y*W_x`.

Это **off-graph** тождество actual field→program law. Нулевые transverse
costates не восстановлены из одних значений на graph. Для этого record
сектора full raw stationarity эквивалентна `e0=0`; она зануляет frame
force. Но она не навязывает `h=q_record[m0]`: raw `h,O` остаются
невидимыми данной программе. Full graph stationarity нельзя переносить
на остальные native sectors, link/shift equations или controller costs.

Если реальное действие содержит geometric measure, native transport,
независимый reference или прямые frame/matter terms, они должны быть
добавлены к (4) собственными derivatives. Наличие совпадающего metric
readout не определяет такой закон. В частности, finite endpoint-price
не доказана функционалом только `q_record`: её прямые internal sources
в (2) остаются. Нормальный metric lift не позволяет их выбросить.

## 3. Тот же matching family: flat h и искривлённая native g

Следующий контроль целиком лежит внутри уже построенного smooth family,
а не использует произвольный внешне заданный metric. Положим

```text
m0(x)=m*+Σ_mu x^mu e_mask(12+mu),
w_a=p², X=x, q_record=h=cI4, c=p³/2,
j=(1,r(m0)), H=−eta+2(eta j)(eta j)ᵀ/(1−|r|²),
F=c^−1/2 O(x)H^1/2, m=rho(F)m0,
eta=diag(1,−1,−1,−1).                              (5)
```

В нуле фактическое fullCAR чтение даёт `N=3`, `r=(−2/3,0,0)`;
strict timelike domain сохраняется в окрестности. Полный `k`-frame
удовлетворяет `kᵀk=6I`, поэтому flat `q_record=cI` следует из того же
literal projector/comparator, а не назначается ему независимо.

На всей strict-timelike области `H eta H=eta`. Поскольку `H>0`,
единственный положительный корень удовлетворяет
`H^1/2 eta H^1/2=eta`: это следует из
`eta H eta=H^−1` и единственности principal positive root.
Поэтому полная native ковариантная Lorentz metric в (5) равна

```text
g=F^−T eta F^−1=c O eta Oᵀ.                       (6)
```

Теперь выберем только для этого контроля свободную `O` как Euclidean
rotation угла `θ=k x0` в плоскости01. Это одно подсемейство имеющихся
шести `O`-полей; они не объявляются gauge. Программа `W(m0)`, её полные
endpoint prices и `h` одинаковы для всех `k`. Между тем

```text
g=c[[cos2θ,sin2θ,0,0],
    [sin2θ,−cos2θ,0,0],
    [0,0,−1,0],[0,0,0,−1]],
R_g=4k² cos(2kx0)/c,
Ric_g(0)=diag(2k²,−2k²,0,0),
G_g=diag(0,0,2k²cos(2kx0),2k²cos(2kx0)).           (7)
```

Знак кривизны — sphere-positive, тот же, что у Lorentz reflection owner.
Для доказательства достаточно буквальной Levi-Civita связи первого
2×2 блока: его determinant равен `−c²`, а scalar curvature равна
`4k²cos(2kx0)/c`. Другие два направления образуют плоский постоянный
product. В двух измерениях `Ric=(R/2)g`, что даёт все компоненты (7).

Таким образом, даже **точное** равенство comparator/native positive
metric на общей smooth программе не определяет Lorentz dynamics.
При `k≠0` native Einstein tensor в нуле ненулевой, хотя `h` плоская
и сама record-программа не видит этого изменения. Если curvature sector
переписан через `g`, полные observer-derivative и boundary terms из
[Lorentz source identity](A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md) должны
компенсировать эту зависимость; их нельзя удалить и оставить только
Einstein term.

Это не утверждение full native joint criticality и не admitted curved
vacuum: blank/volume, preparation, controller, link и shift prices
сохранены как отдельные обязательства. Равенство начальных matching
данных также не является доказанным законом их дальнейшей эволюции.
При двух **данных** frames кинематический link `D_st=F_s F_t^−1`
удовлетворяет `D_st q_t D_stᵀ=q_s` для contravariant
`q_t=F_t eta F_tᵀ`; это не его физическое Euler equation.

[Узкий consumer](sources/d0_native_field_transport_2026-10-16/record_frame_source.py)
экспортирует `run(repo=None)`. Он проверяет literal endpoint source,
все16 rest и frame pullbacks, все10 metric и6 rotation costates,
actual matter-clock germ и точную кривизну (7). Он импортирует только
pin-ированные определения и не запускает старые suites/receipts.

## 3.1. Matching/ring-вход и невозможность исправить output сменой frame при fixed q

Есть точка того же family, где matching выполняется и input одновременно
принадлежит буквальному engine-domain. Не меняя wiring или reference `m*`,
возьмём

```text
m†=−2ap e_mask0+p³ e_mask1
    +e_mask12+e_mask13+e_mask14+e_mask15,
X†=(1,0,0,1), w_a=p²,
L=sqrt(2/p³), m0(x)=m†+L Σ_mu x^mu e_mask(12+mu).
```

Здесь `p³=2p−1`, поэтому первые12 координат совпадают с `m*`.
Actual полное CAR-чтение даёт `N=5`, `J=e0`, `H=I` в нуле: вклад
пространственного α₁ равен `2(m12 m15−m13 m14)=0`, остальные два
также нулевые. Из `DX=L I` получается `q_record(0)=I`, и выбор `O(0)=I`
в matching chart даёт `F(0)=I`, `m(0)=m†`, native `q(0)=eta`.
Все16 координат являются элементами `Z[a]`; шесть engine guards равны
нулю, first-grade pairing `p³` положительна.
Это согласование literal raw **точки** и comparator first-jet reading,
а не допуск raw first jet целиком. В точке retained `G_ref=(FFᵀ)^−1=I`
и `h_J=I`, но вдоль matching germ
`dr1=(2L/5)(dx0−dx1−dx2+dx3)`, `dH01=−2dr1`.
При постоянной `O=I` имеем `dF=dH/2` и `dG_ref=−dH`, вообще ненулевые,
хотя `dh_J=dq_record=0` в нуле. Весь germ не является fixed-reference
engine-germ. Норма `N=5` сохранена; деления состояния на `sqrt(5)` нет.
Никакой новый physical AF image этим также не установлен.

Буквальный `engine.step`, а не reset rest coefficients, выбирает `U+`
и выдаёт полный raw output

```text
m′=(5p−4)e_mask0+t e_mask1
    +(a−p)(e_mask12+e_mask14)−(a+p)(e_mask13+e_mask15),
t=a(4p−3)<0,  t²=65p−40.                          (7a)
```

Норма остаётся5, выходная pairing ненулевая, поэтому этот шаг принят
движком. CAR current при retained `F=I` всё ещё равен `e0`; при
произвольном `F′` это равенство не предполагается. Следующее утверждение
сильнее проверки неудачи при одном фиксированном reference.

**Лемма для всех frames.** Сохраним именно output `m′` из (7a), native
contravariant `q=eta` и прежний readout wiring. Пусть `F′` — **любая**
вещественная невырожденная матрица с `F′ eta F′ᵀ=eta`, включая improper
или time-orientation-reversing frames. Exterior action сохраняет grades,
поэтому first grade новых rest coefficients равна

```text
v=(F′)^−1(t e0),
v0²−|v_spatial|²=t²,  |v0|≥|t|.                  (7b)
```

Между тем probability slot1 того же wiring требует

```text
w1=p²+v0−p³∈(0,1/2)
  iff  3p−2<v0<3p−3/2.
```

Оба конца проверяются буквально: нижний даёт `w1=0`, верхний — `w1=1/2`.
Поскольку `p>7/12`, максимальный абсолютный endpoint равен
`b=3p−3/2`. Но

```text
t²−b²=83p−205/4=83(p−205/332)>0,
(205/332)²+205/332−1=−139/332²<0.                 (7c)
```

Последнее даёт строгую нижнюю границу положительного golden root;
верхняя `p<2/3` следует из `(2/3)²+2/3−1=1/9>0`.
Следовательно, даже замкнутый probability interval не пересекает
необходимую область `|v0|≥|t|`. **Никакой** frame при фиксированном
`q=eta` не возвращает этот output в прежний comparator chart.
Смена time orientation также не помогает.

Вход не обязан быть только flat germ. Например, сохраним те же clocks
`X=X†+Lx`, но положим `w_(01,+)=p²+κ(x0)²`, остальные `w=p²`.
Это меняет raw rest scalar на `κ(x0)²` и оставляет ту же входную точку
`m†`. Из literal metric formula (4) matter-clock owner получаем

```text
q_record(0)=I, Dq_record(0)=0,
∂0²q_record(0)=(κ/3)k_(01,+)k_(01,+)ᵀ
                 +κ² e0e0ᵀ/(6p³),
R_q(0)=−κ/3.                                    (7d)
```

В достаточно малой окрестности определены тот же полный comparator и
matching fields, без назначенных свободных generator jets. Лемма
output относится к их общей нулевой точке. Только эта точка здесь
объявляется literal ring-engine input; весь вещественный germ не
объявляется engine-admitted continuum. Не выведен coupled update
`q′,F′,D′,b′`, допускающий изменение `q`, и не доказана невозможность
другого wiring или другого допущенного процесса. Результат — точная
fixed-q граница данного actual engine step и данного same-program chart,
а не global native no-go или full joint root.

## 4. Настоящая Lorentz link: положительная часть не исчезает

Теперь используется другое уже имеющееся данное: пространственная связь
`D`, переводящая target-векторы в source-векторы. При ковариантных метриках
её полное кинематическое ограничение имеет вид

```text
Dᵀ g_s D=g_t.
```

Это эквивалентно `D q_t Dᵀ=q_s` для `q=g⁻¹`. Никакой временной
эволюции `q,D,b,m` этим не назначается. Пусть `u_s,u_t` — единичные
timelike наблюдатели из полного CAR-чтения с его сохранённым reference,
а не автоматически first-grade оси record/engine. Возьмём уже выведенные
положительные observer metrics

```text
h_a=−g_a+2(g_a u_a)(g_a u_a)ᵀ,
M=h_t⁻¹ Dᵀ h_s D,  B=M^1/2,  R=D B⁻¹.            (8)
```

Корень — единственный principal root положительного в `h_t` смысле
оператора. Он не выбирает дополнительный Euclidean frame. Это точная
полярная факторизация **данной** связи `D=R B`, с сохранением обоих
множителей, а не замена связи её унитарной частью.

Для доказательства положим `K_a=g_a⁻¹h_a=2u_a u_aᵀg_a−I`,
`v=D⁻¹u_s`. Тогда `M=K_t K_v`, откуда `Mᵀg_tM=g_t`.
Principal functional calculus и единственность положительного корня дают
`B⁻¹=g_t⁻¹Bᵀg_t`. Поэтому

```text
Bᵀg_t B=g_t,
Rᵀg_s R=g_t,  Rᵀh_s R=h_t.                       (9)
```

Следовательно, `R` совмещает observer **линии**. Если
`c_pair=u_sᵀg_sD u_t`, то `|c_pair|≥1` и
`R u_t=sign(c_pair)u_s`. Положительный pairing сам не выбирает future
orientation. В плоскости `u_t,v` оператор `M` — boost с rapidity
`±2χ`, `χ=arcosh|c_pair|`; на ортогональном двумерном дополнении он единичен.
Поэтому singular values полного переноса, в соответствующих endpoint
pairings, равны

```text
D on vectors:       exp(χ), exp(−χ), 1, 1,
ΛD on ALL grades:   exp(χ) [4], exp(−χ) [4], 1 [8].
```

Все grades `1,4,6,4,1` сохранены. В частности, для полного exterior
Gram `ΛM` получается точное, не зависящее от выбора basis тождество

```text
Tr_16 ΛM=det_4(I+M)=16 c_pair²,
I_boost:=Tr_16 ΛM−16=16(c_pair²−1),
d I_boost=32 c_pair dc_pair.                       (10)
```

В (10) используется обычный полный exterior counting trace, а не
defining AF PF-trace и не одна из зарегистрированных цен.
`I_boost` здесь — диагностическое чтение уже имеющейся связи. Оно не
объявляется новым членом физического действия, тепловой ценой или
chronological feedback. Замена `D` на `R` удаляет именно эту ненулевую
информацию. Один этот скаляр также не определяет всю связь: `R`, boost
direction, holonomies и affine shifts не удаляются и не заменяются им.
При рациональном boost `coshχ=5/4`, `sinhχ=3/4` полярная
часть `B=D`, `R=I`, полный spectrum `ΛM` равен
`4 [4], 1/4 [4], 1 [8]`; `I_boost=9` и его rapidity-производная равна30.

Полная производная сохраняет оба endpoint pairing и саму связь:

```text
dM=−h_t⁻¹ dh_t M
   +h_t⁻¹[dDᵀh_sD+Dᵀdh_sD+Dᵀh_s dD],
B dB+dB B=dM,
dR=dD B⁻¹−R dB B⁻¹,
dc_pair=du_sᵀg_sD u_t+u_sᵀdg_sD u_t
        +u_sᵀg_s dD u_t+u_sᵀg_sD du_t.            (11)
```

Sylvester equation имеет единственное решение: все eigenvalues `B`
положительны. Для actual полного current `J`,
`u=J/sqrt(κ)`, `κ=JᵀgJ`, используются
`dκ=JᵀdgJ+2Jᵀg dJ` и
`du=dJ/sqrt(κ)−J dκ/(2κ^(3/2))`.
Actual `dJ` включает все16 matter, frame/reference и moving-normalizer
слагаемые владельца. На его собственной подготовке `m(s)` при `s=1`,
`D=I`, `u_t=e0` источник (10) равен `768/25`. Замораживание нормировки
материи вместо этого даёт ошибочное `2304/25`.

Если полный exterior pairing содержит site density
`W_a=ω_a Λh_a`, то `ζ=ω_s/ω_t` остаётся в полном Gram:

```text
Tr_16[(ΛD)^sharp ΛD]=16ζ c_pair²,
dTr=16 c_pair² dζ+32ζ c_pair dc_pair.               (12)
```

В частности, `ΛR` удовлетворяет `(ΛR)^sharpΛR=ζI`, а полностью
weighted-unitary часть есть `U=ζ^−1/2ΛR` с положительной частью
`sqrt(ζ)ΛB`. При переменной density нельзя назвать ненормированный
`ΛR` унитарным для полного `W`.
Нормировка half-density является отдельной операцией, которую нужно
задать и продифференцировать. Она не разрешает молча удалить measure/source.
Например, контракты `ω=sqrt(|det g_cov|)` и принадлежащий прежнему
exterior owner `ω=sqrt(|det q_contra|)` при `q=g⁻¹` дают противоположные
log-density jets. Здесь сохранён произвольный `ω`; ни один из этих
контрактов не выбран новым физическим volume law.

Наконец, `u_pair` не отождествляется с `n_record`: нынешний engine
использует first-grade ось, и её совпадение с full-CAR observer не доказано.
Совмещение observer линий в (9) поэтому не означает автоматически
нулевой источник принадлежащего другому владельцу chronological price.
Связь `D` пространственная; её объявление временным record-переносом
также потребовало бы собственного закона.

## 4.1. Exact second jet совместного metric/link carrier

Для уравнений (0) требуется второй отклик на самом constraint, включая
кривизну его вложения. Он уже строится без выбора нового действия.
Пусть q_s,q_t симметричны и невырождены, D q_t Dᵀ=q_s. Для малых
симметричных V_s,V_t и skew K положим

```text
A_a(V_a)=(I+V_a q_a^−1)^(1/2),
D(V_s,V_t,K)=A_s exp(K q_s^−1) D A_t^−1.           (12a)
```

Корень здесь — вещественная аналитическая ветвь около I, заданная
сходящимся power series при малом V. Он q-selfadjoint, а не обязательно
Euclidean symmetric. Поэтому A_a q_a A_aᵀ=q_a+V_a, а skew K даёт
exp(K q_s^−1) q_s exp(K q_s^−1)ᵀ=q_s. Формула (12a) удовлетворяет
constraint точно. На графе одна A_x применяется ко всем рёбрам вершины;
независимые K_e сохраняют все6 link slots на каждом ребре.

Для направлений i,j обозначим L_ai=V_ai q_a^−1, Omega_i=K_i q_s^−1
и {P,Q}=PQ+QP. Их полные first/mixed-second link jets равны

```text
W_i=(L_si/2+Omega_i)D−D L_ti/2,
Z_ij=[−{L_si,L_sj}/8+(L_si Omega_j+L_sj Omega_i)/2
                       +{Omega_i,Omega_j}/2]D
     −(L_si/4+Omega_i/2)D L_tj
     −(L_sj/4+Omega_j/2)D L_ti
     +3D{L_ti,L_tj}/8.                             (12b)
```

Это следует из A=I+L/2−L²/8+O(L³), A^−1=I−L/2+3L²/8+O(L³)
и exp Omega. Никакая коммутативность матриц не используется. При любом
совместимом first jet K=W q_t Dᵀ+(D V_t Dᵀ−V_s)/2 skew; это также
доказывает полноту параметров всех10+10 metric и6 link направлений.

Если уже заданное S имеет ambient link-covector B_e, то

```text
H_chart[i,j]=H_ambient[v_i,v_j]+sum_e Tr(B_eᵀ Z_eij). (12c)
```

Raw b,m и прочие независимые координаты можно оставить линейными;
их вторые производные тогда нулевые, но все mixed ambient rows остаются.
Добавление conormal extension Tr[Lambdaᵀ(D q_t Dᵀ−q_s)] меняет
два слагаемых (12c) противоположно: их сумма точно ноль, поскольку
вторая производная constraint равна нулю на (12a). Ambient Hessian
без B:Z не обладает этой независимостью. В собственном рациональном
noncommuting контроле его ошибочное значение −8140397/307200 сокращается
ровно до0 после добавления B:Z.

Это Hessian pullback выбранного chart. В constrained critical point он
задаёт независимую от chart билинейную форму; вне него смена координат
добавляет first-source term. Basic carrier chart не доказывает stored
Dirac adjointness, parallel-leg, observer/preparation или holonomy
условия §0. Их полные second jets также нужны для native решения.
Функции joint_link_first_jet/joint_link_second_jet реализованы в том же
lorentz_link_transport consumer, без нового operator или receipt.

## 5. Actual PF-подготовка: полная цена содержит measure-source

В этом разделе адрес `a=(j,i)` — **внутренний defining AF address**,
`r_a=p^(n+1+j)`. Это другой domain, чем spatial archive point `x`.
Владелец ещё не задаёт map `a→x` или `a→X(x)`; внутренний PF trace нельзя
отождествить с пространственным объёмом одним переименованием индекса.

Используется actual flagged channel `Y=Φ_Eσ` из
[preparation owner](A4D_NATIVE_PREPARATION_STATIONARY_SOURCE.md). В локальном
собственном basis эффекта `E` обозначим `w_a=σ_aa`, а через `P_diag`
pinching на actual fine path/address projections. Для его абсолютных
conditional prices `f_a=f_j(e_a)` точное тождество имеет вид

```text
A=6+Σ_a w_a f_a+D(w||r)/g0+C_out/g0,
C_out=D(Y||P_diag Y),  g0=log(phi).                 (13)
```

Здесь baseline именно6. Канонический blank `B_n` дополнительно содержит
`Σ r_a f_a(blank)` и не может заменить6 при абсолютных `f_a`.
Доказательство (13): relative-entropy pinching identity
`D(Y||μ_f)=D(P_diag Y||μ_f)+D(Y||P_diag Y)`, затем actual diagonal
probabilities `w_a P(fine path|a)` дают первые два слагаемых.
Все fine paths, central sectors и coherences остаются в `Y`.

`C_out≥0` сравнивает coherent вход с его **диагональным** входом.
Это не прежняя, вообще неверная для coherences замена полной цены на
`D(σ||μ)/g0+Tr σ f(E)`: её отличие контролируется другой DPI identity.
Moving pinching/eigenbasis при `dE` также входит в полную производную;
никакой выбор eigenvectors физическим законом не объявляется.

На positive-weight chart `w_a,r_a>0`, при `Σdw=Σdr=0` и в области
дифференцируемости retained coherence gap, полная производная (13) равна

```text
dA=Σ w_a df_a
   +Σ [f_a+log(w_a/r_a)/g0]dw_a
   −Σ w_a dlog(r_a)/g0+dC_out/g0.                  (14)
```

При рождении ранга применяется принадлежащий владельцу C¹ amplitude/support
limit; формальные density derivatives `log(w_a)` при `w_a=0` не используются.

На уже доказанном faithful minimum `w_a*=r_a exp(−g0 f_a)/Z`,
`C_out=0`, получается

```text
A*=6−log Z/g0,
dA*=Σ w_a* df_a−Σ w_a* dlog(r_a)/g0.              (15)
```

При фиксированных native `p,n`, reference и code имеем `dr_a=0`.
Если же тот же закон после пространственного pushforward действительно
даёт moving masses, их source нельзя выбросить.
В частности, normalized mean `M=Σ w_a* f_a` имеет другую производную:

```text
dM=E_w(df)−g0 Cov_w(f,df)+Cov_w(f,dlog r).          (16)
```

Именно KL-mass term в (13) компенсирует covariance term; он не является
подогнанным counterterm. Поэтому даже доказанное в будущем совпадение
`w*` с volume probabilities не превратит эту полную цену в одно `M`.
Это классификация **имеющейся внутренней** агрегации. Она не опровергает
условную normalized spatial extension из coherent-compiler owner:
для её применения нужен собственный spatial measure/aggregation theorem.

Для noncommuting вариаций требуется более полное чтение, чем список
движущихся eigenvalue weights. Пусть впервые задан **действительный**
POVM/readout с test observable `O_φ`, включая его собственную field
зависимость. На том же faithful minimum положим

```text
L=log μ−g0 f(E),  σ*=exp(L)/Z,  ν(φ)=Tr(σ* O_φ).
```

Здесь `μ` — central PF-reference; при фиксированном native контракте она
не движется. Производная trace exponential даёт точное operator identity

```text
dν(φ)=Tr(σ* dO_φ)
 +∫_0^1 Tr[σ*^(1−s)(O_φ−ν(φ)I)σ*^s dL]ds,
dL=dlog μ−g0 Df_E[dE].                            (16a)
```

`Df_E` — полный Fréchet derivative, с divided differences
`f^[1](e_i,e_j)`; заменять его на `f'(E)dE` вне trace envelope нельзя.
При совпадающих eigenvalues используется непрерывный предел `f'`.
Это Kubo–Mori covariance, а не предположение о commuting state или
замороженном собственном basis. Производная `O_φ` сохраняет moving
readout, reference и clocks. Само существование такого алгебраического
чтения не доказывает его primitive admission или spatial interpretation.

Например, для actual n1 effect `E2=diag(9/25,16/25)`,
`dE2=σ_x`, `O_φ=σ_x⊕0` имеем
`dν=2p²(q_1−q_2)/(Z(e_1−e_2))`, где
`q_i=exp(−g0 f_0(e_i))`. Это ненулевой источник той же подготовки,
хотя eigenvalue jets обоих `e_i` равны нулю. Поэтому один classical
score не описывает всю допустимую noncommuting вариацию.

Лишь на commuting fixed-address подсемействе, если actual clock map
`a→X_a` уже задан, (16a) упрощается до

```text
dν(φ)=E_w[gradφ(X)·dX]
      +Cov_w(φ(X), dlog r−g0 df).                  (16b)
```

Это конкретная identity для следующего spatial-measure theorem. На
общей фиксированной области в одних и тех же координатах normalized
geometric volume имеет derivative
`dν_h(φ)=Cov_νh(φ,tr(h⁻¹dh))/2`. Следовательно, identification требует
сопоставить её с (16a), либо с действительно применимой (16b), для
**всех** test functions, с собственными sampling/refinement bounds.
Moving coordinate/domain и boundary terms нужно также перенести.
Ни конечная atomic measure, ни один contraction не объявляются уже
равными гладкому volume limit. Назначение `dVol_h/V` по определению не
выполняет это требование и не доказывает исходный raw-norm terminal.

## 5.1. Некоммутирующий Hessian и равномерный inverse блока подготовки

Рассмотрим **ту же** вторую полную цену
A(E,sigma)=6+D(Phi_E sigma||mu_f)/ell, ell=log(phi), и её faithful minimum
A*=6−log Tr exp(L)/ell, L=log(mu)−ell f(E).
Эффекты лежат внутри (0,I), выбранная область не пересекает нули
minus-факторов actual Kraus paths. Это C²-область; прежние C¹ rank-birth
результаты сохраняются, но не заменяют второй производной на её границе.

Пусть угловые скобки означают Tr(sigma* ·). Полная некоммутирующая
ковариация есть

```text
Cov_BKM(A,B)=integral_0^1 Tr[sigma*^(1−s)(A−<A>I)sigma*^s B] ds.
H*[v,w]=−[<L_vw>+Cov_BKM(L_v,L_w)]/ell.           (16c)
```

Это дифференцирование того же глобального log Z, с полной нормировкой.
Все матрицы jets представлены в base spectral basis, а не в движущихся
диагональных координатах. При фиксированном native reference

```text
H*[v,w]=<D²f_E[E_v,E_w]+Df_E[E_vw]>
            −ell Cov_BKM(Df_E[E_v],Df_E[E_w]).      (16d)
```

Первое слагаемое — direct program response, второе — индуцированный
отклик подготовки. При данном допустимом движении reference добавляются
оба jets log(mu) в L_v,L_vw. ell здесь фиксирована. В частности,
E_vw включает actual field-map second jet и acceleration D из (12b).
Нельзя заменить его нулём по совпадению одного first jet.

Из exact coherent gap владельца
A(E,sigma)=A*(E)+D(Phi_E sigma||Phi_E sigma*(E))/ell
следует полный Schur-разбор в точке минимума. Обозначим
Y*=Phi_E sigma*, J_v=D sigma*[v], T={sum_j Tr S_j=0} и

```text
M=Phi_E* Dlog_(Y*) Phi_E/ell,
M_T=P_T M|T,
H_full[(v,S),(w,T1)]=H*[v,w]+<S−J_v,M_T(T1−J_w)>_HS,
H*=A_EE−A_Esigma M_T^−1 A_sigmaE.                 (16e)
```

P_T — лишь HS/Riesz compression на trace-constraint; M само не обязано
сохранять T. Derivatives Phi_E не заморожены: в разности двух одинаковых
baseline output они сокращаются, оставляя Phi_E(S−J_v).
Именно output metric Phi_E* Dlog_(Y*) Phi_E, а не произвольно подставленная
Dlog_(sigma*), принадлежит полному coherent action.

**Равномерная оценка обратного.** В каждом старом центральном блоке
сохранён собственный plus path
A_j+=w_j sqrt(I−E_j)+sqrt(E_j)/sqrt(2),
w_0²=p³, w_1²=p²<1/2. Functional calculus даёт A_j+>=w_j I,
поскольку sqrt(1−e)+sqrt(e)>=1. Для любого Hermitian S_j, включая
[S_j,E_j]!=0, поэтому
||A_j+ S_j A_j+||_HS²>=w_j⁴||S_j||_HS².
Нормированная Y* имеет eigenvalues<=1, а все divided differences log
на этом интервале не меньше1. Следовательно,

```text
<S,M_T S> >= ||Phi_E S||_HS²/ell
             >= p^6 ||S||_HS²/ell,
||M_T^−1||_(HS→HS) <= ell/p^6.                    (16f)
```

Константа не зависит от уровня n, defining dimension или числа адресов;
межблочные mass jets и все внутренние coherences сохранены. Это оценка
нормы обратного density-блока, а не полного condition number. Верхние
собственные значения M, mixed field-jets и derivatives около нулей paths
могут расти. Оценка не переносится на весь GNS amplitude-Hessian:
tau=Tr(CC*) и sigma=CC*/tau остаются, right-unitary и radial fibers
дают нулевые направления этой цены. Они не объявляются physical gauge,
а другие члены S могут их видеть. Независимый physical допуск подготовки
и выбор именно этой стационарной ветви не следуют из (16e)–(16f).

Для **той же** линеаризованной совместной системы с заданными residuals
r_E,r_sigma это даёт конструктивное исключение density-блока:

```text
S=J_v+M_T^−1 r_sigma,
||S−J_v||_HS <= (ell/p^6)||r_sigma||_HS,
H* v=r_E+J* r_sigma.                              (16g)
```

Residuals здесь — невязки собственных уравнений, а не выбранный source.
Обратимость H* и оценки J ещё не установлены. В частности, нулевые
raw h/O строки прежнего rest-only прибора этим не становятся ненулевыми.

Actual n1 двухпараметрический effect
E0=[[9/25+x,y],[y,16/25]], E1=9/25 даёт в нуле

```text
A*_yy=2p²(q1 f0'(9/25)−q2 f0'(16/25))
                    /[Z(9/25−16/25)] < −93/112,
A*_x > 237/1600,
q_i=exp(−ell f0(e_i)), Z=p²(q1+q2)+p³exp(−ell f1(9/25)).
```

Строгие знаки следуют из собственных рациональных log enclosures,
без numerical exp. При dE/dy=sigma_x first eigenvalue jets равны нулю,
а Hessian ненулевой. На isospectral unitary curve с тем же first dE
добавочный E_yy точно сокращает его; это конкретная необходимость direct
second jet. Негативный H*_yy не является положительной физической metric.
Нескалярный effect этого instrument-fixture также не объявляется
допущенным входом прежнего direct AF-to-CAR engine support fiber.

Наконец, BKM Cauchy–Schwarz и logarithmic mean<=arithmetic mean дают
dimension-free bound
|H*[v,w]|<=(||L_vw||_op+||L_v||_op||L_w||_op)/ell.
Для количественного native решения всё ещё требуются равномерные
оценки actual field/readout/transport jets. Прибор, зависящий только от
m0, остаётся слепым к независимым h,O до всех порядков; минимизация
подготовки не создаёт отсутствующей зависимости. Формулы реализованы
в том же preparation_measure consumer.

## 6. Строго наследуемые clocks не создают spatial volume limit

У actual archive adapter `π_n=archiveProjection` и
`|ArchivePoints(0)|=16`. Если clocks удовлетворяют буквальному закону
`X_(n+1)=X_n∘π_n`, то `X_n=X_0∘toBase`. Для **любой** согласованной
вероятности `(π_n)_*μ_(n+1)=μ_n` её pushforward равен

```text
ν_n=(X_n)_*μ_n=(X_0)_*μ_0.                         (17)
```

Следовательно, это одна и та же мера с не более чем16 атомами при любом
refinement. Полная field-производная на гладкой test function `φ` равна

```text
dν(φ)=Σ_b[dμ_0(b)φ(X_0(b))
            +μ_0(b) gradφ(X_0(b))·dX_0(b)].        (18)
```

Больший архив сам по себе не создаёт новых clock values или гладкой
четырёхмерной volume measure в этом классе. Это не запрет richer
refinements: actual archive также допускает nonatomic projective measures,
а новые fine matter/clock states не обязаны быть strict pullbacks.
Но их создание и влияние на полную цену должны иметь собственный допуск.

Если единственное marginal-условие положительного conditional kernel —
parent mass на actual projection fibre, вариации двух child weights с
противоположными знаками её сохраняют. Pushforward не зависит от **всех**
таких вариаций ровно тогда, когда clock constant на каждом таком fibre.
Если дополнительно фиксируется golden-bit marginal, этот критерий
применяется к `(parent,bit)` subfibres допустимых jets: clocks могут
различать bits, оставаясь невидимыми именно этим kernel variations.
Иначе соответствующий kernel/clock source остаётся в pushforward.
Ни internal AF-address trace, ни compatibility parent marginals не
определяют этот source автоматически и не допускают все такие jets физически.

Конструктивный выход из strict-inheritance класса уже дан параллельным
[history/density/coframe результатом](A4D_HISTORY_DENSITY_PALATINI_SYNTHESIS.md).
Его новый child-clock rule делит очередной координатный интервал в долях
p,p² по фактическим F/R cost-cut историям, сохраняя pending returns.
Центры дочерних ячеек образуют martingale, размеры не превосходят
2p^floor(n/8), а объёмы равны cylinder weights. Поэтому pushforward
предельного clock есть Lebesgue measure на адресном кубе, с явной
Lipschitz quadrature error. Это не противоречит (17): clocks уже меняются
у children. Допуск нового rule как native material clocks и его связь
со спектральными setting labels не следуют из этого построения.

Тот же результат даёт обратимую density/coframe замену
ehat=sqrt(m/|det e|)e со всеми16 coframe и10 metric вариациями.
Для **условного** quadratic-anchor first-order сектора Phi(ehat,U,psi)
плюс KL точная стационарность эквивалентна stationary Phi и w=r;
приведён искривлённый Einstein–scalar контроль со всеми его уравнениями.
Полный native spectral price не отождествлён с этим сектором, Lorentz
Palatini не подставляется вместо R_h, а настоящие observer/source terms
остаются. Новый §5.1, в отличие от одного commuting KL, использует полный
coherent output Hessian actual AF channel. Совместить эти инструменты
физически можно лишь после source identity одного native action.

## 7. Следующая общая конструкция

Вычислены три конкретные части одной недостающей стрелки. Имеющийся
comparator слеп к raw frame при фиксированной rest matter; совпадение
его positive metric с native pairing не даёт Lorentz Einstein equation.
Полный actual Lorentz link содержит boost/observer информацию с точной
производной (11)–(12), которую нельзя заменить одной унитарной частью.
Actual preparation несёт собственные KL/normalizer/measure источники
(14)–(18), а не автоматически normalized spacetime average.

Теперь нужен один допущенный field→program закон, который переносит
**эту же полную связь**, подготовку и child-dependent clocks в spatial
carrier, задаёт actual measure и сохраняет их источники. Это не разрешение
добавить `I_boost` или иной compensator к действию. Все остальные
heat, metric, matter, link, shift, controller и archive equations остаются;
временное обновление полей, fixed-source/raw-owner terminal и физическая
ОТО не объявляются замкнутыми.

Свежие результаты того же SOURCE сохранены и потребляются в своих областях.
[Fixed-branch rigidity](A4D_NATIVE_ISOMETRIC_COMMON_PROCESS_METRIC_RIGIDITY.md)
показывает, что общий конечный unitary word и согласованное isometric
embedding сохраняют полный comparator metric; сами по себе они не дают
нового геометрического разрешения.
[Flat factor shear](A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md) имеет нулевой
source исправленной AF preparation price на том же probe, где собственный
положительный heat source ненулевой; дополнительные источники не определены
нужным значением для его отмены.
[Rest-coordinate step](A4D_NATIVE_COMMON_PROCESS_DOMAIN_OBSTRUCTION.md)
выводит именно прямое `m0→U_+m0` за probability domain. Она не подменяет
другую ещё не выведенную raw evolution `m'=U_s m`,
`m0'=rho(F')⁻¹m'`. Эти границы согласованы с (3)–(4): rest coefficients,
raw CAR matter и actual endpoint transport нельзя отождествлять.
Новая точка §3.1 даёт literal raw ring-вход и actual output;
для него исключены **все** frame-исправления при неизменном native `q`.
Это требование к замкнутости данного engine/readout adapter, а не
обязательное временное q′-правило вариационной теории. Её следующий шаг —
общий native map и стационарные строки (0) с полным second pullback.
В (12)–(16g) уже сохранены Gram, constraint-curvature, coherent
preparation и normalizer члены для этого вычисления. Непосредственно
вычислена равномерная оценка обратного блока подготовки, но не обращён
полный field Hessian и не отождествлены разные operator owners.

## 8. Узкая совместная проверка

`certificates/a4d_native_complete_field_source_check.py` вызывает только
три новых source consumers: `record_frame_source`, `lorentz_link_transport`
и `preparation_measure`. После добавления joint second jets и Hessian
общий запуск проходит543 точных условия: 111 raw-source, 56 Lorentz-link
(прежние38 и18 second-jet), 376 preparation/measure (прежние349 и27
Hessian/inverse controls). Обычный запуск — 8.930 s, optimized — 7.996 s;
выводы побайтно совпадают. Actual raw-engine часть §3.1 не изменялась.

Проверяются actual endpoint-price и все raw-source slots, literal
Lorentz curvature matching family, actual ring/engine point и
fixed-q obstruction для всех reference frames, полный16 Gram и constrained endpoint
jets, conormal-independent second source, нормировка собственного CAR current,
actual flagged AF channel, coherences, Fréchet/BKM readout/Hessian и literal
archive projection. Общие доказательства second pullback, Schur-разбора и
равномерного inverse приведены выше; finite controls их поддерживают,
а не заменяют all-level доказательство. Для archive
kernel используются только конечные projection tables и integer fibre
counts; большие operator matrices не создаются. Существующие определения
закреплены SHA256. Старые suite entrypoints, receipt generators и Lean
builds не запускаются; физическое действие или source не регистрируются.
