"""Показать назначения и отчёты пилота D0 из одного опубликованного снимка Git."""
import argparse
from io import BytesIO
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from urllib.parse import quote, unquote, urlsplit

PILOT = Path(__file__).resolve().parent
BRANCH = "codex/d0-pilot-shared-20261118"
REMOTE_REF = f"refs/remotes/origin/{BRANCH}"
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
REPORT = re.compile(r"(direct|open)/round(\d+)/([^/]+\.md)")
TABLE = re.compile(r"^## Текущие задачи\s*\n(.*?)(?=^## |\Z)", re.M | re.S)


def git(*args):
    return subprocess.check_output(["git", "-C", str(PILOT), *args], text=True)


def plain(cell):
    return LINK.sub(r"\1", cell).replace("`", "").strip()


def tasks(readme, files):
    section = TABLE.search(readme)
    active = {}
    seen = set()
    if section:
        lines = []
        for line in section[1].strip().splitlines():
            if line.startswith("|"):
                lines.append(line)
            elif lines:
                break
        if len(lines) < 2 or [c.strip() for c in lines[0].strip("|").split("|")] != [
                "Раунд", "Вопрос", "Владелец", "Базовый SHA"]:
            raise ValueError("Неизвестный формат таблицы «Текущие задачи»")
        for line in lines[2:]:
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if len(cells) != 4:
                raise ValueError(f"Некорректная строка таблицы: {line}")
            label, question, owner, base = cells
            name = plain(label)
            match = re.match(r"^([AB]\d+)\b", name)
            if not match:
                raise ValueError(f"В строке нет номера раунда: {name}")
            key = match[1]
            if key in seen:
                raise ValueError(f"Повтор номера в таблице «Текущие задачи»: {key}")
            seen.add(key)
            partial = "частичн" in name or "совместные проверки" in name
            finished = not partial and "в работе" not in name and (
                LINK.search(label) or re.search(r"опубликован|готово|проверен", name))
            if not finished:
                active[key] = (name, plain(question), plain(owner), plain(base))
            # Result links occur in the round and question cells. An owner may
            # instead link to a JSON receipt; a reservation needs no result file.
            for _, target in LINK.findall(label + " " + question):
                link = urlsplit(target)
                path = posixpath.normpath(unquote(link.path))
                if not (link.scheme or link.netloc) and path.endswith(".md") and path not in files:
                    raise ValueError(f"{key}: в дереве Git нет результата {path}")
    # The first shared indexes gave A73 as a paragraph, also alongside B143.
    old = re.search(r"^\*\*([AB]\d+) в работе\.\*\* (.+)$", readme, re.M)
    if old and old[1] not in seen:
        owner = "Directed" if old[1].startswith("A") else "Open"
        active[old[1]] = (old[1] + ", в работе", plain(old[2]), owner, "")
    return section is not None, active


def latest_reports(readme, files):
    # A63 used a named report instead of READOUT_RU.md. Accept historical
    # report links only if their root-level Markdown file exists at this SHA.
    linked = {}
    for _, target in LINK.findall(readme):
        linked.setdefault(target.split("#", 1)[0], len(linked))
    best = {}
    for path in sorted(files):
        m = REPORT.fullmatch(path)
        if not m:
            continue
        lane, number, name = m.groups()
        canonical = (name == "READOUT_RU.md" if lane == "direct"
                     else name.startswith(f"B{number}_") or name == f"ROUND{number}_RESULT_RU.md")
        if canonical or path in linked:
            score = (int(number), canonical, -linked.get(path, len(linked)))
            if lane not in best or score > best[lane][0]:
                best[lane] = (score, path)
    return {lane: path for lane, (_, path) in best.items()}


def partial_reports(key, files):
    lane = "direct" if key.startswith("A") else "open"
    folder = f"{lane}/round{key[1:]}/"
    groups = {}
    # Research notes in the lanes use *_RU.md. Files under inputs/ are
    # copies of earlier sources; input/ is a research lane in its own right.
    for path in sorted(path for path in files if path.startswith(folder)):
        parts = path[len(folder):].split("/")
        if len(parts) > 1 and parts[-1].endswith("_RU.md") and "inputs" not in parts[:-1]:
            groups.setdefault(parts[0], []).append(path)
    return groups


def search_reports(commit, prefix, files, query, base_url):
    words = set(query.casefold().split())
    if not words:
        raise ValueError("Введите хотя бы одно слово для поиска.")
    paths = sorted(p for p in files if re.match(r"^(direct|open)/round\d+/", p)
                   and p.endswith(".md") and "inputs" not in p.split("/")[:-1])
    requests = b"".join(f"{commit}:{prefix}{path}\0".encode() for path in paths)
    objects = BytesIO(subprocess.check_output(
        ["git", "-C", str(PILOT), "cat-file", "--batch", "-z"], input=requests))
    hits = {"direct": [], "open": []}
    for path in paths:
        header = objects.readline().split()
        if len(header) != 3 or header[1] != b"blob":
            raise ValueError(f"В Git отсутствует текст {path}")
        body = objects.read(int(header[2])).decode("utf-8")
        if objects.read(1) != b"\n":
            raise ValueError(f"Ошибка чтения {path}")
        lines = [plain(line) for line in body.splitlines()]
        normalized = "\n".join(lines).casefold()
        if not all(word in normalized for word in words):
            continue
        title = next((line[2:] for line in lines if line.startswith("# ")), Path(path).name)
        counts = [sum(word in line.casefold() for word in words) for line in lines]
        best = counts.index(max(counts))
        lane, round_id = path.split("/")[:2]
        rank = (sum(word in title.casefold() for word in words), counts[best], int(round_id[5:]))
        hits[lane].append((rank, path, title, best + 1))
    for lane, found in hits.items():
        print(f"\n{lane} · совпадений в отчётах: {len(found)}")
        for _, path, title, line in sorted(found, reverse=True)[:8]:
            print(f"• {title}\n  {base_url}{quote(path)}#L{line}")


def main(revision, query=None):
    if revision is None:
        git("fetch", "--no-tags", "--no-recurse-submodules", "--no-write-fetch-head",
            "--refmap=", "origin", f"+refs/heads/{BRANCH}:{REMOTE_REF}")
        revision = REMOTE_REF
    commit = git("rev-parse", "--verify", "--end-of-options", revision + "^{commit}").strip()
    prefix = git("rev-parse", "--show-prefix").strip()
    readme = git("show", f"{commit}:{prefix}README.md")
    listing = git("ls-tree", "--full-tree", "-r", "-z", "--name-only", commit)
    files = {posixpath.relpath(path, prefix) for path in listing.rstrip("\0").split("\0")}
    has_table, active = tasks(readme, files)
    reports = latest_reports(readme, files)
    base_url = f"https://github.com/gvakhrushev/d0_15/blob/{commit}/{quote(prefix)}"
    print(f"Пилот D0 → ОТО · снимок Git {commit}")
    print(f"Реестр: {base_url}README.md\n\nАктивные вопросы")
    if not has_table:
        print("В этом снимке таблица назначений ещё отсутствует.")
    if has_table and not active:
        print("Открытых вопросов в таблице нет.")
    for key, (label, question, owner, base) in active.items():
        print(f"• {label} — {question}\n  Владелец: {owner}" + (f". База: {base}" if base else ""))
        for group, paths in partial_reports(key, files).items():
            print(f"  Материалы в Git · {group}")
            for path in paths:
                note = git("show", f"{commit}:{prefix}{path}")
                title = re.search(r"^# (.+)$", note, re.M)
                print(f"    {plain(title[1]) if title else posixpath.basename(path)}\n"
                      f"    {base_url}{quote(path)}")
    print("\nПоследние доступные отчёты")
    for lane, mode in (("direct", "A · Directed"), ("open", "B · Open")):
        if lane in reports:
            print(f"• {mode} — {base_url}{quote(reports[lane])}")
        else:
            print(f"• {mode} — в этом снимке отчёт не найден.")
    if query is not None:
        search_reports(commit, prefix, files, query, base_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", metavar="REV", help="прочитать локальный Git-снимок без сети")
    parser.add_argument("--find", metavar="СЛОВА", help="найти все слова в тексте отчёта обоих режимов")
    try:
        args = parser.parse_args()
        main(args.revision, args.find)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Не удалось прочитать статус пилота. {exc}")
