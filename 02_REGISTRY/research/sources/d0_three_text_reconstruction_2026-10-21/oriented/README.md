# Первый приложенный текст: восстановленное математическое содержание

21 октября 2026. Новая реконструкция по полностью прочитанному первому приложению пользователя, на исходниках #334 с repository head `8ba0bd929499e639b0fe4640ffa448631f3b024b`. Репозиторий этим исполнителем не изменялся. Все файлы находятся в отдельном scratch для интегратора.

## Что восстановлено

- `ORIENTED_COMPLETE_PRICE_RECONSTRUCTION.md`: подробное условное доказательство полной цены, конечного sampler f_N/μ_N, реально оплаченного конечного Golden-банка, свежего conditional Golden register, полного mixed source, exact minimum iff и абсолютной нормировки.
- `SOURCE_AND_RANK34.md`: собственный source с числом фактических вызовов, conditional price coefficients исходного full17, применение уже доказанного rank34, полный Lorentz reference и точный finite-N own-price residual.
- `check_oriented_complete_price.py`, `verification_results.json`: НОВАЯ воспроизводимая узкая проверка.
- `SOURCE_PINS.json`: точные Git blobs и SHA потреблённых существующих источников.
- `USER_TEXT_ORIGINAL.txt`: неизменная байтовая копия пользовательского приложения.
- `MANIFEST.json`: SHA всех перечисленных файлов и этого README.

Исторические ZIP, patch, 217 checks, 39424 histories и независимые reviews по sandbox-ссылкам НЕ восстановлены и не предъявляются как выполненные здесь. Документы выше — вновь написанные доказательства математического содержания приложения. В пакете нет поддельного исторического review. Независимый review новой реконструкции выполняется интегратором отдельно.

## Проверка

Из любой директории с установленными Python 3, SymPy и mpmath:

```sh
python3 check_oriented_complete_price.py
```

Запускать из директории пакета либо указать полный путь к скрипту. По умолчанию результат печатается в stdout без изменения файлов. Для отдельного нового receipt используйте `--output /absolute/path/to/new_results.json`; существующий `verification_results.json` и manifest при обычном replay остаются неизменными. При переносе пакета пути внутри checker не зависят от исходного scratch. Проверка формул использует закреплённые source formulas и не требует дорогого original full128 replay.

Фактический итог нового запуска: **PASS, 141 новых контролей**, SymPy 1.14.0, mpmath 1.3.0, около 0.5 s. Exact rational controls проверяют sampler N=1,…,6, конечный Golden bank, исходную null-Lorentz algebra, component polarization, несколько точных reference controls, square completion, covariance source и необходимость второго члена Hessian pullback.

Новый full-record контроль N=1 использует все **17 настоящих исходных Golden17 вероятностей**; это не arbitrary full128 fixture. Банк содержит 14 raw Golden bits, то есть 16384 bank records; 96 готовы. Полное конечное дерево имеет **264144 terminal histories для одной настройки**, включая abort, оба query, SUCCESS/FAILURE/UNRESOLVED и фактически свежие Golden continuations. Четыре настройки оценивают 1056576 листьев через **1464 точных multiplicity buckets** одинаковой вероятности, сохраняя число каждого различимого raw leaf. Это четыре оценки одного малого составного протокола, не новый census нативных сцен/графов. На каждом leaf complete price в контрольной classical valuation равна его surprisal; это НЕ сертификат физического full Book price.

При 70 десятичных знаках максимальная абсолютная ошибка полной цены `8.69345191567e-70`; mixed rectangle `4.3374513028005993886831073513763145e-18`, ошибка против формулы `5.92624238964e-71`. Новый checker не повторяет прежние 217/39424 counts. Прямое отрицательное управление: предзаписанный Golden-bit даёт нулевой mixed entropy source, тогда как свежий conditional register даёт показанный ненулевой результат.

## Уточнения к приложению

1. Literal entropy-price theorem требует **абсолютного** same-full-history w=q binding, полного fresh independence и допустимого continuation. Net-ledger версия отдельно предполагает actual additive net increments 1,2; одного Golden Cost code недостаточно.
2. Exact minimum iff требует чётности **всей** собственной цены, независимой допустимости двух входов и пары (P,P⁻¹). Чётности q17 недостаточно. При gauge quotient строгий минимум понимается на quotient.
3. Предел — предел нормированной field-dependent части `(S_N−C_N)/r_N`; банк может дорожать, readiness может падать. Ни абсолютный предел цены, ни finite-N minimum из одного limiting minimum не следуют.
4. Lorentz reference требует A∈so(1,3); для произвольного геометрического B используется orthogonal projection A=Π_−Bᵀ. Это сохраняет нужную contraction и не вводит нового физического поля/цены.
5. Coarse entropy Hessian относится к probability coordinates. Полевой pullback содержит собственный second-jet term. Если выбранные 34 probabilities имеют retained refinements, нужны также Σ z_i h_i, а не только остаточный r h_tail.
6. Rank34 full128, исходный Golden17 и новый programme остаются различными типизированными приборами. Их общий field chart/preparation/readout maps должны быть доказаны; число координат их не отождествляет.

## Точное оставшееся условие

Существующий full Golden17 channel позволяет построить указанную conditional finite price и получить точный критерий её локального минимума. Чтобы это стало физической Book→Palatini связью, исходная задача должна выбрать данное полное продолжение/подготовку/reference и абсолютный Info/Cost. После этого необходимо проверить нулевой **полный** residual из (S11), сохранив controller, work, normalization, matter и upstream variation. Это применение к уже существующему geometric consumer, не доказанная compulsory action и не закрытая GR.
