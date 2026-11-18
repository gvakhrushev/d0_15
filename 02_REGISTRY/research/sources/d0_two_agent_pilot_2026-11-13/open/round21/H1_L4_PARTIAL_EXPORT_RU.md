# B21: фактическая частичная выгрузка оригинального H.1 на L=4

**Результат.** Выбрана конкретная наименьшая dyadic сетка `L=4` из исходного Fourier128 owner; для неё выгружены настоящие 10 946 исходных F/R-адресов, 256 неравномерных PF-весов, центральная геометрия оригинального Brinkmann-представителя, 3072 полные численные `32×32` Julia-цели и буквальные прямое/обратное слова оригинального семивызовного компаратора по **18 176** вызовов каждое. Построены конечный `m=2688` кандидат chart и точная рациональная оценка его геометрической регулярности на всём кубе, без перечисления `2^2688` вершин. На одном истинном внутреннем узле воспроизведён исходный CAR16 six-face stencil.

Это **ещё не полный H.1 gate export**. Первый конкретный неисполненный узел — не локальный NPS и не компаратор, а сборка настоящих семи source-bank writers: полные `H_f,H_q` с их физическими source-sign selectors, общая оценка `Lambda_h`, полный ten-sign READY factory, actual coframe/link/Choi address catalogue, все точные Julia/Choi targets на ветвях SAM и их marked-prefix compilers. Следующие незавершённые узлы — native SITE loader/inverse, фактическая глобальная привязка local addresses, все исходные `O_t` и reader/seal catalog и реальный conditional bank recovery. Следовательно, текущие `q` и gain могут быть названы **калибровкой эталонного центра**, но не численным actual source полного positive-`s` H.1. `GR_closed=false`.

## 1. Конкретная сетка и исходный золотой адрес

Из [исходного Fourier128 owner](../../../d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_FOUR_COPY_MATTER_RESPONSE.md) берётся первый разрешённый dyadic `L=4`, `h=1/4`, 256 Role-сайтов; продольные `u,v` периодичны, поперечный collar фиксирован. Из [оригинального NPS/Brinkmann owner](../../../../A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L23) взяты `sigma=1/100`, `A_W=3/100`, `nu=3/5`, исходное `lambda_-(2^-20)` и поле

```
H(x,y)=−lambda E(x²+y²)+A_W(x²−y²),
E=(2pi)² sigma²,
Psi_j=sigma r_h (cos(2pi j/4),sin(2pi j/4)),
r_h=pi/(2sqrt(2)).
```

Прямые coframe legs и истинный сдвинутый proper link строятся по формулам владельца; `U_u=exp(−K_x N2−K_y N3)` без фиктивной переадресации узлов. Внешние значения stencil задаются тем же полиномом H, а не ошибочным периодическим поперечным замыканием. Файл [BRINKMANN_L4_CENTRE.jsonl](BRINKMANN_L4_CENTRE.jsonl) содержит 256 позиционных индексов, исходные `rho_x`, все локальные coframe columns, `U_u`, обе matter-компоненты и их slack. Численные matrix entries — диагностические double/80-digit значения формул, не certified native gates.

Сохранены именно настоящие source-cost-20 слова `F/R`, без rank/Morton перестановки: [ORIGINAL_F_R_N20_L4.jsonl](ORIGINAL_F_R_N20_L4.jsonl) содержит все `F_21=10946` последовательностей и их исходные 4D cell addresses. При вычислении каждого адреса сравнение с границей ячейки выполнено в `Q(p)` через рациональный изолирующий интервал; независимое сравнение с owner `original_cost_words(20,4)` совпало. [ORIGINAL_PF_N20_L4.jsonl](ORIGINAL_PF_N20_L4.jsonl) даёт `N_x∈[29,78]` и точно

```
rho_x=256 N_x/10946,      v_x rho_x=N_x/10946.
```

Это исходный фиксированный PF-чарт, не замена истинных весов равномерным prior. Файл [ORIGINAL_FOURIER128_L4.json](ORIGINAL_FOURIER128_L4.json) отдельно содержит 64 пары исходных real Fourier-characters и истинные 10 stencil overlaps `(20,10,10,9,8,8,6,9,5,5)/64`; это разрешённое исходное Fourier128 подсемейство, а не новый Walsh-код.

Для candidate H.1 chart фиксированы collar и исходные `rho_x`, а на 64 внутренних узлах заданы все независимые `16+24+2` направления; [L4_INTERIOR_CHART_COORDINATES.jsonl](L4_INTERIOR_CHART_COORDINATES.jsonl) содержит **2688** имён с однозначным `sam_index`. Сэмплер задан исходным правилом `Y_b=chi^-1(chi(Y0)+s(b-p²))` при `s=2^-30`: coframes/matter — additive, связи — `exp(Σ theta_ab eta^-1(E_ab−E_ba)) U_0`. [CHART_ENVELOPE_RESULT.json](CHART_ENVELOPE_RESULT.json) устанавливает рациональными неравенствами для **всех** его вершин положительную материальную slack, невырожденность coframe и строгие Julia margins у coframe/links. Контрольный расчет не сертифицирует `H_f/H_q` norm, all-prefix compiler или полный task: если фактический H.1 descriptor включает дополнительные свободные boundary/density данные, соответствующий chart надо расширить, а не считать их нулевыми.

## 2. Матрицы геометрии и настоящий SITE target

[CENTRE_JULIA32_TARGETS_NUMERIC.npz](CENTRE_JULIA32_TARGETS_NUMERIC.npz) хранит для всех 256 центров **полные** 32-колоночные Julia targets исходных CAR16 creator legs и proper-link exterior lifts: 1024 raw coframe, 1024 source-compatible `sqrt(rho_x)`-dressed coframe и 1024 link matrices. Использован исходный CAR-порядок `(0,2,3,1)` и полный блок

```
J(C)=[[C, sqrt(I−CC*)], [sqrt(I−C*C), −C*]].
```

Проверены обе степени Julia на каждом target: минимальный левый defect eigenvalue `>0.343`, максимальная ошибка полной ортогональности `<2.3·10^-15` по float. Эти матрицы — материализованные **численные targets центра**; они не являются точными finite Golden words, полным Choi bank, 2^2688 табличной выгрузкой либо доказательством исходных (C^1) bound. Рациональная оценка выше отдельно контролирует строгую геометрическую область при данном chart.

Настоящая canonical SITE-матрица для выбранных PF весов также выписана на всех 256 колонках: [SITE_LOADER_L4_CENTRE_NUMERIC.npz](SITE_LOADER_L4_CENTRE_NUMERIC.npz) содержит `O_chi (G^⊗8)*`, где `chi_x=sqrt(N_x/10946)`, положительный identity-anchor и весь 256-мерный оператор `O_chi` по owner §7cz879. Он численно ортогонален и отображает `v^⊗8` в `chi` с ошибкой `<2·10^-15`. Пока это **target**, а не оплаченный actual native SITE word или его выполненное unprepare.

[ORIGINAL_STENCIL_CHECK.json](ORIGINAL_STENCIL_CHECK.json) содержит не абстрактный скалярный loader, а шесть исходных основанных face `U_r(x)U_s(x+r)U_r(x+s)^−1U_s(x)^−1` и их реальные site/link addresses для узла `(0,0,1,1)`, CAR16 creator/H_eta contractions и настоящий forward-difference matter input. Проверенный центральный `f` и `q` равны нулю на этом null stencil в float. Это не full42 jet и не весь sampled H.1.

## 3. Настоящее готовое слово SC6 и частичный DAG

[SC6_FORWARD.jsonl](SC6_FORWARD.jsonl) и [SC6_INVERSE.jsonl](SC6_INVERSE.jsonl) — оба реальные списки `G`, `CX`, `SourceI` из исходного §7ef.C, не усечённый однобитный A. Каждый содержит точно

```
5888 G + 4096 CX + 8192 SourceI = 18176 calls.
```

Проверены все 512 контрольных колонок **каждого** из восьми disjoint selector-термов, включая signs от SOURCE и сохранение всех control bits. Обратное слово развернуто из точного owner (ZGZ=G^{-1}) с реальной оплатой `SourceI`; его inventory совпадает. Физический локальный map оригинального SC6 witness: selector `0..4`, `READY=(5,7,9,11,13,15,17)`, `REPORT=(6,8,10,12,14,16,18)`, `PORT=19`, `Spin=(20,21)`, optional protected `oldRIGHT=22`. Validator проверил исходные SourceI/frame и запрет oldRIGHT. Это локальный интерфейс **общего H.1 компаратора**, но не численная адресация всего 7-bank ресурса; owner отдельно запрещает считать SC6's 23-wire scalar apparatus целым геометрическим H.1.

[PARTIAL_H1_DAG.json](PARTIAL_H1_DAG.json) связывает настоящие известные модули в исходном порядке, отдельно оставляя `A_f` и `A_b` и включая реальный pre-sign event, `CX(e,r)`, центральный `SourceI²`, E0 и поздний archive. Он содержит **незаполненные** узлы и помечен `full_gate_dag_emitted=false`. Кандидатные роли и рождения [CANDIDATE_PREFIX_BIRTHS.jsonl](CANDIDATE_PREFIX_BIRTHS.jsonl) фиксируют локальный PORT/frame, пять selector и четырнадцать READY/REPORT, `SAM[0..2687]`, 8 SITE wires и optional untouched reference; `r,t` зарезервированы отдельно. Это 2716 перечисленных candidate births на `v`; порядок и адреса всех **остальных** банков не восстановлены и не объявлены истинной полной H.1 хронологией. До её согласования нельзя выдать final seal map, считать clock или запускать восстановление по поддельному списку живых адресов.

## 4. Калибровка: что уже число, а что ещё не число

Оригинальный comparator имеет `kappa_512=sin²(512 theta_G)`, `sin(theta_G)=p`. Точный interval-replay даёт

```
kappa_512 = 0.937931977709336672459479090276...
Q_ref=4 kappa_512 p^7 = 0.129216464009724422695003110517...
q_NPS,ref=p²+p³ Q_ref = 0.412469880568555161907002522845...
```

Это **референс при `Xi_x=0`**, в частности центр исходного null-стенсила; он не равен автоматически настоящему `q` после положительного `s` и всех `SAM` ветвей. Семь исходных `H.1` банков, а не SC6's scalar loaders, должны породить их собственные probabilities и shared-site PF среднее.

Для принадлежащего owner конструктивного референса F2–F6 выбраны допустимые `chi_h=1`, `s_ref=6`, `nu_* =1` и исходный `k0=r_y/r_x`. Действительные F2/F3 Cayley параметры рациональны, и

```
F_h=16517734400/162621047169,
r_x≈1.9168831693611474e−8,   r_y≈4.488651598960132e−7,
delta_h≈(1.8826561057181070e−6)/Lambda_h,
g_h≈(1.6352735855710525e−23) alpha_h²/Lambda_h².
```

В последнем равенстве использованы настоящие T4/F4: `epsilon_h=(64 Lambda_h)^−1`, `delta_h=epsilon_h F_h/(s_ref² k0)` и `g_h=2 kappa p^7 delta_h epsilon_h (alpha_h r_x)(alpha_h r_y)`. `alpha_h` — **полная** фактическая ten-sign READY probability, а не автоматически `2F_21 p^23` скалярной 23-wire демонстрации. Значения условные до построения и учёта полного processor/factory и вычисления допустимого общего `Lambda_h`. Actual sampling gain дополнительно включает настоящий `s`, старый Gram и полную физическую норму; NPS field response имеет принадлежащий owner множитель `p³`.

## 5. Точная остановка сборки и невыдумываемый следующий конструктор

В данном checkout удалось вызвать проверяемые компоненты, но не удалось построить один полный all-column native `A_f(Y_b)`/`A_b(Y_b)` и mark/seal receipt. Узкие отсутствующие **вычислительные операнды**, а не просьба выбрать новую физику:

1. Из 256×4 локальных coframe/link Julia targets и исходных shifted-stencil адресов требуется собрать **оригинальный полный aggregate Choi programme** со всем списком `(address,input,output)`, identity anchor, padding и невозмущённым RIGHT, а также настоящий CAR/Fourier site resource. Формула (879) даёт любой полный bank column и all-column `O_b`; готовый `A`/полный список реально необходимых programme addresses для H.1 здесь не был найден/выпущен. Один 32×32 Julia target или один stencil не заменяет bank.
2. Развернуть принадлежащий исходнику нормальный Lorentz `R2`, degree-82 geometric `H_f`, material `H_q`, все исходные коэффициенты 2+8 sign sectors, норму их **полных** операторов и общий certified `Lambda_h`. Конечная разреженная алгебра по исходным мономам и тензорным copies выражает их без нового физического постулата; фактическая полная таблица, структура подготовки и native selector здесь не сформированы. `180+16` — upper bound на ресурсы одного ten-sign вызова, не доказанное конкретное число births.
3. Для каждого из семи банков и SAM/общего SITE выдать настоящую адресную раскладку, checkpoint, T2 prefix `A_(b,t),O_(b,t)`, full ten-sign/READY factory и его `alpha_h`; затем применить finite full-register `G/CX` compiler со строгой ошибкой для каждой назначенной marks и paid inverse. Исходный compiler [Theorem 1](../../../../A4D_NATIVE_CLOCK_FULL_PRICE_COMPILATION_AND_FINITE_TEST_RECOVERY_2026_10_27.md) действительно задаёт конечный исчерпывающий поиск слов для каждого фиксированного computable SO target, но приведённое доказательство плотности не является уже исполненным генератором giant word и не делает неизвестный выходной каталог свободным. Реализация может быть потоковым/ленивым DAG, а не плотной матрицей полной системы.
4. На полученных **всех живых** конкретных адресах выполнить уже принадлежащие NPS/private-recovery/phase слова, проверить `P_bad=0`, сохранить исходные mark prefixes, для каждого реально требуемого будущего reader выдать оплаченный собственный transport до seal и назвать actual отметку физической регистрации либо её отсутствие. Затем подсчитать births/clock/complements и q/source на настоящих positive-`s` endpoints. Ни одно разрешение в этом списке не создаётся одним совпадением выходного q.

Есть дополнительный проверенный контроль против случайного смешения двух исходных носителей. Если **наивно** взять выбранный uniform Fourier128 и умножить его по сайтам на `sqrt(N_x/10946)`, результирующий RIGHT Gram **не** равен первоначальному `I_128/128`: exact rational [PF_FOURIER_CHECK.json](PF_FOURIER_CHECK.json) даёт ненулевую запись `−477/700544` (индексы 19,37). Правильный H.1 может готовить общий PF SITE и исходный CAR/RIGHT раздельно или применять другой принадлежащий owner платный map; этот тест запрещает только названное отождествление и не опровергает H.1. Он указывает, почему источник «есть SITE probabilities + есть Fourier basis» ещё не является построенным полным correlated bank.

Локальные Python-экспортеры и проверки запущены с `-B -W error`. Два существующих owner JavaScript checker выполнены в V8: проверка всех 1024 sign-ветвей для обеих полярностей и исходного CAR16/Choi moment-control прошла; это не запуск полного H.1. Контрольные значения/хеши и ограничения приведены в `RECEIPT.json`. Дальнейшее продолжение возможно из перечисленных исходных формул без новой теории; его цена, физический допуск, исходная memory-valued Cost−Info связь и ОТО остаются открытыми.
