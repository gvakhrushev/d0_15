# Обратная ОТО → D0: единственный трехглубинный heat selector кривизны на полном native операторе

17 октября 2026. RESEARCH / ANALYTIC SPECTRAL CONSTRUCTION / CONDITIONAL GR CONSUMER, existing Draft #334. Никакой новый Dirac, ghost, контрчлен или выбранная физическая цена не вводится. Full16, все spatial Fourier modes, true adjoint и observer/coframe/link сохраняются. Это **не** proof, что BOOK action выбирает данный selector, и не original all-ten h^-2/#216 terminal.

## 0. Инвертируем цель: как извлечь Einstein–Hilbert из ИМЕЮЩЕГОСЯ теплового оператора

В A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md §3 на истинном полном exterior16 Laplace-type carrier уже получен traced 4D heat coefficient

$$
A_2[e,\omega,w]=\int_M
\left(-\frac43R_G+2|h(T)|^2-4|v(T)-d\log w|^2\right)dV_G.\tag{H1}
$$

Там же доказано: его connection Hessian оставляет tensor16, поэтому один A2 НЕ выводит Levi-Civita, не даёт полный Palatini and matter source. На torsion-free, canonical-volume submanifold T=0, w=constant, (H1) становится A2=−(4/3)∫ R_G dV_G. Это на *positive* frame: переход к Lorentzian физической ОТО — отдельное условие, не слово «продолжение».

Возьмём те же, а не подменённые, тепловые чтения full operator:

$$
K(t;\Phi)=\mathrm{Tr}_{\mathrm{full16,space}}\exp(-t P_\Phi),\quad
\Phi=(e,\omega,w,n,\text{retained fields}).
$$

На smooth compact 4D manifold без boundary стандартная асимптотика Laplace-type:

$$
K(t;\Phi)=(4\pi t)^{-2}
\left[A_0(\Phi)+t A_2(\Phi)+t^2A_4(\Phi)+t^3A_6(\Phi)+O(t^4)\right].\tag{H2}
$$

Нужна соответствующая uniform C1-версия для source; одной pointwise (H2) для дифференцирования недостаточно.

## 1. Нетривиальный обратный вывод: веса (1,-5,4) ФОРСИРОВАНЫ

Не изменяя оператор, рассмотрим три глубины: t,2t,4t. Ищем ненулевые c0,c1,c2, которые при linear combination K(t)+c1 K(2t)+c2 K(4t) удаляют UV volume A0/t² и local A4/t⁰, оставляя A2/t. Два необходимых равенства:

$$
1+\frac{c_1}{4}+\frac{c_2}{16}=0,\qquad 1+c_1+c_2=0.
$$

Единственное решение с c0=1:

$$
\boxed{(c_0,c_1,c_2)=(1,-5,4).}\tag{H3}
$$

Меньше трех различных depths недостаточно: для двух точек s0,s1 матрица [s_j^{-2};1] невырождена. Поэтому (H3) — **минимальная и единственная (до общего множителя) 3-stop linear spectral probe** в данном заранее зафиксированном классе dyadic depths, который annihilates volume и constant heat coefficient. И это не подбор под численное R.

Определим математический диагностический функционал

$$
\mathscr A_{2,t}[\Phi]=-2(4\pi)^2 t
\left[K(t;\Phi)-5K(2t;\Phi)+4K(4t;\Phi)\right].\tag{H4}
$$

A2 coefficient: 1−5/2+4/4=−1/2; A0:1−5/4+4/16=0; A4:1−5+4=0. A6 coefficient:1−5·2+4·4=7. Подстановка (H2) даёт **строгое аналитическое следствие** при указанной small-time expansion:

$$
\boxed{\mathscr A_{2,t}=A_2-14t^2 A_6+O(t^3),\qquad
d\mathscr A_{2,t}=dA_2+O(t^2)\quad\text{при uniform }C^1.}\tag{H5}
$$

На torsion-free canonical-volume geometric chart отсюда

$$
d\mathscr A_{2,t}\ \longrightarrow\
-\frac43\,d\int R_G\,dV_G.\tag{H6}
$$

Это настоящий *Einstein–Hilbert geometric covector* с вычисленным coefficient **только при уже оговоренных геометрических и аналитических предпосылках**; не сам native Cost−Info, не fixed-beta v8 first source и не полный Einstein equation с T_ab.

## 2. Почему это действительно связано с существующим D0 clock, а не новый Laplacian

Буквальная native blank Kraus карта в #334 есть B_h=I−eps_h Delta_h/2. При positive homogeneous symbol и допустимых clock powers, один и тот же оператор дает

$$
K_h(n)=\mathrm{Tr}_{full16,space}\ B_h^{2n},\qquad t_h=n\varepsilon_h.
$$

Исходный v8 fixed beta имеет n=128L², beta=n eps=2p². Те же algebraic powers B_h^{2n}, B_h^{4n}, B_h^{8n} соответствуют nested depths n,2n,4n и временам t_h,2t_h,4t_h. Их счетные множители целые автоматически, без отдельного floor-clock mismatch.

**Новый технический, но ещё НЕ ДОКАЗАННЫЙ предел:** выбрать n_h так, чтобы t_h=n_h eps_h→0 и сетка h→0 достаточно быстрее, и доказать uniform joint small-time heat/source expansion для literal B_h^{2n_h} на variable-coframe/true-adjoint carrier:

$$
-2(4\pi)^2 t_h
\left[K_h(n_h)-5K_h(2n_h)+4K_h(4n_h)\right]
\xrightarrow[C^1]{}A_2.
$$

Fixed-positive-time resolvent and source estimates из #334 ЭТОГО автоматически не доказывают. Для стандартного second-order lattice stencil ожидаемый достаточный режим т_h≫h (например t_h=h^a,0<a<1), но это **эвристика для проверки по действительным error bounds**, не установленный D0 theorem. Диагностические three-depth readings требуют admission всех выбранных stopping cuts, их физической цены и signed combination (1,−5,4); из Book/M1 они пока не выведены. Вычислять (H4) как диагностическую функцию существующего K разрешено; объявлять её action D0 пока НЕТ.

## 3. Сильные ограничения: даже если H5 пройдет, GR еще не закрыта

1. Для (H1) trace/torsion connection source устраняет лишь v−dlog w и three-form h; tensor16 остается. Чтобы получить полноценную Palatini LC connection, нужен отдельный native selector или owner-derived retained equation, без инверсии нулевого saddle block.
2. Curvature на positive frame нельзя автоматически отождествить с Lorentzian Einstein без полного bridge, variation image, Ward и корректных boundary terms.
3. Einstein материальная 3-форма tau_a и spin 3-форма sigma_ab должны получаться из одного admitted matter/source действия: scalar eigenvalue covector eps'(V)=Tr(Pi X_V)/k не заменяет их. Слитые #354/#358 — строго частичные владельцы.
4. Даже если dA2 совпадет с Einstein, он должен быть связан с **тем же** native H+J+R/Cost−Info, с true clock и reference128. Совпадение другого spectral diagnostic не является доказательством физического закона.
5. Оригинальный all-ten unweighted raw h^-2 #216 comparator и непустое точное искривленное совместное refinement family остаются OPEN.

## 4. Независимая проверка весов и коэффициента

На unit flat 4-torus для scalar P=−Delta+m²:

$$
K_m(t)=e^{-tm^2}\left[\sum_{k\in\mathbb Z}e^{-4\pi^2tk^2}\right]^4,\qquad
A_0=1,\quad A_2=-m^2,\quad A_6=-m^6/6.
$$

Подстановка (H4) даёт \mathscr A_{2,t}=−m²+(7/3)m^6 t²+O(t³) (после экспоненциально малого finite-volume tail). Контроль на t=.0025,m²=2.5: selector=−2.4997744322 vs predicted −2.5; m²=0 дает −2.22e−8, true A2=0. Это численная иллюстрация аналитику (H3)-(H5), НЕ curved-D0 certification.

Связанная native relative-clock схема: A4D_NATIVE_RELATIVE_HISTORY_CLOCK_COCYCLE_2026_10_17.md. Two possible routes (relative path KL vs three-depth heat selector) НЕ смешиваются в новую составную action до физического выборщика.

**Решающий next owner consumer**: на actual full16 coframe/operator проверить joint t_h,h uniform C1 source estimate для 3 nested blank powers на одном curved test при сохранении all connection and prepared fields. Если проходит — использовать его только как geometric target extractor при поиске физически выбранного native action. Не переписывать v8 fixed-beta result как этот новый мультичасовой объект.
