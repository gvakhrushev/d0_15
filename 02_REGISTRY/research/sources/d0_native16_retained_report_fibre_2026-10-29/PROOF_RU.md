# Native16: полный источник связанного с записью исполнения

## Точная формулировка результата

Результат §7dr PR [#334](https://github.com/gvakhrushev/d0_15/blob/4b30fcb4dc743e7a04415c9701aae19a847e8dab/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#7dr): для одного буквального исполнения из исходных положительных примитивов `G`, `CX` и `SourceI` полный фиксированный внутренний источник `H+J` сводится к производной фактически читаемого совместного эффекта записи. Это конструктивно закрывает независимую return-source преграду **для указанного исполнения и его полного эффекта**.

Слово

```text
W_* = S_word ; CX(11,10) ; Z_word ; G(11) ; CX(11,10)
```

содержит ровно `1 G + 9 CX + 6 SourceI = 16` оплаченных вызовов. В исходном 16-проводном разрезе провод 10 — новая запись, провод 12 — сохранённая копия исходного seed, а `oldRIGHT` на проводе 15 остаётся неизменным. Никакие входные разряды не стираются и ни один обратный ход не заменяется внешним наблюдателем.

Полный конец слова — инволюция. На всех 16 фактических входных столбцах полный конечный WORK-изометрический оператор совпадает с 27-вызовным нижним контролем. Совпадение конца не отождествляет 16- и 27-шаговые часы или промежуточные истории.

Для реально читаемого совместного события

```text
M = (record10 = 0) AND (seed-copy12 = 0)
P <= M
E_M = i* U* M U i
K   = i* U i
Delta = E_M - K* K = L* L >= 0
```

проверенный native16 даёт `E_M = p Q_return = K* K`, поэтому `L = 0` и `D Delta = 0` на каждом конечном unitary-направлении — до выбора физического касательного пространства. Полный источник тепловой части на таком направлении тоже равен нулю; следовательно весь внутренний `H+J` источник совпадает с pullback производной совместного эффекта `E_M`. Тождество переносится через суффиксы на все 16 отдельных вхождений примитивов; механически связывать прямые и обратные шаги не требуется.

Это не означает, что источник исчезает на произвольном управлении. Для неограниченной вариации фактическое `G`-вхождение на шаге 15 даёт ненулевой источник около `7.41376417151667e-6`. Исполнение достигает точной нижней границы return-цены при фиксированном `E_M`; глобальный минимум полной `H+J` цены не доказан. Для объявленного семейства `E_M=(1-x)Q_return` проверен положительный коэффициент источника с отношением около `1.05901642646979` в указанной точке.

## Проверка и точные входы

Побайтно сохранены источник §7dr, embedded checker и published receipt. Исходные receipts §7dq/§7do сохранены в `inputs/upstream_receipts.md` как точные минимальные входы неизменённого checker; это не копия и не замена полного owner memo. Полная provenance и четыре входных proof-файла перечислены в [source_manifest.json](source_manifest.json).

Точные входные proof-файлы на upstream head `4b30fcb4dc743e7a04415c9701aae19a847e8dab`:

- [task-faithful source](https://github.com/gvakhrushev/d0_15/blob/4b30fcb4dc743e7a04415c9701aae19a847e8dab/02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md), SHA-256 `9f2354817860f9024a597dba4bd14c0580cc021de5c473925740b46b0e8f96e5`.
- [apparatus cotangent descent](https://github.com/gvakhrushev/d0_15/blob/4b30fcb4dc743e7a04415c9701aae19a847e8dab/02_REGISTRY/research/sources/d0_apparatus_cotangent_descent_2026-10-28/PROOF_RU.md), SHA-256 `1db9ebd3d24b57a45b1a3a00a2c2553c2e08019cecc34d18e2e2a94d19b45254`.
- [canonical stationary family](https://github.com/gvakhrushev/d0_15/blob/4b30fcb4dc743e7a04415c9701aae19a847e8dab/02_REGISTRY/research/sources/d0_canonical_stationary_family_2026-10-28/PROOF_RU.md), SHA-256 `fe4b8e9033098ced52299fbc0481ab2ddecceed69c6f4392988803ab0abfa005`.
- [clock winding source](https://github.com/gvakhrushev/d0_15/blob/4b30fcb4dc743e7a04415c9701aae19a847e8dab/02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md), SHA-256 `ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418`.

The current owner remains the existing [#334 task brief](https://github.com/gvakhrushev/d0_15/blob/4b30fcb4dc743e7a04415c9701aae19a847e8dab/00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md), blob `34aefcfc6a136b110b605e9ced458ec524b9204a`.

Checker [check_native16.py](check_native16.py) запущен из изолированной replay-копии входов в Python 3.9.6, SymPy 1.14.0, mpmath 1.3.0. Обычный запуск, `-O` и повтор дали байт-в-байт один published receipt: 288 проверок, SHA-256 `c20bd62754ffaa4fb89a8ae16ab4b3f18c1c04f38112bcaa0e2e550058da3558`; stderr во всех случаях пуст. [replay_native16.py](replay_native16.py) воспроизводит эти запуски, а [replay_manifest.json](replay_manifest.json) и сохранённые stdout/stderr фиксируют результат.

## Оставшиеся обязательства

Это supporting result той же задачи #334, без новой задачи, assembly-узла, носителя или физического постулата. Он не доказывает физический `X_N` и admission этих вариаций; автономный выбор контроллера или задачи; обязательную полную связку Book03 `Cost-Info`; независимые граничные и часовые уравнения; отображение на все 42 уравнения и refinement. Следующее применение — вывести настоящие `P,M,K,Delta` и `D Delta` для уже существующего field/report compiler, сохранить upstream rows и перенести фактические trace, gain, norm и heat/selected-price члены к all42 источнику.

Lean, CI и GR-closure этим результатом не заявляются. `GR_closed=false`.
