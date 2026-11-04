# Book01 и явный бюджет ошибки return-контраста

Продолжение цели #401 в существующем Draft PR #402. Это два связанных
инженерных результата: проверяемая классификация уже доказанного ядра
Book01 и конкретное применение доказанной оценки return-контраста.
C0 целиком не принят; цель остаётся в работе, GR_closed=false.

## Book01: источник, декларации и повторное использование

В primary artifact добавлены 44 кандидата §01.1.8, с собственными
утверждениями, предпосылками, диапазонами исходных байтов и типами Lean.
Текст книги взят из commit a4d0d3919e9c2b8e9f27aeaacaafd6dcf06e6c38,
blob eb2d8ea779189084cdaaca717326df88589ec918; section [14123,18478), SHA-256
bd468ba86fc3eb70004871d2bb5777c40afbfb7f92394d33c52b46759692ea9f.

Проверка использует фактического владельца каждой декларации:
VerificationCore, FutureExecution либо VerifiabilityNecessity. Пространство
имён EmpiricalTheoryFactorization не подменяет source module. Общий парсер
получил schema 2 с обязательным module; прежний Book02 schema 1 и pilot
сохранены. Текст и классификация остаются в primary, Python хранит pins.

Общий механизм теперь проверяет несколько владельцев, точный collector
hash и наличие полных proof/type dependencies. Отрицательные проверки
отвергают перестановку даже двух разрешённых владельцев, изменение второго
owner blob, пропуск декларации, подмену книжного блока и неполные proof
metadata. Book01 требует чистый tracked inventory; прежний неполный
historical crosswalk за него не выдаётся.

Независимый разбор проверил весь фрагмент, список кандидатов и реальные предпосылки.
Повторы displayed/named record/run equations посчитаны один раз;
служебные определения и bundled summaries не создают новых результатов.
Связь с Book02 — явная композиция существующего quotient bridge и
representedRun_state. Это различные выводы при повторном использовании
одного входного результата. E и SigmaWitness остаются заданными;
компьютерные операции над кодами не означают вычислимого encoder
произвольного raw-state. Состав и семантика глобального C0 не приняты.

## Конечный бюджет ошибки

Источник — существующий §5 после (12) в
02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md,
commit fd35893d77e4aa5f819bafa0c6428c8e7a8f1812,
blob c99e90a8c8e96bae70e700fa88d1c2d824a1831b.

ReturnTemplateErrorBudget доказывает η≤2Md, экспоненциальную оценку и
точный предел 4exp(θ+2)d/(|t|λ). TaskFaithfulReturnTemplateBudget применяет
его к двум фактическим return-произведениям с одним K и точным baseline
gain. При M>0, d<1/2 и d≤min[1/(2M),e|t|λ/(4exp(θ+2))] ошибка
нормированного return-контраста не превосходит e. Готовая ошибка цены
не является предпосылкой. Λ=Mλ, реальное число блоков, ненулевой t и
положительные λ/gain сохранены явно. λ — заданный масштаб нормировки;
его физическое происхождение здесь не выводится. Нулевой допуск допустим
при нулевой ошибке. Тепло, независимые preparation/work/clock и
измерительные ошибки остаются отдельными слагаемыми.

## Проверки

Narrow обоих новых модулей прошли, независимый математический разбор
не обнаружил дефектов. Полная локальная D0.All прошла: 4788 Lake jobs.
Source digest: 97b499af27d62fb54eaf1c9e0d9274a471f4ce74371533d5a58198e3b1f9954e.
Точный receipt и полный журнал находятся в build_receipt.json и build.log.gz.
Предупреждения старых модулей сохранены; новые модули их не добавили.
[Чистый инвентарь](declarations.json) собран через публичный D0.All на
implementation commit `c25c66780fa4d9adec99996d512645243bc5ba72`,
worktree_dirty=false. Source digest совпадает с общей сборкой. Он содержит
535 записей: 521 запись прежних foundation/transfer-модулей и 14 записей
новых бюджетных модулей, включая 7 вспомогательных generated theorems.
Семь новых именованных теорем и их вспомогательные доказательства имеют
только стандартные Classical.choice, Quot.sound, propext.
Типы и владельцы всех 44+30 книжных кандидатов повторно сверены без
расхождений. Это число записей, не процент покрытия или C0 acceptance.
Обе read-only сверки на snapshot `aa878117bc00b7bcd9b7f8cf27815889f89d51ea`
прошли без issues: [Book01 — 44](book01_view.json), [Book02 — 30](book02_view.json).
[validation.json](validation.json) фиксирует область, исправление checker и хеши.
Полный тестовый вывод сохранён в [tool_tests.log](tool_tests.log). Ни один такой view сам не запускает Lean
и не принимает научные приложения или глобальный состав C0.

Исправление, найденное реальной сверкой: collector_sha256 удостоверяет
сгенерированный Collect.lean, а не Python-файл генератора. Проверка теперь
отдельно удостоверяет неизменность Python-генератора и воспроизводит точный
Lean-текст с теми же параметрами, без запуска Lake. Новая чистая выгрузка
после этого изменения имеет те же 535 деклараций. Отдельные регрессии
проверяют эту разницу, режим без proof details и неполный запрос владельцев.
Полный связанный набор tooling tests прошёл: 119 тестов.

## Повторение

На указанном implementation/report snapshot, с той же версией генератора:

```bash
python3 tools/c0_reconciliation.py --repo . \
  --snapshot aa878117bc00b7bcd9b7f8cf27815889f89d51ea \
  --kernel-sections --kernel-book book01 \
  --kernel-inventory 02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/reports/book01_template_budget_2026-11-04/declarations.json \
  --kernel-inventory-sha256 581fa2a994be99c6e596d4b27f8fc10a5ce0add6e6929043aded31b130a53eb2
```

Для второго фрагмента заменяется только `--kernel-book book01` на `book02`.
Для сборки: `python3 tools/lean_task_build.py narrow D0.Research.TaskFaithfulReturnTemplateBudget`,
затем `python3 tools/lean_task_build.py final`. Для полного выбранного набора
tooling tests используется команда из validation.json. Инвентарь повторяется
с семью `--module`, перечисленными в его `requested_modules`; он должен
извлекаться на чистой совместимой рабочей копии. Старый успешный receipt
не удостоверяет изменённые источники или другую версию генератора.
