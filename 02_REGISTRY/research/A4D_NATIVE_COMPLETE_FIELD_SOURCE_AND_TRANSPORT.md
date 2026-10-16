# Полный полевой источник: record, лоренцев перенос и мера подготовки

2026-10-16. SOURCE #310. Вычисляется источник уже заданной record-программы
на **полном** raw chart, а не произвольное продолжение цены с matching
graph. Все16 matter,10 positive-metric и6 orthogonal-frame координат
сохраняются. Физический закон агрегации, допуска и полной динамики не выбран.

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
Новая точка §3.1 уже даёт literal raw ring-вход и actual output;
для него исключены **все** frame-исправления при неизменном native `q`.
Следующий закон должен поэтому выводить coupled `q,m` transition либо
отдельно допущенное изменение readout, сохраняя его полную производную.

## 8. Узкая совместная проверка

`certificates/a4d_native_complete_field_source_check.py` вызывает только
три новых source consumers: `record_frame_source`, `lorentz_link_transport`
и `preparation_measure`. После добавления §3.1 общий запуск проходит498
точных условий: 111 raw-source (прежние79 и32 новых fixed-q
engine/matching), 38 Lorentz-link, 349 preparation/measure.
Обычный запуск — 5.996 s, optimized — 5.835 s; выводы побайтно
совпадают. Изменённый raw-source consumer отдельно также прошёл111 условий.

Проверяются actual endpoint-price и все raw-source slots, literal
Lorentz curvature matching family, actual ring/engine point и
fixed-q obstruction для всех reference frames, полный16 Gram и constrained endpoint
jets, нормировка собственного CAR current, actual flagged AF channel,
coherences, Fréchet/BKM readout и literal archive projection. Для archive
kernel используются только конечные projection tables и integer fibre
counts; большие operator matrices не создаются. Существующие определения
закреплены SHA256. Старые suite entrypoints, receipt generators и Lean
builds не запускаются; физическое действие или source не регистрируются.
