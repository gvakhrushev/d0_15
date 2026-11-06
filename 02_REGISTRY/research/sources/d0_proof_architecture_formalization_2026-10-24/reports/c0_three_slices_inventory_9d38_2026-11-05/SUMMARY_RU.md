# Compiled inventory после исправления Book02 — 5 ноября 2026

На чистом `9d386b41c7d3e1ddab0d21b58d49d64a76920a3b` извлечены шесть C0-владельцев из `D0.All` с существующим кэшем. Все 482 декларации по содержанию совпадают с предыдущим inventory; proof details собраны. SHA-256 `declarations.json`: `a23bb1ba6ff7b99afcaf7140106a26267c31da1cb511b1286b4ae46b81fbf841`; digest Lean-источников `14576c364aa1d2e58ce3244c88b6074f8d77bbca8a8cc6eafed4c41a7a6a8f6a`. Семантическое принятие C0 не оценивалось; `GR_closed=false`.

```sh
python3 tools/lean_declaration_inventory.py --module D0.Foundation.FutureExecution --module D0.Foundation.VerificationCore --module D0.Foundation.UncoupledCenterRawWitness --module D0.Foundation.FutureShortlexAdapter --module D0.Foundation.VerifiabilityNecessity --module D0.Foundation.TheoryTransfer --output /tmp/d0-c0-three-slices-inventory-9d386b41c.json
```

На чистом `4fafa9ea90ecb2ddc1dbdb917c229dfff1a1e011` три view содержат 6, 44 и 30 кандидатов без технических замечаний; Book02 явно различает 30 исторических и 30 текущих выдержек, включая 8 пересекающих исправление. Отдельно проверен исторический снимок `b810950c9` с его собственным inventory. Сверка читает compiled metadata и не повторяет Lean; это не semantic acceptance.
