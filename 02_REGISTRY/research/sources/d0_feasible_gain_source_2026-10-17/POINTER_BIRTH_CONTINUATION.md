# Pointer birth: точный вклад шести редких меток и граница полного вывода

17 октября 2026. Аналитическое продолжение того же Draft #334, input
`21f8a25f`; новых вычислительных запусков здесь нет. Это не коэффициент
полной pointer-энтропии и не новая физическая Info/action law.

## 1. Фактические входы и сохраняемый носитель

Все пути ниже относительно `02_REGISTRY/research/`; SHA256 фиксируют
прочитанные входы, а не новый replay или физический допуск.

| Вход | SHA256 |
|---|---|
| `A4D_POINTER_HISTORY_FINITE_PART_SOURCE.md` | `e0a7a9139fc469568111393c9ededdc6dde86e28c4c5a7b85795731183aa371b` |
| `A4D_COMPLETE_RECORD_NORMAL_BIRTH_SCALE.md` | `ca686aba406b81cd88e78def81750d830bba151783d6ac614013b146079e5291` |
| `A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md` | `6a14686fcaab0b48b78b8ff4f784d989ea3ead1edf0ee28d48b7c20f76c4a7ed` |
| `sources/d0_complete_history_information_2026-10-17/check_normal_birth_inputs.py` | `373f1e20b7319269d5805672da8cc12c845d9bfced0f9ec572108f816356f231` |
| `sources/d0_complete_record_channel_2026-10-17/check_flat_relaxation.py` | `0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9` |
| `certificates/a4d_native_curved_soldered_heat.py` | `bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da` |

Используются полный 128-output programme, все пространственные моды,
16 exterior-компонент и reference128. Для явной формулы ведущие поля —
принадлежащий программе LC-cone `e=s O01(theta(y)), n=e0, G=s^2 I`,
period-2pi, `s>1`. Ведущая нормированная амплитуда —
`C0=P_Sigma/sqrt(128)`, восемь первых импульсов по 16 компонент.
В coordinate forms ее reduced density `rho0=P_Sigma/128` стационарна.
Это условие на данное семейство, не доказательство физической подготовки
или утверждение о неизвестном пространственном минимизаторе.

Действуют гладкие h-jets/взвешенные H24-остатки из normal-birth owner,
включая `(Lambda(M_h)-I)/h=R0+hR1+h^2R2+O(h^3)`, и настоящий clock
`epsilon_h=p^2 h^2/64`, `T_h=n_h epsilon_h`. Все нормированные C1,C2,
coframe/link/observer/measure correctors сохраняются. Значения сравниваются
при совпадающем `T_h`; параметры гладкого семейства не меняют clock.

## 2. Событие «хотя бы одна из шести меток»

Выбираются literal Walsh labels `(16,8,24)`, coefficient0, ОБА golden
ports. Их leading rows тождественно нулевые на всем continuum chart.
Из фактического duplicated-word/32 SELECT и true adjoint:

```text
N_kappa,h=h D_chi/16+O(h^2),
ell_kappa,0=-p h D_chi D0/16+O(h^2),
ell_kappa,1=-sqrt(p) h D_chi D0/16+O(h^2).
```

Physical Kraus maps равны `sqrt(epsilon_h) ell`; squared port weights
суммируются в `p^2+p=1`. Нельзя подставить один port или Walsh factor1/32.
Точная algebraic причина: `N_(chi,0)=sum_r chi_r
(P_r+P_r^*-C_r-C_r^*)/16`. Поэтому при `P_r(0)=C_r` равенство N0=0
сохраняется для произвольных moving C_r, не только equal-norm cone.
Это НЕ coefficient1 role-defect sector с суммами `L_r+R_r=(1+b_r)I`.
Если другой выбранный sector имеет baseline0 лишь при equal norms, его
ambient derivative a0' может быть ненулевой. Для amplitude `h g+O(h^2)`
это дает `dq(event)=2h Re integral Tr(g^* a0' rho0)dt+O(h^2)`, а не
автоматически `h^2 dr2`; нужно сохранить его zero-baseline tangent law.
К выбранным здесь coefficient0 word-contrast rows это ограничение не
добавляется: их a0'=0 тождественно на данной programme family.
Пусть `R_h` — сумма этих шести CP maps, `F_h=Phi_h-R_h`. Точное событие R
имеет map `sum_(j<n) Phi_h^(n-1-j) R_h F_h^j`. Замена F-prefix на Phi-prefix
дает count, а не событие. Owned bound
`R_h^*(G^m)<=C epsilon_h h^2 G^(m+2)` и moment4 дают вероятность двух
вставок `O(h^4)`. Поэтому count/event различаются лишь на `O(h^4)`.

Weighted consistency и Riemann sum, с нормированными preparation jets,
дают локально равномерно на указанном гладком семействе

```text
q_h(R)=h^2 r2(T_h)+O(h^3),
r2=integral_0^T Tr[A_R(t) rho0(t)]dt,
A_R=(1/256) sum_chi D0 D_chi^2 D0.                       (P1)
```

Это не Schur-complement mass: здесь нет Q-проекции и не вычитается среднее
J_chi. First h-correctors не меняют r2: derivative ведущего N_kappa,0
равен0 тождественно; C1 входит в редкую амплитуду еще с одним h.

Полный smooth source коэффициента, с реальными pairing/normalizer jets:

```text
dr2=Tr[A_R(T)rho0(T)] dT
    +integral_0^T {Tr[(dA_R)rho0]+Tr[A_R eta]}dt,          (P2)
```

где eta — actual normalized state response. В dA_R дифференцируются оба
D0 и оба D_chi, true adjoints и движущаяся representation; это не fitted
source. Формула также указывает, что требуется при движении leading prep.

## 3. Точное значение на LC-cone, включая кинетический фон

Положим `E=<theta'^2>`, `F=<theta'^2 cos^2(2theta)>`. Full16 CAR input дает
`sum_chi <Tr J_chi^2>=32(2E+F)`. На каждом из восьми импульсов
`D0^2=s^-2 I`; знаки +/- отменяют кинетико-potential cross terms.
Каждый kinetic D_chi дает еще `s^-2 I`, а normalized form trace равен
`Tr16/16`. Следовательно (P1) имеет ТОЧНОЕ значение

```text
r2(theta)=T/(256 s^4) [3+4E+2F],
r2(theta)-r2(constant)=T/(128 s^4) [2E+F].                (P3)
```

Тройка — настоящий kinetic baseline, не новая цена и не свободное
вычитание. При winding `theta=y`: `r2=T/(32s^4)`, contrast `5T/(256s^4)`.
При фиксированных s,T periodic smooth variation имеет covector

```text
dr2[delta theta]=-T/(64s^4)
 <[(2+cos^2(2theta))theta''-sin(4theta)theta'^2]delta theta>.
```

Движение s,T добавляет `-4r2 ds/s+r2 dT/T`. Coherent lower bound из
normal-birth owner вместо этого использует вариации J_chi после удаления
их пространственного среднего; например winding bound `T/(256s^4)`.
Его нельзя назвать ни r2, ни полным pointer birth coefficient.

## 4. Энтропия выбранного сектора: значение и допустимый source

Используем ТОЧНЫЕ waiting cells finite-part owner: m marks занимают m
шагов, `j_final=n-m-sum j_i`, cell volume `epsilon_h^m`. На общем конечном
waiting measure nu положим `f_h=q_h/epsilon_h^m`; R означает наличие
хотя бы одной выбранной метки. Тогда `g_h=1_R f_h/h^2` и `int g_h=r2+O(h)`.
На matched interiors scaled one-rare path products сходятся: обычные
leading factors, ровно один `ell_rare/h`, затем обычные factors.
Две rare-вставки дают vanishing mass после деления на h^2. Fixed-m/gap
core convergence и (P1) дают полную сходимость масс к консервативному
single-insertion path integral. Поэтому `g_h -> g_R` в L1(nu).
Ни один будущий record не стирается: conservativity применяется после
суммирования всех фактических продолжений.

Нужная entropy UI не следует из одной этой L1-сходимости. Она выводится
по ПЕРВОЙ редкой метке. Разложим `log(f_h/h^2)` на prefix log-likelihood,
`log(a_rare/h^2)` и future log-likelihood. Scaled conditional rare rate
не превосходит `C Tr G^2 rho_prefix`. Prefix log^2 под этим весом ограничен
Cauchy-Schwarz: squared rate требует moment4, log^4 требует moment8.
Rare term ограничивается `x log^2 x<=C(1+x^2)` и moment4. Future log^2
линеен в четвертом моменте post-state; взвешивание rare insertion требует
moment6. F-prefix CP-доминируется Phi-prefix. Таким образом moment8
(здесь доступен H24) доказывает `int g_h |log g_h|^2<=C`.
Lipschitz truncation `x clip(log x,-R,R)` теперь дает
`-int g_h log g_h -> J_R:=-int g_R log g_R`.

Следовательно точный вклад этого сектора в ПОЛНУЮ finite part J_h равен

```text
-int_R f_h log f_h
   =2 r2(T_h) h^2 log(1/h)+h^2 J_R+o(h^2).               (P4)
```

Массовый `O(h)` нужен: умноженный на log(1/h), он все еще исчезает.
При локально равномерных семейных bounds (P4) дает distributional parameter
source коэффициента `2 dr2`, посредством integration by parts. Здесь не
заявлена pointwise C1 сходимость h^-2 остатка или исходный rough raw norm;
для нее нужен отдельный logarithmic-jet estimate выбранного сектора.

## 5. Обычные ненулевые leading rows тоже имеют нулевые слова

Выбранные шесть меток НЕ исчерпывают zero-leading pointer histories.
Это видно алгебраически без перебора. У четырех ordinary coefficient1
labels `(6,22,14,30)` на leading flat coordinate programme

```text
N_j=(1-b)/8 E_j,  E_j=sum_r H_jr Z_r,
Z_r=I-2 c_r c_r^*,  b=sqrt(1-s^-2),
H rows=(++++),(++--),(+-+-),(+--+).
```

Все N_j ненулевые. При even occupation parity вектор `(E_j)` имеет ровно
одну ненулевую координату (+/-4); при odd parity все четыре равны +/-2.
На одном shell momentum +/-e_r оператор D0 меняет только occupation r.
Два D0 возвращают исходный occupation, с ненулевым scalar factor. Поэтому
на ВСЕХ16 компонентах, при `a!=c` И `b!=d`,

```text
(E_a D0)(E_b D0)(E_c D0)(E_d D0)=0.                      (P5)
```

Для even input запрещает `a!=c`, для odd input — `b!=d`. Blank waiting
factors скалярны на данном shell. Например четыре разные указанные метки
дают zero-leading complete path несмотря на ненулевые отдельные N_j.
Их возможные first-jet births требуется вычислять; (P5) не объявляет их
коэффициент положительным и не заменяет actual programme другим channel.
Эти coefficient1 rows и их equal-norm specialization не отождествляются
с coefficient0 selected sector раздела2 при ambient metric variations.

## 6. Почему это еще не полный h^2 log-source native action

Для полной суммы нужно исследовать ВСЕ zero-leading words и regular sector,
а не только R. Возможная формула `beta_ptr=||Pi_zero-word v1||^2` требует
собственной normal-jet/tail теоремы и не равна coherent Schur trace b.
Pi здесь относится к matched simplex interiors и literal zero words.
Включать в него внешнюю область `{sum u>T}`, где v0=0 только из-за clock,
неправильно: strip `T_h-T=O(h^2)` может нести O(h^2) mass с density O(1),
а не birth density O(h^2). Аналогично надо отдельно учитывать collision
strips waiting-cell embedding. Их наличие не доказывает logarithmic birth.

Наконец EXACT `H_h=ell_h m_h+J_h`, `ell_h=2log(1/h)-log(p^2/64)`.
Если matching expansion count имеет `m_h=m0+h m1+h^2 m2+...`, а полная
finite part имеет `2 beta_ptr h^2 log(1/h)`, то полный H имеет коэффициент
`2(m2+beta_ptr)`, НЕ `2r2`. m2 содержит реальные state/stencil/Euler/clock
jets; оно здесь не вычислено. SAME-history action дополнительно содержит
`-log N`. Projective Born binding дает N=1 тождественно, но произвольный
raw Book normalizer этого не наследует. Normalizer с обычным matched power expansion не дает log h лишь при
ненулевом ведущем N0>0, локально отделенном от нуля. Положительность
каждого N_h сама недостаточна: N_h=h^2 a0+O(h^3), a0>0, дает
log N_h=2log h+log a0+O(h). Поэтому без nonvanishing leading limit нужно
сохранить и возможные logarithmic normalizer terms, и все source jets. Таким образом (P1)-(P5) — точный потребитель части
полной истории, не full J coefficient, не смена цены и не native-action=EH.
