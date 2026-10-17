# Обратная ОТО: null-сектор двухсторонней записи, Bianchi и одна глобальная строка

17 октября 2026. **RESEARCH / EXACT MATHEMATICAL COMPOSITION / CONDITIONAL NATIVE ROUTE.**
Продолжение существующего Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), без нового task, action, detector и promotion.

**Входы:** [два raw-record Grams и их полный IR Einstein source](A4D_TWO_SIDED_SPATIAL_RECORD_EINSTEIN_SOURCE.md) (публикация 887b74c3); [девять точных null coframe-shears и положительная центральная AF-передача](A4D_BACKWARD_EINSTEIN_SOURCE_COMPLETION.md) (a455e113); [полный finite Ward](A4D_FULL_EXPERIMENT_WARD_AND_METRIC_DESCENT.md); [stored-adjoint конормаль](A4D_STORED_METRIC_PROJECTION_AND_SOURCE_COMPLETION.md); [complete-history cut и normalizer](A4D_RETAINED_HISTORY_READOUT_AND_NORMALIZER.md). Не повторяем их уже закреплённые tensor, CAR, heat, root или compiler computations.

**Главный результат:** две свежие конструкции сцепляются без вычитания volume counterterm. Девять null shear исходного coframe устраняют **точно** доминирующий объёмный source положительного двухстороннего comparator; fixed-beta IR оставляет у них единственно \(\operatorname{Ric}(k,k)\) с вычисленным коэффициентом. Если тот же действительный Cost−Info выбирает этот null-source на своих admissible roots и его полная retained Ward даёт \(\nabla T=0\), девять равенств дают ВСЮ нелинейную Einstein equation с \(\Lambda\) как константой интегрирования. Один настоящий global-scale/source закон определяет её значение. При полном operational SO(3)-equivariance девять физических проверок дополнительно сводятся к **одному универсальному null-закону** на всей инвариантной семье. Все эти выводы имеют точные кванторы ниже; ни одна physical-source premise не объявлена доказанной одной геометрией.

## 1. Исходный обратный объект: положительное полное сравнение

Двусторонний владелец строит нормированные полные raw maps \(J_i=X_iG_i^{-1/2}\), где \(G_i=X_i^*X_i>0\), и \(C=J_1^*J_0\). Полный положительный Julia comparator имеет цену \(-M\log\det(C^*C)\). Из двух **реально нормированных** концов следует точное конечное тождество

\[
J_{\rm cal}=J(E_4)-J(G_0)-J(G_1)+K_{\rm fixed},
\quad
J(E)=-M\operatorname{Tr}\log E .
\tag{1}
\]

Коэффициенты двух endpoint вычитаний не выбираются из Einstein; они следуют из \(G_i^{-1/2}\) в данном comparator. Это не означает, что реальный native engine уже исполняет выбранные \(X_i,C\) и платит именно (1).

На компактном контролируемом семействе positive/ADM геометрий при фиксированных \(\beta,z,M\), \(\beta>0\), и при IR масштабе \(g_L=L^2g\), \(L\to\infty\), уже выведен **условный** полный первый source:

\[
J_{\rm cal,L}=K_L+\lambda_J {\rm Vol}(g_L)
                   +c_J\!\int R(g_L)dV_{g_L}
                   +O_{C^1}(1)+\mathcal E_{\rm setting,L}.
\tag{2}
\]

Здесь \(c_J=4MF_2(r)/[3(4\pi)^2\beta]>0\),
\(\lambda_J=16MF_3(r)/(4\pi\beta)^2>0\),
\(r=z/(1-z)\), \(F_s(r)=\sum_{j\ge1}(-1)^{j+1}r^j/j^s\).
Обе константы — коэффициенты исходного владельца, а не новые параметры.
Остаток (2) относится к smooth controlled first-source/setting limit; он **не** есть исходная strong raw \(h^{-2}\)-оценка.

## 2. Новая сцепка: null shear убивает volume, НЕ curvature

Пусть \(\hat e\) — тот же полный невырожденный Lorentz coframe,
\(\eta=\operatorname{diag}(1,-1,-1,-1)\). Для любого будущего \(\eta\)-null \(\ell\) положим
\(N_\ell=\ell(\ell^T\eta)\). Тогда

\[
N_\ell^2=0,\qquad\operatorname{tr}N_\ell=0,\qquad
\hat e_\varepsilon=(I-\varepsilon fN_\ell/2)\hat e .
\tag{3}
\]

Поскольку \(N_\ell\) nilpotent, \(\det(I-\varepsilon fN_\ell/2)=1\) **точно для любого**
\(\varepsilon\). По прежнему coframe owner, при \(k=\hat e^{-1}\ell\),

\[
g_\varepsilon=g-\varepsilon f\,k^\flat\otimes k^\flat,\quad
g_\varepsilon^{-1}=g^{-1}+\varepsilon f\,k\otimes k,\quad
dV_{g_\varepsilon}=dV_g .
\tag{4}
\]

Итак, \(\delta {\rm Vol}=0\) тождественно вдоль всей конечной кривой (3), а не после вычитания гигантского \(\lambda_JL^4\) слагаемого или только в linearized gauge.

Для \(\delta g_{\mu\nu}=-f k_\mu k_\nu\) первая вариация EH при compact support / сохранённых границах есть

\[
\delta\!\int R(g)\,dV_g
=-\int G^{\mu\nu}\delta g_{\mu\nu}\,dV_g
=\int f\,G_{\mu\nu}k^\mu k^\nu\,dV_g
=\int f\,{\rm Ric}_{\mu\nu}k^\mu k^\nu\,dV_g .
\tag{5}
\]

Поскольку (4) сохраняет volume также после \(g\mapsto g_L\), из (2)–(5) следует **условная теорема об IR null-source**

\[
\boxed{
L^{-2}dJ_{\rm cal,L}[V^{\rm null}_{L,k}(f)]
\longrightarrow
c_J\int f\,{\rm Ric}_g(k,k)\,dV_g .
}
\tag{6}
\]

Здесь \(V^{\rm null}_{L,k}\) — одна и та же относительная coframe-скорость при \(g_L=L^2g\): \(\delta g_L=-L^2f\,k^\flat_g\otimes k^\flat_g\). В (6) дифференцируются ВСЕ actual endpoint Grams, weighted spatial lapse и reference frames уже выбранного comparator. Доказательство использует его опубликованный \(O_{C^1}(1)\) remainder и допускает лишь те settings/quadratures, для которых \(\mathcal E_{\rm setting,L}/L^2\to0\) также по первой вариации. Фиксированная \(\beta\) не стремится к нулю; \(L\) — IR масштаб, не lattice \(h^{-1}\) и не бесплатно выбранные физические часы.

Это действительно улучшает стратегию: **объёмный radial mismatch двухстороннего price не препятствует идентификации null Einstein-формы.** Он по-прежнему препятствует объявлению существования exact large-\(L\) stationary vacuum при произвольно фиксированной форме \(g\): null equations и отдельная scale Euler equation должны иметь совместную физическую ветвь.

## 3. Девять null-равенств плюс FULL Ward => нелинейная Einstein с Lambda

Пусть независимо выведенный matter/source имеет ту же геометрическую конвенцию и на null shear даёт

\[
L^{-2}dS_{m,L}[V^{\rm null}_{L,k}(f)]
\longrightarrow -\frac12\int f\,T_{\mu\nu}k^\mu k^\nu dV_g .
\tag{7}
\]

Это условие: материя не определяется Einstein residual и не добавляется задним числом. Пусть реальная joint stationarity передаёт (6)+(7) для всех compactly supported \(f\). Тогда

\[
{\rm Ric}(k,k)=\kappa T(k,k),\qquad \kappa=(2c_J)^{-1}.
\tag{8}
\]

Достаточно следующих девяти *рационально построенных* null \(k\) в каждом orthonormal frame:
\[
k_i^\pm=u\pm e_i,\quad i=1,2,3;\qquad
k_{ij}=u+(3e_i+4e_j)/5,\quad 1\le i<j\le3 .
\tag{9}
\]

Введём \(S_{\mu\nu}=G_{\mu\nu}-\kappa T_{\mu\nu}\). Поскольку \(G(k,k)={\rm Ric}(k,k)\), (8) эквивалентно \(S(k_a,k_a)=0\) для девяти векторов (9). Точная rational inverse из предшествующего owner доказывает:
\[
\ker(S\mapsto[S(k_a,k_a)]_{a=1}^9)=\mathbb R\,g .
\tag{10}
\]
Следовательно \(S_{\mu\nu}=f(x)g_{\mu\nu}\) **без предположения слабой кривизны**.

Если выполнены все реальные retained и matter Euler rows, полный Ward вместе с contracted Bianchi и \(\nabla^\mu T_{\mu\nu}=0\) даёт
\[
0=\nabla^\mu S_{\mu\nu}=\partial_\nu f .
\]
На связной области \(f\equiv-\Lambda\) и
\[
\boxed{G_{\mu\nu}+\Lambda g_{\mu\nu}=\kappa T_{\mu\nu}.}
\tag{11}
\]

Это математический nonlinear closure theorem. **Простое coordinate Ward полного опыта недостаточно:** когда clock, observer, links, preparation или programme имеют ненулевые собственные Euler, в дивергенцию входят именно они. Равенство (11) не вытекает из девяти измерений без фактически допущенного и полностью стационарного источника.

## 4. Один universal null-law + physical SO(3) covariance заменяет девять независимых законов

Пусть \(\mathfrak F\) — семья действительных подготовок/геометрий, замкнутая относительно *физически допущенных* одновременных frame-transformations, и \(\mathcal D(F,k)\) — полный scalar null source одного SAME record/cut/action. Если

\[
\mathcal D(RF,Rk)=\mathcal D(F,k)\quad
\text{для каждого допустимого }R\in SO(3)_u ,
\tag{12}
\]
и для **всех** \(F\in\mathfrak F\) доказан один общий template
\[
\mathcal D(F,u+e_1)=0,                                     \tag{13}
\]
то \(SO(3)_u\) транзитивно действует на нормированные null направления \(u+n\), \(|n|=1\). Подставляя \(F'=R^{-1}F\) в (13), получаем (8) для любого нормированного \(k=u+n\), а значит все девять (9) и (11).

**Требование к действию группы.** В (12) \(R\) должно переносить **сам физический null-test** \(k\mapsto Rk\) вместе со всей конфигурацией. Одно внутреннее Lorentz-gauge переименование \((e,\ell)\mapsto(Re,R\ell)\), оставляющее пространственно-временной \(k=e^{-1}\ell\) неизменным, не порождает новых физических направлений и НЕ доказывает orbit reduction. Достаточна ковариантность действительно транспортируемого spatial test/cut на всех перенесённых конфигурациях, с включённой стоимостью такого транспорта.

Тождество (13) лишь на **одной фиксированной** конфигурации \(F_0\) этого НЕ даёт. Равенство геометрических рамок под gauge также НЕ означает автоматически (12) для полной физической цены: cut, pointer, observer, reference128 и cost должны трансформироваться одним и тем же допустимым process. Достаточна настоящая spatial SO(3) covariance с перенесённой подготовкой; постулировать новую полную Lorentz group не требуется. При выбранном fixed observer или нарушении label covariance девять направлений остаются самостоятельной проверкой.

**Это ключевая стратегическая редукция:**
полная нелинейная ОТО
\(\Leftarrow\) один *универсальный* операторный null-source law +
operational covariance + on-shell full Ward,
а не каталог десяти независимых fitted stress equations.

## 5. Lambda требует одну global scalar запись, не local trace at every site

После (10)–(11) недостающая trace является постоянной. Если тот же actual native programme даёт одну независимую глобальную response-величину
\[
\mathcal J=\int_M\operatorname{tr}_g(G-\kappa T)\,dV_g ,
\]
то на connected finite-volume \(M\)
\[
\boxed{\Lambda=-\frac{\mathcal J}{4\,{\rm Vol}(M)}.}         \tag{14}
\]
Один uniform scale source или equivalently global trace expectation задаёт \(\mathcal J\); \(4\) следует из dimension, не fit. При отсутствии (14) Einstein+arbitrary integration constant уже является полным локальным GR law. Это не численное определение физической \(\Lambda\).

**Важный контроль:** у complete open Born tree \(N_{\rm raw}=1\) и \(d\log N_{\rm raw}=0\). Одна эта projectivity НЕ определяет ненулевую \(\mathcal J\). У return-cut той же process нормализатор вообще меняется, но физические placement/cost/readout и его relation к global volume ещё надо вывести. Нельзя объявить (14) результатом \(p+p^2=1\) или назначить наблюдательный \(\Lambda\) как параметр ремонта.

## 6. Финитная слабая оценка без дифференцирования null residual

Тот же выигрыш действует до continuum лишь при объявленном discrete Ward. Для **flat periodic four-role finite difference model** с \(\eta=\operatorname{diag}(+---)\) зададим
\[
W_\nu=\sum_{\mu}\eta^{\mu\mu}\Delta_\mu^+S_{\mu\nu},\quad
f=\tfrac14\operatorname{tr}_\eta S,\quad E^\circ=S-f\eta .
\]
Здесь \(\Delta^+\) — честный forward edge difference; \(\Delta^-\) — его periodic backward partner. Для любого finite vector test \(X\) и нулесредней скалярной \(\varphi=\sum_\nu\Delta^-_\nu X^\nu\) точна алгебраическая identity
\[
\boxed{
\sum_x f_x\varphi_x=
-\sum_{x,\mu,\nu}\eta^{\mu\mu}E^\circ_{\mu\nu,x}
                       \Delta^-_\mu X^\nu_x
-\sum_{x,\nu} W_{\nu,x}X^\nu_x .}
\tag{15}
\]

Доказательство: \(\Delta^+f=W-\operatorname{div}E^\circ\);
умножить на \(X\), сложить по всем periodic sites и дважды применить
\(\langle X,\Delta^+Y\rangle=-\langle\Delta^-X,Y\rangle\).
Никакой производной small \(E^\circ\) в RHS нет.

Прежний девятинулевой inverse при **нулевом trace** даёт на каждом site
\[
\sum_{\mu,\nu}|E^\circ_{\mu\nu}|
\le\tfrac{17}{4}\sum_{a=1}^9|E^\circ(k_a,k_a)|
=\tfrac{17}{4}\sum_{a=1}^9|S(k_a,k_a)| .
\tag{16}
\]

Следовательно для smooth/controlled tests \(X\) с bounded \(\Delta^-X\) получаем weak source control без \(\Delta E^\circ\) и без отдельного local trace. При \(W=0\) и exact nine null zeros (15) даёт \(f=\)const на connected graph. Если \(W\ne0\), его второй term обязателен; конкретно designated smooth comparator из #216 может иметь такой defect даже при exact joint root первой ветви.

**Scope:** (15) — точная модельная incidence identity, не доказанная native covariant Ward настоящего full16 proper-link оператора на curved grid. Её реальное применение требует transported/metric-compatible discrete divergence, всех retained Euler и того же density/packed convention. В continuum на compact smooth controlled chart тот же dual аргумент с решением \(\operatorname{div}X=\varphi\) даёт distributional control среднего-нулевого \(f\) через \(L^1\)-null errors и Ward, без потери производной на smooth tests. **Это не strong raw-\(\ell^1\) контроль:** подстановка произвольных grid-frequency tests может потерять uniform bounded derivative. Исходный терминал \(h^{-2}\sum_{x,a\le b}|\Delta E_{ab,x}|\to0\) и независимо заданный smooth comparator остаются OPEN.

## 7. Что надо доказать физически и какой ровно следующий ход

Сочетать центральный AF flag и двухсторонний comparator как будто это уже **один** выбранный Cost−Info нельзя: это два разных составных приборных контракта. Первый даёт source-preserving readout для независимо заданного \(\mathcal Q\); второй конструктивно создаёт правильный nonlinear IR EH coefficient. Их равенство с одной native programme/price/preparation/clock не доказано.

Минимальный **операционный** consumer после настоящего смешанного/root settlement:

\[
\boxed{
L^{-2}\Big(dS_{\rm native,L}
          -dJ_{\rm cal,L}-dS_{\rm matter,L}\Big)
             [V^{\rm null}_{L,u+e_1}(f)]\longrightarrow0
\quad\text{для каждого }F\in\mathfrak F,\ f\in C_c^\infty ,
}
\tag{17}
\]

причём (12), полные retained equations и source conservation должны
следовать из фактически исполняемых old-record placements, all128 outputs,
reference128, all16 matter grades, full controller/failure costs и реального
cut/normalizer; они не могут быть дописаны после получения (11).

Тогда (6)–(13) выводят nonlinear Einstein equation class без
десяти independent source fits. Это точная reduction of *what must be proved*,
не закрытие (17). Для прежнего fixed-g, independent-tau, unweighted
\(h^{-2}\) задачи #334 всё равно нужны отдельный source comparator estimate
и nonempty exact joint-critical refinement, включая curved nongauge UV.
Ключевой разрыв не исчезает от переименования \(L\) в \(1/h\).

Если выбранный физический comparator (17) не проходит admission, другая
математически известная обратная возможность — local horizon first law:
на истинных native records вывести площадь/entropy и boost/energy flux в
одном действительном cut, получить \(R(k,k)=\kappa T(k,k)\) через Raychaudhuri
и ту же (10)–(11). Результат Jacobson,
[Phys. Rev. Lett. 75, 1260 (1995)](https://doi.org/10.1103/PhysRevLett.75.1260),
является **внешним условным математико-физическим мостом**, не доказательством
D0: её \(A/4\) finite capacity ещё не равно дифференцируемой
entanglement-entropy density и native Unruh/boost price.

**Итог:** доминирующий \(L^4\)-volume term уже существующего двухстороннего
comparator **точно не виден** в \(9\)-null sector. Его \(L^2\)-EH coefficient
уже вычислен. Один общий physically admitted null law + operational
rotational covariance + complete on-shell Ward достаточно для
**формы** всей нелинейной ОТО. \(\Lambda\) — одна global response.
Это исследовательский результат, а не native/GR claim promotion.

## 8. Узкие контроли

Файл [check_discrete_null_ward.py](sources/d0_two_sided_null_ward_2026-10-17/check_discrete_null_ward.py)
проверяет exact periodic 4D incidence rank \(15/16\), singleton constant
kernel с одной global trace, полную dual identity (15) с реально ненулевым
off-shell Ward defect, две независимые negative controls
(null без Ward и Ward без null), и nilpotent zero-volume shear.
Эти вычисления не воспроизводят старые null-basis, heat, roots или Lean.
Публикация не означает CI, independent CONTROL или full native admission.

## 9. Нетривиальная дополнительная сцепка: девять световых тестов из золотых амплитуд без рациональной настройки

Предыдущий девятинулевой inverse использовал смешанные направления
\`(3/5,4/5)\` как удобную рациональную нормировку. Для самой D0-цепочки
есть строго более экономный **математический** выбор. Исходный golden split
имеет \`p=phi^-1\`, \`p+p²=1\`: это probabilities двух букв, а реальные
нормированные gate-amplitudes того же уже заданного примитива суть
\`a=sqrt(p), b=p\`. Значит **без внешней пары коэффициентов** имеем
\[
 a^2+b^2=p+p^2=1.
\]
На каждом действительном orthonormal frame выберем
\[
 k_i^\pm=u\pm e_i,\qquad
 \widetilde{k}_{ij}=u+\sqrt p\,e_i+p\,e_j\quad(i<j).
 \tag{18}
\]
Все девять future-null, \`g(u,k)=1\`. Их spatial components — буквально
существующие golden amplitudes \`(sqrt p,p)\`, но **physical mapping**
gate-amplitude → собственная spatial coframe perturbation пока не доказан
и не следует из равенства чисел. Это точный binding candidate, а не новый
запрограммированный закон измерения.

Для симметричного ковектора \`S\` обозначим
\`y_i^±=S(k_i^±,k_i^±)\`, \`z_ij=S(tilde k_ij,tilde k_ij)\`,
\`t=tr_eta S\`; пусть \`d_i=(y_i^++y_i^-)/2\`,
\`b_i^S=(y_i^+-y_i^-)/4\`. Тогда **точно**
\[
\begin{split}
S_{00}&=(d_1+d_2+d_3+t)/4,\qquad S_{ii}=d_i-S_{00},\\
S_{0i}&=b_i^S,\qquad
S_{ij}=\frac{z_{ij}-p\,d_i-p^2 d_j
                        -2\sqrt p\,b_i^S-2p\,b_j^S}
                         {2p\sqrt p}.
\end{split}\tag{19}
\]
Доказательство: в \`S(tilde k_ij,tilde k_ij)\` коэффициент \`S00\`
равен \`1-a²-b²=0\` после подстановки \`Sii=d_i-S00\`; все члены
остаются линейными. В packed10 convention с коэффициентом 2 при
\`i<j\`, measurement determinant равен
\[
 \det L_{\rm golden}=2^{11}p^{9/2}>0.
 \tag{20}
\]
Следовательно kernel девяти golden null rows равен \`span(eta)\`;
добавление одной trace-строки опять восстанавливает все десять
физических метрических компонент. Условие local full-coframe admission
остаётся тем же: конормаль restricted stored-adjoint chart нельзя
просто игнорировать.

Дополнительный выигрыш — **строго лучшая обусловленность**. Прямые
абсолютные суммы столбцов (19) показывают, что максимален столбец
\`y_1^+\`:
\[
 \|L_{\rm golden}^{-1}\|_{1\to1}^{\mathrm{packed10}}
 =1+\frac{1+\sqrt p}{2p}<\frac52,
 \tag{21}
\]
а при summation по полному симметричному \`4×4\`, удваивающему
off-diagonal components,
\[
 \|L_{\rm golden}^{-1}\|_{1\to1}^{\mathrm{full16}}
 =\frac54+\frac{1+\sqrt p}{p}<\frac{17}{4}.
 \tag{22}
\]
Чтобы проверить максимум без численного перебора: diag-столбец каждой
\`y_i^\pm\` в packed-convention имеет сумму absolute coefficients
\`3/4\`, собственный \`S0i\` ещё \`1/4\`; mixed offdiag coefficients
соответственно равны \`(1±a)/(4b)\` для \`i\` как first index,
\`(1±b)/(4a)\` для second index. Так как \`a>b>0\`,
\`(1+a)/b>(1+b)/a\`; первый плюс-столбец превосходит остальные.
Столбец \`z_ij\` имеет сумму \`1/(2ab)\`, а \`t\` — ровно \`1\`;
они меньше \`y_1^+\`. Для полных16 сумм offdiagonal coefficient
считается дважды. Строгие численные потолки следуют из рациональных
оценок \`3/5<p<16/25\`, \`3/4<a<4/5\`:
\`3p>9/5>1+a\`. При переносе к исходной метрической упаковке
сохраняется отдельно \`C_T=sup||T_x^-1||_{1→1}\`, и главное —
то же \`h^-2 sum_x\` **без деления на число ячеек**.
Локальная algebraic conditioning сама не доказывает finite-h
native source-rate и #216 comparator.

**Исполнимый следующий physical binding:** от исходного golden
\`(sqrt p,p)\` через действительно допущенное transport/test слово
получить пространственную null shearing variation (18) и её полный
первый источник. Тогда принцип (12)–(13) сводит девять проверок к
одному universal template, если реально разрешён physical transport
тестов. Такая сцепка устраняет произвольные probe-коэффициенты, но
не импортирует новое пространственное вращение из scalar gate algebra.
