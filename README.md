<div align="center">

# 🛡️ SOC Events Cheat Sheet

### Справочник событий Windows / Linux и мониторинга атак

Рабочая шпаргалка для **SOC-аналитиков**, **Threat Hunter'ов** и **IR-инженеров** на русском языке.
Событие → что оно значит → индикаторы атаки → SPL-запрос → корреляции → MITRE ATT&CK.

![Language](https://img.shields.io/badge/язык-Русский-blue)
![Events](https://img.shields.io/badge/Event_ID-144-critical)
![Sheets](https://img.shields.io/badge/разделов-22-informational)
![Storylines](https://img.shields.io/badge/цепочек_атак-15-orange)
![Tools](https://img.shields.io/badge/инструментов-264-green)
![Platform](https://img.shields.io/badge/Windows-Linux-lightgrey)
![MITRE](https://img.shields.io/badge/MITRE-ATT%26CK-red)

### 🔎 [**Открыть интерактивный поиск →**](https://5yn7hp0w3r.github.io/soc-events-cheatsheet/) &nbsp;·&nbsp; 🌐 [**LOL Links →**](https://5yn7hp0w3r.github.io/soc-events-cheatsheet/lol-links.html)

Поиск по Event ID, IoC, SPL-запросам · фильтры по категории, важности и MITRE ATT&CK · раздельно ⚔️ Атака / 🛡️ Защита · работает в браузере, без установки.

</div>

---

## 📖 О проекте

Это структурированный справочник по событиям безопасности **Windows** и **Linux**, собранный для русскоязычного комьюнити по кибербезопасности. Он помогает быстро ответить на главные вопросы аналитика при разборе инцидента:

> Что это за событие? Насколько оно важно? Это атака или норма? Какие поля смотреть? Как его найти в SIEM? С чем оно связано?

Справочник ориентирован в первую очередь на **новичков** — тех, кто только входит в SOC, threat hunting и DFIR, — и на всех, кто устал искать информацию по десяткам вкладок, статей и англоязычных доков. Здесь **всё собрано в одном месте** и на русском: от расшифровки одного Event ID до готовой цепочки атаки. Не нужно держать в голове сотни номеров событий — открыл, нашёл, понял, применил.

Каждое событие описано на русском, снабжено **индикаторами атаки (IoC)**, привязкой к **MITRE ATT&CK**, готовыми **SPL-шаблонами** для поиска и **корреляциями** с другими событиями для восстановления цепочки атаки.

## ✨ Что внутри

- **144 события Windows** — полный реестр Event ID с важностью, частотой, IoC и false-positive
- **События, сгруппированные по функциям** — входы, управление учётками, процессы, аудит доступа, discovery/PowerShell, сеть, RDP, Sysmon, Active Directory, Defender
- **15 storyline-цепочек** — типовые сценарии атак, разложенные по шагам и размеченные по MITRE ATT&CK (в детализации — 90+ шагов с SPL-логикой)
- **43 события Linux** — auditd / journald / syslog с командами проверки через CLI
- **45 форензик-артефактов Windows** — где искать следы, чем анализировать, пример применения
- **264 инструмента** — 74 атакующих (с process names и Event ID) + 190 защитников (EDR/XDR, SIEM, NDR, DFIR, WAF, VM, AppSec, anti-DDoS, IdM + отечественные вендоры: Positive Technologies, SolidLab, Kaspersky, BI.ZONE, Солар, F6, InfoWatch, UserGate…)
- **Справочники** — LogonType, NTSTATUS-коды ошибок (4625 и полный реестр из 64 кодов)

## 🗂️ Навигация по разделам

### 🪟 Windows — события по функциональным группам

| # | Раздел | Событий | Описание |
|:--:|:--|:--:|:--|
| 02 | [🔐 Logon](MD/02_1Logon.md) | 15 | Входы/выходы: `4624` `4625` `4634` `4648` `4672` `4768/4769/4776` `4778/4779` `4740/4767`. Аутентификация + Special Groups и Credential Manager |
| 03 | [👤 Management](MD/03_2Management.md) | 15 | Учётки и группы: `4720` `4722` `4724` `4725/4726` `4728/4732/4756` `4738` `7045`. Поиск backdoor-аккаунтов и persistence |
| 04 | [⚙️ Process & Tasks](MD/04_3ProcessTasks.md) | 15 | Процессы и задачи: `4688/4689` `4697/4698/4702`, WMI `5857/5861`, AppLocker `8003/8004`, WDAC `3076/3077`. Execution + persistence |
| 05 | [📂 Audit-access](MD/05_4Audit-access.md) | 16 | Доступ к объектам: `4656` `4657` `4660` `4663` `4670` `4719` `5140/5145/5156`. Exfil, ransomware, file-monitoring |
| 06 | [🔎 Discovery / PowerShell](MD/06_5Discovery-powershell.md) | 7 | PowerShell-аудит: `4103` (Module) `4104` (ScriptBlock) `4105/4106`. Discovery-активность |
| 07 | [🌐 System & Network](MD/07_6System-Network.md) | 11 | Системные/сетевые: `1102` `4608/4616` `4946/4947` `5157`, BITS `59`, WinRM `91/168`. Сокрытие следов, firewall |
| 08 | [🖥️ RDP](MD/08_7RDP.md) | 8 | RDP: `1149` `4624 LT=10` `4778/4779` `1158` `1024`. Lateral movement внутри периметра |
| 09 | [🧬 Sysmon](MD/09_8Sysmon.md) | 30 | Sysmon ID 1–29: process create, network, image load, named pipes, DNS, WMI, file create. Глубокий endpoint-аудит |
| 10 | [🏢 Active Directory](MD/10_9Active-Directory.md) | 21 | Kerberos `4768/4769/4771`, DCSync `4662/5136`, учётки компьютеров `4741/4742`, доверия `4706/4707`, CA `4897`, разведка `4798/4799` |
| 11 | [🦠 Windows Defender](MD/11_10Windows-Defender.md) | 15 | Детекты `1116–1119/1006`, tampering `5001/5007/5010`, восстановление `1009`, очистка истории `1013`. Defense Evasion + антифорензика |

### 📚 Сводные реестры и справочники

| # | Раздел | Записей | Описание |
|:--:|:--|:--:|:--|
| 12 | [📋 WinEvents_ALL](MD/12_WinEvents_ALL.md) | 144 | **Главный лист.** Полный реестр Event ID: IoC, False Positive, MITRE TTP, ключевые поля, SPL-шаблоны, корреляции, ссылки на Microsoft Docs |
| 13 | [⭐ Popular events](MD/13_Popular%20events.md) | 21 | Выжимка самых частых событий для L1-аналитика — быстрый старт, только топовые Event ID |
| 14 | [🔑 Logon types](MD/14_Logon%20types.md) | 11 | Типы входа (LogonType 2–13): Interactive, Network, Batch, Service, RemoteInteractive (RDP)… |
| 15 | [❌ Error_4625](MD/15_Error_4625.md) | 11 | Sub_Status коды отказа 4625: `0xC0000064` `0xC000006A` `0xC0000234`… Отличить brute-force от spraying |
| 16 | [⚠️ Error_ALL](MD/16_Error_ALL.md) | 64 | Полный справочник NTSTATUS: hex+dec, категория, значение для SOC, рекомендации |
| 22 | [🧾 Описание колонок](MD/22_Описание%20колонок.md) | 19 | Легенда колонок для WinEvents_ALL и Error_ALL |

### 🎯 Атаки, форензика и инструменты

| # | Раздел | Записей | Описание |
|:--:|:--|:--:|:--|
| 17 | [🧩 Storylines](MD/17_Storylines.md) | 15 | Цепочки атак по MITRE ATT&CK / Kill Chain: brute-force, Kerberoasting, DCSync, lateral movement, ransomware… Сводка + пошаговая детализация с Event ID и IoC |
| 18 | [🔬 Forensics WIN](MD/18_Forensics_WIN.md) | 45 | Артефакты: реестр (Run, ShimCache, AmCache), prefetch, `$MFT`, journal, LNK/Jump Lists. Расположение + инструмент + пример |
| 21 | [⚔️ Инструменты атакующих](MD/21_Инструменты%20атакующих.md) | 74 | Evilginx, Cobalt Strike, Mimikatz, AdFind, RMM-abuse, AADInternals, web-shells… Процессы, MITRE TTP, Event ID, паттерны |
| 20 | [🛡️ Инструменты защитников](MD/20_Инструменты%20защитников.md) | 190 | EDR/XDR, SIEM, NDR, forensics, TI, anti-DDoS, IdM + отечественные (Positive, Kaspersky, BI.ZONE, Солар, F6, UserGate, InfoWatch…) |

### 🐧 Linux

| # | Раздел | Событий | Описание |
|:--:|:--|:--:|:--|
| 19 | [🐧 LINUX](MD/19_LINUX.md) | 43 | Sysmon for Linux (eBPF), auditd (`EXECVE/SYSCALL`), journald, PAM, SSH, sudo, cron, systemd. IoC, CLI-проверки (`journalctl`/`ausearch`), MITRE, SPL |

## 📦 Форматы данных

Справочник доступен в трёх форматах — выбирайте под свою задачу:

| Формат | Папка | Для чего |
|:--|:--|:--|
| 📊 **Excel** | [`Events-cheatsheet-SOC.xlsx`](Events-cheatsheet-SOC.xlsx) | Исходник: 22 листа с фильтрами и цветовой разметкой |
| 📝 **Markdown** | [`MD/`](MD/) | Читать прямо на GitHub, копировать в заметки |
| 🧷 **JSON** | [`json/`](json/) | Импорт в SIEM, скрипты, автоматизация |

## 🚀 Как пользоваться

1. **Разбираете инцидент?** Найдите Event ID в [📋 WinEvents_ALL](MD/12_WinEvents_ALL.md) или в профильном разделе выше.
2. **Смотрите колонки** «Индикаторы атаки», «False Positive» и «Корреляции» — они отвечают на вопрос «атака или норма».
3. **Копируйте SPL-шаблон** из карточки события прямо в Splunk / SIEM.
4. **Восстанавливаете картину атаки?** Загляните в [🧩 Storylines](MD/17_Storylines.md) — там цепочки событий по шагам с привязкой к MITRE ATT&CK.
5. **Нашли подозрительный процесс?** Проверьте его в [⚔️ Инструментах атакующих](MD/21_Инструменты%20атакующих.md) — там имена процессов и связанные Event ID.

> 💡 Не помните, что значит колонка? Всё расшифровано в разделе [🧾 Описание колонок](MD/22_Описание%20колонок.md).

## 🤝 Вклад в проект

Проект развивается силами комьюнити. Заметили ошибку, знаете полезный Event ID, IoC или storyline — welcome:

- 🐛 Откройте **Issue** с описанием
- 🔧 Пришлите **Pull Request** (правьте исходный `.xlsx`, а Markdown/JSON перегенерируются)
- ⭐ Поставьте звезду, если справочник оказался полезен

## ⚖️ Дисклеймер

Материал предназначен исключительно для **защиты**, обучения и легального анализа инцидентов. Раздел с инструментами атакующих приведён для понимания следов, которые они оставляют в логах, — и только для авторизованного использования.

## 🤖 Использование ИИ

При создании этого справочника, интерактивного поиска ([`index.html`](index.html)) и страницы GitHub Pages использовался искусственный интеллект. Данные проверяются и дополняются вручную — если заметили неточность, пожалуйста, откройте Issue или Pull Request.

---

<div align="center">

Сделано ❤️ для русскоязычного комьюнити по информационной безопасности

</div>
