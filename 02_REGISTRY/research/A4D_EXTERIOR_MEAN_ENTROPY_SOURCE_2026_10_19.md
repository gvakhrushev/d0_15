# Полный exterior Shannon readout: интеграция первого источника

Статус: **точный источник выходного Shannon-readout на существующем золотом приборе; физический выбор цены и полный native source/Ward открыты**. Материал принят в существующую ветку исследования #334 как отдельный источник данных. Он не меняет формулу двухтактовой Book-feedback цены и не закрывает G0.

Первичный текст и checker сохранены в [`sources/d0_exterior_mean_entropy_2026-10-19/`](sources/d0_exterior_mean_entropy_2026-10-19/). Закреплённые владельцы: [полный golden-record источник](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md), SHA-256 `748f723516dead3a713f31dd5a49dcbde7805ef0a15e7450f3026790abefa5e2`; [один двухтактовый AF×scene Einstein-source](A4D_ONE_FEEDBACK_NONFLAT_NULL_SCALAR_EINSTEIN_SOURCE_2026_10_18.md), SHA-256 `80bdb2a3ab6189b37ea9cebe1545cfebea2d7300037f4d3e21fa5e1479a5ce84`.

Для заполненного d-модового входа полное occupation-разбиение сохраняет каждый исход S с |S|=d и вероятностью q_S=|det V_S|^2, где V=[K;B] и V*V=I_d. На спектральном блоке F=f_i I, K=w_0(I-rF), положительная часть закона факторизуется в пары good/bad с параметрами

\[
a_i=|w_0(1-rf_i)|^2,\qquad
\kappa(a_i)=a_i\log\frac{a_i}{1-a_i}.
\]

Производная энтропии **всего** выходного закона в фиксированном базисе полярных мод равна

\[
DH_{\rm ext}=2\sum_i\kappa(a_i)\,D[-\log(1-rf_i)].
\]

Нулевые в базовой точке occupation-исходы сохранены: их вероятности имеют нулевой первый джет, поэтому они не добавляют линейного члена к `DH_ext`. В отчёте нормированная цена readout записана как `H_ext/log(phi)`; она не объявляется частью полного native Cost−Info. Точная проверка содержит 25 контролей, включая все шесть исходов при `N=4,d=2`, два допустимых изометрических возмущения, ненулевой некоммутирующий `DF`, нормировку и сумму производных вероятностей. Обычный и `-O` режимы дали побайтно одинаковые JSON receipts.

На золотых блоках Q_0=1-p^6, R_0=1-p^6-p^{12}, p=phi^{-1} итоговая относительная связь этого **mean-readout** равна

\[
\lambda_{\rm mean}=2\sigma p^{-5}
\left[\frac{\kappa_Q}{\kappa_R}\frac{R_0}{Q_0}+p^6\right]
\approx 24.0231937147407\quad(\sigma=+1).
\]

Это отличается от mode/MAP коэффициента того же consumer: lambda_mode≈23.3434588481236. Значит полный закон исходов и его наиболее вероятная мода дают разные первые источники. Для обратной ориентации sigma=−1 знак источника меняется; при подстановке mean-source в pp-wave уравнение отчёт получает A+D=−2 lambda_mean s².

Граница интеграции существенна. H_ext — производная полной выходной Shannon-энтропии, а первичный физический кандидат в закреплённом Einstein-source владельце — двухтактовый feedback J2 из §6.18 исходного golden-record действия. Новый checker **не** доказывает, что H_ext входит в тот же полный native Cost−Info, что он оплачивает подготовку, clock, query, basis и прошлые записи, или что D0 принудительно выбирает эту цену и обратную ориентацию. Он также не повторяет 40-row lattice replay и не доказывает физическую refinement.

Поэтому коэффициент mean-source нельзя молча подставить вместо коэффициента прежнего J2-решения. Оба результата остаются разными условными потребителями одного прибора до вывода единой цены из общей native-подготовки. Это напрямую сужает следующий G0 шаг: закрепить на одном и том же admitted history полную цену readout/подготовки, затем дифференцировать её и получить одну joint Ward identity. Полнота примитивного ActionProtocol и физическая существенность его свободной цены остаются отдельными открытыми обязанностями в [G0 ownership](A4D_NATIVE_DYNAMICAL_OWNERSHIP.md).

Есть ещё более точная граница выбора базиса. Новый hostile control [`check_exterior_basis_ambiguity.py`](sources/d0_exterior_mean_entropy_2026-10-19/check_exterior_basis_ambiguity.py) держит тот же good compression \(K=\operatorname{diag}(3/4,1/2)\), но сравнивает полярное failure-размещение с унитарным Hadamard-размещением тех же failure singular values. Все шесть occupation-исходов в обоих законах сохранены и нормированы; их Shannon-цены отличаются ровно на \(17\log 2/32\). Для общего двухмодового закона с good-массами \((a,b)\) разность равна \([a(1-b)+(1-a)b]\log2\), поэтому её first-source коэффициент по \(Da\) равен \((1-2b)\log2\). На golden \(R\)-блоке он равен примерно \(-0.4017726586\,Da_Q\ne0\). Значит, полярный output basis — нагрузочная часть mean-source, не следствие одного сжатия \(K\) или determinant \(F\). Контроль не доказывает native-допустимость обеих компоновок и не является общим no-go; он точно локализует недостающий выбор полного прибора.

## Воспроизведение

```sh
python3 02_REGISTRY/research/sources/d0_exterior_mean_entropy_2026-10-19/check_exterior_mean_source.py --output 02_REGISTRY/research/sources/d0_exterior_mean_entropy_2026-10-19/RESULT.json
python3 -O 02_REGISTRY/research/sources/d0_exterior_mean_entropy_2026-10-19/check_exterior_mean_source.py --output /tmp/d0-exterior-mean-source-optimized.json
```

Checker SHA-256: `56bda572b4156bbafbb0b4b0985f8014497fbde47d9b3963b3d5b52930cbeef6`.
