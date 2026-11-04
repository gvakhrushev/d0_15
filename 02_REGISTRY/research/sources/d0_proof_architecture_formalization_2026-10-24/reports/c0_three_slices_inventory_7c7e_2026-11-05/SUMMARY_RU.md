# Compiled inventory после композиции полевого среднего — 5 ноября 2026

На чистом `7c7e05b5534c0adeab2fd4e334f92af13fb4a353` извлечены шесть C0-владельцев из `D0.All` с существующим кэшем. Все 482 декларации по содержанию совпадают с предыдущим inventory; proof details собраны. SHA-256 `declarations.json`: `332f830274370c428394ff804fc39cc256ffa31444863ae84f53f508c92419ae`; digest Lean-источников `46a97721b0b0365db9fc1886e392b04c79ebedc8b05c4637b848241ffae34453`. Семантическое принятие C0 не оценивалось; `GR_closed=false`.

```sh
python3 tools/lean_declaration_inventory.py --module D0.Foundation.FutureExecution --module D0.Foundation.VerificationCore --module D0.Foundation.UncoupledCenterRawWitness --module D0.Foundation.FutureShortlexAdapter --module D0.Foundation.VerifiabilityNecessity --module D0.Foundation.TheoryTransfer --output /tmp/d0-c0-three-slices-inventory-7c7e05b55.json
```
