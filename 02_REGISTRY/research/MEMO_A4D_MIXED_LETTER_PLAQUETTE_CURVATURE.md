## 1. Verdict

**`MIXED-LETTER-ODD-CURVATURE-ONLY`**

Task: `EXP-A4D-MIXED-LETTER-PLAQUETTE-CURVATURE`. Research-only; 2026-09-25. Все результаты ниже выведены из заданных конечных тождеств. GitHub, Lean и continuum curvature не использованы.

На коммутирующих archive shifts и для одного общего degree-preserving site dressing:

\[
\boxed{\mathcal P^{\mathrm{mix}}_{rs}(x)
=F(x)T_{\Omega_{rs}(x)}F(x)^{-1}},
\]
\[
\boxed{\Omega_{rs}=\kappa_r+\tau_r\kappa_s-\tau_s\kappa_r-\kappa_s.}
\]

Это точная формула. Even plaquette holonomy тождественно единична: ненулевая even curvature не возникает ни на первом, ни на втором, ни на любом более высоком порядке. При κ=0 вся плакетка равна I для любого общего single-valued F.

**Единственная вторичная квалификация:** уже имеющийся независимый affine-link carrier \(T_{b_r}\rho(L_r)\) действительно несёт оба компонента \((\Lambda_{rs},\Theta_{rs})\); для его использования не нужен новый математический primitive. Но его нельзя отождествить с mixed letter без явно заданной карты, а общий shared-F сектор этой карты имеет \(\Lambda_{rs}=I\).

Оговорки гипотез, существенные для точности: shifts должны коммутировать, F должен сохранять degree для утверждения именно о graded even/odd decomposition, а вывод \(\mathcal P=I\iff\Omega=0\) требует injectivity \(b\mapsto N_b\). Без injectivity верный критерий — \(N_\Omega=0\). Если shifts не коммутируют, остаётся их собственный commutator; dressing не создаёт его.

## 2. Exact mixed-letter plaquette

**Конвенция.** Работаем над конечным site set X, с commuting bijections x↦x+r и полем характеристики 0. На sections:

\[
(U_r\psi)(x)=\psi(x+r),\qquad
(\tau_rh)(x)=h(x+r),\qquad U_rM_h=M_{\tau_rh}U_r.
\]

F означает multiplication operator \(M_F\), \(T_{\kappa_r}=M_{x\mapsto T_{\kappa_r(x)}}\). Каждый link coefficient отображает fibre при x+r в fibre при x: это pull convention. Если owned pull использует x−r, во всех формулах надо заменить τᵣ на этот pull; никаких дополнительных знаковых догадок не требуется. Настоящее направление записи слова фиксировано произведением операторов.

Положим \(B_r=T_{\kappa_r}U_r\). Его обратный:

\[
B_r^{-1}=U_r^{-1}T_{-\kappa_r}
=M_{T_{-\tau_{-r}\kappa_r}}U_{-r}.
\]

Общие F сокращаются **между буквами**:

\[
\mathcal P_{rs}=(FB_rF^{-1})(FB_sF^{-1})
(FB_r^{-1}F^{-1})(FB_s^{-1}F^{-1})
=F(B_rB_sB_r^{-1}B_s^{-1})F^{-1}.
\]

Внутренняя часть вычисляется с сохранением shift order:

\[
\begin{aligned}
B_rB_sB_r^{-1}B_s^{-1}
&=T_{\kappa_r}U_rT_{\kappa_s}U_sU_{-r}T_{-\kappa_r}U_{-s}T_{-\kappa_s}\\
&=T_{\kappa_r}T_{\tau_r\kappa_s}
  T_{-\tau_s\kappa_r}T_{-\kappa_s}\\
&=T_{\Omega_{rs}}.
\end{aligned}
\]

Здесь применены только covariance multiplication/shift, commuting U и точный additive law translations. Никакое site-dependent κ не переставлялось со сдвигом без τ.

Эквивалентная полностью локальная запись:

\[
g_r(x)=F(x)T_{\kappa_r(x)}F(x+r)^{-1},\qquad
\mathscr L_r=M_{g_r}U_r,
\]
\[
\mathcal P_{rs}(x)=g_r(x)g_s(x+r)g_r(x+s)^{-1}g_s(x)^{-1}.
\]

Подстановка g сокращает F на каждом углу и даёт внешнее \(F(x)\cdots F(x)^{-1}\). В частности, обратное ребро у x+r+s использует inverse коэффициента gᵣ(x+s), а не gᵣ(x)⁻¹.

**Точный flatness criterion:**

\[
\mathcal P_{rs}(x)=I\iff N_{\Omega_{rs}(x)}=0.
\]

Если N faithful, это эквивалентно Ωᵣₛ(x)=0. При unfaithful N наблюдается только класс Ω modulo ker N. Из одних nilpotence/additivity без faithfulness более сильное утверждение не следует.

**Noncommuting-shift boundary.** Если Uᵣ,Uₛ не коммутируют, положим

\[
C_U=U_rU_sU_r^{-1}U_s^{-1},\quad
\gamma=\tau_r\tau_s\tau_r^{-1}\tau_s^{-1}.
\]

Тогда без предположения о commuting shifts:

\[
B_rB_sB_r^{-1}B_s^{-1}
=T_{\kappa_r+\tau_r\kappa_s-
\tau_r\tau_s\tau_r^{-1}\kappa_r-\gamma\kappa_s}\ C_U.
\]

При κ=0 это Cᵤ. Такой commutator уже не обязан быть site-local closed square; отождествлять его с кривизной F нельзя. Остальные square/cube формулы относятся к commuting coordinate shifts.

## 3. Even-sector result

При κ=0:

\[
\mathcal P_{rs}=F[U_r,U_s]F^{-1}=I.
\]

В локальной записи coefficients \(g_r^{\rm even}=F(x)F(x+r)^{-1}\) — coboundary. На любом пути внутренние F телескопически сокращаются. На замкнутом coordinate path с net shift identity и single-valued F even holonomy равна I. Если F не periodic/single-valued и вводятся переходные функции, это уже дополнительные global transport data, а не исходный ansatz.

При κ≠0 имеем

\[
\mathcal P_{rs}-I=F N_{\Omega_{rs}}F^{-1},\qquad
(\mathcal P_{rs}-I)^2=0.
\]

Для degree-preserving F оператор справа по-прежнему переводит degree 0 в degree 1 и равен нулю на других input degrees. Поэтому каждый diagonal degree block плакетки равен identity. Если F произвольный invertible, но не degree-preserving, conjugation может перемешать видимые matrix blocks; invariant statement тогда только «плакетка сопряжена чистой translation и unipotent». Называть новые diagonal entries независимой even curvature было бы ошибкой.

\(W(F)=F^{-T}F^{-1}\) — constitutive shadow, не curvature extraction. Он может пространственно меняться при нулевых plaquettes. В witness §8 W(0,0)=diag(1,1/4,1/9), а W на остальных sites равен I; все pure-dressing plaquettes всё равно identity. Это не отождествляет F с W и не утверждает gauge invariance W без указания transformation law.

| Минимальное отклонение от shared-F ansatz | Может дать even holonomy? | Что изменилось математически |
|---|---|---|
| Один общий F(x) | Нет | Только site coboundary |
| Direction-dependent Fᵣ(x) | Да, не обязательно | Coefficients Fᵣ(x)Fᵣ(x+r)⁻¹ уже не обязаны иметь общий site primitive |
| Link-local Gᵣ(x) | Да | Независимые transport coefficients; curvature проверяется их ordered product |
| Независимые Lᵣ(x) в affine link | Да | Уже данный linear connection carrier |
| Flat links с nontrivial cycle holonomy | Не local plaquette curvature | Возможен global transport obstruction даже при всех Pᵣₛ=I |
| Nonzero local holonomy, не представимая одним F | Да | Именно препятствие представимости как common coboundary |

Следовательно, если требуется ненулевая **local even** curvature, необходимо отказаться от ограничения «все link coefficients — один общий coboundary». Из перечисленных способов независимый Lᵣ уже существует в brief; вводить direction-dependent dressings вместо него не вынужденно.

## 4. Odd-sector curvature

Обозначим \(\Delta_r=\tau_r-I\). Тогда

\[
\Omega_{rs}=\Delta_r\kappa_s-\Delta_s\kappa_r,
\quad \Omega_{sr}=-\Omega_{rs}.
\]

Это exact abelian lattice curl, а не аппроксимация. При κ constant по sites Ω=0. При \(\kappa_r=\Delta_r\phi\) имеем Ω=0 из коммутативности Δ. Более того:

\[
T_{\Delta_r\phi}U_r=T_{-\phi}U_rT_\phi,
\]

то есть gradient sector допускает дополнительное translation-valued site dressing. Он не производит even connection.

**Flat не означает globally trivial.** На \((\mathbb Z/L)^d\) direction-r cycle имеет translation period

\[
h_r(x)=\sum_{j=0}^{L-1}(\tau_r^j\kappa_r)(x),\qquad
\mathscr L_r^L(x)=F(x)T_{h_r(x)}F(x)^{-1}.
\]

Если Ω=0, то hᵣ не зависит от transverse base point: \(\Delta_sh_r=\sum_j\tau_r^j\Delta_s\kappa_r=\sum_j\tau_r^j\Delta_r\kappa_s=0\). От сдвига вдоль r он также не зависит по periodicity. Постоянное κᵣ даёт hᵣ=Lκᵣ, обычно ненулевое в характеристике 0.

Для vector-valued κ на стандартном connected periodic cubical torus, Ω=0 и все hᵣ=0 эквивалентны существованию periodic φ с κ=dφ. Доказательство — определение φ суммой κ вдоль пути: elementary squares разрешают перестановки соседних steps, zero periods убирают winding ambiguity, reverse edge cancellation убирает backtracking. При faithfulness N это также criterion trivial translation holonomy всех closed paths; без неё соответствующий criterion формулируется в quotient по ker N.

Термин «translation/torsion candidate» означает только affine translation part. Без coframe и явной карты κ или b к его finite derivative никакого равенства Ω=Cartan torsion не заявляется.

## 5. Affine L+B curvature

Независимо от mixed letter положим

\[
g_r(x)=T_{b_r(x)}\rho(L_r(x)),\qquad
\mathscr A_r=M_{g_r}U_r.
\]

Предполагается, что ρ — degree-preserving group representation и covariance из brief выполнена. Для пар (b,L) exact laws:

\[
(b,L)(c,M)=(b+Lc,LM),\qquad
(b,L)^{-1}=(-L^{-1}b,L^{-1}).
\]

Они следуют из \(\rho(L)T_c=T_{Lc}\rho(L)\). Введём краткие обозначения всех четырёх угловых coefficients:

\[
A=L_r(x),\quad B=L_s(x+r),\quad C=L_r(x+s),\quad D=L_s(x),
\]
\[
u=b_r(x),\quad v=b_s(x+r),\quad w=b_r(x+s),\quad z=b_s(x).
\]

Тогда

\[
\boxed{\Lambda_{rs}=ABC^{-1}D^{-1}},
\]
\[
\boxed{\Theta_{rs}=u+Av-ABC^{-1}w-\Lambda_{rs}z},
\]
\[
\boxed{\mathcal P^{\rm aff}_{rs}(x)=T_{\Theta_{rs}(x)}\rho(\Lambda_{rs}(x)).}
\]

В длинной записи:

\[
\Lambda_{rs}=L_r(\tau_rL_s)(\tau_sL_r)^{-1}L_s^{-1},
\]
\[
\Theta_{rs}=b_r+L_r\tau_rb_s-
 L_r(\tau_rL_s)(\tau_sL_r)^{-1}\tau_sb_r-\Lambda_{rs}b_s.
\]

Проверка умножением четырёх пар:

\[
(u,A)(v,B)(-C^{-1}w,C^{-1})(-D^{-1}z,D^{-1})
=(u+Av-ABC^{-1}w-ABC^{-1}D^{-1}z,ABC^{-1}D^{-1}).
\]

При L=I возвращается \(\Theta=d_1b\), Λ=I. При b=0 остаётся linear holonomy Λ. Ни Λ, ни Θ пока не являются continuum curvature/torsion.

На уровне пар identity iff Θ=0 и Λ=I. На уровне operator representation при degree assumptions identity iff NΘ=0 и ρ(Λ)=I; equivalence с pair identity требует faithfulness обеих relevant representations. Это важно для невидимых curvature modes.

**Точное сравнение letters.** Для degree-preserving F necessary and sufficient conditions на одном link:

\[
F(x)F(x+r)^{-1}=\rho(L_r(x)),\qquad
F(x)N_{\kappa_r(x)}F(x)^{-1}=N_{b_r(x)}.
\]

Действительно,

\[
F(x)T_{\kappa_r(x)}F(x+r)^{-1}
=(I+F(x)N_{\kappa_r(x)}F(x)^{-1})\,[F(x)F(x+r)^{-1}].
\]

Первый фактор identity на diagonal blocks, второй degree-preserving; сравнение diagonal и degree-raising blocks даёт оба условия. Для всей κ-family второе условие означает, что F нормализует translation subspace \(\{N_b\}\). Для конкретного κ достаточно принадлежности соответствующего conjugated operator этому subspace.

Простая достаточная карта, если **дополнительно** \(F(x)=\rho(E(x))\):

\[
\boxed{L_r(x)=E(x)E(x+r)^{-1},\qquad b_r(x)=E(x)\kappa_r(x).}
\]

Тогда affine и mixed letters совпадают буквально. При этой карте

\[
\Lambda_{rs}=I,\qquad \Theta_{rs}=E(x)\Omega_{rs}(x).
\]

Следовательно, affine carrier воспроизводит mixed sector, но произвольный curved affine L не воспроизводится common F. Из самого определения degree-preserving F не следует F∈imρ; такая factorization или более общий normalizer bridge — дополнительное условие, не алгебраический автоматизм.

Частный homogeneous случай: E=R⊕V, F=diag(s,A) с s≠0 даёт \(FN_bF^{-1}=N_{Ab/s}\). Но отношение F(x)F(x+r)⁻¹ должно ещё лежать в выбранном ρ-image. Нормализация translation subspace сама не гарантирует первое условие.

**Нет double counting.** Чтобы представить pure gauge \(FU_rF^{-1}\) в affine chart при F=ρ(E), следует взять b=0, Lᵣ=E(τᵣE)⁻¹ непосредственно в \(M_{\rho(L_r)}U_r\). Дополнительный внешний conjugation тем же F уже меняет выбранные letters и не является той же подстановкой.

На simply connected cover flat L допускает site frame primitive. На finite torus общий single-valued E требует также trivial cycle holonomies. Поэтому даже Λ=I на всех squares недостаточно для глобального shared-F chart.

## 6. Perturbative expansion

Все разложения — формальные конечные matrix jets, не continuum limits. N линейно по своему аргументу.

**Mixed letter.** Пусть

\[
F=I+\varepsilon f+\varepsilon^2f_2+O(\varepsilon^3),\quad
\kappa_r=\varepsilon k_r+\varepsilon^2q_r+O(\varepsilon^3).
\]

Определим \(\omega=d_1k\), \(\chi=d_1q\). Тогда

\[
F^{-1}=I-\varepsilon f+\varepsilon^2(f^2-f_2)+O(\varepsilon^3),
\]
\[
\boxed{\mathcal P^{\rm mix}_{rs}
=I+\varepsilon N_{\omega_{rs}}
+\varepsilon^2\bigl(N_{\chi_{rs}}+[f,N_{\omega_{rs}}]\bigr)
+O(\varepsilon^3).}
\]

f берётся в base site x. f₂ полностью сокращается в этом порядке. Нет Nω² и нет [Nₖᵣ,Nₖₛ]: все products NᵦN꜀=0. Коммутатор [f,Nω] — изменение представления odd curvature при dressing, а не nonabelian even curvature. Для degree-preserving f оба displayed curvature coefficients строго degree raising.

В частности, при k=q=0 оба порядка нулевые, и точная формула доказывает нулевой результат во всех порядках. Можно получить ненулевые local connection-looking differences f−τᵣf при раскрытии elementary letter, но их closed-loop curvature точно сокращается; нельзя оставить только отдельные несократившиеся куски expansion.

**Affine channel: linear part.** Здесь маленькие a,b,c,d ниже обозначают first-order **линейные** link matrices, а не translation coefficients:

\[
a=a_r(x),\quad b=(\tau_ra_s)(x),\quad
c=(\tau_sa_r)(x),\quad d=a_s(x).
\]

Пусть a₂,b₂,c₂,d₂ — соответствующие shifted \(a_r^{(2)}\). Тогда

\[
\Lambda=I+\varepsilon H+\varepsilon^2J+O(\varepsilon^3),
\]
\[
\boxed{H=a+b-c-d=(d_1a)_{rs}},
\]
\[
\boxed{J=a_2+b_2-c_2-d_2
+ab-ac-ad-bc-bd+cd+c^2+d^2.}
\]

Порядок каждого произведения существенен. Это получается из

\[
(I+\varepsilon a+\varepsilon^2a_2)
(I+\varepsilon b+\varepsilon^2b_2)
(I-\varepsilon c+\varepsilon^2(c^2-c_2))
(I-\varepsilon d+\varepsilon^2(d^2-d_2)).
\]

Для site-constant fields c=a,d=b,c₂=a₂,d₂=b₂:

\[
H=0,\qquad J=[a,b].
\]

Следовательно, affine even curvature может начинаться с O(ε) из site-dependent curl, а для constant noncommuting first jets — с O(ε²). Для shared-F mixed ansatz она не возникает никогда.

**Affine channel: translation part.** Пусть

\[
u=\beta_r(x),\ v=(\tau_r\beta_s)(x),\
w=(\tau_s\beta_r)(x),\ z=\beta_s(x),
\]

а u₂,v₂,w₂,z₂ — соответствующие shifted \(\beta^{(2)}\). Тогда

\[
\Theta=\varepsilon\theta_1+\varepsilon^2\theta_2+O(\varepsilon^3),
\]
\[
\boxed{\theta_1=u+v-w-z=(d_1\beta)_{rs}},
\]
\[
\boxed{\theta_2=u_2+v_2-w_2-z_2
+av-(a+b-c)w-Hz.}
\]

Для постоянных first jets: \(\theta_1=0\) и \(\theta_2=a_r\beta_s-a_s\beta_r\), если second-order translation curls отсутствуют. Это semidirect connection–translation term, а не translation–translation commutator.

**Полная represented matrix.** Запишем

\[
\rho(\Lambda)=I+\varepsilon A_1+\varepsilon^2A_2+O(\varepsilon^3).
\]

Тогда

\[
\boxed{\mathcal R^{(1)}=A_1+N_{\theta_1},\quad
\mathcal R^{(2)}=A_2+N_{\theta_2}+N_{\theta_1}A_1.}
\]

A₁,A₂ degree-preserving; остальные члены degree raising. Для differentiable representation с differential ρ*:

\[
A_1=\rho_*(H),\quad
A_2=\rho_*\!\left(J-\tfrac12H^2\right)+\tfrac12\rho_*(H)^2,
\]

где аргумент первого слагаемого — второй coefficient formal log Λ, принадлежащий соответствующей Lie algebra. Если smooth/Lie structure не задана, достаточно предыдущей формулы через jets самой ρ(Λ).

В homogeneous representation ρ(L)=diag(1,L), A₁=diag(0,H), A₂=diag(0,J), и Nθ₁A₁=0, поскольку vacuum fixed. Последнее сокращение нельзя распространять на произвольную representation без этой гипотезы.

| Часть | Degree | Источник |
|---|---|---|
| Nω, Nχ | Raising | Linear discrete curl mismatch |
| [f,Nω] | Raising при graded F | Pure change of odd frame |
| H | Preserving | Linear discrete curl independent connection |
| J и [aᵣ,aₛ] в constant sector | Preserving | Exact nonabelian link multiplication |
| θ₁ | Raising | Discrete curl translation |
| av−(a+b−c)w−Hz | Raising | Semidirect coupling |
| Кривизна общего F при κ=0 | Нулевая | Exact coboundary cancellation |

## 7. Bianchi identities

**Translation closure.** При commuting Δ:

\[
\boxed{\Delta_r\Omega_{st}-\Delta_s\Omega_{rt}+\Delta_t\Omega_{rs}=0.}
\]

Доказательство — раскрыть Ω=d₁κ и попарно сократить шесть second differences. Это exact identity d₂d₁=0, не дополнительное field equation. Произвольная вставленная Ω без link primitive может не удовлетворять ему. На torus даже dΩ=0 недостаточно для Ω=dκ: нужны vanishing two-cycle periods; для link-generated curl они автоматически нулевые.

**Nonabelian cube.** Для любых invertible link coefficients gᵣ определим

\[
P_{rs}=g_r(\tau_rg_s)(\tau_sg_r)^{-1}g_s^{-1},
\qquad
\mathcal T_rH=g_r(\tau_rH)g_r^{-1}.
\]

Все следующие матрицы живут в одном base fibre x. Exact ordered cube identity:

\[
\boxed{P_{rs}\,(\mathcal T_sP_{rt})\,P_{st}
=(\mathcal T_rP_{st})\,P_{rt}\,(\mathcal T_tP_{rs}).}
\]

Эквивалентно, ordered product шести faces равен I:

\[
P_{rs}(\mathcal T_sP_{rt})P_{st}
(\mathcal T_tP_{rs})^{-1}P_{rt}^{-1}
(\mathcal T_rP_{st})^{-1}=I.
\]

Ни один factor не переставляется. Это не неупорядоченное «произведение шести плакеток».

**Доказательство через три-step paths.** Положим

\[
W_{rst}=g_r(\tau_rg_s)(\tau_r\tau_sg_t).
\]

Поочерёдные swaps пути rst→srt→str→tsr дают

\[
W_{rst}W_{tsr}^{-1}=P_{rs}(\mathcal T_sP_{rt})P_{st}.
\]

Swaps rst→rts→trs→tsr дают правую сторону. Это exact equality конечных words, из которой и получается cube identity.

Для mixed links:

\[
P_{rs}=F T_{\Omega_{rs}}F^{-1},\qquad
\mathcal T_rP_{st}=F T_{\tau_r\Omega_{st}}F^{-1}.
\]

Здесь κᵣ в conjugation сокращается, поскольку translations commute. Поэтому cube сводится к additive dΩ=0. Ordinary shift незадрессированной P без transport не даёт корректной covariant identity при site-dependent F.

**Affine decomposition cube.** Для transport link (b,L) и curvature pair (Θ,Λ):

\[
\operatorname{Ad}_{(b,L)}(\Theta,\Lambda)
=\bigl(L\Theta+(I-L\Lambda L^{-1})b,\ L\Lambda L^{-1}\bigr).
\]

Пусть (θᵢ,λᵢ), i=1,…,6 — пары шести факторов ordered cube product, включая сдвиги, conjugations и inverses именно в указанном порядке. Тогда exact consequences:

\[
\boxed{\lambda_1\lambda_2\cdots\lambda_6=I},
\]
\[
\boxed{\theta_1+\lambda_1\theta_2+\lambda_1\lambda_2\theta_3
+\cdots+\lambda_1\cdots\lambda_5\theta_6=0.}
\]

Для inverse factor применяется (θ,λ)⁻¹=(−λ⁻¹θ,λ⁻¹). Linear projection даёт тот же ordered cube identity для Λ с \(\mathcal T_r^LH=L_r(\tau_rH)L_r^{-1}\). Translation component **не** удовлетворяет generally ordinary dΘ=0: transport содержит Λ-dependent origin term. При linearization вокруг I оба first-order curls замкнуты; higher orders удовлетворяют именно expanded ordered identity, а не произвольно импортированному continuum Bianchi law.

## 8. L=3 hostile witnesses

Все числа рациональные; размер тора L=3 здесь не следует путать с матрицами линейных links Lᵣ. Носитель E=R⊕R², degree 0 — первая coordinate, degree 1 — последние две:

\[
T_{(u,v)}=\begin{pmatrix}1&0&0\\u&1&0\\v&0&1\end{pmatrix},\qquad
\rho(L)=\operatorname{diag}(1,L).
\]

Здесь N faithful; direct multiplication даёт NᵦN꜀=0 и covariance. Sites: `(Z/3)^2`, shifts +1 modulo 3.

**1. Flat control.** F=I, κ=0, L=I, b=0 дают I на всех 9 плакетках.

**2. Nonconstant pure dressing.** Возьмём

\[
F(0,0)=D=\operatorname{diag}(1,2,3),\qquad F(x)=I\quad(x\ne(0,0)).
\]

При κ=0 plaquette в origin равна D·I·I·D⁻¹=I. На остальных sites сокращение тоже exact; все 9 проверены. При этом W(origin)=diag(1,1/4,1/9) не равна W(other)=I.

**3. Constant mismatch.** κ₁=(1,1), κ₂=(2,0) во всех sites. Все 9 плакеток identity, но first-direction cycle:

\[
T_{\kappa_1}^3=T_{(3,3)}=
\begin{pmatrix}1&0&0\\3&1&0\\3&0&1\end{pmatrix}\ne I.
\]

Этот control запрещает смешивать plaquette-flatness с отсутствием всей holonomy.

**4. One-site bump.** κ₁(0,0)=(1,0), κ₁(other)=0, κ₂=0. Тогда

\[
\Omega_{12}(0,0)=(1,0),\quad
\Omega_{12}(0,2)=(-1,0),\quad
\Omega_{12}(x)=0\text{ иначе}.
\]

При F=I соответствующие plaquettes T(1,0) и T(−1,0). С nonconstant F из control 2 получаются точные матрицы:

\[
P(0,0)=\begin{pmatrix}1&0&0\\2&1&0\\0&0&1\end{pmatrix},\quad
P(0,2)=\begin{pmatrix}1&0&0\\-1&1&0\\0&0&1\end{pmatrix},
\]

а остальные P=I. Отсутствие взаимного сокращения entries 2 и −1 в разных dressed fibres не нарушает closure: сравнивать их надо с transport, либо использовать исходную Ω.

**5. Noncommuting rational linear links.** Постоянные

\[
L_1=A=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
L_2=B=\begin{pmatrix}1&0\\1&1\end{pmatrix}
\]

дают

\[
\Lambda=ABA^{-1}B^{-1}=\begin{pmatrix}3&-1\\1&0\end{pmatrix}\ne I.
\]

При b=0 это pure even holonomy. При постоянных b₁=(1,0), b₂=(0,1) имеем Θ=(1,0) и

\[
P^{\rm aff}=\begin{pmatrix}1&0&0\\1&3&-1\\0&1&0\end{pmatrix}.
\]

Это example одновременно ненулевых even и odd components в **независимом affine carrier**. Он не получается из shared-F mixed ansatz.

**6. Pure translation affine links.** L₁=L₂=I, b₁ — bump из control 4, b₂=0. Тогда Λ=I на всех squares, Θ=(1,0) в origin и (−1,0) в (0,2). Affine P ровно TΘ, без even block. Это also exact agreement sector F=I, b=κ, L=I.

**7. Exact gradient с periodic boundary.** Зададим φ(i,j)=(ij,i−j), где i,j — представители 0,1,2, а shifted argument всегда берётся modulo 3. Возьмём κᵣ=φ(x+r)−φ(x). В origin:

\[
\kappa_1(0,0)=(0,1),\quad \kappa_2(0,0)=(0,-1),
\]
\[
\kappa_2(1,0)=(1,-1),\quad\kappa_1(0,1)=(1,1),
\]

поэтому Ω(origin)=0. Все 9 squares, включая wrap-around, также имеют Ω=0. Нельзя вместо modulo evaluation использовать непрерывное продолжение polynomial φ за край тора.

**Дополнительный control direction-dependent dressing.** Пусть F₁(0,0)=D, F₁(other)=I, F₂≡I и κ=0. Тогда g₁(0,0)=D, g₁(0,1)=I, g₂=I, так что P₁₂(0,0)=D≠I. Это демонстрирует, какая именно common-F гипотеза необходима; не предлагает менять current letter.

**Nonabelian cube verification.** На `(Z/3)^3` взяты

\[
G_1=\begin{pmatrix}1&0&0\\1&1&1\\0&0&1\end{pmatrix},\quad
G_2=\begin{pmatrix}1&0&0\\0&1&0\\1&1&1\end{pmatrix},\quad
G_3=\begin{pmatrix}1&0&0\\1&2&0\\-1&0&1\end{pmatrix}.
\]

Для direction indices r=0,1,2 в коде использованы site-dependent links

\[
g_r(x)=T_{(x_{r+1},x_{r+2}-1)}G_{r+1},
\]

где coordinate indices cyclic modulo 3. Ordered cube identity проверена на всех 27 base sites точной рациональной арифметикой, включая shifted translations. Дополнительно formal jet multiplication в truncated ring Q[ε]/(ε³) проверило H,J,θ₁,θ₂ на четырёх независимых noncommuting matrix jets.

В том же 3D witness ordinary additive derivative translation component в origin равна

\[
\Delta_0\Theta_{12}-\Delta_1\Theta_{02}+\Delta_2\Theta_{01}
=\left(-2,\tfrac12\right)\ne0.
\]

При этом ordered cube identity выполнена. Это exact hostile counterexample неверной замене affine Bianchi на dΘ=0. Формулы Λ,Θ также отдельно проверены на всех 81 squares этой 3D модели; bridge и direction-dependent control проверены прямым multiplication.

Воспроизводимый код проверок (только Python standard library):

```python
from fractions import Fraction as Q
from itertools import product

def mat(rows): return [[Q(x) for x in r] for r in rows]
def eye(n): return mat([[int(i==j) for j in range(n)] for i in range(n)])
def zero(n): return mat([[0]*n for _ in range(n)])
def add(A,B): return [[a+b for a,b in zip(r,s)] for r,s in zip(A,B)]
def neg(A): return [[-v for v in r] for r in A]
def mul(A,B): return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def inv(A):
 n=len(A); R=[r[:]+s for r,s in zip(A,eye(n))]
 for j in range(n):
  p=next(i for i in range(j,n) if R[i][j]);R[j],R[p]=R[p],R[j]
  v=R[j][j];R[j]=[x/v for x in R[j]]
  for i in range(n):
   if i!=j:
    v=R[i][j];R[i]=[a-v*b for a,b in zip(R[i],R[j])]
 return [r[n:] for r in R]
def chain(*xs):
 out=eye(len(xs[0]))
 for A in xs:out=mul(out,A)
 return out
def affine(L,b):return [[Q(1),Q(0),Q(0)],[Q(b[0])]+L[0],[Q(b[1])]+L[1]]
def T(b):return affine(eye(2),b)
def shift(x,r):return tuple((v+(i==r))%3 for i,v in enumerate(x))
def plaquette(g,x,r,s):
 return chain(g(x,r),g(shift(x,r),s),inv(g(shift(x,s),r)),inv(g(x,s)))
def conjug(A,B):return chain(A,B,inv(A))
I=eye(3);D=mat([[1,0,0],[0,2,0],[0,0,3]])
F=lambda x:D if x==(0,0) else I
sites=list(product(range(3),repeat=2))
gpure=lambda x,r:mul(F(x),inv(F(shift(x,r))))
assert all(plaquette(gpure,x,0,1)==I for x in sites)
k=lambda x,r:(int(x==(0,0) and r==0),0)
gmix=lambda x,r:chain(F(x),T(k(x,r)),inv(F(shift(x,r))))
for x in sites:
 v=(int(x==(0,0))-int(x==(0,2)),0)
 assert plaquette(gmix,x,0,1)==conjug(F(x),T(v))
print('bump origin:',plaquette(gmix,(0,0),0,1))
print('bump negative:',plaquette(gmix,(0,2),0,1))
phi=lambda x:(x[0]*x[1],x[0]-x[1])
grad=lambda x,r:tuple(a-b for a,b in zip(phi(shift(x,r)),phi(x)))
ggradient=lambda x,r:T(grad(x,r))
assert all(plaquette(ggradient,x,0,1)==I for x in sites)
gconstant=lambda x,r:T((r+1,1-r))
assert all(plaquette(gconstant,x,0,1)==I for x in sites)
assert chain(*[gconstant((i,0),0) for i in range(3)])==T((3,3))
A=mat([[1,1],[0,1]]);B=mat([[1,0],[1,1]])
G1=affine(A,(1,0));G2=affine(B,(0,1));G3=affine(mat([[2,0],[0,1]]),(1,-1))
print('linear commutator:',chain(A,B,inv(A),inv(B)))
print('affine commutator:',chain(G1,G2,inv(G1),inv(G2)))
# Exact nonabelian cube, including spatially varying translations.
def g3(x,r):
 base=[G1,G2,G3][r]
 return mul(T((x[(r+1)%3],x[(r+2)%3]-1)),base)
for x in product(range(3),repeat=3):
 prs=plaquette(g3,x,0,1);prt=plaquette(g3,x,0,2);pst=plaquette(g3,x,1,2)
 lhs=chain(prs,conjug(g3(x,1),plaquette(g3,shift(x,1),0,2)),pst)
 rhs=chain(conjug(g3(x,0),plaquette(g3,shift(x,0),1,2)),prt,
           conjug(g3(x,2),plaquette(g3,shift(x,2),0,1)))
 assert lhs==rhs
print('cube: all 27 sites exact')
# Order-two series arithmetic: no floating point or small-epsilon fitting.
def jmul(X,Y):return [sum_m([mul(X[i],Y[k-i]) for i in range(k+1)]) for k in range(3)]
def sum_m(ms):
 out=zero(len(ms[0]))
 for m in ms:out=add(out,m)
 return out
def jinv(X):
 assert X[0]==eye(len(X[0]))
 return [X[0],neg(X[1]),add(mul(X[1],X[1]),neg(X[2]))]
As=[mat([[1,2],[0,-1]]),mat([[0,1],[2,1]]),mat([[2,-1],[1,0]]),mat([[-1,0],[1,2]])]
As2=[mat([[i,1],[-1,2-i]]) for i in range(4)]
bs=[(1,2),(-1,1),(2,0),(0,-2)];bs2=[(i,1-i) for i in range(4)]
def affjet(i):
 return [eye(3),[[Q(0)]*3,[Q(bs[i][0])]+As[i][0],[Q(bs[i][1])]+As[i][1]],
 [[Q(0)]*3,[Q(bs2[i][0])]+As2[i][0],[Q(bs2[i][1])]+As2[i][1]]]
Js=[affjet(i) for i in range(4)]
P=jmul(jmul(jmul(Js[0],Js[1]),jinv(Js[2])),jinv(Js[3]))
a,b,c,d=As; a2,b2,c2,d2=As2
H=sum_m([a,b,neg(c),neg(d)])
J=sum_m([a2,b2,neg(c2),neg(d2),mul(a,b),neg(mul(a,c)),neg(mul(a,d)),neg(mul(b,c)),neg(mul(b,d)),mul(c,d),mul(c,c),mul(d,d)])
def mv(A,v):return [sum(a*b for a,b in zip(r,v)) for r in A]
u,v,w,z=bs
th1=[u[i]+v[i]-w[i]-z[i] for i in range(2)]
av=mv(a,v);abcw=mv(sum_m([a,b,neg(c)]),w);hz=mv(H,z)
th2=[bs2[0][i]+bs2[1][i]-bs2[2][i]-bs2[3][i]+av[i]-abcw[i]-hz[i] for i in range(2)]
assert P[1]==[[Q(0)]*3,[Q(th1[0])]+H[0],[Q(th1[1])]+H[1]]
assert P[2]==[[Q(0)]*3,[Q(th2[0])]+J[0],[Q(th2[1])]+J[1]]
print('second-order affine jet: exact')
print('all controls passed')
# Verify exact affine coefficient formula at every square of the 3D model.
for x in product(range(3),repeat=3):
 for r,s in [(0,1),(0,2),(1,2)]:
  gs=[g3(x,r),g3(shift(x,r),s),g3(shift(x,s),r),g3(x,s)]
  ls=[[row[1:] for row in g[1:]] for g in gs]
  vs=[[g[1][0],g[2][0]] for g in gs]
  AA,BB,CC,DD=ls; uu,vv,ww,zz=vs
  ABC=chain(AA,BB,inv(CC));Lam=mul(ABC,inv(DD))
  av=mv(AA,vv); cw=mv(ABC,ww); lz=mv(Lam,zz)
  theta=[uu[i]+av[i]-cw[i]-lz[i] for i in range(2)]
  assert plaquette(g3,x,r,s)==affine(Lam,theta)
# Nonclosed raw translation component is compatible with ordered Bianchi.
def theta(x,r,s):
 P=plaquette(g3,x,r,s);return [P[1][0],P[2][0]]
x=(0,0,0)
terms=[theta(shift(x,0),1,2),theta(x,1,2),theta(shift(x,1),0,2),
       theta(x,0,2),theta(shift(x,2),0,1),theta(x,0,1)]
dtheta=[sum(sign*v[i] for sign,v in zip([1,-1,-1,1,1,-1],terms)) for i in range(2)]
print('ordinary dTheta at origin:',dtheta)
assert any(dtheta)
# Explicit frame-image bridge and direction-dependent-dressing controls.
Ef=lambda x:[row[1:] for row in F(x)[1:]]
def gbridge(x,r):
 E=Ef(x);L=mul(E,inv(Ef(shift(x,r))));b=mv(E,k(x,r))
 return affine(L,b)
assert all(gbridge(x,r)==gmix(x,r) for x in sites for r in range(2))
def gdirection(x,r):return gpure(x,r) if r==0 else I
assert plaquette(gdirection,(0,0),0,1)==D
assert all(plaquette(lambda x,r:I,x,0,1)==I for x in sites)
print('exact affine formula, bridge, flat and direction controls passed')
```

## 9. Theorem-ready statements

1. **Weighted-shift inverse.** Для bijective shift τ и invertible g, \((M_gU)^{-1}=M_{\tau^{-1}(g^{-1})}U^{-1}\). Доказательство прямым operator multiplication.
2. **Common-conjugation word law.** Для одного invertible F и произвольного word w, \(w(FB_rF^{-1})=Fw(B_r)F^{-1}\), включая обратные буквы. Доказательство последовательным сокращением F⁻¹F.
3. **Mixed plaquette formula.** При commuting shifts, linear N и NᵦN꜀=0, \(P_{rs}=FT_{\kappa_r+\tau_r\kappa_s-\tau_s\kappa_r-\kappa_s}F^{-1}\). Доказательство §2.
4. **Faithfulness-sensitive flatness.** При тех же hypotheses Pᵣₛ=I iff NΩᵣₛ=0. Если N injective, iff Ωᵣₛ=0.
5. **Pure-dressing flatness.** При commuting shifts κ=0 даёт Pᵣₛ=I для любого single-valued F. Без commuting hypothesis верная формула F[Uᵣ,Uₛ]F⁻¹.
6. **Graded odd-only theorem.** Если N переводит degree 0 в degree 1 и F degree-preserving, P−I имеет только этот raising block; (P−I)²=0 и все diagonal degree blocks P единичны.
7. **Gradient and closure.** На commuting shift module d₁d₀=0 и d₂d₁=0. Поэтому κ=dφ flat, и link-generated Ω обязательно closed.
8. **Periodic period obstruction.** На connected cubical torus с vector coefficients closed κ имеет base-independent cycle periods hᵣ; κ=dφ periodic iff все hᵣ=0. Constant nonzero κ даёт flat local plaquettes, но hᵣ=Lκᵣ.
9. **Affine multiplication theorem.** Semidirect covariance влечёт (b,L)(c,M)=(b+Lc,LM) и inverse (−L⁻¹b,L⁻¹).
10. **Affine square theorem.** Для corners (u,A),(v,B),(w,C),(z,D), pair holonomy равна (u+Av−ABC⁻¹w−ABC⁻¹D⁻¹z,ABC⁻¹D⁻¹).
11. **Mixed-to-affine bridge criterion.** Для graded F и ρ exact link equality эквивалентно \(F_xF_{x+r}^{-1}=ρ(L_r)\) и \(F_xN_{κ_r}F_x^{-1}=N_{b_r}\). Sufficiency и necessity следуют из diagonal/raising block separation.
12. **Frame-image bridge.** Если F=ρ(E), выбор bᵣ=Eκᵣ,Lᵣ=E(τᵣE)⁻¹ даёт literal equality letters, Λᵣₛ=I,Θᵣₛ=EΩᵣₛ. Поэтому этот bridge не создаёт independent linear holonomy.
13. **Mixed second jet.** При formal expansions §6 coefficients равны Nω и Nχ+[f,Nω], независимо от f₂; degree-preserving curvature отсутствует во всех orders при graded F.
14. **Affine second jet.** Exact matrix products дают H,J,θ₁,θ₂ из §6. При constant first jets H=θ₁=0,J=[aᵣ,aₛ],θ₂=aᵣβₛ−aₛβᵣ при нулевых second-order curls.
15. **Ordered cube theorem.** Для любых invertible links на commuting 3D shifts, \(P_{rs}(\mathcal T_sP_{rt})P_{st}=(\mathcal T_rP_{st})P_{rt}(\mathcal T_tP_{rs})\). Доказательство двумя цепочками swaps трёх-step paths.
16. **Affine Bianchi projection.** Semidirect decomposition ordered cube даёт product λᵢ=I и prefix-weighted sum θᵢ=0. Ordinary dΘ=0 не является общим nonlinear следствием.
17. **Rational even-curvature witness.** Матрицы A,B §8 имеют commutator [[3,−1],[1,0]]≠I; homogeneous affine representation сохраняет этот nontrivial linear holonomy.
18. **Trace blindness.** При finite graded E и degree-preserving ρ, \(\mathrm{tr}(T_Θρ(Λ))=\mathrm{tr}ρ(Λ)\); mixed plaquette имеет characteristic polynomial (t−1)^dim(E). Доказательство block triangularity и conjugation invariance.
19. **Affine-origin covariance.** Gauge transformation h=(c,E) в base site переводит pair holonomy в \((EΘ+(I-EΛE^{-1})c,EΛE^{-1})\). Поэтому Θ alone не frame-origin invariant при Λ≠I.

Гипотезы faithfulness, commuting shifts, periodicity и degree preservation перечислены явно: ни одна не заменяется геометрической терминологией.

## 10. Minimal next object

**Новый математический primitive для конечной кривизны не требуется.** Уже заданный independent affine link \(M_{T_{b_r}\rho(L_r)}U_r\) является достаточным carrier. Ordinary semidirect composition даёт и square holonomy, и exact ordered cube identity; оснований вводить новый 2-cocycle нет.

Если ограничиться только mixed ansatz, для nonzero even curvature необходимо независимо задаваемое linear link transport, не являющееся common site coboundary. В brief оно уже представлено Lᵣ. Поэтому следующий шаг — использовать этот существующий объект в нужном sector, а не объявлять отсутствующий primitive и не вставлять ρ(L) в прежнюю букву задним числом.

Необязательный bridge к F требует условий §5; это interface для сравнения charts, не условие существования curvature и не идентификация F=W.

## 11. Action handoff

Минимальный algebraic packet для исследователя действия:

| Carrier | Exact curvature data | Ограничения, которые нельзя потерять |
|---|---|---|
| Shared-F mixed | Ω=d₁κ; \(R^{mix}=FN_ΩF^{-1}\) | Only raising block, R²=0, d₂Ω=0; even block точно нулевой |
| Independent affine | \(\Lambda=L_r\tau_rL_s(\tau_sL_r)^{-1}L_s^{-1}\), \(\Theta=b_r+L_r\tau_rb_s-L_r\tau_rL_s(\tau_sL_r)^{-1}\tau_sb_r-\Lambda b_s\) | Ordered cube; semidirect covariance; representation kernels |
| Operator insertion | \(R^{aff}=T_Θρ(Λ)-I\) | Нельзя заменять его только W(F) или только Θ |
| First jets | H=d₁a, θ₁=d₁β; mixed ω=d₁k | На flat background pure dressing f не даёт curvature |
| Second jets | J, θ₂ и represented coefficients §6 | Нужны для quadratic variation linear-curvature actions |
| Global data, если действие чувствительно к циклам | Holonomies noncontractible words; для mixed periods hᵣ | Plaquettes не определяют harmonic sector |

Достаточно передать эти formulas, выбранную representation, shift convention и transport law. Exact covariance под link gauge transformation \(g_r(x)\mapsto h(x)g_r(x)h(x+r)^{-1}\):

\[
P(x)\mapsto h(x)P(x)h(x)^{-1}.
\]

Для affine h=(c,E):

\[
\Lambda\mapsto E\Lambda E^{-1},\qquad
\Theta\mapsto E\Theta+(I-E\Lambda E^{-1})c.
\]

Это ограничивает допустимые scalar contractions. В частности:

\[
\mathrm{tr}P^{mix}=\dim E,\quad
\mathrm{tr}P^{aff}=\mathrm{tr}\rho(\Lambda),\quad
\mathrm{tr}(R^{mix})^j=0\ (j\ge1).
\]

Здесь (Rᵐⁱˣ)²=0 означает композиционный квадрат оператора, а не нулевую положительную Riesz-норму. Ненулевой nilpotent operator вполне может иметь ненулевую норму. Значит, обычный Wilson trace mixed plaquette точно слеп к Ω, а affine Wilson trace видит linear holonomy и стирает Θ. Чтобы видеть translation, нужен совместимый degree-dual pairing или matrix element; его covariance должна проверяться отдельно. Норма Θ не invariant под general affine origin change при Λ≠I. Это ограничение action handoff, а не повод добавить непроверенный matter sector.

Action researcher теперь может использовать independent even curvature **без ожидания неизвестных plaquette coefficients**: все coefficients и second jets приведены выше. Но данные не выбирают contraction, measure, variational law или временную динамику. Данный результат закрывает вопрос о том, где curvature находится: **F — dressing; W — constitutive shadow; dκ — translation curl; независимый L — источник linear holonomy; ordered affine pair — полный finite curvature carrier.**