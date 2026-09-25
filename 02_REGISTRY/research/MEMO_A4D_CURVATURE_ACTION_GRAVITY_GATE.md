## 1. Verdict

**`NEW-VARIATIONAL-PRIMITIVE-REQUIRED`**

Task: `EXP-A4D-CURVATURE-ACTION-GRAVITY-GATE`. Research-only, 2026-09-25. Основание: исключительно frozen inputs приложенного brief. Утверждения ниже не являются аудитом текущего репозитория. GitHub и Lean не использовались.

Из заданной конечной архитектуры **не следует выбранное гравитационное действие**. Доказаны три раздельных препятствия:

1. Законы транспорта и конститутивная форма не выбирают скалярный функционал или его коэффициенты. Даже при фиксированных локальности, калибровочной инвариантности и симметриях периодического архива существуют действия с различными физическими пространственными спектрами.
2. Обычные следы конечной аффинной голономии точно забывают её трансляционную, повышающую степень часть. Положительная норма, которая эту часть видит, не становится автоматически аффинно-инвариантной.
3. Не задан эквивариантный перевод coframe/flux в **двойственное пространство именно носителя кривизны** с правилом конечного спаривания по клеткам. Существующее primal/dual flux pairing само по себе этим переводом не является.

Единственный первичный недостающий принцип: **вариационный закон сопряжения coframe/flux с кривизной**, задающий типизированную естественную dual-area insertion и выбирающий соответствующий функционал. Его точная формулировка — в §12. Это необходимое условие заявленного линейного по кривизне маршрута, а не гарантия получения GR.

Положительный конечный результат: при явной ортогональной специализации носителя связь имеет пространственную curl–curl жёсткость. На `(Z/3)^2` два симметричных локальных действия имеют Hessian-спектры

\[
\operatorname{spec}K_A=\{0^{(10)},3^{(4)},6^{(4)}\},\qquad
\operatorname{spec}K_B=\{0^{(10)},12^{(4)},42^{(4)}\}.
\]

Нули разделяются на 8 калибровочных направлений и 2 гармонические моды. Ненулевые сектора удовлетворяют пространственному momentum gate из brief, но не дают ни spin-2, ни временной волновой динамики. Это **контрмодель единственности**, а не идентификация носителей D0 с этим примером.

Независимы от неизвестных plaquette coefficients: trace-blindness, недостаточность симметрий для выбора действия, необходимость типизации pairing, отсутствие заданной временной динамики. Зависимы от носителя и результатов curvature task: конкретный curl, торсионный смысл \(\Theta\), ранг блоков, разрешённые contraction maps и возможность ненулевого Palatini Hessian.

## 2. Candidate action classification

**Граница классификации.** Frozen inputs не задают полную локальную gauge group, её представления на flux/coframe, размерность, клеточное произведение или действие пространственных симметрий. Поэтому безусловный численный список «всех независимых инвариантов D0» невозможен. Можно дать полную классификацию через пространства invariant tensors и явно классифицировать trace-семейство; подстановка конкретных представлений превращает её в конечную линейную задачу.

Пусть \(\mathcal C_x\) — пространство линейных вариаций кривизны всех ориентированных плакеток у \(x\), \(E_x\) — вариации coframe/constitutive data, \(G_x\) — выбранная группа. До второй степени локальная скалярная плотность имеет вид

\[
c+\ell_E(h)+\ell_C(X)+\tfrac12 A(h,h)+B(h,X)+\tfrac12 Q(X,X),
\]

где

\[
\ell_E\in(E^*)^G,\quad \ell_C\in(\mathcal C^*)^G,\quad
A\in(\mathrm{Sym}^2E^*)^G,\quad
B\in(E^*\otimes\mathcal C^*)^G,\quad
Q\in(\mathrm{Sym}^2\mathcal C^*)^G.
\]

Независимые классы получаются после quotient по точным конечным дивергенциям и алгебраическим тождествам. Межплакеточные contractions включены в \(\mathcal C\). Это исчерпывает полиномы данной степени при фиксированных носителях; дополнительные разности увеличивают stencil. На фоне, нарушающем симметрию, используется стабилизатор фона. Нелинейное gauge completion квадратичного инварианта — отдельное условие.

| Семейство | Скалярная плотность | Доступность и физический тип |
|---|---|---|
| Linear character | \(\ell(X)\) | Нужен invariant covector; для unrestricted End существуют trace characters. Это не EH-contraction |
| Plaquette character | \(\mathrm{tr}[I-(P+P^{-1})/2]\) | Точный conjugacy invariant, curvature-squared Hessian; знак зависит от группы |
| Transpose-sym trace | \(\mathrm{tr}[I-(P+P^T)/2]=n-\mathrm{tr}P\) | Сам trace инвариантен; локально может иметь линейный член |
| Trace quadratics | \(\mathrm{tr}X^2\), \((\mathrm{tr}X)^2\) | Два независимых квадратичных инварианта unrestricted End при размерности ≥2; на sl/so второй исчезает |
| Curvature norm | \(\frac12 Q(X,X)\) | Положительность требует подходящего инвариантного/ковариантного Riesz map; YM-type на связи |
| Flux-curvature | \(\langle B(e,F),X\rangle\) | Нужен \(B(e,F)\in\mathcal C^*\); данный flux pairing не задаёт B |
| Palatini pattern | \(\epsilon_{abcd}e^a e^b X^{cd}\) | Нужны все данные из таблицы ниже; сейчас лишь условная схема |
| Constitutive potential | \(V(W)\) | Только разрешённые симметрией scalar contractions; локальный Hessian без разностей |
| Matter-flux energy | \(\frac12\langle j,Q_Fj\rangle\) | Owned flux energy на своём носителе; подстановка \(j=j(X)\) требует отдельной карты |
| Odd-channel norm | \(\|C^\dagger(\Theta)P_0\|^2\) | Видит odd channel; инвариантность под полными affine changes не следует |
| Derivative-curvature | \(Q(\nabla X,\nabla X)\) | Дополнительный stencil, ещё один допустимый принцип построения; не EH |

Для unrestricted matrix conjugation независимость trace quadratics видна на \(X=\operatorname{diag}(1,-1)\) и \(X=\operatorname{diag}(1,0)\). Для irreducible rotation representations список другой; например, ориентированная четырёхмерная структура может разрешать дополнительный parity-odd contraction. Его наличие нельзя импортировать из слова Role.

**Wilson expansion.** Пусть \(P=I+\varepsilon X+\varepsilon^2Y+O(\varepsilon^3)\). Тогда

\[
P^{-1}=I-\varepsilon X+\varepsilon^2(X^2-Y)+O(\varepsilon^3),
\]
\[
\mathrm{tr}[I-(P+P^{-1})/2]
=-\tfrac{\varepsilon^2}{2}\mathrm{tr}X^2+O(\varepsilon^3).
\]

Этот результат не требует skewness, но положительность требует её или другого ограничения. Для ортогонального носителя \(X^T=-X\): \(-\mathrm{tr}X^2=\|X\|_F^2\). Для \(\operatorname{Sym}P=(P+P^T)/2\) вместо inverse sym:

\[
n-\mathrm{tr}P=-\varepsilon\mathrm{tr}X-\varepsilon^2\mathrm{tr}Y+O(\varepsilon^3).
\]

Следовательно, утверждение «любой plaquette trace локально начинается с R²» ложно для общей GL-группы. На периодическом плоском фоне сумма первого curl-trace — телескопическая и равна нулю. Этот boundary cancellation не превращает trace в coframe-curvature contraction. Для \(P\in SO\) transpose и inverse совпадают.

**Curvature norm.** \(\frac12\langle P-I,Q(P-I)\rangle\) начинается с \(\varepsilon^2\langle X,QX\rangle/2\). Если \(X=d_1a\), это curvature-squared действие на независимой связи. После дополнительного условия \(a\sim\partial h\) оно обычно имеет четыре пространственные производные на \(h\); само такое условие не задано. Оно не становится EH только благодаря положительности.

**Palatini typing audit.** Здесь «missing» означает отсутствующее во frozen inputs; это не утверждение об отсутствии файла в репозитории.

| Требуемое datum | Статус | Причина |
|---|---|---|
| Упорядочивание меток r,s | Уже доступно | Позволяет задать ориентацию плакетки |
| Ориентированный top-dimensional cell complex / fundamental chain | Missing | Не следует из одного набора shifts |
| Primal/dual flux Riesz pairing | Уже доступно, не связано с curvature carrier | Задано в brief, карта между носителями не задана |
| Внутренняя rank-4 orientation и invariant \(\epsilon\) | Missing | Degree и Role не определяют такую форму или группу, сохраняющую её |
| Coframe как упоминаемые данные e | Уже доступно, не связано | Не задано \(e\in C^1(X;V)\) с нужной эквивариантностью |
| Две сравнимые coframe legs / dual area | Missing | Нужно клеточное произведение и сопоставление fibres |
| Curvature в \(\Lambda^2V\) или двойственном пространстве | Missing | \(\rho(\Lambda)\) и End-valued \(P-I\) сами не дают antisymmetric internal pair |
| Path transport как операция | Уже доступно | Affine links дают перенос вдоль выбранного пути |
| Выбор путей/правило вставок в одну клетку | Missing | В кривом фоне разные пути дают разные точные ответы |
| Counting sum по sites | Уже доступно | Достаточно для простого plaquette sum |
| Covariant top-cell integration / physical volume normalization | Missing | Counting measure не заменяет coframe top form |

В четырёхмерной cochain формуле произведение четырёх legs уже может включать объём: дополнительный det(e) тогда не нужен и мог бы удвоить вес. Но это становится определённым только после выбора типов.

**Отрицательный typing control.** Напишем \(\epsilon_{abcd}e^ae^bR^{cd}\), убрав invariant orientation. Если произвольно фиксировать numerical epsilon, общий \(g\in GL(4)\) умножает contraction четырёх vector slots на \(\det g\); объект не является скаляром без компенсирующей density. Более того, превращение \(R^c{}_d\) в \(R^{cd}\) требует подходящего metric/representation map. Даже при наличии этих данных удаление межузлового parallel transport оставляет независимые \(g_x,g_y\), которые в contraction не сокращаются. Так что написанная формула может быть просто нетипизированной.

## 3. Action-selection theorem/no-go

**Теорема о недостаточности frozen inputs.** Пусть набор конечных носителей удовлетворяет указанным законам \(T_bT_c=T_{b+c}\), covariance и conjugation transport. Эти тождества не определяют единственный scalar action, даже с точностью до общей нормировки и граничных членов.

Доказательство конструктивное. В допустимой специализации возьмём \(V=\mathbb R^2\), \(\rho(L)=\operatorname{diag}(1,L)\) на \(\mathbb R\oplus V\), \(L\in SO(2)\),

\[
T_b=\begin{pmatrix}1&0\\b&I_2\end{pmatrix}.
\]

Она в точности удовлетворяет законам brief. Добавление spectator degrees и положительного flux pairing не меняет аргумент. На периодическом квадратном архиве линейная plaquette holonomy равна \(R(q_x)\), где \(q=d_1a\) в локальной angle chart. Действия

\[
S_A=\sum_x(1-\cos q_x),
\]
\[
S_B=S_A+\sum_{x,t=1,2}[1-\cos(q_{x+\hat t}-q_x)]
\]

точно определены через SO(2) group products, поэтому не зависят от выбора ветви angles. Второе слагаемое — character от произведения соседних plaquette holonomies с обратной; в неабелевом обобщении нужен connector transport.

Оба функционала инвариантны под локальными affine gauge changes: linear projection при affine conjugation преобразуется linear conjugation, а SO(2) абелева. Они также инвариантны под translations, square rotations/reflections; reflection меняет orientation sign, который cosine стирает. Оба неотрицательны, локальны с конечным stencil и имеют один и тот же flat minimum. В §10 их ненулевые спектры различаются не общим множителем. Значит, перечисленные симметрии не выбирают operator shape. Единичные коэффициенты здесь — свидетели неоднозначности, а не fitted constants для GR.

Если потребовать строго одноплакеточный stencil, остаются \(\sum(1-\cos q)\) и \(\sum(1-\cos q)^2\). Второе имеет нулевой flat Hessian и ведущую четвёртую степень, первое — ненулевой quadratic Hessian. Требование невырожденного quadratic term дополнительно исключит второй пример, но не следует из transport algebra. При нескольких invariant bilinear forms неоднозначность сохраняется уже на квадратичном одноплакеточном уровне. В единственном простом irreducible секторе quadratic form может быть единственной с точностью до масштаба; это не выбирает полный nonlinear action и не делает его гравитационным.

Таким образом, curvature alone **не выбирает EH**. Trace linear character при его наличии — ещё не EH: он не вставляет две coframe legs и не связывает внутренние и клеточные индексы. Кандидат Palatini здесь даже не доказан как полностью типизированное finite action; поэтому основной verdict — D, а не B.

## 4. Weak-field quadratic action

Для вычислимой специализации: \(X_L=(\mathbb Z/L)^d\), shifts коммутируют, \(\Delta_r=U_r-I\), flat links равны identity. Это дополнительные явные условия расчёта, не скрытое утверждение о любом архиве.

\[
(d_0u)_r=\Delta_ru,\qquad
(d_1a)_{rs}=\Delta_ra_s-\Delta_sa_r,\qquad d_1d_0=0.
\]

Упорядоченный affine plaquette даёт

\[
\Lambda_{rs}=I+\varepsilon(d_1a)_{rs}+O(\varepsilon^2),\quad
\Theta_{rs}=\varepsilon(d_1\beta)_{rs}+O(\varepsilon^2).
\]

Члены \(a\beta\) начинаются со второй степени; конкретные coefficient conventions зависят от ориентации plaquette. При некоммутирующих shifts или другом фоне нужен actual linearized curvature map J вместо d₁.

**Mixed letter.** Когда \(F\) — единый invertible multiplication operator и \(U_rT_kU_r^{-1}=T_{U_rk}\), имеем operator identity

\[
\mathscr L_r=F B_rF^{-1},\quad B_r=T_{\kappa_r}U_r.
\]

В любом замкнутом слове внутренние F сокращаются. При commuting shifts и стандартном oriented plaquette:

\[
P^{\mathrm{mix}}_{rs}=F T_{q_{rs}}F^{-1},\quad
q_{rs}=\kappa_r+U_r\kappa_s-U_s\kappa_r-\kappa_s.
\]

Это точная формула, не только jet. След любого polynomial/word character от такого pure-translation holonomy постоянен. Поле F не может породить кривизну одного conjugated flat word. При \(\kappa=\varepsilon k\) имеем \(X^{mix}=N(d_1k)\), где \(N(v)=C^\dagger(v)P_0\); f входит в conjugation с k лишь со второй степени. Если фактический curvature carrier отличается от этого single-conjugation ansatz, вывод нужно пересчитать.

**Constitutive variation.**

\[
W=F^{-T}F^{-1}=I-\varepsilon(f+f^T)+O(\varepsilon^2).
\]

Skew f невидим для первого jet W. Для условного локального potential \(V=\frac12\|W-I\|^2\):

\[
S_0=S_1=0,\quad S_2=\tfrac12\|(f+f^T)\|^2,
\quad K_f=A^*A,\quad Af=f+f^T.
\]

При Frobenius normalization \(K_f=4\) на symmetric f и 0 на skew f, независимо от p. Это stiffness-only negative control; допустимость V при полной frame symmetry требует covariant reference metric. Null directions здесь не автоматически gauge. Заданная вариация flux Riesz map H(e) не выбирает V и не является уже вычисленным gravitational Hessian.

**Owned flux energy не закрывает gravitational variation.** Пусть на его собственном носителе
\(E(j,F)=\langle j,Q(F)j\rangle/2\), \(Q=Q_0+\varepsilon Q_1(f)+\varepsilon^2Q_2(f)+\cdots\), \(j=j_0+\varepsilon u\). Тогда

\[
E_0=\tfrac12\langle j_0,Q_0j_0\rangle,\quad
E_1=\langle u,Q_0j_0\rangle+\tfrac12\langle j_0,Q_1j_0\rangle,
\]
\[
E_2=\tfrac12\langle u,Q_0u\rangle+\langle u,Q_1j_0\rangle
+\tfrac12\langle j_0,Q_2j_0\rangle.
\]

При j₀=0 quadratic action не содержит f. При j₀≠0 первая constitutive variation H определяет Q₁, но не Q₂ и не весь f-Hessian; сначала также требуется stationary-background condition. Пространственные разности возникают только через доказанный carrier map для j, например j=JΨ. Само наличие Riesz energy такого map не предоставляет.

**Общий curvature-norm блок.** Пусть \(\Psi=(a,\beta,k,f)\) и \(X=J\Psi\). При плоском фоне и \(S=\frac12\langle P-I,Q_F(P-I)\rangle\):

\[
S_0=S_1=0,\quad S_2=\tfrac12\langle J\Psi,Q_0J\Psi\rangle,
\quad K=J^*Q_0J.
\]

\(\delta Q_F\) даёт кубический член, а не f-stiffness: оба curvature factors уже первого порядка. Если связь и mixed carrier независимы и выбрана сумма их norms, ортогональное по степени спаривание даёт

\[
K=\operatorname{diag}
(d_1^*Q_ad_1,\ d_1^*Q_\beta d_1,\ d_1^*Q_kd_1,\ A^*MA).
\]

Последний блок присутствует лишь при добавленном constitutive potential; odd blocks — лишь при разрешённом invariant pairing. Для ordinary trace первые linear-connection blocks могут сохраниться, а \(\beta,k\) стираются точно. Если носители или pairing допускают mixed invariant tensors, возникают \(d_1^*Q_{a\beta}d_1\) и аналогичные блоки. Их коэффициенты не заданы.

Gauge directions при нулевом фоне: \(a=d_0\alpha\), \(\beta=d_0t\), аналогично k при существовании соответствующей gauge symmetry; они лежат в kernel curvature Hessian. Наличие kernel не доказывает, что вся его часть — gauge: harmonic directions выделяются отдельно.

**Условный linear-curvature action.** Пусть уже предоставлены B и curvature extraction C. Разложим

\[
B=B_0+\varepsilon B_1(h)+\varepsilon^2B_2(h)+\cdots,
\quad C=\varepsilon J_a a+\varepsilon^2C_2(a,\beta)+\cdots.
\]

Тогда

\[
S_0=0,\quad S_1=\langle B_0,J_aa\rangle,
\quad S_2=\langle B_1(h),J_aa\rangle+\langle B_0,C_2(a,\beta)\rangle.
\]

Для постоянного covariantly closed B₀ и периодического summation-by-parts первый член исчезает. Иначе flat state не стационарен, и говорить о его физических normal modes преждевременно. На стационарном фоне Hessian имеет схему

\[
K_P=\begin{pmatrix}0&C^*\\C&M\end{pmatrix}_{(h,a)}
\]

без дополнительных potentials; C содержит разности, M определяется точной второй вариацией holonomy и insertion. В finite group-valued discretization M не обязан быть site-local: holonomy содержит shifted products. Если M допускает elimination на выбранном gauge quotient и RHS лежит в его range,

\[
K_{h,\mathrm{eff}}=-C^*M^{-1}C
\]

с appropriate inverse/pseudoinverse и residual constraints. Ни существование такого inverse, ни sign, ни spin decomposition не получены из frozen inputs.

Критический flat-background control: если coframe отождествить с \(b=\varepsilon\beta\) и положить \(e_0=0\), то \(eeR=O(\varepsilon^3)\). Его Hessian нулевой. Для Palatini weak-field gravity нужен отдельно заданный **невырожденный flat coframe**; это не следует из разложения трансляций вокруг нуля.

## 5. Finite momentum spectrum

На \((\mathbb Z/L)^d\), с unitary Fourier convention:

\[
p_r=2\pi n_r/L,\quad z_r(p)=e^{ip_r}-1,\quad
\lambda(p)=\sum_r|z_r|^2=4\sum_r\sin^2(p_r/2).
\]

Для \(S_2=\frac12\sum_{r<s}|z_ra_s-z_sa_r|^2\):

\[
K_{rs}(p)=\lambda(p)\delta_{rs}-z_r(p)\overline{z_s(p)}.
\]

При p≠0: kernel — span(z), остальные d−1 eigenvalues равны λ. При p=0 все d eigenvalues нулевые. Для m независимых orthonormal internal components multiplicities умножаются на m. В real-space count Fourier conjugate pairs уже учтены общей размерностью.

На torus с n=L^d sites: gauge image имеет dimension m(n−1); harmonic sector — md; положительный сектор — m(d−1)(n−1). При d=1 плакеток нет. На слишком маленькой/особой решётке все ненулевые λ могут совпасть; тогда именно строгий criterion сравнения разных non-gauge momenta из brief может не сработать, несмотря на наличие difference operator. Для d=2,L=3 есть два разных ненулевых значения.

При constant internal Q eigenvalues становятся \(\mu_j\lambda(p)\). Для \(S_B\) из §3:

\[
K_B(p)=(1+\lambda(p))K_A(p).
\]

Для constitutive potential Kf(p)=A*MA, без momentum dependence. Для trace-blind pure translation action Kk(p)=0. Для условного Palatini elimination symbol — \(-C(p)^*M(p)^{-1}C(p)\), когда elimination допустимо; конкретный spin-2 symbol без B и M неизвестен.

Таким образом, curvature-square carrier может иметь настоящую **пространственную** дисперсию; отрицательный gravity verdict не означает «всё только алгебраично». Временной mass/kinetic operator, time evolution и причинность здесь не определены.

## 6. Scalar/Poisson result

**На frozen D0 carrier: scalar gravity sector не выведен.** Ни F, ни trace W автоматически не является Newtonian potential. Требуются карта scalar-to-field и доказательство, что выбранное ограничение согласовано с вариациями остальных полей.

Есть точная условная scalar subsector в явно указанной curvature-square модели. В d≥2 выделим направление 0, положим

\[
a_0(x)=\Phi(x_1,\ldots,x_{d-1})J,\quad a_i=0,\quad \Delta_0\Phi=0,
\]

где J — один normalized abelian generator. После деления на число sites направления 0:

\[
S_2[\Phi]=\tfrac12\sum_{x,i>0}|\Delta_i\Phi|^2.
\]

Это не hand-inserted Laplacian: оно получается подстановкой в derived curl norm. Ограничение согласовано с полной **линейной** системой: i-components equations содержат \(\Delta_0^*\Delta_i\Phi=0\); источник с единственной component j₀=ρ независим от x₀ и divergence-free. Gauge projection оставляет \(\Phi\) при transverse momenta. Вторая угловая компонента connection здесь ведёт себя как scalar при remaining spatial transformations, но не установлена как гравитационный потенциал.

Добавим явно выбранный source term \(-\langle\rho,\Phi\rangle\). Тогда

\[
\Delta_{\rm fin}\Phi=\rho,\quad
\Delta_{\rm fin}=\sum_{i>0}\Delta_i^*\Delta_i\ge0.
\]

Kernel на связном periodic lattice — constants. Решение существует iff \(\sum\rho=0\); mean-zero решение:

\[
\Phi_x=\sum_yG(x-y)\rho_y,\quad
G(v)=\frac1{L^{d-1}}\sum_{p\ne0}\frac{e^{ip\cdot v}}{\lambda(p)}.
\]

Реакция зависит от separation vector, а на симметричных орбитах — от соответствующего lattice distance; общий lattice Green function не обязан зависеть только от одного евклидова расстояния. В §10 дан точный Green на `(Z/3)^2`, реализуемый указанным scalar reduction d=3.

Это conditional abelian connection Poisson sector, **не derived Newtonian sector D0**. Source normalization, physical mass density, gravitational sign/strength и carrier map отсутствуют. Для S_B оператор станет \(\Delta_{fin}(I+\Delta_{fin})\), то есть сама Green response зависит от выбора действия.

Обязательный negative control: дописать \(\frac12\langle\operatorname{tr}\delta W,\Delta_{fin}\operatorname{tr}\delta W\rangle\) можно, но это новый функционал. Он не выводится из site-local V(W), чей Hessian не содержит Δ. Так получить желаемую Poisson equation — значит вставить её operator shape вручную.

## 7. TT/spin-2 result

Из первого jet W получается symmetric matrix \(h=-(f+f^T)\) в **внутреннем** пространстве. Для symmetric spacetime tensor нужен solder map от archive directions к этому пространству; он не следует из symmetry матрицы W.

В curvature-norm модели с flat curvature и только R² action блок f нулевой до второй степени. Добавленный site-local V даёт h-stiffness без дисперсии. Connection modes curl–curl — gauge one-form modes с internal labels; их нельзя назвать helicity-2 modes по числу компонент.

Для TT gate требуются explicit carrier map, lattice-compatible symmetric-gradient gauge generator, invariant quadratic operator на его quotient и constraint elimination. Ни один из них для gravitational h не выведен. Наложение заранее существующего TT projector на произвольную matrix не доказывает, что TT sector возникает из действия.

Если предоставленный variational law из §12 создаст effective Kh(p), следующая проверка — сохранение gauge image и TT subspace, rank, sign и p-dependence после constraints. Даже положительное spatial Kh требует отдельного временного принципа, например \(\frac12\langle\dot h,M_t\dot h\rangle\), прежде чем писать \(M_t\ddot h+K_hh=0\). Time variable, Mt, signature и constraints не заданы. **Гравитационные волны не выведены.**

## 8. Einstein–Cartan comparison

При insertion B, не зависящей от connection, для выбранного exact finite action вида \(S=\sum\langle B(e),C(P(a))\rangle\) его настоящие finite Euler equations:

\[
(D_a(C\circ P))^*B(e)=0,\qquad
(DB_e)^*C(P(a))=0.
\]

Если coframe legs сравниваются connection-dependent transport, B=B(e,a), первое уравнение содержит также \((D_aB)^*C(P)\). Если curvature extraction зависит от e, второе содержит дополнительный \((D_eC)^*B\). В §4 displayed Palatini blocks относятся к специально оговорённой форме B(e), C(P(a)); в общем случае надо дифференцировать весь пакет, включая transport. На flat фоне C₀=0 некоторые первые вариации вставок исчезают, но их mixed second variations могут сохраниться. Эти поправки нельзя отбросить по аналогии с continuum notation.

Это chain rule с конечными Jacobians; exact derivatives holonomy включают ordered insertions и переносы. Они не тождественны continuum covariant derivative без доказательства соответствующего finite calculus.

| Сопоставление | Статус | Что именно установлено |
|---|---|---|
| Variation R² → \(J_a^*QJ_aa=0\) | Exact finite theorem для выбранного action | Linearized connection equation, не coframe Einstein equation |
| Полная variation norm | Exact finite theorem при заданном Q,C | Jacobian-adjoint equation плюс variation Q; group-valued nonlinear terms сохраняются |
| Variation linear pairing → две Jacobian equations выше | Conditional exact finite theorem | Требуется типизированный B,C |
| Connection equation \(D(e\wedge e)=0\) | Formal weak-field analogy / conditional calculus theorem | Нужны wedge, invariant pairing, summation-by-parts и derivative-curvature identity |
| Coframe equation \(e\wedge R=0\) | Conditional algebraic structure | При B=epsilon ee derivative B содержит две coframe insertions; их порядок и transport существенны |
| \(D(ee)=0\Rightarrow T=0\) | Absent на frozen inputs | Требуются nondegenerate coframe и injectivity соответствующего torsion map |
| \(\Theta\) = Cartan torsion | Absent | Affine plaquette translation не идентифицирована с De |
| Einstein equation после elimination connection | Absent | Не построен action и не доказано допустимое elimination |
| Continuum EC/EH | Conditional scaling statement ниже | Не выводится из N→∞ |

Точный curvature-square equation имеет divergence-of-curvature структуру, а не linear-curvature coframe equation. Это сохраняется даже при общей геометрической терминологии.

**Минимальная scaling family для условного предела.** Возьмём oriented 4-tori фиксированного размера \(\ell\), spacing a=ℓ/L, L→∞; укажем interpolation клеток в torus, smooth periodic coframe e и connection ω, uniform bounded derivatives. Зададим link holonomy connection ω, integrated coframe legs \(E_r(x)=a e_r(x)+O(a^2)\), и covariant curvature extraction

\[
C_{rs}(P)=a^2R_{rs}(x)+O(a^3)
\]

uniformly в выбранном trivialization/transport convention. Пусть предоставленная dual-area insertion удовлетворяет

\[
B_{rs}(E)=a^2B^{cont}_{rs}(e)+O(a^3),
\]

а contractions и cell weights выбраны так, что \(\sum_{r<s}\langle B^{cont}_{rs},R_{rs}\rangle\) есть заданная coefficient density \(\epsilon e\wedge e\wedge R\). Тогда elementary density имеет вид a⁴Lcont+O(a⁵), число клеток O(a⁻⁴), и Riemann sum converges к интегралу этой density с O(a) error. Это условная теорема о **значениях действий** на sampled smooth fields; convergence variations требует uniform derivative control, convergence solutions — дополнительных coercivity/compactness/constraint results. Указанные hypotheses не доказаны для D0.

Для dimension d norm-action с \(P-I=a^2R+O(a^3)\) нормируется фактором a^(d−4) перед plaquette sum и ведёт к curvature-squared density, не к EH. Если coframe хранится как point value вместо integrated leg, powers a в Palatini insertion надо изменить соответственно. Fixed torus сохраняет periodic Green kernel; infinite-volume limit требует отдельного ℓ→∞ и boundary/zero-mode prescription. Нельзя из fixed-periodic family получить автоматически isolated-source 1/r law.

## 9. Odd-sector visibility

Пусть E=⊕Eᵖ, N(Θ)=C†(Θ)P₀ переводит E⁰ в E¹ и равен нулю на остальных степенях. Тогда N²=0, tr N=0. Degree-preserving rho(Λ) block diagonal, поэтому

\[
\operatorname{tr}[T_\Theta\rho(\Lambda)]
=\operatorname{tr}\rho(\Lambda).
\]

Более сильно: products, inverses и polynomial functions этих block-triangular matrices имеют diagonal blocks, зависящие только от linear parts. Следы любых таких words, determinant и characteristic polynomial не видят Θ. Для pure translation:

\[
\operatorname{tr}T_\Theta=n,\quad
\operatorname{tr}(T_\Theta-I)^j=0\quad(j\ge1).
\]

Supertrace также слеп, поскольку off-diagonal blocks не участвуют. Conjugation by degree-preserving F этого не меняет. Таким образом, standard mixed-letter Wilson action равен нулю на pure-translation holonomies **точно**, даже при ненулевом curl k.

В homogeneous model E=R⊕V:

\[
N(\Theta)=\begin{pmatrix}0&0\\\Theta&0\end{pmatrix},\quad
\operatorname{tr}(N^TN)=\Theta^T\Theta.
\]

Минимальное degree-sensitive pairing — спарить block E⁰→E¹ с его dual E¹→E⁰. Оно реализуется Riesz maps этих двух степеней или матричным элементом между degree-0 и degree-1 flux states. Если owned flux pairing имеет compatible maps на эти degrees, новый matter carrier не нужен. Сам brief не задаёт такие maps, поэтому **численная видимость доказана, принадлежность инвариантного pairing D0 — условна**.

Главная covariance проверка: при смене affine origin g=(c,I)

\[
(\Theta,\Lambda)\longmapsto(\Theta+(I-\Lambda)c,\Lambda).
\]

Поэтому \(\|\Theta\|^2\) не invariant в общем случае Λ≠I. При pure translation Λ=I остаётся только linear-frame covariance; invariant frame metric достаточно. На flat weak-field уровне translational gauge \(\beta\mapsto\beta+d_0t\) действительно оставляет d₁β неизменным, но это не доказывает полную nonlinear affine invariance.

Невозможность fixed positive metric на homogeneous representation, invariant under all nonzero T_b: если T_b было бы изометрией, то \(T_b^nv=v+nNv\) имело бы постоянную положительную норму для всех n. При Nv≠0 её квадрат имеет положительный quadratic coefficient — противоречие. Значит, Frobenius norm полной affine matrix не является автоматически owned invariant action.

Covariant cure возможен условно: affine section v с законом v′=c+Lv позволяет образовать

\[
q_v=\Theta+(\Lambda-I)v,\qquad q'_v=Lq_v.
\]

Его можно спарить с frame metric. Но такая section/доказанная карта из имеющихся данных не дана; вводить её молча нельзя. Аналогично norm \(\mathrm{tr}(W^{-1}R^TWR)\) invariant при R′=GRG⁻¹, W′=G⁻ᵀWG⁻¹, но family W(F) для degree-preserving F block diagonal и не замкнута под general affine G. Ссылка на W сама не решает это препятствие.

## 10. L=3 concrete computation

Полностью конечный hostile model: 9 sites `(Z/3)^2`, 18 real infinitesimal SO(2) link angles, orientation r=1,2. Пусть D₁,D₂ — 9×9 forward difference matrices,

\[
C=(-D_2\ \ D_1),\quad \Delta=D_1^TD_1+D_2^TD_2,
\]
\[
S_{A,2}=\tfrac12 a^TC^TCa,\quad
S_{B,2}=\tfrac12 a^TC^T(I+\Delta)Ca.
\]

Это Hessians **точных** cosine actions §3, а не spectra, вставленные в определение. Для каждого momentum n=(n₁,n₂)∈{0,1,2}² ненулевая coordinate даёт contribution 3 в λ.

| Momentum class | Число p | λ | KA: transverse eigenvalue | KB: transverse eigenvalue |
|---|---:|---:|---:|---:|
| (0,0) | 1 | 0 | Две нулевые harmonic directions | То же |
| Ровно одна coordinate ≠0 | 4 | 3 | 3 | 12 |
| Обе coordinates ≠0 | 4 | 6 | 6 | 42 |

Для каждого p≠0 есть ещё один gauge zero. Итого:

\[
\dim\ker C=10=8_{\rm gauge}+2_{\rm harmonic},\quad
\operatorname{rank}C=8.
\]

После gauge quotient остаются 10 направлений: 2 harmonic null и 8 spatially stiff. Отношение eigenvalues upper/lower равно 2 для A и 7/2 для B: действия не эквивалентны rescaling.

**Точный Green.** Scalar Δ имеет spectrum `{0^(1),3^(4),6^(4)}`. Поэтому

\[
G=\Delta^+=\frac{7\Delta-\Delta^2}{36},\qquad
\Delta G=I-\frac19\mathbf1\mathbf1^T,\quad G\mathbf1=0.
\]

Как функция displacement:

\[
G(0,0)=\frac29,\quad
G(\pm1,0)=G(0,\pm1)=0,\quad
G(\pm1,\pm1)=-\frac1{18}.
\]

Отрицательные entries — следствие mean-zero normalization, а не negative quadratic energy. Для source δ₀−δᵥ potential difference равна \(2[G(0)-G(v)]\): 4/9 для соседнего site, 5/9 для diagonal site. Это явная separation-sensitive response.

Результаты проверены точной рациональной арифметикой Python standard library: ranks всех A−λI, rank C и matrix identity ΔG=I−11ᵀ/9. Воспроизводимый код:

```python
from fractions import Fraction as F
from itertools import product
sites = list(product(range(3), repeat=2)); n = len(sites)
def tr(A): return list(map(list, zip(*A)))
def mul(A,B): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def add(A,B): return [[x+y for x,y in zip(r,s)] for r,s in zip(A,B)]
def scale(c,A): return [[c*x for x in r] for r in A]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def rank(A):
    A = [[F(x) for x in r] for r in A]; k = 0
    for j in range(len(A[0])):
        p = next((i for i in range(k,len(A)) if A[i][j]), None)
        if p is None: continue
        A[k], A[p] = A[p], A[k]
        v = A[k][j]; A[k] = [x/v for x in A[k]]
        for i in range(len(A)):
            if i != k:
                v = A[i][j]; A[i] = [x-v*y for x,y in zip(A[i],A[k])]
        k += 1
    return k
D = []
for r in range(2):
    A = [[0]*n for _ in range(n)]
    for i,x in enumerate(sites):
        y = list(x); y[r] = (y[r]+1)%3
        A[i][sites.index(tuple(y))] += 1; A[i][i] -= 1
    D.append(A)
C = [[-x for x in r]+s for r,s in zip(D[1],D[0])]
Lap = add(mul(tr(D[0]),D[0]), mul(tr(D[1]),D[1]))
KA = mul(tr(C),C)
KB = mul(mul(tr(C),add(eye(n),Lap)),C)
for A,vals in [(KA,[0,3,6]),(KB,[0,12,42]),(Lap,[0,3,6])]:
    print({v:len(A)-rank(add(A,scale(-v,eye(len(A))))) for v in vals})
G = scale(F(1,36),add(scale(7,Lap),scale(-1,mul(Lap,Lap))))
assert mul(Lap,G) == add(eye(n),[[F(-1,n)]*n for _ in range(n)])
assert rank(C) == 8
print(G[0])
```

Это finite theorem в выбранной модели, не эмпирическая подгонка и не результат continuum limit.

## 11. Theorem-ready statements

1. **Affine trace erasure.** Для finite graded E, строго degree-raising N и degree-preserving invertible A, \(\operatorname{tr}[(I+N)A]=\operatorname{tr}A\). Доказательство: диагональные блоки NA нулевые.
2. **Word erasure.** Для группы block triangular affine matrices, diagonal projection — homomorphism. Все polynomial character traces words факторизуются через него; translations неразличимы. Доказательство: diagonal block multiplication и inverse.
3. **Mixed-word conjugation.** Если каждый letter равен FBᵣF⁻¹ с одним F, любое word equals F(word B)F⁻¹. При commuting shifts и translations oriented plaquette имеет q=κᵣ+Uᵣκₛ−Uₛκᵣ−κₛ.
4. **Inverse-symmetric Wilson jet.** Для P=I+εX+ε²Y, coefficient ε² в tr[I−(P+P⁻¹)/2] равен −tr X²/2, coefficient ε равен нулю.
5. **Transpose warning.** Для transpose sym coefficient ε равен −tr X и не обязан исчезать locally; periodic sum vanishes для X=d₁a. Нельзя заменять inverse sym transpose sym без hypotheses.
6. **Flat curvature norm Hessian.** Если R(0)=0 и Q smooth, Hessian \(\frac12\langle R,Q R\rangle\) равен J*Q₀J; derivative Q не входит.
7. **Constitutive first jet.** Для F=I+εf, δW=−(f+fᵀ). Potential \(\|W-I\|²/2\) имеет Hessian 4 на symmetric и 0 на skew directions в Frobenius convention.
8. **Finite curl spectrum.** На periodic cubical torus symbol d₁*d₁ равен λI−zz*, spectrum 0⊕λ^(d−1) при p≠0, и zero_d при p=0.
9. **Gauge versus harmonic count.** Для scalar-valued one-cochains на `(Z/L)^d`, \(\dim\mathrm{im}d_0=L^d-1\), \(\dim(\ker d_1/\mathrm{im}d_0)=d\), \(\operatorname{rank}d_1=(d-1)(L^d-1)\).
10. **Nonselection witness.** Exact SO(2) actions SA,SB §3 preserve local affine gauge symmetry and square lattice symmetries, но при L=3 имеют inequivalent physical spectra 3,6 и 12,42. Поэтому эти axioms не выбирают Hessian shape.
11. **Ultralocal nondispersion.** Для \(S_2=\sum_x\langle h_x,Mh_x\rangle/2\) с constant M Fourier symbol равен M; distance-sensitive inverse между различными sites отсутствует. При локальном gauge quotient conclusion сохраняется; imposing nonlocal constraints — дополнительная операция, которую нужно анализировать отдельно.
12. **Conditional scalar reduction.** Abelian curl-square theory с a₀=Φ, Δ₀Φ=0, aᵢ=0 допускает согласованное linear restriction на transverse Poisson equation с source j₀=ρ independent of x₀.
13. **Periodic Poisson solvability.** На связном finite torus ΔΦ=ρ разрешимо iff mean ρ=0; mean-zero inverse имеет Fourier coefficients 1/λ(p) при p≠0.
14. **L=3 Green identity.** Для `(Z/3)^2`, G=(7Δ−Δ²)/36 удовлетворяет ΔG=I−11ᵀ/9 и G1=0; entries приведены в §10.
15. **No positive unipotent metric.** Нетривиальная N с N²=0 не допускает positive definite bilinear form, для которой I+N — isometry. Доказательство через норму v+nNv.
16. **Affine-origin dependence.** Under translation conjugation Θ′=Θ+(I−Λ)c. Следовательно, Θ-norm generally не invariant; при дополнительной affine section qᵥ=Θ+(Λ−I)v transforms linearly.
17. **Zero-coframe Hessian obstruction.** Если B(e) homogeneous quadratic, e₀=0 и C₀=0, действие ⟨B(e),C⟩ имеет нулевой Hessian в совместном нулевом фоне.
18. **Conditional Palatini Schur operator.** Для stationary background и Hessian [[0,C*],[C,M]], если connection elimination well-defined modulo gauge и range constraints, effective Hessian равен −C*M⁻¹C. Иначе применять эту формулу без дополнительных constraints нельзя.
19. **Typing obstruction.** Flux pairing A×A*→R не задаёт pairing с независимым curvature space C без карты C→A или A→C*. Идентичность размерностей не заменяет equivariant map.
20. **Conditional Riemann-sum limit.** При uniform density expansion a⁴L+O(a⁵) на fixed-volume four-dimensional periodic lattice scalar actions converge с O(a); эта теорема не утверждает convergence equations/solutions.

Пункты 1–7,15–19 применимы без ожидания exact curvature coefficients в оговорённых algebraic hypotheses; 8–14 требуют cubical periodic specialization; 20 требует явно заданной scaling family.

## 12. Minimal missing principle

**Один первичный принцип: естественный конечный вариационный закон coframe–curvature pairing.**

Он должен предоставить единый пакет

\[
\mathfrak V:\quad
S[e,\mathscr A]=\sum_{c}\big\langle
\mathfrak B_c(e,F),\ \mathfrak C_c(P(\mathscr A))
\big\rangle,
\]

где \(\mathfrak B_c\) — canonical dual-curvature insertion, \(\mathfrak C_c\) — указанная эквивариантная extraction из group-valued holonomy, pairing и клеточная сумма типизированы и invariant. Это должен быть **закон выбора действия**, а не просто демонстрация того, что одну из многих формул можно написать.

Обязательства одного пакета: согласовать внутренние representations, two coframe legs, orientation/density и transport; определить allowed variations и stationary nondegenerate background; обосновать coefficients и отсутствие/наличие независимых R², torsion², volume и parity-odd additions. Если только выбрать B и оставить произвольное добавление R², проблема выбора action остаётся. Одна общая coupling normalization может оставаться свободной без изменения operator shape, но её physical value тогда не выведено.

Утверждение необходимости ограничено маршрутом **линейной по кривизне coframe dynamics**: другой новый вариационный принцип, например строго заданная spectral construction, мог бы заменить этот пакет. Никакой известный здесь transport identity не исключает такие альтернативы и не выбирает Palatini по имени.

Почему это первичный недостающий принцип: orientation, wedge, carrier map, integration и contraction являются typing obligations одного variational pairing, а не пятью произвольными физическими аксиомами. После его задания результат ещё может оказаться отрицательным: zero Hessian, extra modes, wrong sign, no scalar sector. Time evolution и scaling limit остаются последующими проверками; данный пакет их не подразумевает.

Все шесть negative controls выполнены: R² norm (§2,4); нетипизированный Palatini при удалении orientation/transport (§2); trace erasure (§9); constant constitutive Hessian (§4,5); hand-inserted scalar Laplacian (§6); две инвариантные spectra (§3,10).

## 13. Next physical calculation

Первая вычислимая без подгонки величина после задания \(\mathfrak V\): **точный symbol и спектр физического coframe Hessian на невырожденном periodic flat фоне размера L=3**, после законного исключения connection и gauge/constraint reduction:

\[
K_{\mathrm{coframe,phys}}(p)
=\left[K_{hh}(p)-K_{ha}(p)K_{aa}(p)^{+}K_{ah}(p)\right]_{\rm physical},
\]

только при проверенных range conditions; иначе сначала residual constraints. Эта величина сразу проверяет нулевой результат, отрицательные направления, spatial dispersion и наличие scalar/symmetric-tensor sectors. Она ещё не является частотой волны.

Первый pressure test: вычислить её при p=(2π/3,0,…) и p=(2π/3,2π/3,…) без вставленного Laplacian и сравнить physical eigenvalues. Затем уже можно получать source Green operator из того же Hessian. Если pairing не задаёт эти числа однозначно, задача выбора динамики остаётся открытой — независимо от того, насколько формула похожа на Einstein–Cartan.