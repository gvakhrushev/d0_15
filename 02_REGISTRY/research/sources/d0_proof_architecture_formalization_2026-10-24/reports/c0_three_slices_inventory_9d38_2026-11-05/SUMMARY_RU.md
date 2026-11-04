# Compiled inventory после исправления Book02 — 5 ноября 2026

На чистом `9d386b41c7d3e1ddab0d21b58d49d64a76920a3b` извлечены шесть C0-владельцев из `D0.All` с существующим кэшем. Все 482 декларации по содержанию совпадают с предыдущим inventory; proof details собраны. SHA-256 `declarations.json`: `a23bb1ba6ff7b99afcaf7140106a26267c31da1cb511b1286b4ae46b81fbf841`; digest Lean-источников `14576c364aa1d2e58ce3244c88b6074f8d77bbca8a8cc6eafed4c41a7a6a8f6a`. Семантическое принятие C0 не оценивалось; `GR_closed=false`.

```sh
python3 tools/lean_declaration_inventory.py --module D0.Foundation.FutureExecution --module D0.Foundation.VerificationCore --module D0.Foundation.UncoupledCenterRawWitness --module D0.Foundation.FutureShortlexAdapter --module D0.Foundation.VerifiabilityNecessity --module D0.Foundation.TheoryTransfer --output /tmp/d0-c0-three-slices-inventory-9d386b41c.json
```
