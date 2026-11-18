# A14/B29: native ошибка подставлена в известную часть полного source budget

Потребитель — исходные H.1 T6–T10 и настоящие source marks. Это bound на вклад уже скомпилированных частей, а не новая цена или новый физический selector. Root повторил B29 interval/rational и hostile checks в отдельной копии; оба output совпали побайтно. В [ROOT_REVIEW_B29.json](ROOT_REVIEW_B29.json) закреплены входы и независимая рациональная проверка gain floor.

## 1. Правильная нормировка и её условие

Для данного A2049 и fixed-collar chart имеются

```
epsilon=2^-1531, s=2^-30, delta=epsilon*d,
d=Fh/(36 k0), k0=ry/rx,
g=2 kappa9 p^7 d epsilon² alpha_target² rx ry
 =kappa9 p^7 Fh epsilon² alpha_target² rx²/18.
```

Здесь alpha_target — готовность **полного идеального** original reporter. При дополнительном доказательстве alpha_target≥1/2 B29 даёт строго `g>2^-3128`, `gs>2^-3158`. Root независимо получил тот же floor через последнюю формулу, rational `p∈(309/500,619/1000)`, `kappa9>937/1000` и integer native power512. Эти условия не подменяют ещё недоказанный переход от A12 component READY к full ideal READY.

Для нормировки после lift unit physical displacement у B29 достаточный пример:

```
eta_forward <=2^-3205,
e_B<=2eta_forward<=2^-3204,
known X/CCX contribution <2^-3206,
ALL other forward errors <=2^-3206.
```

При указанном условном gain floor и ideal physical lift norm<55/s native-член `(e_B/(gs))||X||` тогда меньше2^-10. Full Hessian/Taylor term L, actual marked decoder/right-inverse, E_tau, physical cost/clock residual и actual c,w остаются отдельными величинами. Это не перенос42-row tolerance на2688 координат без карты.

## 2. Какая часть действительно обеспечена A14

В fixed seven-report decoder/first-success slice A13 имеется92 263 351 768 замен X/CCX, меньше2^37. A14 заменяет каждый такой macro actual primitive DAG с all-column error≤2^-4096. Следовательно уже определённый вклад **<2^-4059**, что меньше выделенного условного резерва2^-3206. Это использует все occurrences указанной части, а не количество уникальных видов gates. Native CX точен; огромный repeat count внутри точно заданного G не умножает заново approximation-error macro, но все реальные primitive calls входят в physical cost/clock.

Другие source-DAG dispatch operations, quantum payload routing, H tests, load/read/inverse wrappers и исходные seven-bank preparations пока не включены в завершённое общее расписание. Каждый требует своего all-column error и каждого действительного occurrence. Для новых размеров точность compiler является параметром; текущие4096 bits не объявляются достаточными для произвольного ещё неизвестного дополнения.

## 3. Точные инварианты не заменяются малой ошибкой

B29 hostile пример показывает: norm closeness к scalar corner сама по себе не даёт scalar corner после сжатия SAM. В A14 read-only control bits остаются controls на каждом primitive, oldRIGHT не адресуется, port/Spin восстановлены точно на completed macro boundaries. Это отдельное доказательство адресного/операторного инварианта. Aux относится к retained WORK, и его корреляция учитывается в общей all-column norm. Ни ideal discard, ни reset aux не выполняется.

Для полного writer ещё нужно доказать именно `M_hat=sum_b c_hat_b Pi_b tensor I_D` на его полном исходном носителе. Тогда H.1 использует actual c_hat, actual w и actual old-prefix Gram. У приближённого writer не обязательно существует одна точная alpha_hat: её отклонение от idealtarget law входит в e_B, без замены actual c,w их идеальными значениями. A14 не объявляет свою component estimate полным physical READY.

Для каждого требуемого исходного mark необходим его реальный prefix и отдельный bound `2||O_t|| eta_t+xi_t`. Совпадение конца новой common-port схемы с прежним оператором не переносит старые промежуточные marks, raw source rows или clock. Аналогично full backward word строится как настоящий paid inverse фактического forward: inverse approximate CCX не заменяется повторным forward CCX. `NATIVE_BOOLEAN_LIBRARY.json` хранит отдельный raw reverse; его все calls сохранены.

## 4. Следующая подстановка

Следующий объект — полный source-DAG dispatcher, который из retained selector labels выбирает действительные node/copy offsets/leaf addresses, и controlled routing fair payloads с сохранением всех attempts. Затем можно доказать readiness всей **идеальной** целевой процедуры, применить error ledger к целому writer, скомпилировать полные семь B25 banks и actual marks/clock. После этого остаётся исходный физический Cost−Info/source bridge; существование такой программы не выводит её обязательный выбор из D0.

`physical_C_closed=false`, `GR_closed=false`.
