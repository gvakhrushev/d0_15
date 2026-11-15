# A52: конкретная конечная задача и её исходные REPORT/READY labels

Собрана одна однозначная конечная задача на уже построенной A49 истории:
валидированные labels вызывают **те же** native word, четыре независимых
controls, fixed post, реальные births и growing clock. Все её ранние
prefixes теперь доступны также для независимых Pf/Qf/Qb/Pb и post-probe
плеч, а не только matched сравнения. Восемь существующих пар REPORT/READY
привязаны к фактическим физическим адресам; для них выписан полный
положительный четырёхисходный test с сохранением failure и quantum output.

Это законченный **конечный comparison packet**, а не свободная полевая
семья или физически допущенная Book01 section. A48 SOURCE пока привязан
к одному centre. Параметр Y нельзя незаметно добавить в уже замороженный
catalogue. Исходная physical fine instrument, её suffix и полная
Cost−Info связь всё ещё требуют доказательства.
`physical_C_closed=false`, `GR_closed=false`.

## 1. Один c и точный конечный catalogue

`scoped_comparison_task.py` задаёт строгий label:

    centre;
    (arm, j, sign), arm ∈ {matched,Pf,Qf,Qb,Pb},
                   0≤j<2688, sign∈{−1,+1};
    (post_probe,a,b,sign), 0≤a<b<2^5376.

В обычной части 26881 label: один centre, 5376 matched endpoints и 21504
endpoints четырёх **независимых** legs. Post-probe имеет свой конечный
огромный каталог `2^5376(2^5376−1)` endpoints и не смешивается с Pb,
который исполняется перед post. Каноническое конечное кодирование имеет
точный parse/encode round trip. Неверные axes, signs, planes и неизвестный
Y отвергаются. Зависимые адреса и compiler outputs не выдаются за
дополнительные свободные физические параметры.

Descriptor c фиксирует A23 полное vacuum/Fourier продолжение, A48 centre
и источники, A49 constructor и actual centre-dependent post, его одну
точность, исходные p,z, фиксированное положительное beta и clock profile.
Каждый label меняет только уже предусмотренные control slots. Post не
пересчитывается под sign или axis. Source hashes и actual layout находятся
в `FINITE_COMPARISON_TASK.json`; fixed beta остаётся параметром исходной
A49 теоремы, новым числом оно не заменяется.

Reference для каждого label a — полная операция **реального** W_c(a),
заданного существующим конечным constructor, а не один желаемый scalar
answer. Допуск faithful implementation имеет вид

    native_valid(w), same_actual_birth_tree/layout/input/cut,
    E(w)=E(W_c(a)).                                      (A52.1)

Здесь E содержит полные square segment maps между actual births, сами
birth embeddings и complements, final closing G, оба исходных B82 cuts,
SOURCE_before_Qf и двенадцать завершённых forward marks. Непрочитанные
quantum outputs не выкидываются. Такая математическая reference definition
не доказывает, что исходный физический процесс уже запросил эту задачу;
не использует Einstein predicate или источник как тест допуска.

## 2. Независимые prefixes и полная цена

Пусть signs(a) — исходная A49 функция slot_signs. Для любого label,
включая независимые legs, новый provider возвращает буквальное начало

    Dhat_ν Phat_(signs(a).Qf) Bhat Phat_(signs(a).Pf).

Для SOURCE_before_Qf второй control и Dhat отсутствуют. Реальные padding
каждого control включены; core padding остаётся **после** полного возврата.
Qb, Pb, fixed post, post-probe и retention не переносятся назад. У post-probe
все эти ранние prefixes совпадают с centre; это следует из порядка операций.
Для independent Qb/Pb соответствующие ранние prefixes также не изменены,
но их собственные поздние операции остаются в общем слове и цене.

299 малых буквальных сравнений охватывают все семь arm типов, обе
ориентации независимых controls, две оси, все 13 marks и настоящее
identity-padding. Полные production streams не разворачивались.
Структурное равенство следует из тех же source/stage/control providers
и B58/A51 закрытия transducer на объявленных границах.

Новые providers не распространяют A51 geometric jet на произвольный
independent arm: оценка `<2^-43` относится к matched contrast на двенадцати
post-Qf frontiers. В частности, pre-Qf остаётся отдельным mark.

На каждом label остаются ровно A49 `n=11893774624`, `K=175604`, оплаченные
Lbase и Nbase; `N=Nbase+2K`, `D=2^n(Lbase−2+3·2^K)−1`. Полные `425D`
Hodge modes, proper generated cut и final closing G дают ту же цену

    B=beta^-1 log(359D+2 Tr exp(−beta Delta0))
                    −log(1−z+z C* C).                   (A52.2)

Здесь actual H0=C и rank-one вход. Расширенный all-column SOURCE theorem
не меняет этот физический initial rank. Gain остаётся actual центральным
A49 Gamma; вычисляется DB/Gamma, не D(B/Gamma).

При (A52.1) существующие FN/RAW/EOQ1–7 дают stage gauge, равный I на всех
обязательных marks и концах birth-free segments, с сохранением birth
complements. Он сопрягает T,P и обе Hodge степени, следовательно сохраняет
всю (A52.2), включая плату за every atomic stage. Это proof map, не новая
бесплатная операция. Разные logical labels обычно имеют разные E и не
считаются одной вертикальной fibre. Так A50 finite contrasts переносятся
на faithful реализации **того же label/layout**, но новый логический нуль
из этого не следует.

## 3. Конкретный полный positive test на существующих labels

Для REPORT j namespace вычисляет физические адреса двух существующих
выходов `report_wire` и `all_READY_wire`. Для j=0 это соответственно
21216958 и 21216959. Все восемь пар различны, лежат среди actual early
births и не адресуют CODE. Речь о тех же outputs A17; новый register или
произвольный reader coefficient не добавляется.

На declared canonical SOURCE-private/factory fibre пусть F_a,ν — полная
изометрия выбранного prefix. Для computational projectors этих двух
labels зададим

    K_(r,k)=Pi_(r,k) F_a,ν,
    E_(r,k)=K_(r,k)*K_(r,k)=F_a,ν* Pi_(r,k) F_a,ν,
    sum_(r,k) E_(r,k)=I,         r,k∈{0,1}.              (A52.3)

Доказательство точное: Pi образуют ортогональное разложение единицы,
а F*F=I. Каждый K сохраняет **весь** quantum output, включая factory,
private, remainder и external reference; классический label можно
присоединить как outcome инструмента. Failure k=0 остаётся с его реальной
вероятностью. Положительное объединение outcomes сохраняет сумму I.
На всех разрешённых входных столбцах это CP instrument; для actual A49
входа берётся его конкретное rank-one сечение. Это не замена actual P0
на произвольную input density в самой цене (A52.2).

Для matched arms norm Pi=1, поэтому A51 одновременно даёт каждому
**неусловному** effect (A52.3) finite axis-jet error `<2^-43` относительно
соответствующего полного ideal A17 prefix. У success-conditioned
статистики возникает свой denominator; такой bound здесь не заявлен.
Четыре outcomes не тождественны автоматически всему исходному fine record.

Критическая граница: (A52.3) — математически доступный тест существующих
outputs, **не** утверждение о его фактической регистрации. Невыборочное
считывание даёт dephasing `sum Pi rho Pi`; оно может изменить coherent
inverse и всю дальнейшую цену. Проверяющий пример уменьшает последующую
вероятность с 1 до 1/2 после такого считывания. Нельзя незаметно вставить
его в A49. Если required reader переносится через unitary suffix U,
его правильный effect есть U Pi U*, с соответствующим actual suffix;
математическое сопряжение не оплачивает физический decoder/readback.

## 4. Какие Book01 witnesses уже конкретны

| Условие EOQ10/KAPPA | Применение к этому packet |
| --- | --- |
| Конечный quotient | Labels, исходный finite descriptor и его pins конечны; round trip точен. Общий physical field name ещё не вход constructor. |
| Operator/clock lift | Реальные A49 streams, RAW births, generated cut, closing G и полные Hodge modes сохранены; FN применим к same-layout faithful representatives. |
| Positive response | (A52.3) — явный нормированный retained test; binding к исходному зарегистрированному fine instrument/K9 ещё открыт. |
| Projection/retention | В одном packet нет изменений старых данных и префиксов; накопление уровней и actual future-test compatibility отдельно не доказаны. |
| Finite halt | A49 даёт конечные native providers и interval algorithm actual post при его положительном margin; проверены finite labels/малые prefixes, не исполнено огромное слово. Универсальный halting oracle не нужен. |
| Единая section | У всех labels одна actual A49 цена, параметры, gain и basis. Исходный V_h lift, общий off-shell chart и physical Cost−Info binding ещё открыты. |

Таким образом конечный descriptor предъявлен; вся physical section не
объявляется доказанной по одной таблице. Отсутствие внешнего registry не
является недостающим условием: RO1/XF5 его не требуют.

## 5. Почему следующий шаг — общий field constructor

B101 независимо установил на исходной буквальной Book03 цене контрпример
к выводу «fidelity плюс 2688 малых строк означает малый полный source».
У математического примера 2688 независимых spectator rows равны нулю,
но другая разрешённая logical row даёт `J'(0)=672/337`; heat одинаков
из-за full-clock conjugacy. Этот пример не объявляет такую row допустимой
или ненулевой в A49. Он сохраняет требование доказать полноту конкретного
разрешённого graph, а не считать недостающие направления нулевыми.

В A48 actual centre действительно жёстко задан: coframe templates
используют role/x2/x3, CAR — x0 и сохранённые angle libraries. Следующее
положительное обязательство: один constructor по свободному regular Y,
с тем же chosen full SOURCE extension, retained processor и настоящими
marks. Пост и нормы должны иметь одно семейное определение; если post
зависит от Y, его source нельзя терять. Затем нужны полный logical source
и его actual V_h/right-lift; finite 26881 catalogue этого не доказывает.

Параллельное конкретное обязательство — связать (A52.3) либо уже исходный
fine test с его реальным временем регистрации, failure и future suffix.
Не требуется читать каждый непронаблюдаемый quantum tail. Только после
same-execution binding можно применять физическую Cost−Info формулу;
literal H+J не получает произвольно добавленного R. Условный branch ledger
из BOOK_SOURCE_BINDING требует реальные xi_omega, K_omega, rho и их
производные, а не подобранные веса. Ни source coefficient, ни новое action,
ни новая геометрическая root-задача здесь не вводятся.

Проверки: все 26881 обычных labels, граничные post planes, 299 буквальных
prefix fixtures, actual восемь адресных пар, точные CP/normalization и
dephasing identity. Огромный production history и пост не вычислены;
это не Lean-проверка и не физическая GR closure.
