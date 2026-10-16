# D0 → ОТО: flat-moduli action mismatch на фактическом однородном v8-корне

**16 октября 2026.** Дополнение к существующему Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), задача `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. Статус: **строгий конечный контрсертификат вариационной эквивалентности фиксированной условной v8-цены** с Einstein–Hilbert+Λ+её собственным shell-matter `R` на всей однородной stored-adjoint области. **Не** глобальный запрет ОТО в D0: физический выбор программы, полная Cost−Info цена и общая refinement-теорема остаются открытыми.

## 1. Известные владельцы и действительная цель сравнения

- `A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md`, §§0–0.3: coframe `F`, `q=F η Fᵀ`, faithful-shell state и полный сохранённый v8 operator/price.
- `A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md`, §§1–2: все 10 homogeneous positive Gram variations; сертифицированная совместная stationary-точка `G_*=(d−o)I+o11ᵀ`; полная shell/reference подготовка.
- `sources/d0_native_joint_kernel_2026-10-16/homogeneous_price_convexity.py`: полный 4096-модовый интервальный владелец `0<Z<50`, `w_ground>8/25`, положительная Gram-Hessian **без** отбрасывания нормализатора и feedback.
- `A4D_COFRAME_TORSION_INTRINSIC_GR_RECONSTRUCTION.md`: `g=(FηFᵀ)⁻¹`, full torsion/LC transgression; на постоянном coframe `R_g=T=C=0`.
- `A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md`: даже полное `+ω_LC` не задаёт физический выбор связи/цены; ниже ω_LC тождественно нулевая, и его поправка не может изменить результат.

Сравнивается **один и тот же** исходный `S=H+J+R` с действительно фиксированными `α, m, β, z, M, C` и полным shell `Ψ`. Не подменяем heat operator Hodge–Dirac, не подставляем Einstein как определение материи, не оптимизируем неизвестную подготовку. Смысл результата: вне стационарной точки нет тождества вариаций с Einstein–Hilbert на этой ограниченной, но явно допустимой семье. Поскольку проверка проходит **на самом** однородном stationary-корне во втором порядке, она сильнее общего возражения про нестационарный пробный фон.

## 2. Явная 2-ограниченная траектория — не только масштаб

Положим `p=(√5−1)/2`, `η=diag(1,−1,−1,−1)`, `L=8`, `N=8192`, `m=2N=16384`, `α=p²/N`, `β=mα=2p²`, `z=2⁻²⁰`, `M=128`. На сертифицированном faithful/root-box (радиус ±10⁻¹²):

\[
 d=0.0636351915943445350\ldots,\quad
 o=0.0040167350432317253\ldots,\quad
 G_*=(d-o)I+o\mathbf1\mathbf1^T.
\]

Назовём `a=d+3o`, `b=d−o`; `a>b>0`. Введём рациональные ортогональные проекторы на

\[
 u_0=(1,1,1,1)/2,\quad
 u_1=(1,-1,0,0)/\sqrt2,\quad
 u_2=(1,1,-2,0)/\sqrt6,\quad
 u_3=(1,1,1,-3)/\sqrt{12},\quad P_i=u_iu_i^T.
\]

Пусть `s(t)` — **единственная аналитическая** малая ветвь уравнения

\[
 (a+s)\big[(b-s/3)^2-t^2\big](b-s/3)=ab^3,
 \qquad s(0)=0.
 \tag{1}
\]

Она существует по IFT, поскольку производная левой стороны по `s` при нуле равна `b²(b−a)≠0` и

\[
 s'(0)=0,\quad s''(0)=-\frac{2a}{b(a-b)}.
\]

Определим точную positive Gram trajectory

\[
 \boxed{G(t)=(a+s)P_0+(b-s/3+t)P_1+(b-s/3-t)P_2+(b-s/3)P_3.}\tag{2}
\]

Имеем `tr G(t)=a+3b=4d`, `det G(t)=ab³`, а `G'(0)=V=P₁−P₂≠0`, `tr V=0` и `V\mathbf1=0`. Для достаточно малого `|t|>0` все четыре собственных значения положительны. Берём `F(t)=sqrt(G(t))`, `n=e₀`, stored links `A_xy=I`, одинаковые на каждом узле периодического тора. Обе stored-adjoint own-leg constraints выполняются **точно**; остальные 16 Fock grades и все 128 shell reference не удаляются. Все собственные spatial-leg lengths строго положительны около базового regular root.

Поскольку `F(t)` пространственно-постоянна, любая `g(t)=(F(t)ηF(t)ᵀ)⁻¹` имеет **нулевые Riemann/Ricci/Einstein**, `dθ=0`, `ω_LC=0`, `T=0`, `L_cmp=L_T=0`. При этом `|det g(t)|^{1/2}=(det G(t))^{-1/2}` постоянен. Значит, **весь** Einstein–Hilbert, любой фиксированный cosmological Λ-volume и граничная transgression постоянны на (2).

## 3. Полная фактическая материя тоже постоянна

На восьми shell momenta `±e_r`, каждом из 16 CAR grades, `|z_r(e_r)|²=γ=128−64√2`. Faithful-shell reduced state `P_Ω/128` даёт

\[
 R(G)=\operatorname{Tr}(\rho_{\rm shell}\Delta(G))=\frac\gamma4\operatorname{tr}G. \tag{3}
\]

Следовательно, `R(G(t))=γd` для всех малых `t`, **точно**. Не используется заявление, будто произвольная материя физически не зависит от coframe: это конкретная уже существующая preparation объявленной v8 задачи.

## 4. Строго положительная вторая вариация той же heat+feedback цены

Для всех 4096 четырёхмерных momentum `k∈(ℤ/8)^4` положим

\[
 z_r(k)=8(e^{2πik_r/8}-1),\quad
 \lambda_k(G)=z(k)^*Gz(k),\quad B_k=1-αλ_k,\quad K_k=B_k^m,\quad
 Z=16\sum_k K_k,\quad A_k=1-z+z K_k. \tag{4}
\]

Все коэффициенты `B_k>0` на root box. Предыдущая цена **без изменения**:

\[
 S(G)=\frac{\log(CZ)}\beta-16M\sum_k\log A_k+\frac\gamma4\operatorname{tr}G.
 \tag{5}
\]

`C=128×128^8192` есть константа по `G`, а не удалённое workspace. Для `V=P₁−P₂` обозначим

\[
 y_k=\frac{z(k)^*Vz(k)}{B_k},\qquad
 w_k=16K_k/Z,
 \qquad c=(m-1)α.\tag{6}
\]

Полная неизменённая spectral Hessian для линейной variation `G_*+tV` (вторая производная `R` по линейной карте равна 0):

\[
 \begin{split}
 S''_{\rm affine}[V,V]={}&c\,\mathbb E_w y^2-\beta(\mathbb E_w y)^2\\
 &-M\beta z c Z\,\mathbb E_w(y^2/A)
  +M\beta^2z^2Z\,\mathbb E_w(Ky^2/A^2).
 \end{split}\tag{7}
\]

Это не приближение порядка `α`; сохранены `m−1`, нормализатор, весь logdet. На базовом действительном stationary root все 10 Gram-источников цены (5) равны нулю, поэтому по chain rule **вторая производная вдоль нелинейной ветви (2)** равна (7): вклад `DS[G''(0)]` исчезает. Альтернативно, (3) постоянно и градиент спектральной части в корне равен `−γI/4`, так что его произведение с `tr G''=0` равно нулю.

Поскольку у нулевого импульса `y_0=0`, по Cauchy

\[
 (\mathbb E_w y)^2\le(1-w_0)\mathbb E_w y^2,
 \qquad w_0=16/Z>8/25.
\]

`A_k≥1−z`; отбрасывая только неотрицательный последний член (7) и используя `β<1`, `m=16384`, `Z<50`, получаем **строго, с certified interval-owner Z**:

\[
 S''[V,V]\ge \beta\left(w_0-\frac1m-
 \frac{M\beta zZ}{1-z}\right)\mathbb E_w y^2
 >\frac{3\beta}{10}\mathbb E_w y^2>0.\tag{8}
\]

Последняя строгая неравенство следует уже из `k=e₀`, где `z(k)^*Vz(k)=γ/3≠0` и `w_k>0`. Для воспроизведения численного значения checker использует **все** 4096 моменты и multiplicity16:

\[
 Z=49.33703025058\ldots,\qquad
 \boxed{S''[V,V]\simeq278.33581123688},
 \quad \text{certified lower mechanism: }S''>0.
\]

Для нелинейной (2) центральные разности дают `278.33935` при `t=10⁻⁴`, `278.35696` при `2·10⁻⁴`. Разница `O(t²)` согласована с формулой (7). **Не** следует объявлять действительный finite-β физически выбранным из M1.

## 5. Почему именно GR bridge не может скрыть этот дефект

На (2) все геометрические классические действия вида `c∫R_g dV_g+Λ∫dV_g`, LC/TEGR rewriting, boundary transgression — **константы**. Собственная v8 материя (3) тоже константа. Между тем исходное `H+J+R` меняется во втором порядке с ненулевым коэффициентом (8). Поэтому на полном regular homogeneous stored family **нет** identity функций или первых вариаций во всех её точках

\[
 S_{v8}\equiv c\int R_gdV_g+\Lambda\int dV_g+R_{\rm shell}+\text{boundary}+\text{field-independent constant}.
\]

Коэффициенты `c,Λ` могут быть любыми **постоянными**; результат от них не зависит. Даже совпадение первых источников в единственном stationary-корне не даёт action identity на окрестности. Нельзя исправить эту разность выбором знака contorsion или scalar endpoint weight: на этой семье `T=0`, `ω_LC=0`, `dlog|det e|=0`. Единственный честный выход — другой native programme/physical map, реально выведенный archive/observer/measure источник, либо доказанный refinement remainder, который подавляет этот отклик. Назначить остаток равным «минус расхождение» запрещено: это не derivation.

Результат **не** исключает нелокальную конечную спектральную цену с зависимостью от модулей плоского тора (Casimir/thermal-type response). Он лишь исключает её точное прочтение как *чистого* Einstein+Λ+данного `R` на всей этой карте. Фиксированная `v8` может быть ценой другого физического сектора; допуск его из D0 не доказан.

## 6. Контролируемый fixed-β refinement — shape response не исчезает автоматически

Рассмотрим только точно объявленное математическое продолжение коэффициентов: `L→∞`, `α_L=p²/(128L²)`, `m_L=256L²`, `β_L=2p²` fixed, `M=128`, `z=2⁻²⁰`. Это **не** утверждение о выборе этой траектории исходным D0-history. При постоянном `G(t)` и центрированных momentum `k∈ℤ⁴`,

\[
 \lambda_L(k)=L^2\,(e^{2πik/L}-1)^*G(e^{2πik/L}-1)
 \to(2π)^2 k^TGk,
 \quad K_{L,k}\to e^{-\beta(2π)^2k^TGk}.
\]

Uniform ellipticity `G≥b_{min}I` и `|L(e^{2πik/L}-1)|≥4|k|` для центрированного `|k|≤L/2` дают
`0≤K_{L,k}≤e^{-16β b_min\|k\|²}`. До второго source-jet множители увеличиваются лишь полиномиально по `|k|` при uniform positive `B_L`. Dominated convergence передаёт не только значение, но и первый/второй field-source jet.

После удаления **только независимых от поля** `log C_L/β` и `−16ML⁴log(1−z)` конечное spectral action сходится в C² на малой (2) к

\[
 F_\infty(G)=\frac1\beta\log\!\left(16\sum_{k\in\mathbb Z^4}e^{-\beta(2π)^2k^TGk}\right)
 -16M\sum_{k\in\mathbb Z^4}\log\!\left(1+\frac{z}{1-z}
                 e^{-\beta(2π)^2k^TGk}\right). \tag{9}
\]

Это полная фиксированная температурная *shape potential*, не локальная плотность Einstein–Hilbert. Материя `R_L(G)=γ_L tr(G)/4`, `γ_L=4L²sin²(π/L)`, на (2) постоянна для каждого `L`.

Пусть `q_k=(2π)²k^TVk`, `r_k=(2π)²k^TG''(0)k`, `K_k=e^{-βλ_k}`, `T=∑K_k`, `A_k=1−z+zK_k`. Перестановочная симметрия базового `G_*` даёт `∑K_kq_k=0` **точно**. Тогда конечная по значению сумма второй производной (9) имеет вид

\[
 F_\infty''(0)=\frac{\beta\sum Kq^2-\sum Kr}{T}
 +16M\beta z\sum\frac{Kr}{A}
 -16M\beta^2z(1-z)\sum\frac{Kq^2}{A^2}.\tag{10}
\]

Численно при cutoff `|k_i|≤5` и независимо `≤6` получено

\[
 \boxed{F_\infty''(0)\simeq69.05783945975>0.}
\]

Контроль хвоста: `β(2π)² b>1.7`, `|q_k|≤40||k||²`, `|r_k|≤6400||k||²`. Для `j=1,2` выполняется `||k||^{2j}e^{-1.7||k||²}≤e^{-0.85||k||²}`. Вне куба `|k_i|≤5` поэтому суммарный Gaussian majorant не превосходит

\[
 8\cdot3^3\frac{e^{-0.85\cdot36}}{1-e^{-0.85\cdot13}}
 <4.1\cdot10^{-11}.
\]

Следовательно, суммарные пропущенные слагаемые для `T`, `∑Kq`, `∑Kq²`, `∑Kr` соответственно ограничены этим числом, `40`, `1600`, `6400` кратными. Подстановка в (10) с `T≥1`, `A_k≥1-z`, и фиксированными коэффициентами даёт консервативную ошибку `≪0.001` от усечения. Конкретное число `69.0578...` посчитано обычной float-арифметикой и не обозначает формальную интервальную сертификацию её округлений; строгий знак конечного L=8 результата отдельно доказан (8). В данном fixed-β математическом refinement нет механизма автоматического исчезновения shape-source только от `L→∞`.

## 7. Принятый статус и реальное требование к ОТО

**Доказано для conditional v8:** (i) exact constant-curvature-zero, constant-volume, constant-shell-preparation family; (ii) positive second native response at an actual jointly stationary root with owned interval inputs; (iii) fixed-β continuum theta-functional and convergence of derivatives; (iv) numerical continuum nonzero positive shape-response with explicit rapidly decaying tail.

**Не доказано для D0:** что именно v8 полное native физическое Cost−Info; что эти постоянные coframes являются реальными preparation/history траекториями исходного M1 прибора, а не лишь матрично допустимыми полями условной программы; что другой admissible calibration/record law или proper-source subtraction отсутствуют; что выбранный fixed-β refinement есть физический. Нельзя promote `BOOK`, `CLAIM` или назвать полную ОТО «закрытой».

**Decisive parent consumer:** если исходная D0-native программа действительно выбирает этот v8 `H+J+R` и именно весь этот homogeneous joint carrier, то требуемый off-shell source identity `dS_native=c dEH+dR_actual+remainder` должен учитывать строго положительный flat-modulus остаток уже до кривизны. Проверка достаточности предполагаемого `remainder_h` обязана включать **(2)** и требовать `D²remainder_h[V,V]→0` при реально выведенном h-schedule. При fixed β,M,z выше он не обращается автоматически в ноль. Смена LC-связи, scalar weight и софреймного torsion тут бессильна, так как все их curvature/torsion jets нулевые.

### Проверка

```bash
python3 02_REGISTRY/research/sources/d0_native_flatmoduli_action_2026-10-16/check_flatmoduli.py
python3 -O 02_REGISTRY/research/sources/d0_native_flatmoduli_action_2026-10-16/check_flatmoduli.py
```

В локальном исполнении normal/optimized output JSON побайтно идентичен, SHA256 `53e542e245ca08915082891ea8d92b4e88f51b1294d95cd05839929cc34e4ac4`. Оригинальные owner inputs читаются как зарегистрированные теоремы; 4096 Fourier symbols пересчитаны только для нового контраста, старый interval proof не перезапускался. Ни Lean, ни full CI не запускались.

## 8. Положительный условный ход: короткий тепловой масштаб убирает *именно этот* flat-moduli дефект

Предыдущий пункт даёт не только препятствие, но и математически определённый способ его подавить **без добавления компенсирующего действия**. Это не выбор закона D0 — условный asymptotic test существующей функции.

Для любого компактного семейства положительных `G(t)` с `det G(t)=const` формула Пуассона даёт точное тождество

\[
\Theta_\beta(G)=\sum_{k\in\mathbb Z^4}e^{-4\pi^2\beta k^TGk}
 =\frac{1}{(4\pi\beta)^2\sqrt{\det G}}
  \sum_{n\in\mathbb Z^4}e^{-n^TG^{-1}n/(4\beta)}. \tag{11}
\]

При `β→0` весь ведущий локальный вклад `β⁻²/√detG` одинаков на (2), а отличия по shape содержатся только в ненулевых dual modes. Для `j=1,2`, равномерной эллиптичности и bounded `G^{(j)}`:

\[
\left|\partial_t^j\left[\beta^{-1}\log\Theta_\beta(G(t))\right]\right|
 \le C_j\beta^{-1-j}e^{-c/\beta}, \tag{12}
\]

где `c>0` может быть меньше `1/(4 sup_t λ_max(G(t)))`.

Пусть дополнительно `0<z(β)<1/2` и `M(β)` ограничена. Положим `r=z/(1-z)<1`. Для того же **уже заданного** feedback logdet, после единственной field-independent subtraction:

\[
 -16M\sum_k \log(1+r e^{-\beta\lambda_k})
 =-16M\sum_{l\ge1}\frac{(-1)^{l+1}r^l}{l}\Theta_{l\beta}(G).\tag{13}
\]

Ряд абсолютно сходится по каждому `β>0`. Применим (11) к `l≤β^{-1/2}`: shape-производные подавлены `e^{-c/\sqrt\beta}` с полиномиальным по `1/β` множителем. Хвост `l>β^{-1/2}` ограничивается геометрическим множителем `r^{\lfloor\beta^{-1/2}\rfloor}` и тем же полиномиальным пределом на heat-jet. Итак **все flat-moduli shape derivatives до второго порядка стремятся к нулю быстрее любой степени β** при `β→0` и фиксированном `r<1` (равномерно при `r` с запасом меньше 1).

Это доказывает, что flat-moduli no-go §4 **специфичен для fixed positive β**, а не является вечным запретом получить EH как локальный continuum leading term. Но full scale-source owner `A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md`, §7, требует одновременно `MzβZ<1`, а `Z~const β⁻²` для `β→0`. Поэтому при bounded `M>0` совместная стационарность потребует по крайней мере `z=O(β)` с коэффициентным ограничением; `z=o(β)` — безопасный *только с точки зрения необходимого scale inequality* пробный режим. Ни `z(β)`, ни `β(L)` не выбраны D0-процессом в текущих владельцах.

**Критическая оставшаяся физика:** даже когда flat-moduli shape response подавлен, на кривом фоне heat a₂ источает Riemannian/observer curvature `R_G` и torsion/measure terms из `A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md`, а не автоматически лоренцев `R_g`. Следовательно, high-temperature limit закрывает ровно один спектральный шум, но не завершает Einstein–matter variation, физический источник/наблюдателя или весь 10-slot admissible image. Кандидат на завершение обязан одновременно (i) вывести scale law из actual record/clock, (ii) устранить различие `R_G` и `R_g` законными operator/source jets, (iii) сохранить full rank по допустимым физическим metric probes, (iv) доказать uniform nonlinear refinement и source norm.
