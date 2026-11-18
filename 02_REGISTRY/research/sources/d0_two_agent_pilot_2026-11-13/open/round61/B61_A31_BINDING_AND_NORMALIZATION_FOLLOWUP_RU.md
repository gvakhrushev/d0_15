# B61 follow-up. Проверка A31 и точная нормировка H.4

Независимо сверены **все 2688** записей A31 с B25 chart и исходной A11 mark table, а также все **4096** entries 256 link-blocks: именно `J[2^i,2^j]` на f Choi slot 392, coframe на том же slot, `Psi` на q CAR slot 1342, в правильных little-endian физических DATA wires. Векторное считывание сохраняет исходный знак `eta_null log(U U0^-1)` и не вводит factor 2 сверх исходного Choi link multiplier. [Проверка](audit_a31_binding_and_bias.py), [результат](A31_BINDING_BIAS_NORM_INDEPENDENT.json).

Рационально подтверждены `||J−I||<2^-23`, decoded mean-centre сдвиг `<2^-48`, Neumann truncation examples, исходный raw physical lift `<55/s` и coframe conversion factor `<20/3`. Поэтому для принятой Frobenius нормы `(e,theta,Psi)` достаточно `<(1100/3)/s`. При отдельных условиях A30 `e_B<2^-3231`, `g s>2^-3158` нормированный **native-only** T10 residual меньше `2^-37` для raw chart и `2^-34` с этим дополнительным coframe factor. Это не сумма остальных ошибок и не выполненный reader.

Важно различать две нормировки. Для corrected **физического mean-readout** lift из B61

\[
X(v)=(us)^{-1}\sum_j(J^{-1}v)_jJ_j,
\quad L_\rho X(v)=s^{-1}J^{-1}v.
\]

Следовательно исходная H.4 нормировка `Gamma_s=4wgs/c` даёт ведущую строку `s^-1 DI_tau(Y0)[J^-1 v]`, а не непосредственно `DI_tau[v]`. Для unit physical comparison используется `Gamma_s/s=4wg/c`, и весь соответствующий нормированный residual также умножается на `s`. Оставшиеся разности включают `J^-1−I`, shift `<2^-48` с настоящими bounds на производные, source/Taylor и `E_tau`, а также heat, old-prefix, finite-comparison и independent F/B rows. Никаких их исчезновений или полной исходной цены эти оценки не доказывают.

Actual giant mean/J matrix, physical source reader, соответствующее исполнение endpoint preparation и полный Book03 source остаются открытыми. `physical_C_closed=false`; `GR_closed=false`.
