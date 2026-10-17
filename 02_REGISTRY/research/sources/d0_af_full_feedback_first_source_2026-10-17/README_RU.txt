D0 — исходная полная AF-обратная связь и локальная вакуумная сборка

RESULT_RU.md — доказательство источников и совместной редукции.
RECOVERY_COMPOSITION_RU.md — точный перенос новой all-40 искривлённой семьи.
PUBLICATION.json — проверенные GitHub-срезы и ссылки на комментарии по ID.
manifest.json — хеши первичного пакета; хеш нового следствия в PUBLICATION.json.

Проверки (Python 3.13.5 / SymPy 1.14.0):
  python check_feedback_source.py
  python -O check_feedback_source.py
  python check_joint_extension.py
  python -O check_joint_extension.py

78+11 точных контролей. JSON в обычном и оптимизированном режиме совпадает.
Физическое замыкание ОТО и независимая перепроверка прежнего геометрического пакета не заявлены.
