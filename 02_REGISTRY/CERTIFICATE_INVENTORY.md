# Инвентаризация 26 файлов сертификатов

Снимок `5d632e3c613e9b7ef44aff1a2a3377ec36fe788e`, 26 ноября 2026. В `04_CERTIFICATES` 526 Python-файлов. У приведённых ниже 26 имена с расширением `.py` отсутствуют в `claims.csv` и десяти книгах. Ссылки относительны каталогу `02_REGISTRY`. Скрипты не запускались.

| Файл | Классификация и подтверждение |
|---|---|
| `cert_runtime.py` | Общая библиотека вывода, [output_path](../04_CERTIFICATES/cert_runtime.py#L26), например [импорт](../04_CERTIFICATES/vp_archive_phason_dark_matter.py#L9). |
| `vp_internal_feedback_resolvent.py` | Исполняется [агрегатором feedback](../04_CERTIFICATES/vp_closed_vacuum_feedback_full_wave.py#L14). |
| `vp_feedback_partition_function.py` | Исполняется [агрегатором feedback](../04_CERTIFICATES/vp_closed_vacuum_feedback_full_wave.py#L15). |
| `vp_finite_feedback_equation_of_state.py` | Исполняется [агрегатором feedback](../04_CERTIFICATES/vp_closed_vacuum_feedback_full_wave.py#L16). |
| `vp_terminal_feedback_modes.py` | Исполняется [агрегатором feedback](../04_CERTIFICATES/vp_closed_vacuum_feedback_full_wave.py#L17). |
| `vp_pressure_capacity_balance.py` | Исполняется [агрегатором feedback](../04_CERTIFICATES/vp_closed_vacuum_feedback_full_wave.py#L18). |
| `vp_sde_feedback_reduction.py` | Исполняется [агрегатором feedback](../04_CERTIFICATES/vp_closed_vacuum_feedback_full_wave.py#L19). |
| `vp_quasi_generation_inflation.py` | Исполняется [агрегатором phenomenology](../04_CERTIFICATES/vp_quasicrystal_phenomenology_operator_origin.py#L16). |
| `vp_archive_phason_dark_matter.py` | Исполняется [агрегатором phenomenology](../04_CERTIFICATES/vp_quasicrystal_phenomenology_operator_origin.py#L17). |
| `vp_window_offset_chirality.py` | Исполняется [агрегатором phenomenology](../04_CERTIFICATES/vp_quasicrystal_phenomenology_operator_origin.py#L18). |
| `vp_phason_flip_inertia.py` | Исполняется [агрегатором phenomenology](../04_CERTIFICATES/vp_quasicrystal_phenomenology_operator_origin.py#L19). |
| `vp_window_fractional_charge.py` | Исполняется [агрегатором phenomenology](../04_CERTIFICATES/vp_quasicrystal_phenomenology_operator_origin.py#L20). |
| `vp_desi_bao_sde_real_data.py` | Диагностика рекомендует запуск при наличии данных. [Упоминание](../04_CERTIFICATES/vp_desi_bao_sde_failure_diagnostics.py#L69). |
| `vp_finite_spin2_wave_operator.py` | Публичная совместимая обёртка над конкретной реализацией, используется макроинтерфейсом. [Обёртка](../04_CERTIFICATES/vp_finite_spin2_wave_operator.py) · [потребитель](../04_CERTIFICATES/vp_macro_einstein_interface.py#L67). |
| `vp_external_research_status_guard.py` | Исторический guard требует проверки на актуальных статусах. [Условия](../04_CERTIFICATES/vp_external_research_status_guard.py#L47) · [историческая диагностика FAIL](research/D0_NATIVE_TANGENT_SOURCE_PLAN_2026-10-09.md#L865). |
| `vp_toral_time_markov_conjugacy.py` | Исторический манифест `PROOF-TARGET`, указанный в Lean и frontier. Соответствующий claim теперь `NO-GO`. [Скрипт](../04_CERTIFICATES/vp_toral_time_markov_conjugacy.py#L2) · [Lean](../03_FORMALIZATION/D0/Geometry/LucasVoronoiMarkovPartition.lean#L9) · [frontier](frontier/continuation_frontier.csv#L40) · [claims](claims.csv#L345). Нужна согласованная редактура ссылок и статусов. |
| `vp_archive_car_dirac_square.py` | Внешних потребителей по имени не найдено. Скрипт указывает `ArchiveCARDirac`, связанный с несколькими строками, включая `PROOF-TARGET`. [Источник](../04_CERTIFICATES/vp_archive_car_dirac_square.py#L110) · [строка](claims.csv#L815). |
| `vp_archive_car_permutation_canonicity.py` | Внешних потребителей по имени не найдено. Скрипт указывает `ArchiveCARFockCarrier`, строка имеет `CORE-FORMALIZED`. [Источник](../04_CERTIFICATES/vp_archive_car_permutation_canonicity.py#L88) · [строка](claims.csv#L812). |
| `vp_archive_car_relations.py` | Внешних потребителей по имени не найдено. Скрипт указывает `ArchiveCARRelations`, строка имеет `CORE-FORMALIZED`. [Источник](../04_CERTIFICATES/vp_archive_car_relations.py#L122) · [строка](claims.csv#L813). |
| `vp_archive_hodge_zero_mode_pollution.py` | Внешних потребителей по имени не найдено. Скрипт указывает `ArchiveHodgeDiracZeroModePollutionNoGo`, строка имеет `NO-GO`. [Источник](../04_CERTIFICATES/vp_archive_hodge_zero_mode_pollution.py#L67) · [строка](claims.csv#L808). |
| `vp_archive_pseudoinverse_twist.py` | Внешних потребителей по имени не найдено. Скрипт указывает `ArchivePseudoinverseTwist`, связанный владелец имеет `PROOF-TARGET`. [Источник](../04_CERTIFICATES/vp_archive_pseudoinverse_twist.py#L104) · [строка](claims.csv#L823). |
| `vp_archive_cochain_refinement.py` | Внешних потребителей по имени не найдено. Проверяет конечное уточнение коцепей и отрицательные контроли. [Описание](../04_CERTIFICATES/vp_archive_cochain_refinement.py#L2). |
| `vp_archive_graded_rg_extrinsic_curvature.py` | Внешних потребителей по имени не найдено. Проверяет тождество формы и конечный закон следа. [Описание](../04_CERTIFICATES/vp_archive_graded_rg_extrinsic_curvature.py#L2). |
| `vp_archive_hodge_weight_owner.py` | Внешних потребителей по имени не найдено. Проверяет весовые матрицы и следы. [Описание](../04_CERTIFICATES/vp_archive_hodge_weight_owner.py#L2). |
| `vp_archive_tensor_seam_metric_measure.py` | Внешних потребителей по имени не найдено. Проверяет конечные плотности и компоненты метрики. [Описание](../04_CERTIFICATES/vp_archive_tensor_seam_metric_measure.py#L2). |
| `vp_archive_weighted_hodge_dirac.py` | Внешних потребителей по имени не найдено. Проверяет взвешенный оператор Ходжа и сохранение степеней. [Описание](../04_CERTIFICATES/vp_archive_weighted_hodge_dirac.py#L2). |

Последние десять файлов требуют сравнения конкретных входов, утверждений, отрицательных контролей и области вычисления с предполагаемой записью реестра и её Lean-владельцем. Совпадение названия или модуля недостаточно для привязки. Связь сертификата с `PROOF-TARGET` не меняет статус цели. Для обнаружения дубля нужен эквивалентный проверенный потребитель и проверка исторических ссылок и закреплённых входов.

## Проверка ID и статусов

Regex действующего валидатора нашёл 482 уникальных ID в книгах. Из них 425 находятся только в `claims.csv`, 56 только в `aliases.csv`, один в обоих файлах, неразрешённых нет. Из 58 записей `aliases.csv` у 56 отсутствует каноническая цель, они маркированы как исторические идентификаторы. `D0-ACTION-001`, `D0-CARRIER-001` и `D0-CKM-001` уже входят в эту группу. `D0-3-` в [BOOK_07](../01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md#L1387) входит в термин `D0-3-manifold`.

Единственный `UNPROVED` — `D0-ALBERT-SM-SUBGROUP-REPRESENTATION-OWNER-001`, `PROOF-TARGET`, для точного построения вложения и действия, без зарегистрированной теоремы. [Строка](claims.csv#L827).

Шесть строк имеют `release_status=DEPRECATED`, ещё одна имеет `lean_status=DEPRECATED`, `release_status=EXTERNAL-BACKGROUND`. Три deprecated-записи названы в книгах с исторической квалификацией. [Седенионы](../01_BOOKS/BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md#L1072) · [solid/TC](../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md#L868) · [Gromov–Hausdorff](../01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md#L2099).
