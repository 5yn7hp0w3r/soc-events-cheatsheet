#!/usr/bin/env python3
"""
build.py — собирает data.js для интерактивного поиска (index.html) из папки json/.

Что делает:
  1. Берёт json/all.json как основу (все листы книги).
  2. Подменяет лист «Инструменты атакующих» чистой версией из json/Инструменты_атакующих.json.
  3. Нормализует лист «Инструменты защитников» из json/Инструменты_защитников.json
     (понимает и «сырой» формат col_1..col_9, и чистый формат с ключом name).
  4. Пишет результат в data.js  (window.SOC_DATA = {...};).

Запуск:  python3 build.py
После сборки: git add data.js json/ && git commit && git push  → сайт обновится сам.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(ROOT, "json")


def load(name):
    with open(os.path.join(JSON_DIR, name), encoding="utf-8") as f:
        return json.load(f)


# порядок колонок «сырого» листа защитников (Excel → col_N)
DEF_COLS = {
    "id":            "Инструменты защитников",
    "category":      "col_1",
    "name":          "col_2",
    "type":          "col_3",
    "platform":      "col_4",
    "description":   "col_5",
    "process_names": "col_6",
    "d3fend":        "col_7",
    "capabilities":  "col_8",
    "reference":     "col_9",
}
DEF_CLEAN_KEYS = list(DEF_COLS.keys())


def clean_defenders(raw):
    """Нормализует записи защитников. Пропускает заголовок/описание сверху."""
    out = []
    for r in raw:
        if r.get("name"):                       # уже чистая строка (добавлена вручную)
            out.append({k: r.get(k) for k in DEF_CLEAN_KEYS})
            continue
        idv = str(r.get(DEF_COLS["id"]) or "").strip()
        if not idv.isdigit():                   # строка-заголовок / описание — пропускаем
            continue
        out.append({k: r.get(col) for k, col in DEF_COLS.items()})
    return out


def main():
    data = load("all.json")

    # 1) атакующие — чистый файл целиком
    attackers = load("Инструменты_атакующих.json")
    data["Инструменты атакующих"] = attackers

    # 2) защитники — нормализуем
    defenders = clean_defenders(load("Инструменты_защитников.json"))
    data["Инструменты защитников"] = defenders

    # 2b) storylines — чистая версия из standalone (в all.json колонки битые)
    data["Storylines"] = load("Storylines.json")

    # 3) пишем data.js
    out_path = os.path.join(ROOT, "data.js")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("window.SOC_DATA = ")
        json.dump(data, f, ensure_ascii=False)
        f.write(";")

    # сводка
    n_atk = sum(1 for r in attackers if r.get("name"))
    n_def = sum(1 for r in defenders if r.get("name"))
    n_win = len([r for r in data.get("WinEvents_ALL", []) if r.get("Event ID")])
    size_kb = os.path.getsize(out_path) // 1024
    print("✓ data.js собран  ({} КБ)".format(size_kb))
    print("  Windows Event ID : {}".format(n_win))
    print("  Инструменты атаки : {}".format(n_atk))
    print("  Инструменты защиты: {}".format(n_def))
    if not n_atk or not n_def:
        print("⚠ ВНИМАНИЕ: один из списков инструментов пуст — проверь JSON!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
