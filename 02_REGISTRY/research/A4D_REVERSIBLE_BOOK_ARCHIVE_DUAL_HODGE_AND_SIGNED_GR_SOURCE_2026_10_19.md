# D0 → ОТО: ДВА ОРИГИНАЛЬНЫХ HODGE-УРАВНЕНИЯ ДЛЯ ВСЕГО BOOK-АРХИВА, 327 ОРИЕНТИРОВАННЫХ ЦИКЛОВ И 326 СИММЕТРИЧНЫХ ИСТОЧНИКОВ

**Дата:** 19.10.2026  
**Owner / consumer:** действующий научный интегратор #334, \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`.  
**Статус:** EXACT MATHEMATICAL NATIVE-SCENE SYNTHESIS + самостоятельная арифметическая проверка; полный D0→GR не доказан.  
**Входы:** исходные \`K(9,11,13)\` (33/718), #384 \`A4D_BOOK_FLOW_HESSIAN_EQUALS_ORIGINAL_ARCHIVE_METRIC_AND_FUTURE_SOURCE_SELECTOR_2026_10_19.md\` и \`A4D_ORIGINAL_BOOK_FLOW_HESSIAN_NATIVE_ARCHIVE_POISSON_AND_RANK32_DARK653_2026_10_19.md\` (одно полное скалярное Book-функциональное действие, Q_A/685, future rank32, полный Poisson Schur), #334 \`A4D_SINGLE_RUN_PERRON_BOOK_CAR16_FRESH_FLAG_SOURCE_WELD_2026_10_19.md\` (§7–8: **оригинальный p-Golden**, положительные шесть Lorentz-источников и редкий clock), #334 \`A4D_BOOK_PRETRACE_ORIENTED_GR_MEMORY_SYNTHESIS_2026_10_19.md\` (ориентированная память до trace), исходный 327-модальный Lie/triangle owner и контроль H1=0 на заполненном clique-комплексе.  
**Проверяющий скрипт:** \`sources/d0_book_signed_hodge_2026-10-19/check_native_718_signed_signless_hodge.py\`. Новый скрипт читает уже-owned оригинальные размеры/операторы и не изменяет \`Book03\`, G0, ActionProtocol, source, norm или физический selector.

## 0. Стратегическое открытие

Новый точный результат #384: гессиан **скалярного исторического Book macro-action** равен норме его 685-мерного исходного архива, а 33-мерный future detector видит только rank32. Следующие 653 невидимых направлений были известны как одно остаточное пространство. Его внутренняя структура теперь полностью разрешима без каких-либо 718×718 обратных матриц:

\`\`\`
original full directed scalar source 718
  = 33 scalar/history-null    (one absolute constant + 32 endpoint gradients)
  + 32 future archive source
  + 327 reversal-odd / directed graph-cycle source
  + 326 reversal-even / symmetric two-endpoint source.
\`\`\`

Это НЕ четыре независимых компоненты выбранного физического действия. Строго: после факторизации по 33-мерному ядру Cost→архив происходит изоморфизм на ортогональную сумму original future32 ⊕ odd327 ⊕ even326 на **исходном обратимом Perron-фоне**, в метрике, вынужденной исходным \`ln φ\`.

Ключевой конструктивный результат: **каждое из двух тёмных пространств есть точный образ одного 33×33 Poisson-оператора** — обычного Markov Laplacian \`I-P\` и **signless** Markov Laplacian \`I+P\` соответственно. Это делает уже-существующий реальный 653-dimensional archive source вычислимым с двумя исходными вершинными решениями, не предполагая, что он физически исчезает.

## 1. Exact all-718 327+326 decomposition, not a number match

На исходном каноническом Cost=1 графе \`K(9,11,13)\` Perron transfer симметричен и \`P\` обратима по detailed balance: \`μ_uv=π_uP_uv=μ_vu>0\` на всех настоящих рёбрах. Пусть \`J0,J1: R^33 → R^718\` — уже построенные исходные source/target изометрии #334/#384. На их пересечении определим

\`\`\`
D = ker J0^T ∩ ker J1^T ⊂ R^718.
\`\`\`

При \`η_uv=z_uv/sqrt(μ_uv)\` условия \`η∈D\` эквивалентны \`sum_v z_uv=0=sum_u z_uv\` (ZERO BOTH MARGINALS). Поскольку μ симметрична, обращение ребра \`η_uv↔η_vu\` сохраняет D и его евклидову метрику; собственные ± пространства ортогональны:

\`\`\`
D = D^- ⊕^orth D^+ .
\`\`\`

Точный размер:

- Антисимметричное \`z_uv=-z_vu\`: дивергенция на 359 исходных ненаправленных рёбрах имеет rank \`V-1=32\` из связности. Поэтому \`dim D^-=359-32=327\`.
- Симметричное \`z_uv=z_vu\`: unsigned/signless incidence имеет rank \`V=33\`, потому что граф связен и содержит исходные треугольники (у уравнений \`a_u+a_v=0\` по всем рёбрам только нулевой корень). Поэтому \`dim D^+=359-33=326\`.

Таким образом, буквально на исходном носителе:

\`\`\`
rank Q_A = 718-33 = 685,
rank (Q_A J1) = 32,
D653 = D^-_327 ⊕^orth D^+_326 .
\`\`\`

ВАЖНО: 327 — cycle-space первой СКЕЛЕТНОЙ графовой цепи. На исходном ЗАПОЛНЕННОМ треугольниками clique-комплексе H1=0, а все эти 327 циркуляций являются \`im ∂2\`; это не 327 нетривиальных классов H1 полного комплекса. Ровно поэтому исходные 327 ориентированных triangle-matrix coordinates могут служить базисом представления, но скалярные circulations и некоммутативные Lorentz holonomies остаются разными операторами.

## 2. Universal reversal-ODD Hodge projection, without any 718 Schur solve

Для любого настоящего допустимого направленного edge-Cost first source \`d_uv\` на исходном обратимом reference разделим:

\`\`\`
d^-_uv=(d_uv-d_vu)/2,     d^+_uv=(d_uv+d_vu)/2.
\`\`\`

Для \`d^-\` зададим исходную настоящую Markov строку \`m^-_u=sum_v P_uv d^-_uv\`. Detailed balance даёт \`π·m^-=sum_uv μ_uv d^-_uv=0\`. Следовательно конечное Poisson-уравнение

\`\`\`
(I-P) ψ = m^- ,     π·ψ=0
\`\`\`

имеет единственное нормированное решение, вычислимое через \`(I-P+1π^T)^(-1)\`. Вводим

\`\`\`
c^-_uv=d^-_uv+ψ_v-ψ_u.
\`\`\`

Оно антисимметрично и имеет нулевой outgoing и incoming weighted marginals:

\`\`\`
sum_v P_uv c^-_uv = m^-_u+(Pψ)_u-ψ_u=0.
\`\`\`

Так как μ симметрична, incoming равен минус outgoing после обратного ребра. Поэтому

\`\`\`
G^-(d)_{uv} = sqrt(μ_uv)c^-_uv ∈ D^-_327.
\`\`\`

Это именно ODD-часть настоящего #384 Poisson archive source. Для любого полностью reversal-odd d, **весь** scalar-history Schur source лежит в D^-_327 и ортогонален исходному future rank32 — не только единственный тестовый zone-chiral Cost из #384.

Moreover \`G^-=0\` iff \`d^-_uv=ξ_u-ξ_v\`, точный 32-dimensional endpoint coboundary. Любой nonzero orientated graph-cycle circulation создаёт СТРОГО ненулевую archive cost curvature

\`\`\`
δ² A_eff(d^-,d^-)=-(ln φ) ||G^-(d)||² < 0
\`\`\`

в исходном скалярном all-walk Book sector. Никакого физического Einstein tensor этим не вставлено. Если reversal-odd field Cost не admitted by actual G0, теорема остаётся тестом существующего 718-dimensional математического source fiber, а не утверждением о реальном Lorentz поле.

## 3. Universal reversal-EVEN SIGNLESS Poisson projection

Для всякого reversal-even \`d^+_uv=d^+_vu\` определим \`m^+_u=sum_v P_uv d^+_uv\`. На исходном не-бипартитном графе со строго положительными весами не существует eigenvalue \`-1\` у обратимого P: треугольники убивают period-2. Поэтому \`I+P\` обратимо, и существует единственное

\`\`\`
(I+P) χ=m^+ .
\`\`\`

Тогда

\`\`\`
c^+_uv=d^+_uv-χ_u-χ_v
\`\`\`

симметрично и имеет ОБА нулевых marginals, поскольку

\`\`\`
sum_v P_uv c^+_uv=m^+_u-χ_u-(Pχ)_u=0.
\`\`\`

Следовательно \`G^+(d)_{uv}=sqrt(μ_uv)c^+_uv ∈ D^+_326\` есть ТОЧНАЯ ортогональная проекция original scalar-history source на even dark326. Она равна нулю iff \`d^+_uv=α_u+α_v\` — в точности уже-known necessary/sufficient rank32 selection criterion #384 в reversal-even классе. Новое здесь — **прямая signless Hodge формула и единственное решение на исходных 33 вершинах**, а не ещё одна проверка ранга 653.

При любом d полный original history Schur splitting имеет исходную геометрически полезную форму:

\`\`\`
-δ² A_eff(d,d)/ln φ
   = ||G_future(d)||² + ||G^-(d)||² + ||G^+(d)||²,
\`\`\`

всем правым членам соответствует одна и та же genuine original Poisson archive isometry #384. Для cross directions используют соответствующую симметричную поляризацию. Будущее rank32, odd327 и even326 ортогональны на данном обратимом фоне. Никакие члены не стираются.

## 4. Strong parity firewall: native scalar Book is EVEN in every anti Cost deformation

Пусть \(K_0=K_0^T>0\) на собственном оригинальном support и \`d^-=-d^-T\`. Рассмотрим уже-allowed математическую оригинальную направленную Cost-family

\`\`\`
K_uv(t)=K0_uv exp[-(ln φ)t d^-_uv].
\`\`\`

Имеем точное неоспоримое \`K(t)^T=K(-t)\`. Спектральный радиус матрицы равен таковому у транспонированной, значит

\`\`\`
ρ(t)=ρ(-t),   A_eff(t)=-log_φρ(t)=A_eff(-t).
\`\`\`

**Любые нечётные Taylor derivatives scalar Book pressure на обратимом фоне равны НУЛЮ**. Однако второй derivative для non-gradient anti d строго отрицателен в #384 Schur norm. Следовательно скалярная all-walk price может хранить chiral current как информационную КРИВИЗНУ / Fisher second source, но не как first-order oriented signed Cartan force. Чтобы получить геометрический нечётный source FIRST variation, действительно необходимо сохранить порядок и фазу до scalar trace через original pretrace Lorentz/CAR/Hodge; само "просто заменим скаляр на matrix logdet" не решает это (§PRETRACE scope).

Это не no-go для всего Book03: его исходное \`[q(γ)]\` НЕкоммутативное представление и фактический положительный complete Golden/Julia tester доступны как **математические** carriers. Не утверждать, что любой антисимметричный source меняет физический G0: actual field→directed Cost map остаётся неизвестным.

## 5. Exact original 9/11/13 chirality: THREE derivations agree, no fitted coefficient

На ОРИГИНАЛЬНОЙ полной support выбираем \`d_AB=d_BC=d_CA=+1\`, \`d_BA=d_CB=d_AC=-1\`. Все 718 directed edges остаются. С \(p=φ^{-1}, \ell=\ln φ\), original equal Cost=1 \`K(t)=p A\odot \exp(-\ell t d)\` имеет exact three-zone Perron reduction с \`R(t)=ρ(K(t))/p\`:

\`\`\`
R(t)^3 -359 R(t)-2574 cosh(3 ell t)=0,
R(0)=rho0,  rho0^3-359 rho0-2574=0.
\`\`\`

Его scalar Book action \`A_eff(t)=1-log_φR(t)\` имеет:

\`\`\`
A_eff'(0)=0,
A_eff''(0)= -(ln φ) * 23166/[rho0*(3 rho0²-359)]
          = -0.4763744515526457...
\`\`\`

Это АНАЛИТИЧЕСКОЕ вычисление из original three-zone graph, не вторая подгонка.

Независимо original full33 Perron P,μ и настоящий Book Poisson archive #384 дают

\`\`\`
||G^-(d)||² = 0.9899475173820561...
23166/[rho0*(3 rho0²-359)] = 0.9899475173820622...
\`\`\`

Равенство подтверждено до 6.2e-15 в независимом JS 33×33 solver. Это уже pinned #384 численный chiral-Schur terminal, теперь получивший **закрытый характеристический многочлен и exact parity-Hodge происхождение**.

Третий proof: представим исходный ровно ONE zone-permutation invariant antisymmetric balanced flow (каждый zone→zone arc несёт +/-1, распределённый поровну по n_a n_b primitive ребрам) как \`z^χ\`. Его outgoing/incoming marginals НУЛЕВЫ; \`∑_e z^χ_e d_e=6\`. На исходном zone-symmetric Perron-фоне весь \(G^-(d)\) лежит в этой ОДНОЙ из 327 oriented zone-invariant archive directions. Поэтому Cauchy–Schwarz НАСЫЩАЕТСЯ:

\`\`\`
||G^-(d)||² = 36 / Σ_e [(z^χ_e)^2 / μ_e]
            = 23166/[rho0*(3 rho0²-359)] .
\`\`\`

Это третье точное независимое описание одного и того же первоначально "тёмного" информационного источника: характеристический полином, Markov Poisson и oriented graph Hodge cycle. NO gravity coefficient or extra graph chosen.

Второй уже реальный original Cost-probe #384 — повышение ТОЛЬКО пары обратимых рёбер 0↔9 — имеет \`G^-=0\`, но \`||G^+||² ln φ=0.0013000035359633177...\`: подписанный второй Poisson \`I+P\` воспроизводит именно зарегистрированную 326-even-dark долю. Простое обращение симметрии Cost НЕ закрывает архив.

## 6. Strategic consequence coupled to latest #334 native-p Golden and rare clock

#334 at its current 2026-10-19 head supplies a genuinely positive **native Golden p=φ^-1** Lorentz/CAR16 Julia chart, NOT arbitrary 1/2 contraction:
\`J(pI)=Xflip G_original\`. Its strictly complete fixed 14-outcome detector has physical mathematical six-proper-Lorentz Fisher \`I6 p²/6\`. Under a **declared** original full128 IID exit/marked instrument with native \(ε_h=p²h²/64\), \(n_h ε_h→β>0\), the SIX eigenvalues survive as \`β λ p²/6 >0\`. The all-good success/fail complement and whole clock are retained; compulsory actual fullStep and controller/cost selection remain missing. Thus there is no generic "refinement automatically destroys six Lorentz directions" excuse on that controlled native-type chart.

Combined inference:

1. Original scalar Book Cost/Info now has a FULL exact internal force split into future32, oriented-cycle327 and symmetric-dark326, with just TWO 33×33 Hodge solves and a native \`ln φ\` coefficient. These are the complete priced scalar HISTORY sources, not Einstein already.
2. Original ordered CAR/Lorentz has a six-dimensional positive FIRST observable with an existing Golden normalization and controlled event-clock Fisher. On smooth geometry it can distinguish the directions the scalar pressure loses under reversal parity. It remains a mathematical admitted-class construction, not a compulsory G0 programme.
3. Original finite star/Cartan with full40 variation, accepted #377 smooth geometric EH probe, exact Brinkmann+CAR nonvacuum family and nonlinear crossed-Weyl quartic jet are already owned independently.

Hence the ONLY scientifically load-bearing new D0→GR physical binding is **one actual G0/Book same-history field-to-directed-edge Cost and ordered-Lorentz representation** with full paid flags/oldRIGHT/clock/prep/CAR. It must verify BOTH components on the SAME cut, THEN compare the COMPLETE native \(16+24+2+\mathrm{PREP}+\mathrm{CLOCK}\) first source to original star+matter and satisfy the actual Ward and exact physical recovery/refinement. Do not define missing stress as a difference to Einstein. No numerical Newton constant or Λ is fixed.

**KILL FIRST / strongest cheap test:** take one ACTUAL admissible original Lorentz J23 tangent and one independent coframe/matter tangent. Calculate its true entire primitive \`Ds_uv\` and ordered CAR memory jet, including failures. Project \`Ds\` through the two original Poisson solves above. If chiral 327 source or symmetric-dark326 remains nonzero, it CANNOT be "included automatically" by future rank32, and the ordered/complete native Book price must explicitly carry/cancel it. If all unseen components vanish, 33-mode future feedback is scalar-history complete on THAT admitted field subspace, not universally. The decisive comparison is with one original complete same-action stationary history and its native Ward, NOT another Ricci or rank classification.

**Firewalls:** This memo does not prove the actual physical Cost selection; #384 independently proves primitive ActionProtocol alone cannot fix it. It does not equate graph 327 triangles with original 4D Role faces, show Lorentz connection is a native scene graph assignment, or treat Fisher information as signed Palatini action. It does not prove full nonlinear off-shell gravitational action selection, full Planck/effective coupling, classical limit of complete coherent history, arbitrary periodic exact roots, physical stress or RAW-216. \`GR_closed=false\`.

## 7. Reproduction

\`python3 02_REGISTRY/research/sources/d0_book_signed_hodge_2026-10-19/check_native_718_signed_signless_hodge.py\`.

Author-independent exact math: signed incidence rank32, unsigned incidence rank33, source-target rank65 on the original supported graph. First two modular exact ranks and the third double-cover rank were independently checked over \`F_1000003\` in an external V8 arithmetic reproduction, with ranks 32/33/65. Analytic characteristic polynomial verified symbolically by direct 3×3 determinant expansion. The original 33×33 Perron/Poisson source and BOTH parity Hodge projectors were independently checked numerically in V8 against the original #384 718-dimensional full operator results; errors \`<1e-13\` in all asserted projections, and observed Book chiral analytic-vs-Poisson discrepancy \`6.2e-15\`. The committed Python checker repeats the same evidence and native exact SymPy ranks; current-head repository execution and CI for the NEW checker are not yet claimed.
