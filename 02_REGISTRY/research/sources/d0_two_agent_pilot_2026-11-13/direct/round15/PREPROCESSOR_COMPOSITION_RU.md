# A15 + B31. Готовность вычисления инструкций одного report

Это компонентная композиция A12/A13/A14/A15 и B31, а не вывод полного
H.1 `alpha_h` или физического Cost−Info. Схема ещё не исполняет SELECT
на source copies и не содержит семи native bank preparations.

Пусть фактически разрешены все заявленные disjoint fresh RAW births,
port/Spin и workspace. Все computational-zero входы выполняются через
owned `G^-1 v=0`, Golden coins являются исходными v, а каждый из прежних
`M=10 248 262` fair wires получает output отдельного B31 cap28 bank.
Это **тот же** fair ресурс A12, без повторного умножения на его вероятность.

Конкретное соединение: output B31 alias-ится с соответствующим входным
fair wire A13, остальные142 logical B31 wires выделяются отдельно и
сохраняются; source port/Spin и arbitrary auxiliary можно разделять между
macros на доказанном A14/B31 all-column интерфейсе. B31 готовит все banks
перед потреблением их outputs; их READY/one-hot/C/B registers больше не
адресуются контроллером. Оставшиеся fair wires для будущих leaf deltas и
postprocessor пока просто сохраняются. A15 выдаёт реальные chronological
stage maps top/internal decoders и всех выбранных переходов.

В идеальной схеме проектирование на совместный fair READY даёт
`|+>^tensor M tensor E`, с нормой² `q28^M`, по B31. Проектор коммутирует
с последующими операциями, потому что они не меняют его READY registers.
Поэтому можно математически сначала условиться на этом checkpoint, не
вводя физического измерения или отбрасывания failure.

Каждый selector с любым palette j имеет одну и ту же готовность tau.
Для семи попыток она равна `r=1-(1-tau)^7`; этот эффект равен `r I` на
входном j и произвольной внешней системе при фиксированном правильном
coin input. Isometry/environment могут зависеть от j — их равенство здесь
не предполагается. Scalar effect и новые независимые coin registers
позволяют последовательно перемножать вероятности даже при когерентном
адаптивном j. В A15 будущий j вычисляется обратимо из retained прошлых
состояний; все455/18 slots, включая dummy, используют свои семь попыток.
READY каждого slot остаётся неизменным до общего projector.

Следовательно для **одного report instruction preprocessor**

```
Q_pre = q28^M * [1-(1-tau_i)^7]^1054 * [1-(1-tau_t)^7]^10.
1-Q_pre <= M*(53/100)^28 +1054*(1-tau_i)^7 +10*(1-tau_t)^7
        < 1/2.
```

Это вероятность (`||Pi U input||²`), не амплитуда. Точный rational upper
bound сохранён в `PREPROCESSOR_READY_COMPOSITION.json`; его десятичное
диагностическое значение около0.3208597503. Независимые семь таких
checkpoints имеют совместную вероятность `Q_pre^7`, **а не Q_pre**.
Нельзя подставлять компонентный результат вместо недоказанного полного
`alpha_h>=1/2` в B29. У полного writer иной набор shared/fresh registers
и готовностей должен быть показан явно.

Для фактических A14 replacements рассматриваем идеальные logical gates
как target. Общий all-column error уже известных семи report частей
(A13 selectors/labels + A15 controller + B31 fair routers) ограничен

```
(92 263 351 768 + 65 981 803 692 + 4 232 532 206) * 2^-4096
 = 162 477 687 666 * 2^-4096 < 2^-4058.
```

Это консервативная сумма; A13 включает ещё postprocessor, пока не нужный
для вычисления инструкций. Она тем более ограничивает один preprocessor.
По изменению вероятности фиксированного projector получаем для него
`Pr_native(READY)>1/2-2^-4057` при указанных admitted input/schedule
условиях. Exact scalar READY и exact fair factorization actual native
слова не утверждаются. Временные residual correlations не обнуляются.

Чистое доказательство component readiness устраняет прежнюю гипотетичность
Boolean/payload части A12. Оно не оплачивает и не удостоверяет целый
физический граф само по себе, не доказывает H.1 exact SAM/D block structure,
не оценивает остальные gates, marks, preparation covectors, Hessian и
clock, и не определяет исходную Info из желаемой статистики.

`GR_closed=false`; следующий потребитель — фактический SELECT на disjoint
source copies и сборка H.1 с реальными исходными состояниями и всеми
marked/clock эффектами.
