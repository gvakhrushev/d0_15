# B110. Полный аналитический CODE-skew heat и статистическая ориентация

**Результат.** Для выбранного A54/B105 fixed-`Y` graph построена математическая четырёхслотовая smooth variation на его фактических стадиях. Прямая производная полного growing-clock heat удовлетворяет `||DH/Γ(Y)||raw*<2^-40672`. Вместе с B109 это даёт на всём real CODE-skew пространстве

    ||D(H+J)/Γ(Y) − DIτ(Y)∘L||raw* <2^-34.                  (1)

При **явно принятой исходной Book03 operator-statistical partition law**, той же сцене, clock и proper cut, для `ell=log φ`, `A_stat=−log Z/ell`, `Γ_A=Γ/ell` та же оценка справедлива для правильно ориентированной строки `−DA_stat/Γ_A`. Это условное статистическое приложение, а не закрытие physical C. Поздний owner §7fu прямо отозвал прежнее утверждение §7fs о закрытии physical C; прежние receipts не изменяются. `physical_C_closed=false`, `GR_closed=false`.

[Проверка](check_analytic_heat_statistical_source.py) содержит точную рациональную оценку и малый clock fixture; [receipt](B110_ANALYTIC_HEAT_STATISTICAL_CHECK.json) закрепляет inputs. Полное production слово, новый native compiler и произвольные finite-skew сравнения не исполнялись.

## 1. Какие именно стадии меняются

Зафиксируем один допустимый рациональный `Y` и actual B105 `M(Y)`/post. В центре все четыре control slots являются действительно оплаченными identity words. Каждый имеет как минимум четыре настоящие padded primitive stages. Для произвольного real CODE-skew tuple `X=(X_Pf,X_Qf,X_Qb,X_Pb)` на последней primitive stage каждого слота заменим её квадратную матрицу `U_last` математической кривой

    F_a(t)=exp(s_a t X_a) U_last,
    (s_Pf,s_Qf,s_Qb,s_Pb)=(+1,−1,+1,−1).                  (2)

Поскольку весь нулевой slot равен I, эта замена реализует в конечном произведении именно аналитические slot variations B109. При `t=0` каждая из четырёх матриц равна исходному **actual** primitive gate, весь graph, его actual post, marks, cut и последний closing gate совпадают с B105. Число стадий и birth layout в (2) не меняются; сама `exp(tX_a)U_last` при произвольном X **не объявляется native G/CX gate** и никакого нового физического исполнения не заявляется. Цель кривой — строго определить аналитическую производную на фиксированном графе.

Все четыре изменённые стадии расположены после всех ранних births и до retention: их полный carrier dimension равен `2^n`, `n=11893774624`. Actual B105 padded lengths дают

    Nbase=n+Lbase,    N=Nbase+2K,    K=175604,
    D=2^n(Lbase−2+3·2^K)−1,   bit_length(Nbase)=30833.      (3)

`Nbase` и `Lbase` вычисляются из **нового** A54 componentwise upper и действительно испускаемого padding, не берутся из старого A49. Последний retention gate и все births остаются неизменными. Proper cut — полный propagated input cut G7–G10 с исходным rank-one scene cut, включая все birth complements; не заменяется success-only или подготовленной колонкой.

## 2. Прямая производная полного heat

На настоящем clock carrier `K_clock=⊕H_j` и с полной canonical closure `R`, зависящей только от фиксированных births,

    T(t)=S(t)+R g E_f,       T(t)*T(t)=T(t)T(t)*=I.

Производная имеет четыре блока в различных stage domains и codomains, без изменения closure. Умножение на unitary не увеличивает trace norm, поэтому

    ||T′(t)||₁ = Σ_a ||F′_a(t)||₁
                 ≤2^n Σ_a ||X_a||op.                        (4)

Это **прямая аналитическая** оценка; она не выводится из конечной побазисной `heat_full_skew_dual_error` B105. На B109 raw unit ball `max_a||X_a||op≤52`, следовательно сумма в (4) не больше 208. Все старые WORK и возможные SOURCE remainders при этом остаются в полном carrier; здесь меняются только указанные CODE slots.

На исходной `K(9,11,13)` сцене, с 33 вершинами и 359 рёбрами, полный Hodge carrier содержит **425D** мод, в том числе harmonic:

    Δ₀=I−B_s⊗I−C_s⊗(T+T*),
    Z_H=359D+2 Tr_(33D) exp(−βΔ₀),
    H=β⁻¹ log Z_H,     0≤Δ₀≤2I,     Tr C_s≤33/22.

Для `β=2p²>0` дифференцирование настоящего полного trace и cyclicity дают

    |H′| ≤ (2/Z_H)||Δ₀′||₁
         ≤ (4 Tr C_s)/(359D) ||T′||₁
         ≤ 6||T′||₁/(359D).                                 (5)

Здесь `Z_H≥359D`: harmonic baseline сохранён. Это тот же G14/G16, применённый непосредственно к производной, а не разность, оценённая константой с последующим незаконным пределом `t→0`. Никакие тепловые моды или retained complements не отбрасываются.

Фиксированная central normalization использует actual `c₀(Y)` и ту же B105 feedback gain

    Γ(Y)=4 z p^K c_ref gσ/[1−z+z p^K c₀(Y)²],
    Γ(Y)≥γ_under p^K,   γ_under=(8/3)·2^-20·2^-3208.

Она положительна по B105: `c_ref>2/3`, actual post corner `c₀>2/3`, `gσ>2^-3208`. Из (3) имеем `D>2^n2^K`; из `p>3/5`, `(5/6)^4<1/2` и `4|K` получаем `(2p)^-K<2^(-K/4)`. Поэтому

    ||DH/Γ||raw* ≤ [6·208/(359 γ_under)]·2^(-K/4)
                  <2^-40672.                                (6)

Оценка равномерна для четырёх независимых произвольных skew и для всех рациональных Y заявленного chart. Γ фиксируется в дифференциале; здесь не вычисляется `D(H/Γ)`. Она является оценкой аналитической кривой (2), не доказательством доступности native версии для любого X.

## 3. Композиция с B109 и Book partition

B109 даёт feedback analytic `T_J=DJ/Γ` и конкретный рациональный residual

    ||T_J−DIτ(Y)∘L||raw* ≤ ε_J
      =52[2(H₂σR_v²+e_weight+e_corner)+2k+4e_post] <2^-34,

где `H₂=2^25`, `σ=2^-80`, `R_v=104`, `k<2^-116`; полный all-skew scalar remainder имеет порядок `σH₂R_v²`, а не осевое `σ²`. Точный расчёт повторно добавляет (6) до сравнения с `2^-34`, поэтому (1) следует без сложения двух округлённых пределов. Полный raw norm `max(||L||₂,max_a||X_a||op/52)` остаётся положительным на kernel, Pb и correlations; right lift и σ-калибровка B109 не меняются.

В исходной статистической предпосылке §§7fs.B/7fu для **того же** graph и того же исходного determinant power

    Z=Z_H det(I−zF)^−1,       J=−log det(I−zF),
    B=H+J,     A_stat=−log Z/ell,     ell=log φ.

При фиксированных `β=2p²`, `z=2^-20`, φ и scene имеем точную covector identity

    −ell DA_stat = DJ+β DH = DB+(β−1)DH = DB−p³DH.

С `Γ_A=Γ/ell>0` и **единой глобальной ориентацией**

    −DA_stat/Γ_A=(DJ+βDH)/Γ.

Поскольку `0<β<1`, из B109 и (6) также непосредственно следует

    ||−DA_stat/Γ_A − DIτ(Y)∘L||raw* ≤ ε_J+β·2^-40672 <2^-34.   (7)

Никакая финальная нормировка не подбирается по градиенту. При независимо варьируемом β добавляется `H Dβ`; его здесь нет, поскольку β зафиксирована. Равенство (7) — применение выбранного operator-statistical закона к тем же `Δ,F,T,P`, не derivation этого закона из bare kernel и не утверждение о максимуме/минимуме.

## 4. Проверка и физическая граница

Проверяющий код пересчитывает exact B109 и новое heat inequalities на `Fraction`, заново использует actual B105 `Nbase/K`, проверяет signs и исходную алгебру `β−1=−p³`. В конечном непроизводственном fixture построены полный growing clock с одним рождением и canonical complement, четыре изменяемых unitary stages, настоящая сцена `K(9,11,13)`, unitarity, trace-norm bound и spectral heat formula. Ненулевая производная шестишагового temporal trace подтверждает, что тест не предполагает неподвижный clock. На этой малой сцене численный heat derivative очень мал; конечная разность служит только диагностикой, строгая production bound — аналитические (4)–(6), а не floating-point fixture.

Для применения исходной operator-statistical partition как **математически заданной** цены не нужно вводить отдельный тариф на каждый gate или физически готовить Gibbs sampler. Однако поздний §7fu сохраняет конкретную physical C обязанность: связать фактически взвешенный memory-valued Cost−Info history object с этой graph partition полной source equivalence либо контролируемым residual на том же исполнении. Одна общность графа и (7) этого не доказывают; более сильный kernel-only dictionary тоже остаётся отдельным вопросом. Это не новое требование уникальных тарифов.

Кроме того, (2) не является оплаченным native full-skew compiler; остаются его реальные finite comparisons, accuracy/marks/heat, физические `iota_h` и `V_h`, остальные независимые old/input/WORK/scene/record/Info directions, original vacuum/`Dν` marked transport и GR refinement. Поэтому `physical_C_closed=false`, `GR_closed=false`.
