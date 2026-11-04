# Compiled inventory трёх срезов после объединения — 4 ноября 2026

На чистом `0b1e77ad4da31fe7d37d38828bf619aa7c6e8a0c` извлечены шесть владельцев C0 с использованием `D0.All` и существующего кэша. Все 482 записи по содержанию совпадают с предыдущим inventory; proof details собраны. SHA-256 `declarations.json`: `21eaede13c667a50dd877c31dd1e0bf2a5b8e7df402cba4cbae328e9ed24697c`; digest Lean-исходников `7b4ccbefefc6e2d88caba0375d39a47a53a954e2460890e226c2b1c91d3b6f88`. Семантическое принятие C0 не оценивалось; `GR_closed=false`.

```sh
python3 tools/lean_declaration_inventory.py --module D0.Foundation.FutureExecution --module D0.Foundation.VerificationCore --module D0.Foundation.UncoupledCenterRawWitness --module D0.Foundation.FutureShortlexAdapter --module D0.Foundation.VerifiabilityNecessity --module D0.Foundation.TheoryTransfer --output /tmp/d0-c0-three-slices-inventory-0b1e77ad4.json
```

На чистом `cc950a1b333e273944bb731fd48c6a20d3fedc6a` три view содержат 6, 44 и 30 кандидатов, технических замечаний нет. Сверка читает записанные compiled metadata и не повторяет Lean; это не семантическое принятие.
