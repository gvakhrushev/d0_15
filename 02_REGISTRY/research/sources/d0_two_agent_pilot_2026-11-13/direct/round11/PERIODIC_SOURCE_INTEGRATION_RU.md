# A11 + B23–B24: глобальная привязка операторов H.1

Это подстановка двух уже проверенных результатов на один конкретный конечный carrier. [A11](FULL_SOURCE_OPERATOR_RU.md) даёт полные тензорные операторы и норму. [B23](../../open/round23/PF_SITE_CHOICAR_CONTRACT_RU.md) разделяет внешний общий PF SITE и внутренний равномерный CAR/Fourier-site. [B24](../../open/round24/TORUS_BOUNDARY_REVIEW_RU.md) задаёт допустимую для выбранного fixed-collar chart периодическую привязку и проверяет её ограниченную source-эквивалентность. Это не равенство полных физических историй и не закрытие Book03.

## 1. Полностью определённые source effects на всех 256 SITE

`bind_periodic_sources.py` потребляет исходные B21 PF labels и настоящий B24 periodic catalogue. [PERIODIC_SOURCE_BINDING.json](PERIODIC_SOURCE_BINDING.json) содержит:

* `A=2049` active Choi addresses, исходный anchor `1/sqrt(65568)`, полный active space `2049*32²` и padding до `2^22`;
* 282 leaf templates с точными `(input,output)`, множителем 1 для coframe и 2 для link `J(Lambda(U)/2)`, а также исходными CAR masks `(1,0)` и `(1,15)`;
* **72 192 конкретных leaf-address bindings** для 256 настоящих внешних site-меток; 1536 face bindings сверены с B24;
* все site-specific PF probabilities и их единственные inverse-density множители.

Теперь оба фиксированных source operators математически заданы на **всём** соответствующем пространстве:

```
H_f,global = direct_sum_(external SITE=x) H_f,x,
H_q,global = direct_sum_(external SITE=x) H_q,x,
H_kind,x = (1/rho_x) * A11_DAG_kind(actual leaf bindings at x).
```

Block-diagonal norm равна максимальной norm блока. Поэтому общий `Lambda_h=2^1525` из точного A11 сертификата действительно покрывает эту глобальную periodic binding: `2049<=4096`, весь материальный stencil остаётся в исходных 256 site, минимум PF тот же. Исходные `(I +/- H_kind,global/Lambda_h)/2` положительны на всех колонках, в том числе при произвольном input вне геометрического подмногообразия.

Это готовая **математическая операторная спецификация**, не native gate sequence или обещание дешёвой реализации. Её leaves адресуют координаты настоящего Choi/CAR пространства; абсолютные физические wire numbers, raw births и момент исполнения каждого reader ещё должны появиться в compiled writer/processor. Неизвестный oldRIGHT — отдельный неизменяемый spectator. Внутренний RIGHT каждой свежей CAR-копии не переименован в oldRIGHT.

В каждом из семи вызовов один и тот же fixed effect читает отдельно регенерированные `Z_j(Y_b)` ресурсы. Общий внешний SITE сохраняется до компаратора; PF averaging семи report probabilities по отдельности запрещено уже проверенным B23 counterexample.

## 2. Что именно позволяет periodic binding

Полное source-поле на 256 site сохраняется. Свободный chart содержит по 16 raw-u, 24 proper-link и 2 matter coordinates на 64 interior site; все collar, exterior comparator-values и PF фиксированы. B24 перебрал каждую зависимость: 112 изменённых open/periodic строк не содержат ни одного свободного operand; остальные 144 используют те же operands. Поэтому при одной report law/reference/normalization разность `sum_x w_x Xi_x` постоянна относительно всех 2688 координат.

Следовательно переход не удаляет свободные source equations этого chart. Но baseline `c`, абсолютный return, полные states/marks/clock, independent raw-gate variations и factory READY **не** объявлены одинаковыми. Реальная программа будет только одна — на выбранной periodic binding, с её собственными `c`, gain, ошибки и стоимостью. Не требуется сначала физически построить вторую открытую программу.

Если свободны boundary или density, приведённая source-эквивалентность более не следует; B24 содержит counterexamples. Ни torus centre как глобальный Einstein root, ни общая GR-refinement граница этим не доказаны. Для полной цели физический source должен быть перенесён на весь исходный требуемый набор вариаций, с их настоящим boundary contract.

## 3. Current и reference frame принадлежат одному интерфейсу

Для current centre используется подтверждённая A11/B24 карта `R=diag(1,1,-1,-1)` и raw `u=nu eta_null e^-T`; PF dressing не добавляется. Прямой chart — additive u, обратимый по всем 16 компонентам.

Для исходных Cartesian reference F2–F6 нужен отдельный фиксированный ортогональный `T`: Hadamard block в 0,1, единица в 2 и минус единица в 3. Тогда `det T=1`, `T eta_cart T^T=eta_null`,

```
e_ref=T (6/sqrt(rho)) I,
u_ref=(nu sqrt(rho)/6) T eta_cart,
U_ref=T U_ref,cart T^T,
u_ref^T eta_null u_ref/nu²=(rho/36) eta_cart.
```

Именно поэтому реальные time/space references дают противоположные ненулевые `q`, а не ноль от неправильного null-frame identity. B24 проверил точные frame identities и подставил реальные ссылки в полный A11 source DAG: `f_ref±=±rho F_h/36`, `q_time/space=±rho d_h`. Для всех 256 reference bank targets это один и тот же аналитический рецепт; фактические их matrix outputs и native prepare ещё не выпущены как полная семёрка.

## 4. Проверка и следующий конструктор

Root повторил B23 и B24 из отдельных временных копий: все 11 сгенерированных файлов совпали побайтно, 6 команд завершились успешно. B24 независимо воспроизвёл A11 DAG, точную norm certification, все 282 coordinate diagnostics и current-frame checker. Взаимная проверка закреплена `ROOT_REVIEW_B23.json`, `ROOT_REVIEW_B24.json` и B24 receipts.

Глобальная leaf-binding добавлена root **после** B24 review A11: она проверена cross-check всех 1536 face lists и всех CAR neighbours по B24; не выдаётся за отдельный независимый replay B24. Формулы/код уже просмотренного A11 core не менялись.

Следующие конкретные обязательства: сформировать фактические full-column targets семи `Z_j(Y_b)` с правильным current/reference frame; конструктивно реализовать fixed source-sign processor на выписанном tensor DAG и вычислить его data-independent READY/factory probability; составить literal prefix/reader/clock ledger. Затем применить A10 к действительному NPS слова и проверить полную исходную Cost−Info на той же истории. Прямое развёртывание гигантской плотной матрицы не требуется, но аналитическая компактность не делает операции бесплатными.

`GR_closed=false`; локальная исследовательская сборка, без публикации.
