Полная Shannon-цена golden exterior readout

RESULT_RU.md и check_exterior_mean_source.py — исходные материалы. Они сохранены без изменений. RESULT.json — точный receipt; его checksum и pinned-owner hashes находятся в самом JSON.

Результат выводит первый source полной occupation-энтропии для существующего golden прибора. В полной проверке сохранены все шесть occupation исходов минимального fixture N=4,d=2, включая исходы с нулевой базовой вероятностью. Точный checker содержит 25 контролей; запуск в обычном и -O режимах даёт идентичные receipts.

Интеграция и границы применения: ../../A4D_EXTERIOR_MEAN_ENTROPY_SOURCE_2026_10_19.md. Это отдельный detector/readout consumer. Он не переопределяет двухтактовую feedback-цену J2, не выбирает физическую цену D0, не подтверждает native admission или Ward identity и не закрывает ОТО.

Отдельный hostile control check_exterior_basis_ambiguity.py сохраняет тот же good compression, но точно меняет распределение и first source поворотом Hadamard внутри failure-пространства; receipt — BASIS_COMPLETION_CONTROL.json. Это показывает, почему фиксированный polar basis нельзя вывести из одного feedback compression. Проверка не утверждает, что обе компоновки native-допустимы.
