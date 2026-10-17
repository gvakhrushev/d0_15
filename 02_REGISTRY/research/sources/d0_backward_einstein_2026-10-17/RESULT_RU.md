# Обратная сборка: результат ограниченной проверки

17 октября 2026. Продолжение существующего Draft #334.
Научный срез: `3f368179627acc9f2c3e9616df729ac2280a77a0`.
Потребитель: [A4D_BACKWARD_EINSTEIN_SOURCE_COMPLETION.md](../../A4D_BACKWARD_EINSTEIN_SOURCE_COMPLETION.md).

## Математический результат

Полный центральный output существующего signed-loop compiler допускает
точную classical KL chain rule. Поэтому fixed complete block-preserving
pointer передаёт тот же геометрический covector `lambda a dQ`, что quantum
terminal relative price, без universal quantum-gain saturation.

Действительный pointer optimum равен
`6-log(sum_j d_j mu_j exp(-ell f_j))/ell`; на полном AF density space
его minimizing preparations образуют непустой компактный выпуклый слой
фиксированных measured masses. Все его состояния имеют один первый
источник. Для буквального pointer при нетривиальном kernel измерения
они могут иметь разные coherences и ranks. Native reachability и
посторонние реальные цены не предполагаются доказанными.

Девять рациональных null shears и масштаб полного coframe дают явный
inverse всех десяти symmetric metric rows. В internal-frame packed10 raw-l1 norm его
null coefficient равен `5/2`, trace coefficient `1`; при full16 упаковке
они равны `17/4` и `1`. Перенос в исходную coordinate/packed norm включает
явную bounded константу смены frame `C_T`, memo(29a). Один общий cell sum
и исходный `h^-2` сохраняются.
Fixed-mass density dressing — точная инволюция; поэтому local scale
полного geometric chart доступен без изменения нормированной массы.
Ограниченный stored-native admissible chart этой алгеброй не расширяется.

## Выполненные проверки

`check_null_source_basis.py` использует только точные рациональные
матрицы. Проверены обе стороны явного inverse, null kernel `span(eta)`,
column norms, точные конечные metric/inverse/determinant identities на
недиагональном coframe, density involution и fixed-mass scale. Контроли
отвергают удаление trace, неверный trace-sign и ненормированный probe;
отдельно сохраняют невидимый global multiplier нормированных mass-only
вариаций. Обычный Python и `python -O` дали успешный одинаковый вывод
в `RESULTS.txt`.

`check_central_pointer.py` использует Fraction и точные линейные формы
логарифмов рациональных чисел. В одном согласованном положительном
fixture полные conditional KL prices равны `log(5/4)` и `log(5/3)`;
их tilt равен `4/5,3/5`, нормализатор `2/3`. Проверены chain rule,
Gibbs remainder, все normalized pointer tangents, actual amplitude
normalizer, различные PSD ranks на одном fibre и полный flag source
непосредственно из probability jets. Moving central reference даёт
ненулевой source `-1/100`; удаление flag и замораживание normalizer
меняют настоящий source. Обычный Python и `python -O` дали побайтно
одинаковый успешный вывод в `POINTER_RESULTS.txt`.

Rational pointer fixture проверяет общую алгебру, доказанную в memo;
он не заменяет полный AF/golden прибор. Существующие golden bounds
`2/5<a<5/2` и полный signed-loop compiler потребляются с указанным
исходным срезом без повторного запуска. Проверки не зависят от `assert`.

## Воспроизведение

Из корня репозитория:

```bash
python 02_REGISTRY/research/sources/d0_backward_einstein_2026-10-17/check_null_source_basis.py
python 02_REGISTRY/research/sources/d0_backward_einstein_2026-10-17/check_central_pointer.py
```

Оба скрипта только печатают результат и не меняют файлы. Их источники,
memo и stdout фиксируются одним Git commit; provenance.json содержит
локальные SHA256 каждого deliverable до добавления этой provenance.

## Граница потребления

Доказаны конечные композиционные тождества и полный variation-basis.
Не доказано физическое отождествление terminal relative price с
SAME-history `(H-log N_raw)/ell`, primitive admission центрального
ориентированного сумматора, доступность нужного preparation fibre или
исходный joint-critical refinement относительно #216. Никакая из этих
предпосылок не заменена тестовым fixture.

Следующий source-потребитель имеет вид
`dA_native=lambda_h a_h dcalQ_h+r_h` на действительном retained stationary
correspondence, с одним общим multiplier геометрии и независимо
определённого matter/source. Для приближённого splice нужен
`||r_h||=o(lambda_h h^2)` в исходной норме. Этот контроль относится к
equation residual; отдельный designated comparator residual сохраняется
в точном разложении memo(37a). Это конкретное соединение
существующих объектов; все более сильные требования, снятые memo,
можно исключить из его предварительных задач.

Старые научные suites, spectrum/rank census и Lean не исполнялись.
Repository-wide Ready gates не исполнялись: execution остаётся Draft,
исходный terminal и lifecycle не меняются. Независимые математические
проверки сосредоточены на новых source/composition утверждениях.
