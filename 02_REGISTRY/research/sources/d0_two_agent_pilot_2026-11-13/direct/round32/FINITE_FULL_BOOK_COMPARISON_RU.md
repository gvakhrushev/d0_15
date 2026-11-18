# A32 — две конечные программы и полная Book03-разность

Построен отдельный **canonical-start witness**: исходная пустая
RAW-история `H0=C, Omega0=1, P0=I_1`, затем все действительные
рождения и операции A30. Он потребляет R1–R11, A30/A31 и достаточный
B63 angle certificate. Это не объявление пустым прошлого иной
исходной задачи и не вывод обязательной стационарной истории.

## 1. Исходные коэффициенты и сравниваемые программы

В retained-source `SOURCE_PROOF_RU.md` §1 уже фиксированы внешний
feedback `z=2^-20`, beta=2p². Reporter имеет отдельно заданный
`z0=2^-20`; совпадение чисел не делает эти параметры одним объектом.
Они здесь не подбираются. У пустого старого префикса `A_old=1`,
`rank P0=Tr A_old=1`: до новых RAW births нет скрытого paid stage.

Для каждого из 2688 SAM направлений j берутся два положительных
показателя n+,n− из B63. Они сертифицированно приближают
`R(+t), R(-t)`, где

    t=2^-1618,   error каждой степени G <2^-4852.

Один сертификат проверен integer-ball arithmetic, второй независимый
пересчёт — исходными прямоугольными целочисленными интервалами.
Candidate search и floating point не считаются доказательством.
Оба показателя конечны, их длины — 4876 и 4869 бит.

Хронология двух endpoints:

    +: G_SAM^n+ ; paid identity ; A30 core ; G_SAM^(n−−1)
       ; paid identity ; K отдельные birth;G ; final G_SAM.
    −: G_SAM^n− ; paid identity ; A30 core ; G_SAM^(n+−1)
       ; paid identity ; K отдельные birth;G ; final G_SAM.

Они исходят из одной канонической начальной истории. Дополнительные
биты не предоставляются в выбранном чистом состоянии: все имеют
исходный pullback `psi -> psi tensor (sqrt(p),p)`.
Post-power не объявляется точным обратным pre-power; конечная
operator-norm ошибка учитывается отдельно.

## 2. Одинаковые mark ordinals и настоящий последний gate

Для одинаковой длины **каждого** pre/post интервала используются
точные identity слова на живых aux, port и новом helper:

    CX(a,b); CX(a,b),
    CX(a,b); CX(b,c); CX(a,b); CX(b,c); CX(a,c).

Они равны I на всех колонках, без условий о чистоте WORK.
Любая длина >=4 представляется `2a+5b`; специальные пары оплаченных
padding длины5/4 и5/2 покрывают разности1 и3. Каждый identity gate
сохраняется в clock, даже если целый блок ничего не меняет.

Пусть P — полученная общая длина pre- и post-интервала, L_core —
реальное число G/CX в A30. Тогда `L_base=L_core+2P`.
Общий source mark A30 с prefix count j теперь находится на
одинаковом layer `n+P+j` у обеих программ. Его observables — те же
исходные A30 RAW marks на тех же source DATA. Состояния изменены
соответствующей incoming SAM preparation, что и является сравнением.

Последний настоящий gate обеих полных историй — G на физическом
SAM wire `2+j`. Прежний последний CX A30 теперь обычный внутренний
edge. Все старые предположения о closing g пересчитаны.
Никакие detector/record/seal stages не добавлялись и не объявлялись
исполненными; если они потребуются, их полная история должна войти
в тот же учёт.

## 3. Поздние рождения и весь clock

Взято `K=66076`. После n=10407050782 ранних RAW births исполняются
`L_base-1` square gates, затем K отдельных пар `birth;G`, затем
реальный final G_SAM. Новые retention-биты не адресуются final gate.
Каждая пара даёт на всех старых колонках точный return sqrt(p),
поэтому cold return всего tuple равен `p^(K/2)c_endpoint`.

При d0=1 и без удаления каких-либо complements:

    N = n+L_base+2K,
    D = dim K_clock = 2^n (L_base-3+4*2^K)-1,
    dim H_final = 2^(n+K).

Это реальная сумма before-stage dimensions, а не frontloaded
формула `(L+1)2^n−1`. R6 строит из той же последовательности
причинные A_j,P_j, canonical terminal R, unitary T и исходные
heat/cut операторы. Сохраняются все **425D** thermal modes:

    Z01 = 359D + 2 Tr_(33D) exp(-beta Delta0(T)),
    J_endpoint = -log(1-z+z p^K c_endpoint²).

Формулы описывают полную исходную operator-price данного tuple.
Огромные матрицы, абсолютные trace/determinant и само слово не
исполнялись и не вычислялись плоско.

## 4. Строгий достаточный finite-difference бюджет

Для analytic conjugation фактического A30 cold corner
`c(alpha)=<phi|R(-alpha)M_core R(alpha)|phi>` имеем
`|c^(j)|<=2^j`. B62/B63 дают для исходного logdet после retention
третью derivative bound и angle-synthesis bound. При настоящей
normalization `Gamma_s>=gamma_under p^K`,
`gamma_under=(8/3)z*2^-3158`, получаем

    E_FD <= t² 2^3158 /16 *
      [64/(1-z)+192z/(1-z)²+128z²/(1-z)³],
    E_angle <= (3/[2(1-z)]) 2^3158 delta/|t|.

Подставлены именно сертифицированные t и delta. Рациональный расчёт
даёт `E_FD+E_angle<2^-74`. Подстановка не требует свободно
дифференцировать угол фиксированного native G.

Для полного growing-clock heat у ± одинаковы birth layout,
dimensions и final g. Все differing stages находятся в конечном
prefix до retention; отсюда `B_prefix<=2 N_base d_base`,
где `N_base=n+L_base<2^11647`, `d_base=2^n`. На поздних стадиях
операторы совпадают. Исходная R11 даёт

    E_heat <= 3 B_prefix /
       [359 |t| gamma_under d_base] * (2p)^(-K).

Здесь `|t|z Tr A_old=2^-1638`, p>3/5,
`(5/6)^4<1/2` и K=66076. Точный расчёт показывает
`E_heat<2^-76` при собственных исходных гипотезах R6/R11.
Ни нулевая heat derivative, ни равенство старого и нового heat
не использовались. Одинаковый baseline359D также остаётся в формуле.

Таким образом на каждое направление J_j сумма errors **полной
Book03 finite price difference** относительно центральной
determinant derivative удовлетворяет

    E_FD + E_angle + E_heat < 2^-73  при Gamma_s.

В это утверждение входят stage list и bound полного H+J на данной
паре. Оно не включает ещё не добавленные readers, другую старую
историю или независимые вариационные строки первоначальной задачи.

## 5. Правильная векторная нормировка и граница центральной производной

Пусть `d_j=FD(J_j)/Gamma_s`. Исправленная unit raw physical
mean-geometry форма под `Gamma_0=Gamma_s/s` есть

    (1/u_sampling) J_actual^-T d.

Из A31 `sqrt(2688)/[u_sampling(1-2^-23)]<55`, поэтому error всего
2688-компонентного covector меньше `55*2^-73<2^-67`.
Однострочную оценку нельзя назвать оценкой всего вектора без этого
множителя. С native-core source residual появляется ещё отдельный
член <2^-67. Taylor, reference E_tau, смещение decoded центра,
J^-1 correction и остальные independent physical rows остаются.

Центральная производная здесь — производная analytic conjugation
**действительного native core A30** при alpha=0. Не построено
полное padded native t=0 слово на том же clock и не утверждается
native smooth actuation. Два конечных endpoint являются настоящими
G/CX программами; их сравнение приближает указанную математическую
производную с доказанным остатком. Это не точная stationary history.

## 6. Достигнутое родительское условие

Теперь имеются конкретные конечные программы на исходном RAW/G/CX
носителе, общий начальный cut, настоящие source ordinals и последние
gates, весь growing-clock carrier и достаточный normalised price
comparison bound для этого canonical-start примера.

Это снимает необходимость **предполагать** бесплатную непрерывную
SAM-операцию в данном finite comparison. Следующий source шаг —
потребить реальные geometric/Taylor/reference bounds и независимые
уравнения на том же носителе. Выбранность именно этого writer,
его ковектора или stationary law исходной мерой Cost−Info не
следует из существования такой программы. Никакая полная
Cost−Info-эквивалентность или вывод ОТО здесь не заявлены.

`physical_C_closed=false`, `GR_closed=false`.
