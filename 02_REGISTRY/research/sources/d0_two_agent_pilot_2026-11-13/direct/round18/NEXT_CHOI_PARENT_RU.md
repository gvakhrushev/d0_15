# Следующий конкретный parent: полная Choi-подготовка B35

CAR compilation A18 не снимает Choi parent. Нужно подготовить
`u_b=(r+Omega_b)/sqrt(2(1+c))`, `c=1/sqrt(65568)`, равномерно по всем
SAM labels и внешним запутанным факторам; затем применить исходную B35
joint-reflection рамку, сохранив RAW inverse и полные input columns.
Ни готовая численная Omega, ни правильная единственная output column
сами по себе не заменяют этот контракт.

Есть конкретная структурная возможность, которую следует проверить
до плоского перебора `2^2688` состояний. В исходном B25 каталоге
`A=2049=1+1024+1024`; каждый Julia block J_a имеет размер 32×32. Формулы
`precision_name.at_site/J_at` и chart catalogue показывают:

- coframe-column block зависит только от четырёх raw-coframe bits
  соответствующего столбца на одном свободном site;
- proper-link block зависит только от шести link-generator bits
  соответствующего направления на одном свободном site;
- q links фиксированы; reference banks не зависят от SAM.

Это согласуется с текущим исходным списком:1024 coframe coordinates,
1536 proper-link и 128 matter; в каждой локальной группе соответственно
4 и 6 независимых параметров. Это локальность **отдельного J_a**; весь
Choi state всё ещё зависит от всех соответствующих SAM coordinates.

Для нормированного Omega есть точное исходное разложение:

```
(1/sqrt(A)) sum_(a=0..A−1)|a>
    tensor (1/sqrt(32)) sum_(i=0..31)|i>|i>
    -- controlled J_a on the last 5 wires -->
Omega[a,i,j] = J_a[j,i]/sqrt(32A).
```

Здесь J_0=I, другие J_a — исходные Julia matrices; padded addresses не
входят в uniform A. Нужно реально скомпилировать приготовление address,
entangled i/j и эти SAM/address-controlled J_a с uniform norm/error,
полной grammar, буквальными inverses и фактическими ресурсами. Формула
пока только сокращает размер именованной операции, не доказывает её
физическое приготовление.

Отдельным шагом остаётся переход от Omega к **half-vector u**. Его нельзя
заменить отражением относительно Omega: B35 уже имеет точный контрпример.
Если использовать дополнительную когерентную ветвь или усиление, нужно
вывести действительный amplitude/phase, вернуть private work в заданный
target с uniform error и включить его в joint anchor. Предположение о
бесплатном postselection, стирании garbage или фазовом oracle запрещено.

Все native коэффициенты фиксируются до upstream вариации. Не требуется
новый геометрический root, изменение action/Info или новая интерпретация
PF. Полный physical Cost−Info и GR остаются открытыми.
