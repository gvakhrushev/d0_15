# Следующий parent A22: full original RAW Choi bank

A21 U удовлетворяет B35 joint-anchor isometry contract с24private wires
и ошибкой eta<2^-3230. Нужно реально собрать исходное
`O_b(G†)^⊗22`, где `O_b=R_u R_r`, на **всех**22DATA колонках, с U-private
на входе0 и произвольными SAM/port/Spin/aux/oldRIGHT/external factors.
Это не только проверка приготовления Omega из одной исходной колонки.

Стандартная A13 clean-comparator схема для joint anchor22+24=46 требует
45 новых нулевых проводов. B44 подтвердил это для этой конкретной
конструкции; нижней границей для всех native способов это число не является.

## Проверяемая альтернатива без новых clean wires

Исходная A14 Walsh identity допускает pattern0 на всех46 joint controls
и arbitrary aux как target. Все Walsh coefficients тогда положительны.
Конкретная степень k с `2^46 k theta≈pi` даёт на joint anchor вращение
aux, приближающее −I, и **точно I** вне anchor. Поэтому этот native word
может приближать полный `R_joint⊗I_aux` с uniform operator error deltaR,
без flag/work и без условия чистого aux. Нужно найти действительный k,
сертифицировать его целочисленно и выписать реальную конечную grammar.
Достаточно deltaR<=2^-3264; это пока предложение, не готовый сертификат.

Можно исследовать Gray-cycle порядок Walsh subsets: последовательность
`G_aux^k`, затем при каждом следующем Gray subset один CX на aux и G^k,
в конце CX для замыкания parity к0. Это потенциально уменьшает CX с
`K*2^K` до `2^K`, сохраняя G count=`2^K*k`. Равенство проверять как
полный оператор, не на чистом aux. Это **новая явная оплаченная история**;
не приравнивать её marks/price к старому comparator или к отменённым CX.
Literal inverse должен обращать именно эту фактическую последовательность.

## Сборка и целевой bound

Если Rhat построено, хронология full bank:

`(G†)^⊗22; Rhat; U†; Rhat; U`.

При условии initial U-private=0 projector-isometry lemma B35 даёт
`||actual bank − O_b(G†)^⊗22 ⊗ |0private>|| <=4eta+2deltaR`
на полном DATA/external входе. Approximate Rhat не обязано быть точным
involution; его literal inverse нельзя подменять тем же forward word.
Каждый U† и inverse-of-inverse учитывается с целой глубиной инверсии.

RAW preparation24private из born v следует выписать отдельно; DATA22
RAW inverse уже часть исходного full bank. Physical birth/clock/Info
admission не следует из наличия этих native sequences.

B45 после B44 строит исходный внешний SITE `O_chi(G†)^⊗8` через прямую
подготовку half-vector `u_chi=(r+chi)/sqrt(2(1+chi0))` и binary-tree
mass rotations. Он сможет потребить проверенную scratch-free reflection
при меньшем K, если её общий proof и реальные степени будут завершены.

После этого остаются исходный vacuum/Fourier CAR prefix, полная marked
H1 execution, настоящий alpha и original physical Cost−Info source.
Никакой новый action/Info или очередной geometry search не вводить.
