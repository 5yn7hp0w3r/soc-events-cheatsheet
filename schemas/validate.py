#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверяет данные справочника перед публикацией.
Запуск локально:  python3 schemas/validate.py
В CI запускается автоматически на каждый PR и push.

Что проверяет:
  1. Все файлы в json/ — валидный JSON (нет висячих запятых, кавычки на месте).
  2. Инструменты (атака/защита) и события Windows — соответствуют схеме
     (обязательные поля на месте, «Важность» из допустимого списка и т.д.).
Строки-заголовки (без name / Event ID) пропускаются — это не записи.
"""
import json, os, sys, glob

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("Нужен пакет jsonschema:  pip install jsonschema", file=sys.stderr)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(ROOT, "json")
SCHEMA_DIR = os.path.join(ROOT, "schemas")
errors = []


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# 1) все json валидны
for f in sorted(glob.glob(os.path.join(JSON_DIR, "*.json"))):
    try:
        load(f)
    except Exception as e:
        errors.append("%s — невалидный JSON: %s" % (os.path.basename(f), e))

# 2) схемы для ключевых файлов
def check(fname, key, schema_file, label):
    path = os.path.join(JSON_DIR, fname)
    if not os.path.exists(path):
        return
    try:
        data = load(path)
    except Exception:
        return  # уже зафиксировано выше
    validator = Draft7Validator(load(os.path.join(SCHEMA_DIR, schema_file)))
    for rec in data:
        if not isinstance(rec, dict):
            continue
        kv = rec.get(key)
        if kv is None or (isinstance(kv, str) and not kv.strip()):
            continue  # заголовок / мета-строка — пропускаем
        for err in validator.iter_errors(rec):
            where = " → ".join(str(p) for p in err.absolute_path) or "запись"
            errors.append("%s [%s «%s»]: %s (%s)" % (fname, label, rec.get(key), err.message, where))

check("Инструменты_атакующих.json", "name", "tool.schema.json", "атака")
check("Инструменты_защитников.json", "name", "tool.schema.json", "защита")
check("WinEvents_ALL.json", "Event ID", "event.schema.json", "событие")

if errors:
    print("❌ Найдены ошибки (%d):" % len(errors))
    for e in errors:
        print("   •", e)
    print("\nИсправь их и попробуй снова. Подробности — в CONTRIBUTING.md")
    sys.exit(1)

print("✅ Все проверки пройдены — данные корректны.")
