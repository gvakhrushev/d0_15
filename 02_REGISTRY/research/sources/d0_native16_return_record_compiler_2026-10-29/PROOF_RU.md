# Native16: оплаченная компиляция полного return-record

## Родительский переход

Продолжение §7ds в существующем PR [#334](https://github.com/gvakhrushev/d0_15/blob/0f2e421fda2029df92b174c39f594160ce31294f/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md): оно прямо применяет §7dr к существующему compiled native word. Для каждого использованного обычного processing blank `a` выбирается отдельный реально инициализированный, не затронутый старым словом reserve `r(a)`. Преобразование использует только прежний `CX`:

```text
C_R ; W ; C_R,       C_R = product_a CX(a, r(a)),       N_new = N + 2|A|.
```

Оба слоя вызовов оплачены. Входные данные, неизвестные/записанные степени свободы, Spin и неизменный `oldRIGHT` сохраняются. Преобразование проверяет реальную ширину, source frame, gate grammar и резервы существующим native validator; оно отвергает использованные, отсутствующие и неинициализированные reserve wires. Оно не создаёт новый чистый кубит и не доказывает, что физический D0 выбрал эти резервы.

Пусть `i` — исходная инициализирующая изометрия, `P=i i*`, `M_z` — настоящий проектор записи, а `M=M_0`. Тогда на всех допустимых входах:

```text
K_rec = K_original,
E_z   = i* U* Pi_(A=z) U i,     sum_z E_z = I,
E_0   = K* K,
Delta = E_0 - K_rec* K_rec = 0.
```

Это точное операторное равенство для произвольного старого конечного U на объявленном активном носителе, включая его реальные конечные ошибки. Оно не выводится из малого остатка конечного эксперимента. Все старые prefix-состояния сохраняются на сдвинутых часовых позициях; новые такты и их абсолютная цена остаются частью исполнения.

## Полный источник и независимые вариации

Если исходный endpoint — однородная внутренняя reflection, преобразованный endpoint также reflection. Тогда полный источник тепла равен нулю на endpoint unitary-направлениях, а полный INTERNAL `H+J` источник принимает вид

```text
DB[v] = -zeta Tr[((1-zeta)I + zeta K* K)^(-1) D E_0[v]].
```

Равенство `Delta=0` означает, что его производная тоже ноль даже при независимой вариации обоих слоёв copy, прямых/обратных контролей и preparation. Все прежние control rows переносятся тождественно: сохраняются исходные коэффициент, trace, norm, field/apparatus remainders и максимальная stage-норма. Новый copy fault, меняющий саму запись, имеет ненулевой источник и не объявляется task-preserving.

Для исходного endpoint, который не является reflection, return-тождество сохраняется, но полный источник включает настоящий
`D H_(N+2|A|)`. Сопряжение даёт `H_(N+2|A|)(U_rec)=H_(N+2|A|)(U)`, а не `H_N(U)`. Тепловой источник не выбрасывается.

Отдельно доказана upstream-подготовка до первого copy. При отражении и насыщении для любой unitary-вариации `V`, сохраняющей реальный нулевой record-сектор, полный первый источник равен нулю; processing blanks и inverse legs фиксировать не нужно. 18 исходных preparation вызовов не сливаются в фиктивную нулевую операцию: checker использует оплаченный `R_word; R_inverse_word` identity-prefix. Исходные геометрические/body/source-preparations остаются внутри старого `W` и сохраняют собственный источник. Начальные record preparations, rank changes и перемещение record-frame остаются вне этой теоремы.

## Буквальные примеры и hostile controls

Для существующего 31-call запроса используются processing blanks `A=(0,11,12)` и уже имеющиеся неиспользованные RIGHT blanks `R=(7,8,9)`. Получается полное 37-call слово с `25 CX + 2 G + 10 SourceI`, без изменения исходных 16 проводов, ранга и 12 начальных blank wires. Его mirror имеет тот же inventory и все те же восемь операторов retained-record effects, хотя когерентные terminal WORK-состояния различаются. Оба endpoint — reflections с одинаковыми полными heat trace и ценой при `N=37`. Все 1,030,553,600 Hodge modes сохранены; абсолютная цена около `27.05459937490956`.

Направление на позднем `CX(11,8)`, меняющее настоящий retained law, имеет ненулевой источник около `3.50030650432416e-6`. Оно сохраняет видимую старую запись, если разряд записи опустить, но это не task-preserving направление полного joint effect. Это проверяет, что pullback включает новые управляющие строки, а не зануляет их по конструкции.

Добавление перед тем же 37-call словом оплаченного 18-call identity даёт 55-call исполнение; все 18 upstream-preparation rows отдельно равны нулю. Альтернатива того же 55-call inventory, `R_word; R_word; SourceI^4`, сохраняет те же retained effects и exact heat, но повышает полную цену на
`8 log[(1-zeta+zeta c^2)/(1-zeta+zeta c^4)] ≈ 4.01477956345875e-7`.
Это точное сравнение двух конкретных оплаченных исполнений при одинаковой задаче. Оно не доказывает общий минимум по всем словам или физический выбор автономным контроллером.

Однослойный 34-call вариант с тем же return corner не является полной reflection; его heat-source нельзя объявить нулём. Неполное копирование, пропускающее query wire, оставляет `Delta=(1-c^2)Q_return>0`, а task-preserving rotation и upstream row в этом контроле ненулевые. Эти отрицательные контроли сохраняются в точном checker, а не заменяются положительным результатом.

## Повтор и границы

В [replay intake](source_manifest.json) сохранены точный фрагмент §7ds, неизменённый embedded checker и его receipt. Минимальный checker fixture включает точный §7cq source slice, предыдущий §7dr receipt и неизменённый §7do heat receipt. Он не подменяет полный owner memo. [replay_return_record.py](replay_return_record.py) повторяет ordinary, `-O` и обычный запуск; Python 3.9.6, SymPy 1.14.0 и mpmath 1.3.0 дают побайтно одинаковый published receipt с 279 checks, SHA-256 `5ca575b88ade09944cdd6af7b1a013620ed7caa6e9ca2628f1773941d8e9f19e`, без stderr. Результат и все stdout/stderr сохранены в `replay/` и `replay_manifest.json`.

§7ds закрывает конкретное применение §7dr для объявленного binary compiler и двух same-boundary исполнений. Для большего field compiler ещё надо инстанцировать его настоящий reserve map, ширину и новый clock. Физические admission/task/initial-record supply и valuation, полный Book03 `Cost-Info`, независимые clock/boundary уравнения и common all42 matter refinement остаются открыты. Нового GR root, Lean/CI replay, assembly acceptance или физического выбора не доказано; `GR_closed=false`.

Upstream commit `0f2e421fda2029df92b174c39f594160ce31294f`: [owner memo](https://github.com/gvakhrushev/d0_15/blob/0f2e421fda2029df92b174c39f594160ce31294f/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md), blob `c1417beeb828773482bda67b6e9db146a5ce04d9`, SHA-256 `37846d696a8da22baa02029f1043ccd5db873612d5c145bf6a4c09c000a23c82`; [task brief](https://github.com/gvakhrushev/d0_15/blob/0f2e421fda2029df92b174c39f594160ce31294f/00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md), blob `2b10f402167e7c14c77db51887bff43419c506d7`.

Pinned execution inputs: [native execution domain](https://github.com/gvakhrushev/d0_15/blob/0f2e421fda2029df92b174c39f594160ce31294f/02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py), SHA-256 `222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c`; [apparatus cotangent descent](https://github.com/gvakhrushev/d0_15/blob/0f2e421fda2029df92b174c39f594160ce31294f/02_REGISTRY/research/sources/d0_apparatus_cotangent_descent_2026-10-28/PROOF_RU.md), SHA-256 `1db9ebd3d24b57a45b1a3a00a2c2553c2e08019cecc34d18e2e2a94d19b45254`; [task-faithful source](https://github.com/gvakhrushev/d0_15/blob/0f2e421fda2029df92b174c39f594160ce31294f/02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md), SHA-256 `9f2354817860f9024a597dba4bd14c0580cc021de5c473925740b46b0e8f96e5`; [clock winding source](https://github.com/gvakhrushev/d0_15/blob/0f2e421fda2029df92b174c39f594160ce31294f/02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md), SHA-256 `ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418`.
