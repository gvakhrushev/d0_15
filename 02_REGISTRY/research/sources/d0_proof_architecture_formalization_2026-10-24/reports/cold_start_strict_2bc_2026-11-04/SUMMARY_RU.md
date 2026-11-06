# Полный cold-start: строгая проверка источников — 4 ноября 2026

Чистый снимок `2bc79af4ae8bf4bc493d1f801be9db72c2905227`: обработаны все 414 запросов. Найдены все требуемые источники в **44 из 50** сценариев. Отдельная проверка влияния изменения исходного источника прошла. Шесть сценариев остаются неполными:

- `labelled-native-raising-inverse`: `02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`
- `finite-hermitian-adjoint-twisted-car-application`: `02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_differential_nilpotency_adapter_2026-10-25.json`
- `native-stationary-recording-seed-whole-word-source`: `02_REGISTRY/research/A4D_NATIVE_STATIONARY_RECORDING_SEED_2026_10_28.md`
- `archive-preserving-binary-seed-full-query-source`: `02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md`
- `canonical-af-native16-retained-report-fibre`: `02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/replay_native16.py`
- `pr334-native-af-paid-futures-and-full-price-separation`: `02_REGISTRY/research/sources/d0_pr334_native_af_paid_futures_2026-11-04/owner_task_delta.md`, `02_REGISTRY/research/sources/d0_pr334_native_af_paid_futures_2026-11-04/PROOF_RU.md`

Полный вывод сохранён в `full_replay.json.gz` с проверенной побайтово декомпрессией; `summary.json` сохраняет отдельные receipts всех обязательных источников. SHA-256, точные входы и длительность указаны в `manifest.json`, стадии — в `progress.stderr`. Компактор проверяет структуру и согласованность результата, но не перезапускает поиск и не удостоверяет происхождение переданного файла.

Прежний результат 49/50 относится к другому снимку и прежнему критерию. Этот прогон применяет более строгое требование совпадения самого содержимого; неполные сценарии не объявляются пройденными. Сценарий native-kappa найден полностью. Это проверка обнаружения источников, а не принятие C0 или физическое замыкание; `GR_closed=false`.
