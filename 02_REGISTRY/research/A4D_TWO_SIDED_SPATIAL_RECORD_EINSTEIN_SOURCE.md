# Две нормировки записи: конструктивный пространственный источник и полный Einstein-коэффициент

17 октября 2026. `gvakhrushev/d0_15`, существующий Draft #334.
Начальный SOURCE: `3f368179627acc9f2c3e9616df729ac2280a77a0`.
Потреблённое параллельное усиление: `cea62e743610ccbf70a8c7de55ecb1f2475d22c7`.

**Класс результата:** точная конечная теорема о полном двухзаписном comparator; явный curved spatial/lapse reference на всех16 формах; условная fixed-beta macroscopic теорема о его полном десятикомпонентном метрическом источнике. **Не** селекция новой физической цены или окончательный вывод ОТО из D0.

## 0. Зачем этот результат и что уже принадлежит другим владельцам

Свежий `sources/d0_reverse_einstein_ir_2026-10-17/RESULT_RU.md` доказывает полный ADM identity и фиксированный-beta IR коэффициент прежнего logdet. Его §§8–9, добавленные при работе, также потребляют accepted `ArchiveSpatialHistorySplit.lean` и дают точный конечный golden 4D−2×3D curvature readout. Этого НЕ нужно строить заново. Осталось объяснить происхождение двух пространственных вычитаний в одном сравнении, а не объявлять их выбранным Einstein counterterm.

Здесь выполняется следующая композиция:

```
полная двухзаписная Gram-нормировка
  -> точные −1 и −1 перед двумя endpoint-ценами
  -> положительный полный comparator с равномерным запасом
  -> curved spatial reference с настоящим lapse и его сопряжением
  -> тот же нелинейный Einstein-ковектор в ведущем IR-порядке.
```

Конкретная новая идея: **−2 может происходить из двух обязательных нормировок уже выбранных записей**, а не из свободного коэффициента добавленного функционала. Это объясняет коэффициент внутри построенной сравнительной архитектуры. Оно НЕ доказывает, что реальный D0 experiment выбирает именно данные endpoint Grams, cross-amplitude, reference programme и logdet как свой полный Cost−Info.

Пины входов:

- `A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md`, §1: полный `W_y*W_x`, `A_yx=J_y*J_x`, `F=I-A* A` и цена при z_compare=1. Этот comparator имеет собственный математический owner; новая физическая Info law не импортируется.
- `A4D_COHERENT_COMPILATION_COST_DESCENT.md`: различие same effect и same full instrument; дополнительный coherent completion не становится бесплатным из-за равенства спектра.
- `sources/d0_reverse_einstein_ir_2026-10-17/RESULT_RU.md`: полная ADM формула, all16 Hodge coefficients, fixed-beta IR, позже spatial split и конечное golden чтение. Входной blob при cea62e74: `52b88dcc5c0d6cf34424db5f677be7a691ef2b2d`.
- `A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md`, `A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md`: positive full16 Hodge и действительное сопряжение/источник в их объявленных областях.
- `A4D_LOCAL_GAIN_PROJECTIVITY_RIGIDITY.md`: не отождествлять новую сравнительную цену с full normalized pointer entropy или неизменённой v8.

**Исходный терминал #334 не изменяется:** fixed smooth nonconstant g, независимый tau, все10 packed rows, unweighted raw sum и h^-2. Макроскопическое R->infinity ниже — другой, явно названный предел.

## 1. Две конечные полные записи, а не разность вероятностей вручную

Пусть H=C^d, а X_0,X_1:H->K — две полные raw record maps с положительными Gram

```
G_i=X_i* X_i>0,       K=X_1* X_0.
```

Их канонические нормированные frames:

```
J_i=X_i G_i^(-1/2),   J_i*J_i=I,
C=J_1*J_0=G_1^(-1/2) K G_0^(-1/2).                    (1)
```

Положительный выбор G^(-1/2) единственен: если W>0 и WGW=I, то `(G^(1/2) W G^(1/2))^2=G`, поэтому W=G^(-1/2). Общая нормировка отличается справа унитарным frame; determinant price не меняется. Это ограниченная вынужденность нормировки ДАННОЙ записи, не единственность самих raw X_i.

При invertible C собственный complete comparator owner даёт

```
J_cal=-M log det(C* C).
```

На полном completion-пространстве остальные failure eigenvalues равны0 и остаются в полном `det(I-F)`; история не выбрасывается частичным следом. Независимо от коммутирования G_i,K:

```
J_cal=-M log det(K* K)+M log det G_0+M log det G_1.      (2)
```

**Два минуса в относительной цене получаются из двух нормировок.** Их нельзя независимо менять, сохраняя одновременно те же X_i и изометричность J_i. Скалярный контроль: замена G^(-1/2) на G^(-s) даёт норму G^(1-2s), тождественно равную1 для всех G лишь при s=1/2.

В общем реальном приборе raw cross K уже задан двумя X_i, и его нельзя назначить желаемой геометрией без нового построения. Следующий раздел именно строит допустимую полную Gram-систему для указанного входа; он не утверждает её совпадение с прежним записанным прибором.

## 2. Положительный comparator из трёх actual spectral effects

Берём положительные эффекты одного и того же математического return-типа:

```
E_4=(1-z)I+z K_4,
G_0=(1-z)I+z K_0,
G_1=(1-z)I+z K_1,
0<=K_i<=I,      0<z<1,      a=1-z.
```

В континуальном Hodge чтении `K_i=exp(-beta Delta_i)`; до предела это соответствующие собственные finite survival effects, не скалярное значение R, поданное как oracle. Все три эффекта читаются в одном фиксированном counting Hilbert chart через действительные Gram/observer isometries. Их матрицы могут не коммутировать; derivatives этих representations сохраняются.

Положим p=phi^-1, p+p²=1 и выберем **одну field-independent** attenuation

```
kappa=sqrt(p)*a,
K=kappa sqrt(E_4),
C=G_1^(-1/2) K G_0^(-1/2).                              (3)
```

Это достаточная безопасная нормировка, не уникальная физическая длина программы. Значение z — прежняя фиксированная калибровка, не fitted source. Из `aI<=E_4,G_i<=I` следуют dimension-independent singular-value bounds

```
sqrt(p)*a^(3/2) <= s_min(C) <= s_max(C) <= sqrt(p),
p a³ I <= C* C <= p I,
p² I <= I-C* C <= (1-p a³)I.                             (4)
```

Итак, оба comparator outcomes имеют строгий положительный запас, независимый от h, числа узлов и возможных нулевых modes Delta. Ни одного спектрального усечения не требуется.

### Полное построение raw maps и унитарного опыта

На H (+) H возьмём

```
J_0=[I;0],
J_1=[C*; sqrt(I-C C*)],
X_i=J_i sqrt(G_i).
```

Тогда `X_i*X_i=G_i`, `X_1*X_0=K` и (1) выполнены тождественно. Обычный полный Julia block

```
U_C = [[C, sqrt(I-C C*)],
       [sqrt(I-C* C), -C*]]
```

унитарен. Это явный finite comparison с сохранённым дополнительным флагом; не постселекция на успех. Если требуется также физически приготовить raw contractions X_i, их собственные failure completions и их цены должны сохраняться. Когерентный переход от такого full raw programme к нормированным J_i — добавленная операция, не бесплатное равенство по одному эффекту. Все эти пространства конечны; формальное существование U_C не доказывает его native gate admission.

Для `J(E)=-M log det E` из (2),(3) точно

```
J_cal = J(E_4)-J(G_0)-J(G_1)-2Md log kappa.              (5)
```

Последний член известен и постоянен по полям на фиксированном carrier/clock chart. Если kappa, M или кодовая глубина меняются физически, их собственные derivatives обязательны. Само число координат d не заменяется metric volume.

Здесь z_compare=1 у *внешнего* complete comparator, как в его старом owner. Малое z внутри E_i остаётся исходным спектральным return parameter. Это разные места одной составной схемы; нельзя сказать, что мы незаметно доказали тождество для прежнего outer-v8 с неизменённым z.

### Источники и условие воспроизводимости

При фиксированных kappa,M,d полная первая производная:

```
dJ_cal=-M Tr(E_4^-1 dE_4)
       +M Tr(G_0^-1 dG_0)+M Tr(G_1^-1 dG_1).            (6)
```

Для каждого матричного аргумента A второй logdet jet равен

```
d² log det A[U,V]
 =Tr(A^-1 d²A[U,V]-A^-1 dA[U] A^-1 dA[V]).            (7)
```

Никакие endpoint, preparation, lapse, observer или нормировочные derivatives в (6),(7) не замораживаются. В (1) derivative sqrt(G) решает полный Sylvester equation `sqrt(G) d sqrt(G)+d sqrt(G) sqrt(G)=dG`. Bounds из a>0 дают bounded smooth maps; например

```
||dC||op <= kappa[||dE_4||op/(2a^(3/2))
                 +(||dG_0||op+||dG_1||op)/(2a²)].       (8)
```

Тождество (6) переносит ошибки трёх известных источников аддитивно. Оно не создаёт произвольной обратной для всего field Hessian и не является новым h^-2 raw estimate.

Скалярный static control E_4=G_0=G_1=E даёт `J_cal=const-J(E)`, а не0. Это НЕ Gaussian mutual information двух независимых temporal блоков, которая на таком продукте может быть нулевой. Полные raw records здесь не одинаковы только потому, что их Grams совпали: cross K в (3) другой. Именно поэтому прежний static-product контрпример к mutual-information названию не относится к (5).

## 3. Spatial reference без нового независимого метрического поля

Пусть g и G заданы одним полным ADM chart на I_t×Sigma:

```
g=N²dt²-h_ij(dx^i+s^i dt)(dx^j+s^j dt),
G=N²dt²+h_ij(dx^i+s^i dt)(dx^j+s^j dt),
N>0,   h>0.
```

Выберем fixed coordinate time length T и для каждой настройки tau∈I определим auxiliary reference geometry

```
Ghat_tau = N(tau,x)² du²+h_ij(tau,x) dx^i dx^j,
u∈S^1_T.                                                   (9)
```

Это **замороженная во вспомогательном времени u** версия уже данного spatial geometry/lapse. Не вводится новое dynamical metric field. При реальной field variation N(tau,x),h(tau,x) изменяются; tau сохраняется как настройка с полным label. Утверждение `partial_u h=0` не означает `delta h=0` или `partial_t h=0` у действительной геометрии.

u — координата reference clock; она не объявляется равной бесконечной физической истории или Role-A phase. Свежий accepted spatial split доказывает flat all16 spatial Hodge и циклическую Role-A факторизацию, но его same-axis/orientation/history bridge остаётся условием применения. Называть один finite cyclic shift физическим hyperbolic time было бы неверно.

Для каждого (9) используем стандартный *полный* Hodge operator на всех16 формах с настоящим volume `N du dV_h`, а не искусственное сокращение положительного 4D operator. При constant N это product clock и две spatial exterior copies 8+8. При moving spatial N появляются обязательные lapse-gradient terms. Ниже они выведены, а не добавлены для желаемого R3.

## 4. Явный reference differential: обязательная half-density поправка

Положим eta=N du, a=d_Sigma log N. Любая форма единственно записывается `Omega=alpha+eta wedge beta` с spatial alpha,beta. По правилу внешнего дифференциала и `d eta=-eta wedge a`:

```
dhat = [[d_Sigma, 0],
        [N^-1 partial_u, -d_Sigma-a wedge]].                (10)
```

На Hilbert space с весом N истинное сопряжение использует

```
(d_Sigma)^†_N=delta_Sigma-i_(grad log N).
```

В частности, нижняя правая компонента dhat† равна `-delta_Sigma`; её дополнительные члены сокращаются только после учёта *двух* вкладов. После unitary half-density transfer `Omega -> sqrt(N) Omega` в меру `du dV_h`:

```
Dhat = [[D_Sigma-(a wedge+i_a)/2, -N^-1 partial_u],
        [N^-1 partial_u, -D_Sigma-(a wedge+i_a)/2]].          (11)
```

Здесь D_Sigma — действительный curved 3D Hodge–de Rham operator h(tau), не выбранный скалярный Laplacian. Коэффициент1/2 в (11) вынужден unitary weight transfer. На полном Fock carrier equivalent formula использует `N_time=c_0 i_0` и нулевой член `(N_time-1/2)(c(a)+i_a)`. Он сохранён во всех16 grades.

(10) имеет dhat²=0, поскольку a=d log N; true-adjoint и (11) дают соответствующий positive full16 square. Конечный checker проверяет все derivative coefficients dhat², formal adjoint и half-density term на переменном lapse. Для curved h те же identities следуют из правил d_Sigma, его true adjoint и unitary conjugation; finite flat-spatial test не выдаётся за доказательство произвольной metric family.

Это конструктивная curved/clock специализация spatial readout: весь reference operator определяется уже заданными h,N и clock. Но настройка такого reference посредством реального D0 engine и цена её приготовления не следуют из одного вычисления (11).

## 5. Теперь spatial source имеет правильную размерность и правильный lapse

Для (9) точно

```
R(Ghat_tau)=R3(h_tau)-2 N_tau^-1 Delta_(h_tau) N_tau,
dV(Ghat_tau)=N_tau du dV(h_tau).                           (12)
```

Это не 3D heat trace, ошибочно переименованный 4D trace. Reference имеет одну явную clock-координату u и полный 4D Hodge operator, поэтому его тепловой множитель `(4 pi t)^-2`, а не `(4 pi t)^-3/2`. В product case это ровно дополнительный `(4 pi t)^-1/2` от clock. Невакуумная positive spatial geometry и lapse-source остаются.

Определим математическое **равномерное per-setting чтение**:

```
Jbar_ref=(1/T) integral_I J(exp(-beta Delta_(Ghat_tau))) d tau,
```

где в J аргумент survival дополнен тем же `(1-z)I+zK` как в §2. На сетке сначала берётся конечное число m заранее заданных tau-настроек; полная direct-sum цена comparator равна СУММЕ m цен (5). Деление на m — явно известное count-normalized чтение, а не якобы бесплатно выбранная физическая цена. При фиксации m оно не меняет stationary set; его множитель нельзя терять в исходной raw-норме. Все setting labels и failure outcomes сохраняются.

Из (12) и длины clock T:

```
(1/T) integral_I Vol(Ghat_tau) d tau = Vol(G),
(1/T) integral_I integral R(Ghat_tau) dV d tau
 = integral [R3-2N^-1 Delta_h N] dV_G.                     (13)
```

Потребляемая новая полная ADM identity из peer owner теперь даёт без подгонки

```
integral R_G dV_G
 - (2/T) integral_I integral R(Ghat_tau) dV d tau
 = integral R_g dV_g.                                      (14)
```

При retained lapse Laplacian равенство соответствует полному pointwise identity, а не выбрасыванию нужной границы. Для heat expansions ниже используем закрытые пространственные листья и periodic smooth regulator по времени либо вариации с неизменными boundary jets и отдельно сохранёнными heat-boundary terms. Никаких claims о глобальной причинности compact timelike circle не делается: Einstein source — локальный covector, регулятор не является физической временной топологией.

Shift не заморожен в действительном G/g. Reference (9) не содержит s, поскольку сравнивает тот же induced leaf/lapse без cross-time transport. В (14) вся shift-dependence actual G сохраняется; поэтому его variation даёт momentum constraints, а не только семь lapse/spatial equations.

## 6. Полный IR-источник двухстороннего сравнения

Потребляем фиксированный-beta спектральный результат peer owner, не повторяя его nonlocal form-factor или root calculations. При R->infinity, `G_R=R²G`, beta>0 fixed, `r=z/(1-z)<1`,

```
J_4^field(R)=-lambda_J R^4 V(G)+c_J R² int R_G dV_G+O_C1(1),
lambda_J=16M F3(r)/(4pi beta)^2,
c_J=4M F2(r)/(3(4pi)^2 beta),
Fs(r)=sum_(j>=1) (-1)^(j+1) r^j/j^s.                       (15)
```

F2,F3>0: alternating series gives `Fs>=r-r²/2^s>0`. Все16 Hodge grades нужны для общего a2=-4R/3. На той же compact controlled family (9) имеет точно те же lambda_J,c_J, а не новые adjustable spatial coefficients. Из (5),(13) и (14):

```
Jbar_cal(R)=K_(h,m)
       +lambda_J Vol(g_R)
       +c_J integral R(g_R)dV_(g_R)
       +O_C1(1)+finite-mesh/quadrature errors.              (16)
```

**Объёмный член меняет знак:** `-lambda V-2(-lambda V)=+lambda V`. Его нельзя сохранить со старым знаком или выдать за constant code overhead. Последний действительно постоянен по полям при fixed carrier:

```
K_(h,m)=-Md log[p(1-z)]
```

для per-setting normalization, после выделения одинаковых field-independent finite-dimension factors. У полной m-setting суммы он умножается на m. Абсолютная конечная цена не отбрасывается; (16) описывает её field-dependent source в том же фиксированном carrier.

Вариации (16) по всем десяти ADM полям дают

```
d Jbar_cal[V]
 = integral [lambda_J g_R^(mu nu)/2-c_J G_R^(mu nu)]
                 delta g_(R,mu nu)[V] dV_(g_R)
   + controlled remainder.                               (17)
```

Число десять не выведено этой формулой: используется собственный peer chart с `|det D(N,s,h -> g)|=2N det h>0`, чья inverse map выписана в его доказательстве. Мы сохраняем полный chart, а не ограничиваем source TT/trace/одной волной.

С настоящим, независимо полученным и не изменённым matter functional знак/нормировка в этой convention были бы

```
G_(mu nu)+Lambda_eff g_(mu nu)=T_(mu nu)/(2 c_J),
Lambda_eff=-lambda_J/(2c_J).                              (18)
```

Формула (18) — полевая система ВЕДУЩЕГО constructed comparison, а не объявление, что actual matter/reference/observer equations уже решены. Никакой T не определяется разностью до желаемого G.

### Что именно улучшилось относительно предыдущего reverse owner

Его необходимый spatial coefficient −2 теперь имеет точное происхождение в (1)–(5), а нужный curved weighted spatial источник построен как (9)–(14) с действительным Hodge/half-density differential. Не требуется угадывать Gaussian covariance полной ленты. Конечный golden curvature result peer owner также сохраняется: это другой, уже более короткий точный geometric readout. Настоящая работа не объявляет его heat-оценку обязательной; она даёт независимое происхождение относительного коэффициента в полной logdet comparison architecture.

## 7. Ошибка, clock и что нельзя выдать за новое совместное решение

C1 remainder в (15) — source в fixed smooth parameter chart. Он не равен исходной raw-l1 норме #334 автоматически. Непрерывные reference-настройки можно заменить m-point quadrature. При uniform C2 dependence по tau и соответствующих первых полевых jets:

```
||source quadrature error|| <= C R^4/m²,
R^-2 ||error|| <= C R²/m².                                (19)
```

Например, математический выбор m(R)>=R² даёт O(R^-2) после curvature scaling. Это достаточное правило precision для этой процедуры, не выведенный physical record clock. Интеграция полной конечной lattice цены использует уже имеющиеся fixed-R/source convergence для каждого из трёх geometries. Для каждого R,m можно выбрать h достаточно малым, чтобы ошибка (6) была меньше нужного допуска; совместный diagonal sequence существует как обычная аналитическая конструкция. Uniform endogenous clocks, programme costs и nonempty joint roots из неё не следуют.

На leading local функционале зависимость от выбранной foliation при фиксированном Lorentz g сокращается по (14). Это относится к допустимым hypersurface-orthogonal variations и правильным границам. Независимая twisted observer family и конечные O(1) record effects не уничтожаются. Совместное Ward всего native опыта должно включить их настоящие equations.

**Важный незакрытый scale condition:** lambda_J/c_J остаётся ненулевым при fixed beta. В vacuum leading Einstein system из (18) имеет `R(g)=4Lambda_eff=-2lambda_J/c_J`. Поэтому

```
beta R(g)=-24 F3(r)/F2(r),                               (20)
```

а это не малое IR curvature. При фиксированной shape g и `g_R=R²g` космологический source растёт как R^4, curvature source — R². Нельзя просто объявить large-R exact vacuum branch из (16). Для физического macroscopic on-shell результата необходимы реально выведенные дополнительные volume/matter/clock equations либо иной совместимый масштабный закон. Это обязательство уже присутствовало у первоначального IR volume term; две нормировки не решают космологическую задачу автоматически и не дают разрешения вычесть volume term.

Именно поэтому положительность построенного comparator и Einstein-форма его локального источника не означают physical GR-closure.

## 8. Полная граница применения — одно определённое требование вместо новых каталогов

Чтобы (17) стало выводом D0, нужно доказать на самом принятом полном процессе:

```
actual endpoint record Grams = G_0,G_1 из reference (9),
actual cross-amplitude = kappa sqrt(E_4) up to declared source-invisible frames,
actual physically selected full price/source = the comparator (5)
   plus independently owned retained costs, all with their real variations.
```

Здесь source-invisible determinant frames не объявляются невидимыми для всех последующих физических тестов. (1)–(5) доказывают реализацию и вынужденность коэффициента после такого programme binding. Они не выводят binding из M1, не приравнивают coherent Cost−Info и pointer Shannon, не обходят local-gain projectivity theorem и не переписывают unchanged v8. Появление positive unitary dilation не означает, что fixed native golden controls умеют исполнить поле-зависимое inverse square root без отдельного кода и source.

Не решены physical code/Info/test admission, совпадение Role-A и observer slicing, полный mixed-state/reference128 readout, independent link/torsion equations за пределами LC family и требуемая exact joint refinement. Эти вопросы не свёрнуты в слово «интерпретация». Мы не меняем их status и не регистрируем новый физический action.

**Результат этого прохода:** две ранее раздельные стрелки — нормировка полных записей и spatial Einstein correction — соединены конструктивно. В этом классе −2 больше не является вручную выбранным множителем; все10 leading metric rows получены с теми же c_J и вычисленным volume term. Следующее продвижение должно проверять именно показанную raw-record/programme binding, а не искать другой постоянный коэффициент или снова доказывать ADM/Hodge геометрию.

## 9. Воспроизведение и источники

Новый self-contained `check_two_sided.py` прошёл 82 точные проверки: noncommuting raw Grams, полные изометрии/comparator, full16 плюс retained flag, first/second normalizer jets, golden positivity margins, full16 nilpotent reference differential и его weighted adjoint, half-density term, независимая lapse/spatial curvature проверка, ADM10 и полный IR volume/source bookkeeping. Ordinary/-O JSON совпадают побайтно. Четыре действительно изменённых вычисления отвергнуты; ожидаемые receipts не редактируются. Конечные примеры не доказывают analytic heat estimates или physical programme admission; соответствующие теоремы/гипотезы названы выше.

Стандартная внешняя математика heat expansion: D. V. Vassilevich, *Heat kernel expansion: user's manual*, hep-th/0306138, Phys. Rep.388(2003),279–360, DOI10.1016/j.physrep.2003.09.002. Это математический контекст, не новая физическая предпосылка. Существенные coefficients и C1 IR используются у непосредственно прочитанного peer owner, а не приписываются внешней статье как доказательство D0.

Новых Lean-деклараций, независимой научной приёмки, запуска агентов, main-merge или GR/CORE promotion здесь нет.
