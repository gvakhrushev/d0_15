# Геометрическая макроистория: явный полный вес и проверка динамического источника

17 октября 2026. Продолжение существующего Draft #334, задача EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE. Вход: `48fbb7a144b124b5ed881103d466041b317d5590`.

## 0. Результат и потребитель

Заполнен ранее символический кандидат W геометрической записи: из собственного 15-setting CAR/clock протокола построен полный count-macroevent, вычислены его source и все десять метрических Hessian-направлений. На плоском fixed-volume семействе его полный source отличается от чистого Einstein–Hilbert плюс cosmological volume. Этот конкретный кандидат описывает likelihood сравнения с сохранённой записью, не вакуумную динамику.

Дополнительно доказано: полная условная регистрация, не переводящая геометрические сектора друг в друга, сохраняет исходный геометрический marginal. Поэтому накопление условных записей не определяет первоначальный weight/source геометрии. Это не общий D0 no-go и не объявление произвольного prior физически допустимым.

Потребитель — переход от operational readout и Cost−Info к полному source в существующей нормальной форме/структурной сборке. Не вводятся action, opcode, claim, новая задача или ослабленный terminal. Физический допуск всех probe-слов сохраняет область исходного владельца. Original fixed-g/tau/all-ten/raw-h^-2/#216 остаётся OPEN.

## 1. Входы

На указанном SHA, относительно `02_REGISTRY/research/`:

- [CAR/clock owner](../d0_operational_car_clock_readout_2026-10-17/RESULT_RU.md): пять elementary dilations, десять coherent products, реальный metric inverse и full16/reference128.
- Его [checker](../d0_operational_car_clock_readout_2026-10-17/check_operational_metric.py), blob `1c5df0367784f911b4684d2d1aacc87bf469ea2f`: новый расчёт проверяет blob и потребляет только `creators()`, не исполняя старый `main()`.
- [Branch information](../../A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md), [normalizer](../../A4D_RETAINED_HISTORY_READOUT_AND_NORMALIZER.md), [whole-history scale](../../A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md): уже выведенный branch/cut закон, не новая Info.
- [Новое determinant-событие](../d0_cost_info_event_source_2026-10-17/RESULT_RU.md), §§6–7: сохраняется со своим many-body programme/ресурсным условием.
- [Full-source normal form](../../A4D_AF_FULL_SOURCE_EINSTEIN_NORMAL_FORM_2026_10_17.md), [structural source](../d0_structural_source_closure_2026-10-17/RESULT_RU.md): нужны полная цена, истинное чтение и реальные retained equations.
- [Homogeneous physical reduction](../../A4D_HOMOGENEOUS_PHYSICAL_METRIC_REDUCTION.md): прежний independent flat shape-source не пересчитывается.

Общие binomial, likelihood и conditional-factorization identities не заявляются новыми мировыми теоремами. Новое потребление — настоящий макровес именно этого CAR-протокола, все его метрические sources и проверка gravity consumer.

## 2. Та же полная программа, не новый вероятностный прибор

Сохраняем `eta=diag(1,-1,-1,-1)`, обратную тетраду F (не feedback!), `n^T eta n=1`,

    h_n=-eta+2(eta n)(eta n)^T, L^T L=h_n,
    nu=L n, u_r=L eta F_r^T,
    Q_rs=u_r.u_s, b_r=nu.u_r,
    q=2bb^T-Q=F eta F^T, g=q^-1.

На всём CAR16 `zeta(w)=sum_i w_i(C_i-C_i*)` удовлетворяет `zeta*=-zeta`, `zeta*zeta=|w|²I`. Собственная дилатация

    V_delta(w)=[[s_w I,delta zeta(w)],
                [delta zeta(w),s_w I]],
    s_w=sqrt(1-delta²|w|²)

имеет scalar flag effect `r_w I`, `r_w=delta²|w|²`. У настоящего произведения двух таких операций ДО регистрации нижний block есть `delta[s_u zeta(v)+s_v zeta(u)]`, откуда

    r_uv=r_u+r_v-2r_u r_v+2delta²s_us_v(u.v).          (1)

Пять singles: nu и четыре u_r. Десять pairs: шесть u_r,u_s и четыре u_r,nu. Их probability functions обозначаются r_a, a=1,...,15. Все complements сохраняются.

После любой положительной прежней истории нормированная matter/reference подготовка может измениться, но следующая вероятность остаётся r_a: её effect скалярен на ВСЁМ data carrier. Поэтому при фиксированных коэффициентах повторения дают точное Bernoulli product даже при исходной запутанности. Fresh flags требуются; старые records не reset. Физическое наличие этих слов, силы и расписания не доказывается матричной формулой.

## 3. Полный макровес

В каждой ячейке x каждая настройка a исполняется M раз. Полная лента хранит порядок и все исходы. Пусть K={k_xa} — событие заданных counts flag1. Его projector есть сумма ортогональных pointer projectors всех соответствующих полных слов. Это положительное grouping, не когерентная сумма amplitudes до Born; вся исходная лента остаётся доступной.

Точный вес:

    W_K=product_(x,a) binom(M,k_xa) r_a(x)^k_xa
                                  (1-r_a(x))^(M-k_xa). (2)

Сумма по ВСЕМ count-событиям равна1. Биномиальные множители сохраняют реальную microscopic multiplicity. При исходном same-history likelihood binding цена ЭТОЙ макроветви равна

    S_K=-log W_K/ell, ell=log(phi).                    (3)

Она не равна среднему H/count-энтропии. Весь complement события входит в полный опыт.

Для фиксированных целых M,K и произвольного настоящего полевого tangent:

    ell dS_K=sum_(x,a) [(M r_a-k_xa)/(r_a(1-r_a))] dr_a. (4)

dr_a содержит настоящие coframe, clock, strength и square-root derivatives. Нормированная preparation source отменяется здесь только по scalar effect identity. Целые counts или число повторений не имеют выдуманной гладкой производной.

Если в F_* counts совпадают с вероятностями, `k_xa=M r_a(F_*)`, то

    dS_K|F_*=0,
    ell d²S_K[U,V]=M sum_(x,a) dr_a[U]dr_a[V]/(r_a(1-r_a)). (5)

Коэффициенты при d²r равны0 по полному (4), не по замораживанию jets. Более того, точно

    S_K(F)-S_K(F_*)=(M/ell)sum_(x,a)
                          D_Bern(r_a(F_*)||r_a(F)).    (6)

Это разность цен одного и того же события, а не counterterm. (6) уже полностью идентифицирует динамический смысл данного functional: сравнение с сохранёнными частотами.

## 4. Все десять slots и решающий flat source

При F_*=I,n=e0, `r=delta²`, `0<r<1/2`, singles имеют вероятность r; orthogonal pairs — `2r(1-r)`; time/clock pair — `4r(1-r)`.

Для каждого symmetric V настоящая coframe-вариация

    delta F=V eta/2

даёт `delta(F eta F^T)=V`. Новый checker получает15×10 Jacobian непосредственно из полных CAR-effect jets. Её rank10, а Hessian (5) положительна на всех10 metric slots. Невзвешенная потеря off-diagonal entries не используется.

В рациональном fixture `delta=3/5,M=625` все counts целые: 225 для каждого single, 288 для orthogonal pairs, 576 для time/clock. Это диагностический параметр, не новая physical calibration. Общий вывод (7) ниже действует для всего `0<r<1/2`, включая `delta=1/64` прежнего fixture; в последнем случае можно взять M=2^24.

Возьмём пространственно ПОСТОЯННОЕ семейство

    F(t)=diag((1+t)^-1,1+t,1,1),
    g(t)=diag((1+t)^2,-(1+t)^-2,-1,-1).

Все spacetime jets g равны0 и `det g=-1`. Поэтому на замкнутом coordinate torus Einstein–Hilbert равен0, volume постоянен для каждого t. Но полный source (5), при фиксированных K, даёт

    (ell/M)S_K''(0)
      =12r/(1-r)+10r(1-2r)^2/[(1-r)(1-2r+2r²)]>0.      (7)

В проверенном рациональном fixture:

    S_K''(0)=12751875/[2696 log(phi)]>0.               (8)

Уже две singles дают нижнюю границу `8r/(1-r)`; остальные сохранённые настройки её не компенсируют. Проверены все10 rows, не только один scalar detector.

**Следствие:** никакие постоянные a,b,c не дают тождество `S_K=a S_EH+b Vol+c` на этой окрестности. Тот же нулевой Rayleigh component на constant zero-momentum формах этого не меняет. Это не запрещает GR с реальным измерительным прибором: K, clock и programme являются сохраняемыми аппаратными данными; их likelihood-source может принадлежать материи. Именно поэтому он не является найденным metric-only vacuum source.

На решётке (2) факторизуется по x: между разными ячейками его Hessian равна0. Увеличение M не создаёт curvature kinetic. Coupled spatial acceptance или geometry-changing evolution были бы другим настоящим programme/source, а не следствием (2). Нельзя варьировать событие вместе с полем по k=M r(F) и называть это source фиксированной истории. Суммирование по всем K даёт1, но это также другой coarse event.

## 5. Полная условная запись не создаёт исходный геометрический marginal

Пусть существует конечный geometry-sector readout Pi_g и настоящая isometry

    V=sum_g Pi_g tensor V_g, V_g*V_g=I.

Тогда операторно

    V*(Pi_g tensor I_record)V=Pi_g.                  (9)

Доказательство — ортогональность Pi и изометричность каждого V_g. Поэтому для любой rho, в том числе с межсекторными coherences и полной reference, вероятность g сохраняется при каждом таком НЕусловном новом record. Тождество композиционно. Оно не запрещает backreaction на conjugate variables или изменение будущих probabilities после отдельного geometry-changing operator; к такому оператору (9) не применяется. Negative control включён.

Классическое следствие при исходном геометрическом весе W0:

    W(g,omega)=W0(g)q(omega|g), sum_omega q=1,
    sum_omega W(g,omega)=W0(g),
    S_event(g)=S0(g)-log q(omega|g)/ell.               (10)

После суммирования всей новой ленты остаётся прежний source S0. Выбор конкретной записи добавляет её реальный conditional source, например (4), но не выводит прежний закон геометрии. Прежний metrology owner сам задаёт coefficients как параметры; (9) не объявляет доказанным quantum carrier всей геометрии D0.

## 6. Что именно условные данные не определяют

Все q(omega|g), включая любые их jets, совместимы с разными положительными W0(g). Замена `W0 -> exp(-ell B(g))W0` оставляет эти conditional data неизменными, но меняет исходный source на dB. Это не новая допустимая D0 gauge-операция и не разрешение добавить counterterm. Это доказательство недостаточности условных данных для идентификации полного веса; различные W0 означали бы разные реальные preparations/laws.

На связном chart два положительных веса дают один геометрический source тогда и только тогда, когда `d log(W1/W2)=0`, то есть их отношение постоянно по настоящим вариациям. Таков точный source-equivalence критерий.

Даже на одном полном трёхбуквенном golden F/R дереве событие «первая F» имеет массу p, а «все три F» — p³. Все8 слов и оба complements сохраняются. Оба readout определены без внешнего catalogue, но это разные события. Они не предлагаются как две полные физические теории; скалярный Cost−Info закон сам не заменяет geometric event map.

Это согласуется с фактическим `M1ClassAdmissibility.lean`: no-catalogue класс может иметь много объектов, а M1Forced требует отдельного уникального constraint. `EndogenousActionQuantum.ActionProtocol` содержит action_refl и посылку action_nontrivial>=1; он не задаёт полного W0(g,psi). Доверие к верным theorem owners не расширяет их кванторы.

## 7. Параллельный determinant и альтернативная вариационная ветвь

Положительная collective construction `Pr(E0)=det(I-zF)` сохраняется. Но canonical trace-input для ТОЙ ЖЕ одночастичной survival effect K даёт `Tr K/d`, а d независимо подготовленных trace-inputs — `(Tr K/d)^d`. Это разные ensembles/cuts; их ресурсные и native-selection условия не исчезают.

На принадлежащей AF двухкопийной структуре `F=diag(E,E)`, `E=diag(e+u,e-u)`, точно

    W_det=[(1-ze)^2-z²u²]^2,
    W_repeated_trace=(1-ze)^4,
    d_u²[-log W_det+log W_repeated_trace]|0=4z²/(1-ze)².

При scalar variation на u=0 первые sources совпадают. Поэтому этот контроль НЕ отвергает общую leading infrared universality; он запрещает молчаливую замену полной цены одного события другим. Standard determinant/Fock context: Klich, arXiv:cond-mat/0209642.

Наконец, W над пространством метрик НЕ является обязательной предпосылкой любого вывода GR. При уже заданной полной native вариационной цене можно идти прямо от её истинных finite equations, как допускает BOOK03 §03.8. Прежнее требование обязательно сначала построить probability prior было слишком сильным. Требуется либо полный history weight с собственным geometric readout, либо полный primitive action на настоящем carrier/constraints. Оба маршрута должны дать один полный source, а не только conditional meter action.

Существующая homogeneous stored-v8 reduction уже даёт собственную Gamma с положительным flat shape-source после retained equations; она не отождествляется с новой AF-star конструкцией по названию. Lovelock применяется после действительного metric-only natural/local second-order source, не к (5) при наличии записи K. Он также не доказывает ненулевой coefficient всей цены.

## 8. Статус и воспроизводимость

Главная цель D0→GR НЕ достигнута этим пакетом. Положительные Palatini/recovery владельцы не опровергнуты. Завершена проверка конкретного заполнения W через literal geometric count-record: это приборная likelihood, не недостающий вакуумный закон. Условные record/code/gain identities сами не добавляют geometry dynamics. Это точная граница применённой цепочки, не утверждение об отсутствии любых иных полезных данных во всём репозитории.

[check_macrohistory.py](check_macrohistory.py): Python3.13.5, SymPy1.14.0; 246 explicit exact checks, normal и python -O совпали. Большинство строк — компонентная сверка всех10 jets15 исходов, не246 независимых физических теорем. Проверены full reference128, все complements, count normalizer/source, полный Fisher/LDL, fixed-volume flat witness, QND и geometry-changing control, golden events и collective-source distinction. Старый owner main, old roots/spectra/Lean, global validators и full CI не запускались. Physical execution/admission, full-source selection и original raw terminal не повышаются.
