# Раздел: Storylines (цепочки атак)

> Типовые цепочки атак по MITRE ATT&CK / Cyber Kill Chain: сводка + пошаговая детализация с Event ID, ключевыми полями и логикой корреляции.

**Всего цепочек: 24**

## Сводка

| # | Категория | Название | Цепочка событий | MITRE |
|:--:|:--|:--|:--|:--|
| 1 | Initial Access / Credential Access | **Brute-force → успешный вход** | 4625 (×N) → 4740 → 4767 → 4624 | TA0006 / T1110, T1110.001, T1110.003 |
| 2 | Credential Access | **Password Spraying по домену** | 4625 (много юзеров) → 4768 fail → 4624 успех | TA0006 / T1110.003 |
| 3 | Credential Access | **Kerberoasting** | 4624 LT=3 → 4768 → 4769 (RC4, SPN) → 4688 (Rubeus/PS) | TA0006 / T1558.003 |
| 4 | Credential Access | **AS-REP Roasting** | 4768 (Pre-Auth=0, RC4) → 4769 → 4624 LT=3 | TA0006 / T1558.004 |
| 5 | Credential Access | **DCSync (кража хешей через репликацию)** | 4624 LT=3 (на DC) → 4662 (DRS GUID) → 4742 | TA0006 / T1003.006 |
| 6 | Lateral Movement / Execution | **PSExec (admin share + service install)** | 5140 (ADMIN$) → 4624 LT=3 → 4672 → 4688 (psexec.exe) → 4697/7045 | TA0008 / T1021.002, T1569.002, T1543.003 |
| 7 | Lateral Movement / Execution | **WMI / WMIC Remote Execution** | 4624 LT=3 → 4672 → 4688 (wmic.exe / WmiPrvSE.exe) | TA0008 / T1021.006, T1047 |
| 8 | Lateral Movement | **RDP-перемещение внутри сети** | 4624 LT=10 → 1149 → 4778 → 4688 (mstsc.exe) | TA0008 / T1021.001 |
| 9 | Lateral Movement / Persistence | **Pass-the-Hash (NTLM)** | 4776 → 4624 LT=3 (NTLM, AuthPkg=NTLM) → 4672 | TA0008 / T1550.002 |
| 10 | Persistence / Privilege Escalation | **Backdoor-аккаунт в Domain Admins** | 4720 → 4722 → 4724 → 4728/4732 (Domain Admins) → 4738 | TA0003+TA0004 / T1136.002, T1098, T1078.002 |
| 11 | Persistence | **Scheduled Task как backdoor** | 4688 (schtasks.exe) → 4698 → 4624 LT=5 → 4688 (из задачи) | TA0003 / T1053.005 |
| 12 | Privilege Escalation | **UAC bypass / runas escalation** | 4624 LT=2 → 4648 → 4672 → 4688 (Token Elev=1) | TA0004 / T1548.002, T1134 |
| 13 | Defense Evasion | **Очистка журналов и отключение аудита** | 4688 (wevtutil/PS) → 4719 → 1102 → (тишина) | TA0005 / T1070.001, T1562.002 |
| 14 | Defense Evasion / Impact | **Ransomware-паттерн (shadow copies + файлы)** | 4688 (vssadmin/wbadmin) → 4663 (массовые write/delete) → 4946 → 7045 | TA0040 / T1490, T1486, T1562.004 |
| 15 | Credential Access / Lateral Movement | **Pass-the-Cert (PKINIT)** | 4886/4887 (CA) → 4768 (Cert Info) → 4769 → 4624 LT=3 | TA0006+TA0008 / T1550.003, T1649 |
| 16 | Credential Access / Privilege Escalation | **Golden Ticket (подделка TGT)** | 4662/DCSync (krbtgt) → 4769 (без 4768) → 4624 LT=3 | TA0006 / T1558.001 |
| 17 | Credential Access | **Silver Ticket (подделка TGS)** | хеш сервисной/машинной учётки → доступ к сервису БЕЗ 4768/4769 на DC → 4624 на целевом хосте | TA0006 / T1558.002 |
| 18 | Initial Access / Execution | **Фишинг → выполнение макроса → C2** | письмо → 4688 (Office → cmd/powershell) → 4104 → Sysmon 3 (C2) | TA0001 / T1566.001, T1204.002, T1059.001 |
| 19 | Execution / Defense Evasion | **LOLBin-доставка payload (certutil / bitsadmin)** | 4688 (certutil/bitsadmin с URL) → 4688 (payload из TEMP) → 4104 / Sysmon 3 | TA0002 / T1105, T1218 |
| 20 | Credential Access / Lateral Movement | **Дамп LSASS → боковое перемещение** | Sysmon 10 / 4656 (lsass) → 4663 (.dmp) → 4624 LT=3 (другой хост) → 4672 | TA0006 / T1003.001, T1550, T1021 |
| 21 | Persistence / Execution | **Вредоносная служба → закрепление / C2** | 7045 → 4697 → 4688 (services.exe → payload) → Sysmon 3 | TA0003 / T1543.003, T1569.002 |
| 22 | Initial Access / Persistence | **Web-shell → выполнение команд (Exchange / IIS)** | эксплойт → Sysmon 11 (файл в wwwroot) → 4688 (w3wp → cmd) → 4688 (recon) | TA0001 / T1190, T1505.003, T1059 |
| 23 | Credential Access / Privilege Escalation | **Shadow Credentials → PKINIT** | 5136 (msDS-KeyCredentialLink) → 4662 → 4768 (PKINIT, cert) → 4624 | TA0006 / T1556, T1558 |
| 24 | Privilege Escalation / Credential Access | **PetitPotam → NTLM-relay → AD CS (ESC8)** | 5145 (принуждение MS-EFSR) → 4624 (relay DC$ на CA) → 4887 (выдан сертификат) → 4768 PKINIT → 4662 (DCSync) | TA0004 / T1187, T1557.001, T1649 |

## Детализация по шагам

### 1. Brute-force → успешный вход

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 1.1 | 4625 | Reconnaissance → Access | Повторяющиеся неудачные попытки входа с одного источника на одну учётку | TargetUserName=victim, IpAddress=ext, SubStatus=0xC000006A (неверный пароль), LogonType=3/10 |
| 1.2 | 4740 | Lockout | Учётка заблокирована политикой | TargetUserName, CallerComputerName (откуда вызван локаут) |
| 1.3 | 4767 | Unlock | Админ (или скомпрометированный привилегированный аккаунт) разблокировал учётку | TargetUserName=victim, SubjectUserName=admin |
| 1.4 | 4624 | Success | Успешный вход после множества 4625 | TargetUserName=та же, IpAddress=тот же или рядом, LogonType=3/10 |

> 🎯 **Итоговая корреляция:** Связь этапов в единый alert (Окно: 1 час; порог 4625: >10; последовательность обязательная)

### 2. Password Spraying по домену

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 2.1 | 4625 | Access (spray) | 1–2 неудачные попытки на множестве учёток | Один IpAddress; >20 разных TargetUserName за 10 мин; часто с веба/OWA/RDG |
| 2.2 | 4768 | Kerberos pre-auth fail | TGT отказ в выдаче (Result Code 0x18) | Result_Code=0x18; Client_Address; Service_Name=krbtgt |
| 2.3 | 4624 | Success | Первый успех с того же IP | IpAddress = из 4625; LogonType=3/10 |

> 🎯 **Итоговая корреляция:** Spray-источник + успех (Окно: 30 мин; мин. 20 учёток в 4625)

### 3. Kerberoasting

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 3.1 | 4624 | Access | Вход атакующего под любым доменным аккаунтом | LogonType=3, TargetUserName — любой доменный юзер |
| 3.2 | 4768 | TGT (опц) | Запрос TGT | Result_Code=0x0, Encryption Type=0x12 (легит) или 0x17 |
| 3.3 | 4769 | TGS Request (KEY) | Запрос TGS для сервисных счетов с RC4 | Ticket_Encryption_Type=0x17 (RC4); Service_Name!=krbtgt; много разных SPN в окне |
| 3.4 | 4688 | Execution (инструмент) | Запуск Rubeus / Invoke-Kerberoast / GetUserSPNs.py | CommandLine contains "kerberoast", "asktgs", "-rc4", "GetUserSPNs"; Image=powershell/rubeus |

> 🎯 **Итоговая корреляция:** Массовый RC4 TGS с одного юзера + инструмент (Окно: 30 мин; порог SPN: ≥5 разных)

### 4. AS-REP Roasting

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 4.1 | 4768 | TGT без pre-auth (KEY) | Запрос TGT для учёток с отключённой предавтентификацией | Pre-Authentication Type=0 (выключена); Encryption Type=0x17; Result_Code=0x0 |
| 4.2 | 4688 | Execution | Rubeus asreproast / Get-ASREPHash | CommandLine contains "asreproast", "GetNPUsers", "ASRepCatcher" |
| 4.3 | 4624 | Access (взлом offline → вход) | Вход под скомпрометированным аккаунтом | TargetUserName — из 4768 с Pre-Auth=0 |

> 🎯 **Итоговая корреляция:** Обычно самого 4768 с PreAuth=0 достаточно — это строгий IoC (Базовый фон должен быть малый; исключить легитимные аккаунты)

### 5. DCSync (кража хешей через репликацию)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 5.1 | 4624 | Access на DC | Вход на контроллер домена | LogonType=3, хост — DC; Account с Replicating Directory Changes |
| 5.2 | 4662 | Directory Service Access (KEY) | Доступ к объекту с расширенными правами репликации | Properties: 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2 (DS-Replication-Get-Changes) или 1131f6ad-... (DS-Replication-Get-Changes-All) |
| 5.3 | 4688 | Execution | mimikatz / DSInternals / impacket secretsdump | CommandLine: lsadump::dcsync, secretsdump, Get-ADReplAccount |

> 🎯 **Итоговая корреляция:** Любой 4662 с DS-Replication GUID от не-DC или не-белого аккаунта — инцидент (Белый список: AAD Connect, все DC; всё остальное — подозрительно)

### 6. PSExec (admin share + service install)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 6.1 | 5140 | Lateral Movement (admin share) | Подключение к ADMIN$ / IPC$ — копирование бинарника | ShareName=\\\\*\\ADMIN$, AccessMask=0x100081; SourceAddress=внутренний |
| 6.2 | 4624 | Network Logon | Сетевой вход для разворачивания службы | LogonType=3, AuthenticationPackage=NTLM или Kerberos; ElevatedToken=Yes |
| 6.3 | 4672 | Privilege Use | Назначение специальных привилегий админу | SeDebugPrivilege, SeTcbPrivilege, SeImpersonate и др. |
| 6.4 | 4697/7045 | Service Install (KEY) | Создание службы PSEXESVC | Service_Name=PSEXESVC (или рандомный); Service_File_Name=*PSEXESVC.exe; Service_Type=user mode service |
| 6.5 | 4688 | Execution | Запуск PSEXESVC.exe и дочерних команд | ParentImage=PSEXESVC.exe; дочерние: cmd, powershell |

> 🎯 **Итоговая корреляция:** Admin share + Service install в коротком окне (Окно: 5 мин между 5140 и 4697; источник=тот же хост)

### 7. WMI / WMIC Remote Execution

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 7.1 | 4624 | Network Logon | Сетевой вход на целевой хост | LogonType=3; IpAddress — внутренний |
| 7.2 | 4672 | Privilege Use | Назначение привилегий | SubjectUserSid — элевация |
| 7.3 | 4688 | WMI Execution (KEY) | Запуск процесса через WmiPrvSE.exe | ParentImage=C:\\Windows\\System32\\wbem\\WmiPrvSE.exe; дочерние: powershell, cmd, rundll32, regsvr32 |
| 7.4 | 4688 | WMIC клиент (опц) | На исходном хосте: wmic /node:... | NewProcessName=*wmic.exe; CommandLine contains "/node:", "process call create" |

> 🎯 **Итоговая корреляция:** WmiPrvSE → опасный чайлд (WmiPrvSE сам по себе легитен, но не должен порождать оболочки)

### 8. RDP-перемещение внутри сети

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 8.1 | 4624 | Interactive Logon | RDP-вход | LogonType=10 (RemoteInteractive); IpAddress — внутренний |
| 8.2 | 1149 | RDP Session Start | TerminalServices: успешная аутентификация | User, SourceNetworkAddress; лог: Microsoft-Windows-TerminalServices-RemoteConnectionManager |
| 8.3 | 4778 | Session Reconnect (опц) | Переподключение к сессии | AccountName, ClientAddress; возможный перехват сессии |
| 8.4 | 4688 | Pivot | mstsc.exe из этой же RDP-сессии → следующий хост | NewProcessName=*mstsc.exe; ParentLogonId = LogonId из 4624 LT=10 |

> 🎯 **Итоговая корреляция:** RDP-chain через >=2 хоста (Окно: 1 час; юзер тот же; хосты разные; нерабочее время — бонус)

### 9. Pass-the-Hash (NTLM)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 9.1 | 4776 | NTLM Auth (KEY) | NTLM-валидация учётки | PackageName=NTLM/MICROSOFT_AUTHENTICATION_PACKAGE_V1_0; Workstation=источник |
| 9.2 | 4624 | Network Logon (KEY) | Сетевой вход с NTLM для доменной учётки | LogonType=3, AuthenticationPackageName=NTLM, LogonProcessName=NtLmSsp; TargetDomainName=DOMAIN (не WORKGROUP/local) |
| 9.3 | 4672 | Privilege Use | Элевация на целевом хосте | Привилегии SeDebug, SeImpersonate |

> 🎯 **Итоговая корреляция:** NTLM в домене — аномалия (Исключить legacy-системы; baseline NTLM/host)

### 10. Backdoor-аккаунт в Domain Admins

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 10.1 | 4720 | Persistence: Create | Создание новой учётки | TargetUserName, SubjectUserName (кто создал); имя похожее на системное: svc_*, admin$, helpdesk |
| 10.2 | 4722 | Enable | Активация учётки | TargetUserName=тот же |
| 10.3 | 4724 | Password Set | Сброс пароля админом | SubjectUserName=admin; TargetUserName=новый |
| 10.4 | 4728/4732/4756 | Group Add (KEY) | Добавление в Domain Admins / Administrators / Enterprise Admins | TargetGroupName=Domain Admins / Administrators / Enterprise Admins / Schema Admins; MemberName=новый юзер |

> 🎯 **Итоговая корреляция:** Создание + добавление в привилегированную группу < 5 мин (Быстрая последовательность — классический IoC; внерабочее время усиливает подозрение)

### 11. Scheduled Task как backdoor

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 11.1 | 4688 | Execution (создание) | Запуск schtasks.exe / PowerShell New-ScheduledTask | NewProcessName=*schtasks.exe; CommandLine="/create", "/sc", "/tr"; либо powershell New-ScheduledTask* |
| 11.2 | 4698 | Persistence (KEY) | Создание запланированной задачи | TaskName, TaskContent XML; в Actions виден Command и Arguments |
| 11.3 | 4624 | Trigger | Вход в качестве службы/батча из задачи | LogonType=5 (Service) или 4 (Batch); SubjectUserName=SYSTEM |
| 11.4 | 4688 | Execution задачи | ParentProcess=svchost.exe -k netsvcs → вредонос из задачи | ParentImage=*taskeng.exe или *svchost.exe; NewProcessName — из Task_Content |

> 🎯 **Итоговая корреляция:** TaskContent с подозрительным command line (Белый список: Adobe, Google Update, Microsoft Office)

### 12. UAC bypass / runas escalation

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 12.1 | 4624 | Interactive Logon | Обычный интерактивный вход юзера | LogonType=2, ElevatedToken=No |
| 12.2 | 4648 | Explicit Credentials (KEY) | Попытка входа с явными учётными данными (runas) | SubjectUserName и TargetUserName различаются; TargetServerName — текущий хост |
| 12.3 | 4672 | Privilege Use | Назначены SeDebug / SeTcb / SeImpersonate | Аномалия: обычный юзер получает такие привилегии |
| 12.4 | 4688 | Execution (элевация) | Процесс с TokenElevationType=1 (полный токен) от obj. юзера | Token_Elevation_Type=%%1936 (полный); ParentImage — fodhelper.exe, eventvwr.exe, sdclt.exe (типичные UAC bypass) |

> 🎯 **Итоговая корреляция:** Runas + элевация привилегий без админской истории (Окно: 5 мин; связка по LogonId)

### 13. Очистка журналов и отключение аудита

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 13.1 | 4688 | Execution (подготовка) | Запуск wevtutil.exe / PowerShell Clear-EventLog / auditpol.exe | CommandLine: wevtutil cl, Clear-EventLog, auditpol /clear, /set /category:* /success:disable |
| 13.2 | 4719 | Defense Evasion | Изменена системная политика аудита | Аномалия: изменение вне GPO; отключение категорий Logon/Account Management/Process Creation |
| 13.3 | 1102 | Defense Evasion (главный) | Журнал Security очищен | Любое 1102 — инцидент. Account = кто очистил. Сравнить с окном тишины после |
| 13.4 | (любое) | Detection-by-absence | Пропажа событий 4624/4688 после 1102 — вероятно и аудит выключен | Счётчик 4624/час резко падает ниже baseline |

> 🎯 **Итоговая корреляция:** Полная цепь сокрытия следов (Окно: 30 мин; связь по Computer + User)

### 14. Ransomware-паттерн (shadow copies + файлы)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 14.1 | 4688 | Inhibit Recovery | Удаление теневых копий и backup catalog | CommandLine: vssadmin delete shadows /all, wbadmin delete catalog, wmic shadowcopy delete, bcdedit /set recoveryenabled No |
| 14.2 | 4688/4946 | Defense Evasion | Отключение Defender / изменение firewall (4946) | Set-MpPreference -DisableRealtimeMonitoring; netsh advfirewall set ... state off; добавление исключений |
| 14.3 | 4663 | Impact (шифрование) | Массовое WriteData/DeleteFile в файловых share-ах | AccessMask 0x2/0x10000 (Write/Delete) по тысячам файлов за минуты; новые расширения (.locked, .enc, random) |
| 14.4 | 4697/7045 | Service Install (опц.) | Размещение ransomware-бинаря как службы для исполнения по всему домену | ServiceFile в ProgramData/Temp; случайное имя; запуск на десятках хостов |

> 🎯 **Итоговая корреляция:** Спарка vssadmin + шторм письма = ransomware (Окно: 10 мин после vssadmin)

### 15. Pass-the-Cert (PKINIT)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 15.1 | 4662 | Resource Discovery | Перечисление ADCS-шаблонов (Certify, certipy enumerate) — поиск vulnerable templates (ESC1–ESC11) | ObjectType=pKICertificateTemplate; SubjectUserName — обычный юзер; много LDAP-запросов к CN=Certificate Templates |
| 15.2 | 4886 | Certificate Request | Запрос сертификата на CA (с SAN/UPN жертвы — ESC1) | Requester — одна учётка, SAN/UPN в запросе — другая (часто — Domain Admin); Template Name — один из уязвимых |
| 15.3 | 4887 | Certificate Issued | CA выдала сертификат с EKU Client Authentication | Disposition=Issued; Certificate Hash — записываем в baseline для дальнейшего сопоставления |
| 15.4 | 4768 | PKINIT Pre-Auth | TGT запрошен с PKINIT — в 4768 заполнен Certificate Issuer/Serial/Thumbprint | Certificate Issuer Name и Certificate Serial Number заполнены (обычно эти поля пусты!); IP клиента — внутренний, не DC; время — вблизи 4886/4887 |
| 15.5 | 4769 → 4624 | Lateral / Privilege Use | TGS на сервисы и вход LogonType=3 под именем жертвы (часто — Domain Admin) | TargetUserName из 4624 = UPN из сертификата; LogonId связан с 4768/PKINIT |

> 🎯 **Итоговая корреляция:** Выдача сертификата с «чужим» SAN + быстрый PKINIT-вход под этим именем (Окно: 30 мин от выдачи до PKINIT-входа; особенно опасно для Tier-0 учёток)

### 16. Golden Ticket (подделка TGT)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 16.1 | 4662 | Preparation | Получение хеша учётки krbtgt (обычно через DCSync — см. цепочку «DCSync») | ObjectType=DS-Replication-Get-Changes |
| 16.2 | 4769 | Forge & Use | Запрос сервисных билетов (TGS) без предшествующего AS-REQ (4768) для той же учётки — TGT подделан, DC его не выдавал | TicketEncryptionType=0x17 (RC4), ServiceName |
| 16.3 | 4769 | Anomaly | Аномальное время жизни билета или несуществующая/отключённая учётка внутри билета | TargetUserName отсутствует в AD, TicketOptions |
| 16.4 | 4624 | Access | Доступ к ресурсам с поддельным билетом | LogonType=3, в истории нет парного 4768 |

> 🎯 **Итоговая корреляция:** 4769 без парного 4768 для учётки + RC4 + доступ к критичным ресурсам (Окно: сессия; признак — 4769 без 4768, TGT-lifetime > политики домена)

### 17. Silver Ticket (подделка TGS)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 17.1 | — | Prereq | Получен NTLM-хеш сервисной или машинной учётной записи (напр. через дамп) | цель — конкретный сервис (CIFS/HOST/MSSQL) |
| 17.2 | 4624 | Forge & Use | Доступ к сервису с поддельным TGS — обращения к DC нет (нет 4768/4769) | LogonType=3, ServiceName=целевой хост |
| 17.3 | 4624 | Anomaly | На контроллере домена отсутствуют парные Kerberos-события для этого доступа | рассинхрон: доступ на хосте есть, TGS на DC нет |

> 🎯 **Итоговая корреляция:** Доступ к сервису (4624 LT=3) при отсутствии соответствующих 4768/4769 на DC (Сравнение логов целевого хоста и DC за окно сессии)

### 18. Фишинг → выполнение макроса → C2

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 18.1 | — | Delivery | Фишинговое письмо с вложением (docm/xlsm) или ссылкой | источник — почтовый шлюз / прокси |
| 18.2 | 4688 | Execution | Офисное приложение порождает интерпретатор: WINWORD.EXE/EXCEL.EXE → cmd.exe/powershell.exe/mshta.exe | ParentProcessName=WINWORD.EXE, ProcessName=powershell.exe |
| 18.3 | 4104 | Script | Подозрительный ScriptBlock: -enc / -nop / DownloadString / IEX | ScriptBlockText (base64, IEX, http) |
| 18.4 | — | C2 | Исходящее соединение к C2 от порождённого процесса (Sysmon Event 3) | DestinationIp/Port, редкий домен |

> 🎯 **Итоговая корреляция:** Office → интерпретатор + подозрительный 4104 + исходящее соединение в короткое окно (Окно: 5 мин; последовательность обязательна)

### 19. LOLBin-доставка payload (certutil / bitsadmin)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 19.1 | 4688 | Ingress | Загрузка через доверенный бинарь: certutil -urlcache -f http… / bitsadmin /transfer / curl | ProcessName=certutil.exe, CommandLine содержит URL |
| 19.2 | 4688 | Execution | Запуск загруженного payload (rundll32/regsvr32/mshta или сам .exe из %TEMP%) | ParentProcessName, ProcessName из %TEMP% |
| 19.3 | 4104 | Script / C2 | PowerShell-загрузчик (IEX) и/или исходящее соединение | ScriptBlockText, Sysmon Event 3 |

> 🎯 **Итоговая корреляция:** Доверенный бинарь с URL в командной строке + запуск из TEMP + исходящее соединение (Окно: 10 мин)

### 20. Дамп LSASS → боковое перемещение

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 20.1 | 4656 | Access | Запрос доступа к процессу lsass.exe (или Sysmon Event 10 ProcessAccess) | ObjectName=lsass.exe, GrantedAccess=0x1010/0x1410 |
| 20.2 | 4663 | Dump | Создание дампа памяти lsass (procdump/comsvcs/nanodump) | ProcessName, файл .dmp |
| 20.3 | 4624 | Reuse | Вход на другом хосте с добытыми учётными данными (pass-the-hash/ticket) | LogonType=3/9, AuthenticationPackage |
| 20.4 | 4672 | Escalate | Привилегированный вход на новом хосте | SeDebugPrivilege и др. |

> 🎯 **Итоговая корреляция:** Доступ к lsass с подозрительной маской + дамп-файл + вход на другом хосте той же учёткой (Окно: 30 мин; коррелировать хосты)

### 21. Вредоносная служба → закрепление / C2

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 21.1 | 7045 | Install | Установлена новая служба с подозрительным путём/именем | ServiceName, ImagePath (%TEMP%, cmd /c, powershell -enc) |
| 21.2 | 4697 | Audit | Установка службы в Security-логе (если включён аудит) | ServiceName, ServiceFileName |
| 21.3 | 4688 | Exec | services.exe порождает payload службы | ParentProcessName=services.exe, ProcessName |
| 21.4 | — | C2 | Исходящее соединение от процесса службы (Sysmon Event 3) | DestinationIp |

> 🎯 **Итоговая корреляция:** 7045 с ImagePath в TEMP/скрипте + запуск от services.exe + исходящее соединение (Окно: 10 мин)

### 22. Web-shell → выполнение команд (Exchange / IIS)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 22.1 | — | Exploit | Эксплуатация уязвимости веб-приложения/Exchange (напр. ProxyShell) | IIS-логи: POST к аномальному URL |
| 22.2 | 11 | Drop | Создание файла веб-шелла в веб-каталоге (Sysmon Event 11) | TargetFilename в inetpub/wwwroot/aspnet_client, .aspx |
| 22.3 | 4688 | RCE | w3wp.exe (или дочерний) порождает cmd.exe/powershell.exe | ParentProcessName=w3wp.exe |
| 22.4 | 4688 | Recon | Через web-shell: whoami / ipconfig / net user | ProcessName=cmd/whoami, Parent=w3wp.exe |

> 🎯 **Итоговая корреляция:** Создание скрипта в веб-каталоге + w3wp как родитель интерпретатора (Окно: сессия)

### 23. Shadow Credentials → PKINIT

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 23.1 | 5136 | Write | Запись в атрибут msDS-KeyCredentialLink целевого объекта (Whisker/pyWhisker) | AttributeLDAPDisplayName=msDS-KeyCredentialLink, ObjectDN |
| 23.2 | 4662 | Audit | Операция над объектом каталога с изменением ключевого атрибута | ObjectType, AccessMask=Write Property |
| 23.3 | 4768 | PKINIT | Запрос TGT по сертификату (PKINIT) от имени цели | Certificate Information заполнено, PreAuthType=16/17 |
| 23.4 | 4624 | Access | Аутентификация под целевой учётной записью | LogonType=3 |

> 🎯 **Итоговая корреляция:** Изменение msDS-KeyCredentialLink + последующий 4768 с Certificate Information для той же цели (Окно: 1 час)

### 24. PetitPotam → NTLM-relay → AD CS (ESC8)

| Шаг | Event ID | Фаза | Описание | Ключевые поля / IoC |
|:--|:--|:--|:--|:--|
| 24.1 | 5145 | Coerce | Принуждение аутентификации DC через MS-EFSR/MS-RPRN (PetitPotam/PrinterBug) | ShareName=IPC$, RelativeTargetName=efsrpc/spoolss |
| 24.2 | 4624 | Relay | Реле NTLM-аутентификации DC на HTTP-энролмент AD CS | LogonType=3, источник — атакующий, аккаунт=DC$ |
| 24.3 | 4887 | Cert | Центр сертификации выдал сертификат от имени DC (Web Enrollment, шаблон ESC8) | Requester=DC$, Web Enrollment |
| 24.4 | 4768 | PKINIT | Аутентификация по выданному сертификату (PKINIT) → билет с правами DC | Certificate Information |
| 24.5 | 4662 | Impact | DCSync / полный доступ к домену с правами DC | DS-Replication-Get-Changes |

> 🎯 **Итоговая корреляция:** Принуждение (5145 efsrpc) + вход DC$ с внешнего источника + выдача сертификата 4887 + PKINIT (Окно: 15 мин)

