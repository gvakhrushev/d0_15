# D0 → ОТО: физическое действие — полный native history source несовместим с нормированным Cost−Info=v8 при фиксированном β

**17 октября 2026, RESEARCH / SCOPED ACTION-SELECTION NO-GO.** Существующий Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. Исходная программа, её CAR, 128 выходов и reference128, полная thermal sum и Price `H+J+R` **не изменяются**. Не изменяются BOOK/CLAIM, очередь, чужие receipts, математические калибровки. Это **не** доказательство ОТО и **не** no-go для всех native Info, физических clock laws или других допустимых подготовок.

## 0. Потребление действительных владельцев

1. `A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md` §§1–5: полный настоящий Julia/golden раунд. Blank Kraus `K_0=B_h=I−ε_h Δ_h/2`, остальные **127** исходов без сброса архива, полная эффектная сумма `E_exit=I−B_h²=ε_h Δ_h−ε_h² Δ_h²/4`; каждый homogeneous Fourier block сохраняется всеми flat Kraus. На ненулевом k `Δ_h(k)=λ_h(k)I_16`, остальные grades не удалены. Reference128 не обнуляется.
2. `A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md` §§1–5: для *того же полного 128-outcome tape* доказано `D_V H(q_h)/log(1/ε_h)→D_V m_T` при указанных bounded-smooth, fourth-moment, actual preparation/field first-jet гипотезах; в случае `w=q` имеем `E_q Cost−Info=H(q)/lnφ`. Без binding `w=q` надо сохранять `−d log N/lnφ`.
3. `A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md` §0.1 и `sources/d0_native_flatmoduli_action_2026-10-16/RESULT_RU.md`: условный **фактический стационарный v8** на `L=8`, homogeneous `G_*=(d−o)I+o11ᵀ`, `d=0.0636351915943445350…`, `o=0.0040167350432317253…`; faithful shell `8×16=128` и её реальная нормализованная подготовка `P_Ω/128`; thermal `16L⁴` (не shell-only), β=2p², z=2^−20,M=128.
4. `A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md` и `A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md`: цена по **тем же** `K=B^{2n}` и препарационному `R`, fixed-calibration настоящий first source.

**Общая конвенция:** `h=1/L`, `p=φ^-1`, `ε_h=p²h²/64`, `α_h=ε_h/2`, `n_h=128L²`, `m_h^{clock}=2n_h=256L²`, `β=n_h ε_h=m_h^{clock} α_h=2p²=3−√5`, `M=128`, `z=2^-20`. Отличаем clock depth `n` от ожидаемого числа выходов `m_exit` и от ранга full record. Все L кратные4 для совместимости с исходной сеткой; дополнительный контроль L=12,24 — математическая проверка той же homogeneous formula, не новое допускающее правило сетки. **Семейство n_L=128L² является точным допустимым по арифметике продолжением фиксированной v8-калибровки β; утверждения, что M1 независимо выбирает такой межуровневый clock schedule, нет.**

## 1. Теорема: внутри НАСТОЯЩЕГО native full128 round выходы имеют Bernoulli source

Берём один и тот же homogeneous flat coframe `F(t)=sqrt(1+t)F_*`, `A=I`, на периодическом L^4 графе. В предыдущем владельце его Euclidean Gram `G(t)=(1+t)G_*` допустим при |t| малом. Пусть начальная подготовка системы **та же** faithful `ρ_Ω=P_Ω/128` на восьми shell моментах `±e_r`, **всех 16** CAR grades, с сохранённой purification в reference128. Эта подготовка при t≠0 не объявляется новым joint root — мы вычисляем законный off-shell covector.

На каждом из восьми k в Ω имеется только одна отличная от нуля Fourier-coordinate. Из CAR на полном exterior 16:

```
Δ_h(k,t)=λ_L(t) I_16,
λ_L(t)=(1+t) γ_L d,
γ_L=4L² sin²(π/L),   γ_8=128−64√2.
```

Все homogeneous Kraus-множители диагональны по momentum: их исходные role-операторы являются комбинациями постоянных внутренних CAR-матриц и пространственных сдвигов, которые коммутируют с трансляциями. Поэтому для **каждой conditional system/reference state после любого полного сохранённого префикса** поддержка остаётся в Ω. Хотя её Fock/AF внутренности, порты и marks могут меняться, **неизмеренный агрегированный эффект** имеет на этой поддержке вид

```
Pr(exit | полный прошлый prefix)=q_L(t),
q_L(t)=ε_L λ_L(t)−ε_L² λ_L(t)²/4,
Pr(blank | полный prefix)=1−q_L(t).
```

Следовательно коарсированный retained-процесс индикаторов выхода является iid Bernoulli с параметром q_L: это индукция по полной условной истории, а не заменённый «2-outcome прибор». Все 127 nonblank marks, оба порта, прошлые записи и reference остаются в оригинальном full tape; coarse bit — только вычисляемый marginal.

Для **общего количества выходов во всех n rounds**, не first exit, точны

\[
\begin{aligned}
\mathbb E M_L(t)&=n_Lq_L(t)=\beta\lambda_L(t)-\frac{\beta\varepsilon_L\lambda_L(t)^2}{4},\\
\partial_t\mathbb E M_L(0)&=\beta\gamma_Ld\left(1-\frac{\varepsilon_L\gamma_Ld}{2}\right) >0,\\
\lim_{L\to\infty}\partial_t\mathbb E M_L(0)&=\beta(4\pi^2)d>0.
\end{aligned}\tag{1}
\]

Фиксированное `d` взято из ранее сертифицированного homogeneous root box; для строгой ненулевости достаточно его доказанной нижней положительной границы. Числовое значение предельного коэффициента — иллюстрация, не новый interval owner.

Бинарный marginal имеет **точную** энтропию `n h₂(q)` и source `n q' log((1−q)/q)`. Это отдельный проверяемый negative control: binary entropy не объявляется равной entropy **полной** размеченной записи. Полную entropy/source читает следующий уже доказанный владелец.

## 2. Полная 128-labelled entropy: положительный логарифмически растущий ПЕРВЫЙ источник

Для исходной full128 output distribution `Q_{L,t}` за n rounds используем не эвристику про iid marks, а теорему `A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md`:

\[
\frac{\partial_t H(Q_{L,t})|_{t=0}}{\log(1/\varepsilon_L)}
\ \longrightarrow\ \lim_{L\to\infty}\partial_t\mathbb E M_L(0)
=\beta(4\pi^2)d.\tag{2}
\]

Здесь используются **реальные** complete-record source и bound: homogeneous family имеет bounded energy moments любого фиксированного порядка на Ω, normalized pure/reference128 initial state, smooth radial coframe/true adjoint/record jets и реальный clock `nε=β` без выдуманного запуска `β(L)`. Полный conditional tape не замораживается. Старый theorem сохраняет нормализатор и all-field derivatives; на нашей trajectory его `dm_T` равен (1), поскольку Δ на поддержке scalar.

В единицах logφ:

\[
\boxed{\lim_{L\to\infty}
\frac{\partial_t[H(Q_{L,t})/\ln\varphi]_{t=0}}{\log(1/\varepsilon_L)}
=\frac{\beta(4\pi^2)d}{\ln\varphi}\approx 3.988187031727065>0.}\tag{3}
\]

Следовательно source **полной** pointer Shannon price растёт ~`3.988... log(1/ε_L)`. Не только ее значение, но и настоящий первый source, благодаря Fisher/orthogonal-innovation proof уже существующего владельца. Это не замена полной записи её coarse exit bit.

## 3. Источник настоящей условной v8-цены в том же направлении равномерно ограничен

На том же 4D homogeneous coframe, но с **всеми** L⁴ thermal momenta ×16 CAR grades, собственный spectral symbol равен `Λ_L(k,t)=(1+t)Λ_L(k)`, где

```
z_r(k)=L(exp(2π i k_r/L)−1),  Λ_L(k)=z(k)* G_* z(k),
B_k=1−α_L Λ_L(k), K_k=B_k^(m_clock),
Z_L=16 Σ_k K_k,   A_k=1−z+z K_k.
```

При fixed β,M,z,C по существующему full-source owner:

\[
\begin{aligned}
H'_L&=-\frac{16}{Z_L}\sum_k \Lambda_L(k) B_k^{m-1},\\
J'_L&=16M\beta z\sum_k\frac{\Lambda_L(k)B_k^{m-1}}{A_k},\\
R'_L&=\gamma_L d, \qquad S'_L=H'_L+J'_L+R'_L.
\end{aligned}\tag{4}
\]

Уже на исходном `L=8` корне `S'_8≈0` (все исходные три слагаемых сохранены; ни одного root search не произведено). Для всех L>=4 имеется *аналитическая* uniform оценка. Обозначим `b=d−o>0`, `a=d+3o`, и приведём k к `[-L/2,L/2]^4`. Тогда

\[
16b|k|^2\le \Lambda_L(k)\le4\pi^2a|k|^2,
\quad B_k\ge1-\frac{p^2a}{8}>0.996,
\]
\[
B_k^{m-1}\le B_*^{-1}e^{-\beta\Lambda_L(k)},
\quad Z_L\ge16,\quad A_k\ge1-z.
\]

Поэтому все `∑_k Λ B^{m−1}` доминированы ОДНОЙ сходящейся lattice-Gaussian суммой

\[
B_*^{-1}4\pi^2a\sum_{k\in\mathbb Z^4}|k|^2e^{-16\beta b|k|^2}<\infty.
\]

Аналогично ограничен `R'`. Следовательно **строго** `sup_L |S'_L|<∞` и

\[
\boxed{\lim_{L\to\infty}\frac{S'_L}{\log(1/\varepsilon_L)}=0.}\tag{5}
\]

Из (3),(5) получается точное неравенство source scaling для данной, объявленной гипотезы выбора действия.

### Сильнее: два уже представленных event normalizer не могут заплатить логарифмический долг

Условная событийная реализация той же v8-цены из `sources/d0_native_action_selection_2026-10-16/RESULT_RU.md` использует `P_surv=Z/(16L⁴)` и `P_blank=det[(1-z)I+zK]`. При одном и том же физическом параметре t **тождественно**

\[
\partial_t\log P_{\rm surv}=\beta H'_L,\qquad
\partial_t\log P_{\rm blank}=-J'_L/M.\tag{5a}
\]

Оба источника равномерно bounded по уже доказанной Gaussian-оценке. Таким образом **ни один фиксированный линейный комбинационный нормализатор** `N_L = const(L) P_surv^a P_blank^b` с L-независимыми конечными a,b не удовлетворяет необходимому ниже условию (7). Даже если `P_blank` само становится очень малой probability из-за числа UV-мод, **его первая полевая производная** остаётся O(1). Это не исключает иных настоящих raw normalizers, но исключает попытку объявить уже построенные survival/blank scalar events недостающим `log(1/ε)` нормировочным источником без нового clock-dependent веса.

## 4. Decisive conditional selector/no-go и необходимый correction debt

Предположим, что **физический** Book-III Cost−Info приклеен к **той же** полной normalized actual history: `w_ω=q_ω`, `N=Σw=1`, `S_ω=−log_φ q_ω`. По уже доказанной pathwise identity

\[
\mathbb E_q(Cost-Info)=H_\varphi(Q_L)=H(Q_L)/\ln\varphi.
\]

Тогда на этой же faithful-shell coframe траектории

\[
\boxed{\lim_{L\to\infty}
\frac{\partial_t\big(\mathbb E_q(Cost-Info)-S_{v8}\big)_{t=0}}
{\log(1/\varepsilon_L)}
=\frac{\beta(4\pi^2)d}{\ln\varphi}>0.}\tag{6}
\]

**Тем самым** normalized same-history `Cost−Info` **не может** быть тождественно исходной условной v8-ценой modulo field-independent constant **или** `C¹` остатком `o(log(1/ε))` вдоль этой действительной admitted off-shell family. Это не доказательство двух разных on-shell roots и не общетеоретический запрет D0→GR.

Более общая binding raw weights `w=N q` имеет source

\[
d\mathbb E(Cost-Info)=\frac{dH-d\log N}{\ln\varphi}.
\]

**Необходимое условие**, чтобы получить bounded first source fixed-β v8 на этой trajectory:

\[
\boxed{\lim_{L\to\infty}\frac{\partial_t\log N_L|_0}{\log(1/\varepsilon_L)}
=\beta(4\pi^2)d.}\tag{7}
\]

Никакой `N_L` не назначается и не подгоняется. (7) — строго необходимый долг любого proposed full-history/raw-price morphism. Для проектных prefix weights с `w_empty=1` и `Σ_child w_child=w_parent` все `N_L=1`, значит (7) НЕ выполняется; такой отождествляющий morphism отвергнут. Иной event cut, reservoir, coherent archive, условная вероятность, стоимость контроллера либо фактически другой clock *могут* дать неединичный `N`, но их правильная цена, знак и все источники обязаны исходить из реального native процесса; (7) не разрешает их добавлять вручную.

## 5. Точная воспроизводимая проверка, отличие от старых расчётов

`check_entropy_action.py` проверяет:

- все16 CAR grades с комплексным `D²=λI` (точная sympy матрица) и ту же восьмиосевую оболочку 128;
- точный golden split, clock `nε=mα=β`, Born-нормировку и `total exits` вместо ошибочного `first exit`, истинный binary entropy source;
- `L=4,8,12,16,24,32` собственные shell энергии, expected exit-count и его derivative;
- полный v8 trace на `L=8,12,16,24,32` по **всем L⁴ momentum ×16**, сохраняя `M=128,z=2^-20`, true normalizer and material source;
- same-source finite difference на `L=8`, позитивность uniform Gaussian-bound и строгую ненулевость leading log coefficient;
- `python` / `python -O` даёт байт-в-байт один научный `RESULT.json`. Никакой full `128^n` enumeration, повторного старого Lean/expensive proof, stationary root search или новых fitted fields.

Зависимость: Python3, NumPy, SymPy. Вход `d` в численном тесте — центр сохранённого корневого интервала, не новый eigenvalue proof. Аналитический знак (6) требует только `d>0`, которое обеспечивает исходная регулярная область.

**Consumer:** `MORPH_NATIVE_RETAINED_HISTORY_TO_V8_ACTION` → `LAW_SELECT_V8_PROGRAM_AND_PRICE`: исключить путь «Book price = expected surprisal полностью нормированной native tape» для неизменённых fixed-positive-β v8; проверить любой иной raw partition/source по (7). Оставить Draft #334, полный physically-selected Cost−Info, full Lorentz Einstein source, nonlinear joint roots и `h^-2` терминал OPEN.