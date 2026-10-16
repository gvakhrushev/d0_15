# Вторая волна поддержки главного синтеза

[Общий план и десять поручений](../../D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md).
Сначала [N01 CONTROL](CONTROL_WAVE2_INTAKE.md), затем девять обычных WORKER briefs.

SOURCE: `74e62cdc716e10883accba9d34ccf0e21d58eb65`. Main при подготовке: `add17919b344f0e46115619aa53d2173ecdcf219`.
Тексты опубликованы для прямого чтения в GitHub, без ZIP и истории чата.
Регистрация в main и запуск не выполнены созданием файлов. #331 сохраняет
свой старый task; завершённые задачи #325–333 не дублируются.

`register_wave2.py` переиспользует неизменённую транзакцию первой волны
по Git blob `d64442f2a5ecbf2da19a1e9f29312a267d9d7668`.
Её path, parent/claim checks, rollback, actual renderer/validators и защита
от воскрешения retired briefs сохранены. Рабочий flow не заменяется.

Новый предел физической теории, Lean proof или научная приёмка в этом
пакете не заявлены. Ведущий сохраняет собственный hardest synthesis;
medium-агенты поставляют конкретные проверяемые входы.

## Проверка поручений и адаптера

```sh
python 02_REGISTRY/research/sources/d0_medium_wave2_2026-10-16/test_wave2.py
python -O 02_REGISTRY/research/sources/d0_medium_wave2_2026-10-16/test_wave2.py
```

14 структурных tests проверяют подготовку девяти новых строк, сохранение
чужих состояний и лимитов, отсутствие пересечений, idempotence и fail-closed
проверку старого helper до импорта. Они не исполняют реальный --apply,
не запускают repository validators или агентов. См. VALIDATION.json.
