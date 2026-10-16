# Настоящее исключение прибора при фиксированной физической метрике

17 октября 2026. Тот же Draft #334 и условная stored-v8 цена.
Вход: `237829b10d6b2f0d7c9b5b1d768ac1bb37882cad`.

**Результат.** В окрестности существующего faithful корня построена
гладкая подготовка вместе с наблюдателем и stored-связями для **каждой
близкой постоянной физической Lorentz-метрики**. Их собственные уравнения
выполнены, а десять метрических уравнений остаются производными той же
цены. Их Hessian имеет семь положительных направлений и три нулевых.
Даже после этого настоящего исключения переменных остаётся положительный
отклик на плоской кривой с постоянными объёмом и собственной ценой материи.
Следовательно, в данном секторе нельзя получить pure EH+Lambda+same R
одним Schur-исключением наблюдателя и подготовки.

Это локальная однородная теорема исходного stored chart. Она не переносит
его классификацию на расширенный full-Lorentz interface, не выбирает
физическую цену и не является исходным fixed-g/fixed-tau/raw terminal.

## 1. Потреблённые доказательства и неизменённые объекты

Используются [совместный владелец](A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md),
§§2,3,5,9, и [точное развёртывание цены](A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md).
Их spectrum/root suites не запускаются заново. Новый результат заполняет
реальный, но только однородный, случай условного retained-section перехода
[полного Ward-владельца](A4D_FULL_EXPERIMENT_WARD_AND_METRIC_DESCENT.md), §5.

Сохраняются L=8, full16, все4096 тепловых momenta, reference128,
исходные workspace multiplicities, fixed alpha,beta,z,M,C и

    S=F_price(Delta)+Tr(rho Delta),
    F_price=log(C Tr B^m)/beta-M Tr log[(1-z)I+zB^m],
    B=I-alpha Delta, beta=m alpha, m=16384.

Подготовка нормирована. На восьми momenta +/-e_r проектор P содержит
ВСЕ16 grades, rank128. Translation-invariant density на P имеет
8*16^2-1=2047 вещественных координат. Полная amplitude/reference
структура восстанавливается из rho; дополнительные вариации не удаляются.

Пишем q=F eta F^T для **контравариантной** физической метрики, g=q^-1.
Все десять q-slots эквивалентны десяти g-slots через обратимую производную
инверсии. Positive operator Gram обозначается G, не q. У корня

    F*=c I+b 11^T, c=a-b>0, b>0,
    G*=F*F*^T=c^2 I+k 11^T, k=2bc+4b^2>0.

## 2. Все десять физических метрических направлений имеют matter lift

Для произвольного постоянного observer n^T eta n=1 имеем точно

    G=F(-eta+2nn^T)F^T.

Выбираем локальное smooth section F(q) отображения F->F eta F^T;
его differential можно взять

    delta F=(1/2) delta q F^-T eta.

Остальные шесть frame coordinates сохраняются как параметры, а не
объявляются отсутствующими физическими переменными. При fixed F и
n=e0 observer tangent delta n=(0,nu) даёт

    delta G=2F(e0 nu^T+nu e0^T)F^T,
    delta(G_ii-G_00)=4bc[nu_i-sum_j nu_j], i=1,2,3.

Здесь nu в первой формуле дополнен нулевой временной компонентой.
Следовательно, соответствующий 3x3 Jacobian и обратный равны

    J_obs=4bc(I_3-11^T), det J_obs=-128 b^3 c^3 !=0,
    J_obs^-1=(I_3-11^T/2)/(4bc).

Для любого delta q сначала берём указанный delta F, затем

    nu=-J_obs^-1 [delta(FF^T)_ii-delta(FF^T)_00]_(i=1..3).

Это явный lift всех десяти метрических slots с равными diagonal G jets.
Нелинейный IFT даёт единственный близкий n(q) с
G_11=G_22=G_33=G_00=d(q). Ставим все четыре stored link angles равными0.
При постоянных полях сами proper links тогда I и оба stored-adjoint
условия выполняются точно. Это не подстановка SO4 links вместо SO3.

## 3. Решены собственные уравнения ВСЕЙ подготовки, а не семь тестов

Любой homogeneous operator сохраняет каждый momentum. Поэтому P/Q
не смешиваются даже вне полного joint root. При links I и равных
diagonal G

    P Delta P=epsilon(q) P, epsilon(q)=gamma d(q),
    gamma=128-64sqrt(2)>0.

Все amplitude equations выполнены для любой rho, поддержанной на P.
Нормировка Tr rho=1 остаётся точной. Внеспектральные amplitude rows,
межмоментные вариации и все reference columns тоже имеют нулевой
matter residual, поскольку Delta действует скаляром на всём P.

У корня trace-centered shell map T имеет rank7. Три scalar rows —
разности diagonal G; четыре независимые traceless rows — link angles
(это полный16 rank theorem совместного владельца, §9). На retained
field coordinates y=(observer3,link4) его restriction T_ret обратимо:
J_obs обратим, а scalar и traceless link images независимы.

Разлагаем 2047 density coordinates на семь направлений, dual к T_ret,
и 2040 neutral parameters eta_r. Выбранные семь density equations
имеют обратимый y-Jacobian. Их точное решение уже предъявлено выше:
y=y0(q), links I, равные diagonals. Поэтому локальная уникальность IFT
заставляет это быть решением выбранной системы, а весь scalar-shell
identity делает остальные2040 density equations тождественно нулевыми.
Нельзя заменить этот аргумент одним подсчётом rank на линейном jet.

Оставшиеся семь y-field equations линейны по rho. Их Jacobian по
семи dual-density coordinates равен T_ret^*. Поэтому эти семь
коэффициентов определяются однозначно и гладко при любых малых
(q,eta_r,frame6). Это решения **собственных** source equations той же
цены, не назначенный внешний stress. В достаточно малой окрестности
rho*>0 сохраняется от исходной P/128. Подготовка
Psi=sqrt(rho) U_ref имеет все128 reference columns; U_ref сохраняется.

Шесть frame equations следуют из точного internal-Lorentz representation
identity при уже выполненных observer/link/matter equations. Меняется
весь прибор и matter, а не только F. При fixed-coordinate density вместо
совместно преобразованной добавляется уже нулевая density row.
Это применение covariance, не объявление этих параметров физическим
gauge. Ненулевые Fourier first-source rows равны0 по translation
invariance самой подготовки и полей. Построено решение retained rows
над пространством **постоянных** метрик; не построена секция над всеми
неоднородными q(x).

## 4. Полная reduced цена и её семь положительных направлений

На найденной секции цена в точности равна

    Gamma(q)=F_price(G(q,n(q)))+gamma d(q).

Она не зависит от2040 neutral density parameters и шести frame
parameters. Собственная matter price равна gamma d(q); thermal
normalizer, feedback и их derivatives остаются в F_price.

Обозначим L:delta q->delta G после observer correction. Его image —
все семь symmetric equal-diagonal G directions. Явный right inverse:
для любого такого delta G берём delta F=delta G F^-T/2, затем вычисляем
delta q=delta F eta F^T+F eta delta F^T. Observer correction в выбранном
F(q) section восстанавливает ровно исходный delta G: разность двух
подъёмов есть internal Lorentz variation, чей boost-image в diagonal
differences обратим. Три kernel directions имеют вид

    delta q_i=F*(K_i eta-eta K_i)F*^T,
    (K_i)_0i=1, (K_i)_i0=-1, i=1,2,3.

Это независимые изменения Lorentz reflection при fixed positive G.
Они не удалены как gauge. Поэтому rank L=7, dim ker L=3.

Уже доказанная полная finite-price convexity (§9, (30)-(31)) даёт для
V(G)=F_price(G)+gamma d на этом семимерном пространстве

    H_V[f,f] > (3 beta/10) E_w[(f_k/B_k)^2] >0 for f!=0,
    w_k=16 B_k^m/Z, Z=Tr_H B^m.

Ground multiplicity16 и moving global Z существенны для этой границы.
Поскольку dV(G*)=0, acceleration карты G(q) исчезает из Hessian:

    Hess Gamma=L^* H_V L, inertia=(7 positive,0 negative,3 zero).

Проверка через настоящий Schur даёт тот же вывод. Retained14 block
имеет вид [[H_yy,T_ret^*],[T_ret,0]] и inertia(7,7,0) при любом H_yy.
Его обратимость не требует обращения нулевого density block.
Из полной q0 inertia(14,7,2049), после сохранения frame6 как параметров
и исключения этой пары блоков, получаются metric(7,0,3) и2040 neutral
zeros. Уникальные entropy/precision auxiliaries не подменяют этот расчёт.

## 5. Pure EH+Lambda+тот же R исключается уже ПОСЛЕ retained equations

Для исключения volume/matter ambiguity берём actual root G* и

    H=E01+E10-E02-E20, V=E01+E10,
    G(t)=G*+tH+r(t)V, det G(t)=det G*, r(0)=r'(0)=0.

Все diagonals постоянны точно. Если G*^-1=A I+D 11^T, то
A=1/c^2, D=-k/[c^2(c^2+4k)]<0 и

    Tr(G*^-1 H)=0, Tr(G*^-1 V)=2D !=0,
    r''(0)=Tr(G*^-1 H G*^-1 H)/(2D)=2A(A+D)/D.

По IFT такая smooth constant-determinant кривая существует.
Чтобы получить соответствующий physical q(t), берём smooth F(t)
с F(t)F(t)^T=G(t), n=e0 и links I; затем применяем доказанную
retained-section конструкцию. На том же q(t) она сохраняет этот G(t)
по локальной уникальности, решая также собственные density/source rows.

Для каждого t метрика постоянна в пространстве, поэтому R(g(t))=0.
Кроме того, det q=-det G и d(t)=d*, откуда одновременно

    I_EH(g(t))=0, Vol(g(t))=constant, R_actual(t)=gamma d*=constant.

Но off-diagonal gradient F_price в корне нулевой; acceleration r''V
не даёт вклада. Следовательно

    Gamma''(0)=H_V[H,H]>0.

Можно сохранить явную нижнюю границу без нового spectral replay. Четыре
уже существующих grid momenta +/- (e0+e1), +/- (e0+e2) имеют
f_H=+/-2gamma, lambda=2gamma(d*+k), B_pair=1-alpha lambda>0. Поэтому

    Gamma''(0)>(3 beta/10)(256 gamma^2/Z) B_pair^(m-2)>0.

Никакие постоянные c_EH, Lambda не дают на этой окрестности тождество
Gamma=c_EH I_EH+Lambda Vol+R_actual+constant. Это усиливает прежний
flat-modulus test: теперь observer/link/preparation equations решены,
и предположительная компенсация их Schur term вычислена, а не опущена.

## 6. Что именно теперь потребляется маршрутом

Полный Ward сам по себе не делает существующую fixed-beta цену local
metric-only Einstein действием. Для данного нулевого Fourier сектора
retained elimination действительно существует, но сохраняет global
torus shape/scale potential. Его нельзя устранить словами «решим
уравнения наблюдателя» или residual-defined matter.

Требуется собственная native history/price и допустимый controlled limit,
в котором реальный дополнительный отклик либо остаётся самостоятельным
derived сектором, либо исчезает с доказанным source estimate. Здесь не
добавляется counterterm, не выбирается clock/coupling law и не исключается
иная физически выведенная полная цена. Неоднородная retained section,
full-Lorentz joint system, physical admission и исходный raw terminal
остаются задачами своих действительных интерфейсов.

Новый [ограниченный расчёт](sources/d0_homogeneous_metric_reduction_2026-10-17/)
проверяет только новый Jacobian/lifts/ranks/saddle/volume consumer.
Математические основания общего IFT и positivity аргумента даны выше;
finite fixtures не заменяют их. Independent analytical review проведён
двумя помощниками в рамках того же PR; отдельной CONTROL-приёмки нет.
