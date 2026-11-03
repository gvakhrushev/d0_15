# Краткий contract scoped native κ → Einstein closure

3 ноября 2026. Existing research owner [#334](https://github.com/gvakhrushev/d0_15/pull/334).
Вход: `e63ef7a3073f4854a2fc8fd4c69bf004bc42d544`.
Потребитель: `constitutive` / `native_sector` → `gr_operational_realization`.
Это уточнение [общего контракта](D0_GR_CLOSURE_CONTRACT_RU.md), а не новая
очередь, аксиома или принятый terminal. **Closure пока не установлен.**

## A. Какое утверждение закрываем

На объявленном непустом локальном регулярном классе, с указанными материей,
границами, gauge, физической нормой и κ-топологией, вывести из owned D0
primitives **одну допустимую семью полных оплаченных историй**. Её реально
выбранная полная цена и совместные уравнения metric/link/matter,
preparation/clock/record/scene должны давать Einstein + declared matter
и обратное восстановление каждого решения заявленного класса.

Допуск задачи и её вариаций не может предполагать Einstein residual = 0.
Нужна физическая binding/equivalence полной цены; произвольный новый Info/R
не добавляется. Внешний controller, подбор c и уничтожение поля через
свободный shared-c controller не закрывают этот contract.

## B. Какой источник принимаем

Пусть \(Y\) — все оставленные физические переменные, \(n\) — все **реально**
независимые внутренние переменные. Для полной цены \(S(Y,n)\) вычислить
\(E_Y,E_n\) на одном execution, сохраняя generated-state adjoints и реакции.
На допустимой стационарной секции \(E_n=0\) требуется самостоятельный
\(\mathcal E(Y)=E_Y(Y,n_*(Y))\), не тождественно нулевой off shell.

Неидентичность \(E_Y\ne L^*E_t\) лишь с одним scalar controller — первый
фильтр; свободные record/preparation переменные также могут поглотить поле.
Нужен faithful off-shell transport
\[
\mathcal E_h/\Gamma_h=A_h^*\mathscr E_{\rm Einstein+matter}+\varepsilon_h,
\]
с actual gain \(\Gamma_h>0\), контролем \(\varepsilon_h\) **после нормировки**
и восстановлением всех relevant residual components через \(A_h^*\).
Количественно: right lift \(A_hR_h=I\) и
\(\|R_h\|\|\varepsilon_h\|\to0\) в объявленном κ-масштабе; затухающий
gain или вырождающийся lift не может скрыть ненулевой residual.
Свободный \(t\), отсутствующий в proved task graph, не вводится искусственно;
его исключение само требует обоснования D.

## C. Что именно склеиваем

Один word → actual fullStep/birth/clock/Golden weights → полная цена →
полный covector → geometric reporter → κ-source. Перенос между разными
исполнениями сохраняет носитель, цену, вариации, gain, норму и историю.
Отождествлять все исторические full128 и geometric конструкции не требуется,
если их неперенесённые предпосылки не используются.

Потребить уже построенные §§7ei–7eo [source owner](A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md)
и [κ soundness/recovery](sources/d0_retained_response_concentration_2026-10-28/KAPPA_CLOSURE_RU.md).
Они действуют для declared H+J/fixed-writer graph; full Cost−Info binding
этим не заменяется. Exact zeros выбранного finite-comparison covector,
κ-zero и exact zeros другого finite Euler — разные утверждения.

## D. Минимальный допуск и все реакции

Из retained primitive/task data обосновать именно используемый READY/report,
ten-sign или source-equivalent task, его clock/cut и независимые inputs.
Исполнимость одного алгоритма не доказывает необходимость его задачи.
Достаточно заявленной семьи; требования одинакового scheduler во всех мирах нет.

Для H.1 отдельно решить статус independent READY, reference \(P_0\),
visibility, seed/frame, scene и clock/layout: либо вывести их generated/guarded
характер из задачи, либо включить реальные Euler rows. Реакция на constraint
не считается свободным Euler equation = 0. Terminal STORE/readout добавляется
только со своим доказанным переносом.

## Критерий результата и текущая остановка

Только совместное выполнение A–D, включая two-way recovery, позволяет
предлагать `SCOPED-NATIVE-KAPPA-EINSTEIN-CLOSED` для независимой приёмки.
Ширина материи, global extension и Lean могут оставаться за пределами
явно заявленного scoped theorem. Старый raw216 contract не ослабляется.

После этого дополнения: **A записан; C существенно построен условно; B и D не сняты**.
Не являются заменой: ещё один critical c, heat balance, spatial Hessian match,
positive-G rename или новый Bloch/circle census.
Ближайший расчёт — [один actual return/record source](A4D_NATIVE_RETURN_RECORD_SOURCE_GATE_2026_11_03.md)
и его остаток после всех независимых внутренних уравнений.
