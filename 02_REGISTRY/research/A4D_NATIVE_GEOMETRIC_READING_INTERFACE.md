# Record-геометрия: нормальные поля, десять metric slots и условный source consumer

15 октября 2026. Исследовательский интерфейс к существующему SOURCE #310.
Исходные пять пользовательских файлов сохранены без изменений в
[архиве входа](sources/d0_record_second_jet_intake_2026-10-15/provenance.json).
Это исправленное математическое чтение, не объявление нового native action,
физического допуска, выбранного observer или закрытия ОТО.

Используется ровно Pauli-product fixture из архивного `INPUT_check_record_2jet.py`.
[Узкий consumer](sources/d0_record_second_jet_intake_2026-10-15/record_consumer.py)
проверяет его SHA, исполняет исходный код один раз с перехватом JSON и
потребляет его матрицы. Вторая копия реализации germ не создаётся.

## 1. Что действительно задано

Параметр `x` лежит в открытой окрестности нуля в R4. Он не отождествлён с
узлом конечной scene, физической координатой или scale h. При d=4 положим

    J_U psi = sqrt(p)|0>psi + p|1>U(x)psi,
    P_U = J_U J_U*,  p+p²=1,
    P_U = [[p I, sqrt(p³) U*], [sqrt(p³) U, p² I]].

Для U(x) унитарной это настоящая изометрия и проектор, без postselection.
Вход задаёт свободный аналитический germ

    U(x)=exp(i H(x)),
    H(x)=sum A_mu x_mu + (1/2)sum B_mu,nu x_mu x_nu.

Использованы четыре A из labels `(01),(02),(03),(10)` и десять B из
`(11),(12),(13),(20),(21),(22),(23),(30),(31),(32)` в Pauli-product basis.
Их получение из admitted D0 operations и их общего field law не доказано.
В частности, здесь не определяется собственное пространство всех допустимых
подготовок Omega_h и не строится его физическое чтение Pi_h.

## 2. Метрика, connection и кривизна с одной нормировкой

На вещественном пространстве Hermitian 2d-матриц используется постоянное
положительное скалярное произведение

    <X,Y>_d = Re Tr(X*Y)/(2d),
    E_mu = partial_mu P_U,
    q_mu,nu = <E_mu,E_nu>_d
            = (p³/d) Re Tr[(partial_mu U)* partial_nu U].

В точке 0: `q=p³ I4`, `partial q=0`. Умножение всех projector jets на
`sqrt(p³)` восстанавливает множитель, вынесенный из исходной проверки.
Levi-Civita connection и second fundamental form относительно этого же
ambient inner product равны

    Gamma^rho_mu,nu = q^(rho,sigma) <E_sigma,partial_mu partial_nu P>_d,
    b_mu,nu = partial_mu partial_nu P-Gamma^rho_mu,nu E_rho.

Если использовать raw `Re Tr(X*Y)`, справа в Gamma обязателен множитель
`1/(2d)`. При исходном Gamma(0)=0 его пропуск не обнаружить. Consumer
проверяет настоящую замену координат `x0=y0+3 y0²/4`: правильное
`Gamma^0_00=3/2`, а ошибочное raw-trace чтение даёт 12.

Для полной second fundamental form Gauss formula даёт sectional curvatures
`p^-3*(0,0,-1,0,-1,-1)` в порядке `(01,02,03,12,13,23)`, а scalar
curvature равна `-6/p³`. Это геометрия свободного положительного germ;
она ещё не является кривизной физического Lorentz metric D0.

## 3. Настоящая normal metric variation

Пусть `N_A=sqrt(p³)[[0,-i B_A],[i B_A,0]]` в точке 0. Эти десять векторов
одновременно являются tangent vectors к unitary graph P_U и нормальны к
четырёхмерной immersion. Они имеют Gram `p³ I10`. В выбранном germ

    <b_mu,nu,N_A>_d = p³ delta_((mu,nu),A), mu<=nu.      (1)

Равенство (1) само по себе ещё не задаёт variation of the metric. Нужны
нормальные ПОЛЯ вдоль immersion, а не только векторы в одной точке.
Их можно построить внутри того же unitary graph. Возьмём

    Y_A(x)=D P_U[i B_A U(x)],
    eta_A=Y_A-E_rho q^(rho,sigma)<E_sigma,Y_A>_d.

Вблизи 0 метрика невырождена, поэтому поля гладкие. Каждое eta_A нормально
ко всем E_mu и по-прежнему tangent к unitary graph. В нуле eta_A=N_A.
Соответствующий return tangent `delta U_A` удовлетворяет
`delta U_A U*+U delta U_A*=0`; его реализует точная унитарная деформация

    U_epsilon(x)=exp(epsilon delta U_A(x) U(x)*) U(x).

Для любого гладкого normal field `eta=sum f^A eta_A` дифференцирование
`<eta,E_mu>_d=0` даёт действительное тождество

    delta q_mu,nu=-2<b_mu,nu,eta>_d,
    delta q_upper(0)=-2p³ f(0).                         (2)

Consumer независимо проверяет значение и первый x-jet этих полей,
линеаризованную унитарность и саму производную q. Умножение U слева на
`exp(i epsilon B_A)` без normal projection даёт изометрический перенос:
при тех же point normals его `delta q=0`. Поэтому условие normal FIELD
нельзя опустить.

Другое важное различие: изменение только коэффициентов B_mu,nu в H при
неизменных U(0),partial U(0) оставляет q(0) неизменной. В (2) B обозначают
генераторы normal displacement; это не утверждение, что изменение second
Taylor coefficients само по себе меняет q(0).

## 4. Packed pairing, right inverse и условная стационарность

Порядок metric coordinates:

    q_upper=(q00,q01,q02,q03,q11,q12,q13,q22,q23,q33).

Если tensor source определён через полный symmetric contraction
`sum_(mu,nu) E^(mu,nu) delta q_mu,nu`, его packed DUAL равен

    e=(E00,2E01,2E02,2E03,E11,2E12,2E13,E22,2E23,E33).

В normal COEFFICIENT coordinates f имеем

    ell=-2p³ e,
    e=-(2p³)^-1 ell,
    ||e||_2=(2p³)^-1 ||ell||_2.                         (3)

Это точный pointwise inverse в указанных Euclidean norms. При норме самого
ambient normal field `||eta||_d=sqrt(p³)||f||_2` постоянная меняется:
right inverse от upper metric norm к ambient normal norm имеет
норму `1/(2 sqrt(p³))`. Это не refinement-uniform physical bound.

Условный functional consumer: пусть полный variation на независимо заданном
физическом классе имеет вид

    delta S = integral sum E^(mu,nu) delta q_mu,nu

после сохранения нормализатора и всех link/matter/archive terms. Если
компактно поддержанные поля f^A действительно допустимы, другие поля
фиксированы либо их собственные Euler terms равны нулю, то стационарность
по этим полям и (2) влечёт E=0. Полный ранг сохраняется в достаточно малой
окрестности нуля по непрерывности, поэтому применима fundamental lemma.

Без этого action factorization и допуска вариаций (3) не выводит Einstein
equations, physical Ward или source descent на общую preparation fibre.
Другие переменные, меняющиеся вместе с normal deformation, должны иметь
свои слагаемые в variation. Ambient unconstrained Euler по всем Hermitian
P также нельзя подставить вместо constrained unitary/projector variation.

## 5. Что доказывает linear control

При B_mu,nu=0 first metric остаётся p³I. Полная ambient second normal form
имеет span rank 4, а не 0: это Hermitian anticommutator terms. Их нижние
блоки не skew-Hermitian, поэтому они не являются допустимыми return
tangents внутри unitary graph. Их пары с выбранными десятью N_A равны
нулю. Таким образом исходный `rank0` относится к выбранным unitary-graph
normal probes, тогда как ambient normal span имеет rank4.

Полный nonlinear fixture имеет rank10 уже на выбранных допустимых normal
probes. Удаление одной выбранной нормали даёт rank9 на оставшемся
подпространстве; оно не доказывает, что никаких других допустимых нормалей
нет. Это controls заявленного интерфейса, не классификация всей D0.

## 6. Связь с реальными source owners

Уже принадлежат репозиторию [полная source recursion и критерий спуска](A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md),
[все joint tangents](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md),
[intrinsic constrained covector](A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md)
и [field-to-instrument first-jet boundary](A4D_NATIVE_FIELD_TO_INSTRUMENT_JET_BOUNDARY.md).
Они не выбирают A_mu,B_mu,nu и не превращают свободную U(4) germ в native law.

Не установлено additive identity `A=H+J+R+Info+normalizer`. Entropy readouts,
prepared expectation, feedback determinant и полная тепловая цена имеют
разные владельцы и требуют одной общей preparation/action binding.
Материя и нормализатор не замораживаются для получения (3).

При независимо заданной ненулевой observer line t можно отразить signature:

    g=2(qt)(qt)^T/(t^T q t)-q.

При фиксированном t это involution между соответствующими positive/Lorentz
charts. В точке q=p³I,t=e0 его ten-slot derivative имеет знаки + на 00,0i
и - на ij, i,j>0, и квадрат I. Это проверка rank preservation; сама line,
её совместный jet и физическая time/future orientation не выведены.

Finite Fibonacci trace-band identity также не определяет beta(h), AF depth
как physical mesh, или совместное refinement variation law. Тепловой
контрпример beta=h рассматривается отдельным владельцем; second-jet rank
не заменяет его spectral/action hypotheses. Полный native источник,
совместная стационарная ветвь и вывод ОТО остаются открытыми.

Содержательный consumer уже есть в
[интеграции second-jet пакета](A4D_NATIVE_RECORD_SECOND_JET_SOURCE_CLOSURE.md):
на фактической full-blank кривой второго AF record observer pairing остаётся
I, но полный operator Cost-Info имеет ненулевой derivative. Сохранённая
наблюдаемая `r_B=Tr(sigma4,B)` имеет `r'_B=-8ap7` и видит эту кривую.
Поэтому одного observer-metric чтения недостаточно для этого source;
`r_B` пока не отождествляется с resonant chi и не заменяет полный joint
matter/archive covector. Свободная projector metric настоящего раздела
также не отождествлена с данным observer pairing.

Параллельный [price-metric source owner](A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md)
уже выводит projector metric как Hessian действительной comparator-price и
строит phase-complete lift для отдельной twelve-channel record family.
[Конечное cylinder curvature reading](A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md)
даёт точный calibrated curvature covector с полным moving-preparation jet.
Эти результаты потребляются в [общем intake](A4D_NATIVE_RECORD_SECOND_JET_SOURCE_CLOSURE.md).
Они не превращают свободную U(4) family в native AF/CAR автоматически;
оставшееся отождествление относится к общему native action/field law.
Для чисто геометрического потребления cylinder-теоремы на настоящем P_U
берётся полное normal Parseval family в Herm(C8): ambient dimension64,
normal dimension60. Тогда её exact reading в нуле равно `-6/p³`.
Десять выбранных graph-normal probes из (2) не заменяют это полное семейство.
