# A20. Конкретный native SELECT исходных coframe Julia-блоков

Потребляется точное полноколоночное разложение A19/B40. Вместо нового
geometric target строятся реальные вращения для исходного `C=a†(u)`
B25. Каждый native gate по-прежнему G, CX или SourceI. Никакой новый
phase oracle, угол как бесплатная примитива или физический Info не добавлен.
Полный Choi loader и физическая Cost−Info этим этапом ещё не закрыты.

## Точные исходные семейства

Каталог исходных coframe sectors семи bank имеет 14848 записей:
по 4864 для f/q, по 1024 для остальных пяти. Аналитические формулы дают
247 source specs: 127 current и 120 reference. Дедупликация основана
на точном site/column/PF-count/local-bit имени формулы. Float64 не
используется для слияния физических target states или их сертификации.

Для current с `x2,x3` — целочисленными координатами:

`H=k0*pi²*(x2²+x3²)/40000 + 3*(x2²−x3²)/1600`.

Столбцы исходного coframe соответственно `(0,nu,0,0)`,
`(nu,−nu*H/2,0,0)`, `(0,0,nu,0)`, `(0,0,0,nu)`, `nu=3/5`.
На свободном site каждая компонента получает именно
`2^-30*(b−p²)`. Для остальных столбцов зависимость от x2/x3 отсутствует
алгебраически. Y0 и all-zero SAM различаются и не отождествляются.

Для reference `rho=256*N_x/10946` и coframe равен
`sqrt(rho)/10 * T*diag(1,−1,−1,−1)`. Равенство PF counts позволяет
переиспользовать угол, но не отождествляет исполняемые bank/address calls.
Все 14848 sectors остаются в paid word.

Все числа вычисляются outward dyadic intervals на 7168 битах. p, k0
выводятся из исходной Golden формулы; pi — из Machin series с остатком.
Для каждого source spec строго проверены `0<n<1`, где `n=||u||`, и
радиусы выбранного alignment порядка `radius>=n/2`. Выбор первого
направления закреплён типом столбца и проверяется интервалами; float
argmax не является основанием утверждения. Identity mode rotation
пропускается только при **точно нулевой** исключаемой компоненте и
положительной первой компоненте. Остальные сколь угодно малые повороты
сохраняются.

## Конкретные степени G

Для нужных pair rotations определены целевые cos/sin с учётом
фермионного parity и ориентации computational-basis pair. У всех Fock
пар и base pair исходный pivot bit=1, поэтому native sine равен
отрицанию желаемой pair sine. Для base target sine=−n, native sine=+n.

Для каждого неэквивалентного enclosure выбрано реальное положительное
целое k и сертифицирована степень `G^(2^20 k)`. Поиск k использует
численную continued-fraction сетку, но не доказывает точность. Доказательство
каждого угла — целочисленные outward bounds target и native power.

Native powering использует комплексный диск: если две точные степени
имеют модуль 1, а центры имеют ошибки r/R, ошибка произведения центров
не больше `r+R+rR`. Два целочисленных округления добавляют меньше
`2/2^precision`. Исходный диск содержит `sqrt(p)+ip`, чей модуль точно 1
по `p²+p=1`. Индукция двоичного powering даёт содержащий диск для
каждого огромного exponent; его проекции дают bounds cos/sin. Сумма
покоординатных разностей с target intervals ограничивает полную
операторную норму разности rotations. Для каждого macro требуется
ошибка не больше `delta=2^-3264`.

Контролируемый X на Julia flag использует одну и ту же k для native
углов `2^20 k theta≈pi/2` и `2^21 k theta≈pi`. Вторая степень проверяется
отдельно, и **сумма** двух ошибок ограничена delta. Сначала aux-rotation
при target=1 даёт приближённый conditional Z, затем target-rotation даёт
X. Aux, port и Spin произвольны; private clean work отсутствует.

## Фактическая finite grammar

Default namespace — A19: SAM2688, address12, Choi input5, Choi output5,
branch, port, настоящий Spin, отдельный arbitrary aux и oldRIGHT witness.
В `choi_output` первые четыре бита — occupation grades, пятый — Julia t.
Choi input, oldRIGHT не адресуются; адрес/SAM/branch нигде не являются
target примитивной операции.

К каждой двумерной паре применяется CNOT basis permutation, A14 Walsh
sequence на одном target и обратная permutation. Максимум 20 controls;
при K<20 масштабируется целая степень `k←2^(20−K)k`, поэтому активный
**фактический** угол один и тот же. Для X phase общий multiplier равен
2^21. Неактивный sector точно I на всём пространстве. Добавление
branch=1 даёт точный controlled вариант фактического оператора.

В каждом sector хронология `F_actual†; X_actual; base_actual; F_actual`.
F — три mode rotations, каждая до четырёх occupation pairs. Слово
содержит все sectors, включая неактивные на данном входе, а их ресурсы
суммируются. Emitter выдаёт конечные native DAG blocks по индексам sector
и Walsh mask. Это не исполнение огромного развёрнутого слова.

Особое внимание обратным операциям: сохраняется **число** применений
буквального inversion, а не переключатель. Полный reverse содержит в
том числе inverse от уже выписанного inverse F; его primitive calls
нельзя бесплатно сократить. Для счётчика
`R=(G_port,G_other,CX,SourceI)` каждое inversion применяет

`T(R)=(Gp+Go,0,CX+6Go,3SourceI+4(Gp+Go))`.

Один и тот же endpoint unitary не объявляется одной и той же оплаченной
историей. Начальная чистота DATA, RAW births, preparation clock и
oldRIGHT/Info/work ещё должны быть включены в полное физическое исполнение.

## Uniform error и место в полном loader

При m<=3 mode rotations ошибка F<=4m delta, а фактический literal
inverse имеет ту же norm error. Sector error не больше
`2*4m delta+delta+delta<=26 delta<2^-3259`.

Секторы ортогональны по неизменяемым address/SAM/branch, а каждый
actual sector word точно тождественен на остальных patterns. Поэтому
полная coframe SELECT ошибка — максимум по секторам, также `<2^-3259`,
при произвольной когерентной суперпозиции и внешней запутанности.
Она не умножается на число sectors. На адресах anchor, proper-link и
padding эта coframe часть точно I. Paid resource sums при этом полные.

Для получения полного Omega остаётся настоящий proper-link SELECT.
Его B41 factorization даёт максимум 101 macro; при такой же delta
полный blockwise SELECT имел бы ошибку `<2^-3257`, но это условие нельзя
считать выполненным до actual angle/native proof. Префикс A19 тогда
добавляет `<2^-4091`, что удовлетворит контракту B39 `<=2^-3250`.

Далее остаются объединённая namespace и RAW preparation, весь B39
адаптер, B35 full reflection, vacuum/Fourier/SITE, H1 и его настоящий
alpha. Нормированный report, его полный физический источник и исходная
Cost−Info остаются разными объектами до доказанной связи. Native
программа здесь не устанавливает selection физической динамики ОТО.
Все найденные целые k фиксируются до upstream вариаций. Дифференцирование
численного алгоритма выбора k или подстановка его output в качестве
нового физического field-writer не входят в доказательство. Исходные
target/source derivative identities сохраняют собственные условия.
`physical_C_closed=false`, `GR_closed=false`.
