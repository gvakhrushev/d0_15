# WRK-D0-RESEARCH-REPLAY-REPAIR

Class: `WORKER`
Parent: `CTRL-D0-BOTTOM-UP-GR-SYNTHESIS`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/d0-research-replay-repair`
Primary artifact: `02_REGISTRY/research/D0_EVIDENCE_REPAIR_REVIEW.md`
Execution: `GitHub-first`

## Mission and preserved strategy

Read `D0_START_HERE_RU.md`, the full strategy and idea register under `02_REGISTRY/research/`. This bounded task frees the scientific integrator from replay maintenance without weakening proof standards.

Первый известный сбой — `a4d_native_fock_record_binding_check.py`, `IMMUTABLE_FULL_RECORD_LEDGER_MISMATCH`, SOURCE f0a6a851 и CI run 38707826518, job 116331527810. Проверить, не исправлен ли он новым SOURCE. Старое время/ошибка — указатель, не актуальное заключение.

В изолированном read-only checkout закреплённого SOURCE повторить вычисление без записи в ожидаемую квитанцию. Получить полный fieldwise diff; объяснить каждое различие: математическое, сериализация, зависимость, версия или исторический pin. Сохранить исторические входы. Проверить действительную зависимость последующих сертификатов и предложить минимальный патч с отрицательным контролем; не повышать лимиты и не менять expected ради PASS.

Дополнительно проверить побайтовое восстановление 20 файлов приложенного joint Ward-пакета и повторить его declared entrypoint на нужной upstream-капсуле, если это ещё не принято. Если основная Fock-ошибка требует научного исправления, вернуть точную границу интегратору, а не изменять физическую модель самостоятельно.

Записывать только отчёт, отдельный патч и журналы в выделенном каталоге; исходную #310-ветку меняет назначенный её единственный владелец. Не переносить весь её тысячефайловый diff в новый WORKER PR. Потребитель — проверенная приёмка и G3.

## Inputs and launch gate

Registration must be in main and the single writer assigned before normal execution. Audit base: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`; SOURCE: `f0a6a85111c28f21a18ebf6ad9276eaa713abbd8`; upstream full4D capsule: `9fbc75db0a94707dc3105cdfb3f322a14e62a979`. Fetch exact source commits into separate read-only worktrees when absent from main. Read live PRs first; no duplicate execution or implicit full merge of #310. Record all source/environment pins.

## Why delegated

This is a bounded independently reproducible fieldwise evidence comparison and minimal repair. It removes integration latency from the synthesis bottleneck; it does not select a physical action or certify general relativity.

## Collision fences and non-goals

Write `02_REGISTRY/research/D0_EVIDENCE_REPAIR_REVIEW.md` and `02_REGISTRY/research/sources/d0_evidence_repair/` only, apart from required task lifecycle/generated changes. Submit scientific-source repairs as an explicit patch to that source's owner. No shared Lean-cache edits, overwritten historical receipts, claim/BOOK promotion, CI bypass or self-merge.

## GitHub execution contract

After resolving live PRs and the launch gate, branch from current main, run `python tools/task_lifecycle.py start WRK-D0-RESEARCH-REPLAY-REPAIR` and open a Draft PR before work. Iterate locally with narrow tests; publish a coherent repaired slice. Before Ready run applicable guards, retire this WORKER in the same PR using `python tools/task_lifecycle.py retire WRK-D0-RESEARCH-REPLAY-REPAIR`, update its role as retired with acceptance provenance in the execution overlay under CONTROL coordination, and regenerate views.

## Acceptance and consumer

Localize the complete fieldwise Fock ledger mismatch on the pinned source/CI tree; provide an independently replayed minimal repair or exact unresolved cause, with preserved historical receipts, negative control and explicit downstream consumer.

Run ordinary and optimized checks where applicable. Distinguish source preservation, numerical diagnostics, mathematical replay and independent acceptance. The original Ward receipts are inputs, not a new PASS claim.

## Chat handoff

Return repository, PR/head, the exact mismatch/repair verdict, replay scope, one remaining blocker and the G3/intake consumer. Do not paste large logs or claim that a pin refresh recompiles an old Lean owner.
