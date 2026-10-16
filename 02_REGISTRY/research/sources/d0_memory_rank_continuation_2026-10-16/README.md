# Источник памяти и нелинейный отбор геометрии

[Доказательство](../../A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md).
Продолжение уже опубликованного [memory-source owner](../../A4D_NATIVE_MEMORY_SOURCE_FIBRE.md),
не повтор стационарного слоя или полевого fullrank kernel.

Новые результаты: точная support function трёх полных источников; явная pure-state
обратная на эллипсоиде с golden margin p^6 для всей известной history-пробы;
rank-aware source tangent (1983 вместо16383 целевых shell-компонент при k=8);
полная second-order matter compatibility; дополнительное необходимое nonlinear
условие от стационарных вариаций самой памяти.

На faithful internal fibre кандидат скорости v обязан удовлетворять
`M_v in span_R{I,B1,B2,B3}`. На pure-memory конце условие имеет вид
`M_v chi=lambda chi+sum beta_r B_r chi`, с реальными multiplier coefficients.
Это разные ранговые условия. Ни полевая zero eigenvalue, ни малая scalar
Hessian не заменяет их. Для смешанных Fourier velocities сохраняются полные
bilinear terms; здесь отдельно разобран field-only q/−q сектор.

```sh
python 02_REGISTRY/research/certificates/a4d_memory_rank_continuation_check.py
python -O 02_REGISTRY/research/certificates/a4d_memory_rank_continuation_check.py
python 02_REGISTRY/research/sources/d0_memory_rank_continuation_2026-10-16/test_mutations.py
```

Точный checker исполняет только новые проверки, потребляя неизменённые actual
CAR definitions предыдущего пакета по SHA256. Он не запускает старые171 tests,
старыеroot solvers, весь65536-dimensional operator или Lean.

`diagnostic_memory_fibre.py` — отдельная полная4096-momentum floating разведка.
Её apparent crossing около0.43036 НЕ является native root certificate;
непренебрежимый memory-fibre residual записан в DIAGNOSTIC_FLOW.json. Числа
не используются точным checker. Запуск диагностики требует NumPy/SciPy;
точный пакет — только Python/SymPy. Ни один скрипт не скачивает внешние данные.

Не доказаны: физический закон приготовления inverse-source состояний,
конвергентная curved native branch, full programme admission из M1,
Einstein/refinement terminal. Исходная v8-цена не меняется. Свежие fullrank
shell/q0 результаты другого исполнителя на b1283e96 потреблены как текущий
контекст, не переобъявлены результатом этого пакета.
