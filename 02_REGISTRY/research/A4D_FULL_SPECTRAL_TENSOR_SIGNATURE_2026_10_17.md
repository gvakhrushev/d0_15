# Полный спектральный источник: timelike matter и тензорная сигнатура

17 октября 2026. Продолжение того же Draft #334.
Научный вход: `d5c0528e099097f1b62964d049e8f34713ff0dae`.
Потребитель: native first-source → Lorentz-star/Einstein, без нового действия.

## 1. Что проверяется

Потребляются точная continuum-факторизация из [causal metric/source owner](A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md), §§2–5, действительное [coframe/Hodge intertwining](A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md), [неизменённый IR feedback](A4D_NATIVE_FEEDBACK_IR_EINSTEIN_TORSION_SELECTION_2026_10_17.md), §§0–3, и [пространственный tensor16](sources/d0_spatial_tensor_vacuum_2026-10-17/RESULT_RU.md), §§6–8. Различие R_G/R_g и прежние pp-wave/cone controls уже принадлежат этим владельцам и не объявляются новым открытием.

Новый потребитель: точная time/space изоспектральная пара с ненулевым timelike P1 и нулевым собственным Rayleigh source; все десять линейных TT-строк и их principal symbol. Результат относится к объявленной полной условной spectral-plus-Rayleigh цене. Он не доказывает невозможность D0, не выбирает полную physical Cost−Info и не меняет original fixed-g/tau/raw-h^-2/#216. Точные Lorentz-AF-star результаты сохраняются.

## 2. Настоящие поля и timelike preparation

На координатном 4-торе одинаковых периодов 2pi, для гладкой a(t,z), берём

    e=diag(1,exp(a),exp(-a),1), n=e0,
    g=diag(1,-exp(2a),-exp(-2a),-1),
    G=diag(1,exp(2a),exp(-2a),1)=2dt⊗dt-g.

Обе volume densities равны1. Ставится настоящая Lorentz omega_LC(g) в исходный raising slot. По уже доказанному полному intertwiner соответствующий positive operator есть d+d_G^dagger на всех16 формах. Это путь в объявленном полном матричном carrier, не утверждение, что link Euler выбирает его.

Выбираем C_form=dt/sqrt(Vol_G). Тогда

    d(dt)=0,
    d_G^dagger(dt)=-partial_mu G^(mu0)=0,
    ||dt||_G,pointwise²=1.

Поэтому D C=0 и R=0. Полный первый differential нормированного ||DC||²/||C||² равен0 по всем гладким совместным directions, не только по данному ansatz. Все16 matter components сохраняются. На принадлежащем single16 P1 chart U_e=Lambda(e^T eta) переводит ненормированное native e0 в dt. У нормированной подготовки P1 psi=e0/sqrt(Vol_G), поэтому оно timelike и собственное правило n=P1 psi/|P1 psi|_eta даёт e0. Это не scalar/P1=0 контроль.

Reference128 можно сохранить как C_form tensor r с произвольным нормированным r, без выделения reference-колонки. Это rank1 system/reference state, не faithful128 preparation. Закон observer для произвольного 4x128 P1-блока и физическое порождение этой подготовки не объявляются доказанными. При физическом масштабе e_s=s e нормированная форма равна dt/(s sqrt(Vol_G)), а native amplitude — e0/(s² sqrt(Vol_G)); гармоничность и R=0 сохраняются.

## 3. Точная граница для всех spectral functions

Для непостоянной периодической f положим a_t=A f(t), a_z=A f(z). Положительные G_t,G_z изометричны перестановкой t,z. Поэтому полные Hodge-операторы унитарно эквивалентны со всеми модами и кратностями. Любая определённая unitarily invariant F_spec даёт

    F_spec[D_t]=F_spec[D_z].                              (1)

В частности, равны континуальные H,J при одинаковых beta,z,M. Два R равны0, хотя перестановка dt в dz не обязана сохранять саму подготовку: dt гармонична на обоих фонах. Следовательно равны вся объявленная цена и её derivative по A:

    S_cont,t(A)=S_cont,z(A).                              (2)

Это exact continuum statement. Точная finite-h изоспектральность исходного proper stencil не утверждается; его subleading corrections и original h^-2 задача сохраняются.

На этих двух семействах выполнены также первые observer equations данной цены. При fixed g observer tangent создаёт лишь G_0i. У G_t полный spectral E_G,0i нулевой по пространственным отражениям и трансляциям. У G_z компоненты01,02 зануляются отражениями x,y, а03 — отражением и трансляцией t. Настоящий R имеет нулевой первый source. На single16 P1 chart это сохраняет H,J matter derivatives через observer chain rule. Собственные link/torsion equations здесь НЕ решены.

Прямое вычисление Ricci для обеих сигнатур даёт, с одной конвенцией кривизны,

    R_G=-2[(partial_t a)²+(partial_z a)²],
    R_g=-2[(partial_t a)²-(partial_z a)²].                 (3)

Для K=(2pi)^3 integral(f')²>0 имеем

    I_EH[g_t]=-2A²K, I_EH[g_z]=+2A²K.                     (4)

Volume и actual R одинаковы, а цены (2) равны. Поэтому нет ненулевого постоянного c и постоянных Lambda,C, для которых на этой области

    S_cont=c I_EH[g]+Lambda Vol(g)+R_actual+C,             (5)

или соответствующее тождество first sources. Из (2),(4) следовало бы -4cAK=+4cAK. Перебор spectral functions того же D не исправит это противоречие. Это не общий запрет GR с другим independently derived observer/matter action и не запрет иной native истории или физического ограничения области.

## 4. Ненулевой IR источник и все10 TT rows

В принадлежащем two-scale режиме

    J_s^ren=-rho_vol s^4 Vol(G)+c_R s² I_EH[G]-b4 A4+O_C1(s^-2),
    c_R=M Phi2(z/(1-z))/(12pi² beta)>0.

На (3) volume фиксирован, H source есть O(s^-2) по log heat expansion, R=0. Поэтому полный source удовлетворяет s^-2 dS_s→c_R dI_EH[G] на этих smooth probes. При a=A cos(m(t-z)), m!=0 целое,

    R_g=0, mean R_G=-2A²m²,
    mean s^-2 dS_s/dA→-4c_R A m².

Полная Ric_g этой нелинейной семьи ненулевая порядка A²: это НЕ exact vacuum solution. Здесь применён C1 first-source input, не выдуман C2 lattice limit.

При flat g=eta, k_cov=(omega,0,0,k), пусть

    h_xx=-2A_plus, h_yy=2A_plus, h_xy=h_yx=-2A_cross,
    прочие h_mu nu=0.

Трасса и дивергенция равны0. Все десять symmetric components полной линейной Einstein formula дают

    E_g^(1)[h]=(omega²-k²)h/2,
    E_G^(1)[-h]=(omega²+k²)(-h)/2.                         (6)

При omega=k!=0 обе Lorentz TT-поляризации зануляют ВСЕ Lorentz rows, но не positive rows. В этих real operational coordinates ведущий native spectral tensor operator elliptic, не Lorentz wave operator.

Observer tangent создаёт0i blocks, их mixed pairing с (6) нулевой. Эквивалентно, под вращениями x,y TT имеет helicity2, тогда как observer3 и linear full16 exterior matter на invariant scalar/timelike фоне имеют только helicities0,1. На полном16 rotation generator J_12 удовлетворяет J(J²+I)=0; trivial reference multiplicity этого не меняет. Их regular stationary elimination не может изменить этот quadratic TT block; никакой inverse нулевого observer блока не используется.

Trace4/axial4 из A2 квадратичны по torsion и не имеют h-T mixed term на T=0. Реальный tensor16 из A4 имеет C_Y~|k|², B_hY=O(|k|³) по предыдущему владельцу, давая correction O(|k|⁴) там, где разрешено это ненулевое-frequency исключение. Нельзя обращать k=0, объявлять нелинейное recovery доказанным или переносить утверждение на другие gapless поля. Защита порядка2 сохраняет здесь positive, не Lorentz, символ.

Вещественная невырожденная algebraic field redefinition даёт конгруэнцию Hessian и не меняет real characteristic set. Умножение S на i также не меняет Euler equation. Настоящая Lorentz/Wick reconstruction с её аналитическими и physical-clock условиями — отдельный возможный маршрут, но он здесь не доказан.

## 5. Конкретный source consumer

На всём shear chart u=dt имеет expansion=acceleration=vorticity=0 и shearSq=2(partial_t a)². Точно

    I_EH[G]=-I_EH[g]-2 integral shearSq.

Чтобы при согласованном spatial coefficient получить -c_R I_EH[g], недостающий вклад полной цены обязан давать на этом chart

    Delta S^(2)=4c_R integral(partial_t a)².                (7)

(7) — диагностически необходимая разность, НЕ добавляемый counterterm или новый opcode. Его обязан породить настоящий пока не отождествлённый источник, либо нужен другой физически обоснованный Lorentz механизм.

Для предполагаемого c I_EH[g] плюс time/space-symmetric contamination полезен необходимый тест

    c=[S_z''(0)-S_t''(0)]/(8K).

Все spectrum-only члены сокращаются из числителя точно. Ненулевой тест ещё не достаточен для GR: реальные matter и higher-derivative sources остаются. Саму difference нельзя объявлять новым physical action.

Итак, один маршрут имеет правильный Lorentz-star carrier, но не выбранную полную physical source map; другой имеет явный H+J+R, но его положительный source нельзя отождествить с первым. Lovelock на G не превращает его в g. Это точная граница текущей композиции, не доказательство невозможности всей D0. Заявленный полный вывод ОТО остаётся недоказанным.

## 6. Проверка

В текущем чате локально исполнен самостоятельный SymPy расчёт Christoffel/Ricci для обеих сигнатур, timelike harmonic reading, retained observer shear, всех10 TT rows и обеих поляризаций, full16 rotation polynomial и source controls. Normal и python -O stdout совпали. Расширенная записка, код и JSON передаются в локальном пакете D0_tensor_signature_2026_10_17; этот Git-файл содержит самостоятельное аналитическое доказательство, а не заявляет уже подключённый новый CI entrypoint. Старые native/root/spectrum/Lean suites, global validators и full CI не запускались.

Внешний контекст: Barbero–Villaseñor, Lorentz Violations and Euclidean Signature Metrics, arXiv:gr-qc/0307066; Jacobson–Mattingly, Einstein-Aether Waves, arXiv:gr-qc/0402005. Общая известная возможность скрыть Euclidean gravity в metric/vector переписывании не объявляется новым результатом D0.
