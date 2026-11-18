# Soz — управление личным и социальным бюджетом (`data3` / Budget Assist DE)

## Назначение проекта

Репозиторий `data3` посвящен созданию программного решения для автоматизации управления социальным и персональным бюджетом:

- В основной ветке `main` на текущий момент размещена только базовая заготовка репозитория («Soz — управление личным бюджетом»: файлы `LICENSE` и `README.md`, без исходного кода приложения).
- В неслитой ветке `codex/develop-budget-management-application` (открытый PR [#1](https://github.com/svend4/data3/pull/1)) представлен проект **Budget Assist DE** — инфраструктурный шаблон, проектная документация и рабочий CLI-прототип системы управления персональным бюджетом для людей с инвалидностью в Германии. Решение ориентировано на получателей бюджета, социальные ведомства, НКО, волонтёрские службы и специалистов социальной работы.

---

## Архитектура и основные компоненты

### Ветка `main`
Содержит только файл лицензии (`LICENSE`) и краткий `README.md`; прикладной код и документация прототипа находятся в ветке `codex/develop-budget-management-application`.

### Ветка `codex/develop-budget-management-application` (PR #1)

1. **CLI-прототип (`src/budget_app/`)**
   Локальное консольное приложение с сохранением состояния в JSON-файл (валюта по умолчанию — `EUR`):
   - `models.py` — модели данных `Transaction` (`transaction_id`, `kind`, `amount: Decimal`, `category`, `note`, `created_at`) и `BudgetState` (`currency`, `incomes`, `expenses`).
   - `storage.py` — чтение и запись состояния в JSON (`load_state`, `save_state`) с сериализацией `Decimal` и дат в формате ISO, а также автоматическим созданием родительских каталогов.
   - `services.py` — бизнес-логика учёта транзакций: `add_income`, `add_expense` (генерация `uuid4` и отметки времени UTC) и `summarize` (расчёт суммарных доходов, расходов и баланса).
   - `cli.py` — парсер аргументов `argparse` с общим параметром `--storage` (по умолчанию `data/budget.json`) и подкомандами:
     - `init` (`--currency`, по умолчанию `EUR`) — инициализация хранилища;
     - `add-income` (`--amount`, `--source`) — добавление дохода;
     - `add-expense` (`--amount`, `--category`, `--note`) — добавление расхода;
     - `summary` — вывод итогов по доходам, расходам и балансу.

2. **Проектная и техническая документация (`docs/`)**
   - `docs/design.md` — продуктовый и UX-дизайн: пользовательские группы, 5 ключевых сценариев (планирование бюджета, отчётность, согласование, мониторинг лимитов, социальное сопровождение), требования доступности (WCAG 2.2, BITV 2.0, Leichte Sprache), метрики и риски.
   - `docs/technical.md` — целевая модульная архитектура (Web API, Case Management, Document Service, Reporting & Analytics, Identity & Access), ролевая модель доступа, схема таблиц БД (`users`, `budgets`, `transactions`, `approvals`, `cases`, `documents`), требования безопасности (TLS + KMS, multi-tenant, аудит, GDPR/BDSG) и интеграции (REST/SOAP, экспорт PDF/CSV).
   - `docs/infrastructure.md` — целевой технологический ландшафт (SPA на React/Vue, API на Python/FastAPI или Node.js, PostgreSQL, S3/MinIO, RabbitMQ/Kafka, Keycloak/OIDC, Grafana/Prometheus/Loki) и разделение окружений Dev/Stage/Prod.
   - `docs/api.md` — черновик REST API контракта (`/auth/token`, `/budgets`, `/transactions`, `/approvals`, `/cases`).

3. **Конфигурация сборки и контейнеризации**
   - `pyproject.toml` — описание пакета `budget-assist-de` (`0.1.0`), объявление консольной точки входа `budget-assist = "budget_app.cli:main"` и настройки `black` (`line-length = 88`).
   - `Dockerfile` — образ на базе `python:3.11-slim`, устанавливающий пакет в editable-режиме (`pip install --no-cache-dir -e .`) с точкой входа `ENTRYPOINT ["budget-assist"]`.
   - `docker-compose.yml` — сервис `cli`, монтирующий `./data:/app/data` и запускающий по умолчанию `summary --storage data/budget.json`.

---

## Стек технологий и структура каталогов

- **Стек прототипа:** Python `>=3.10` (в `Dockerfile` — `python:3.11-slim`), стандартная библиотека Python (`argparse`, `dataclasses`, `decimal`, `datetime`, `json`, `pathlib`, `uuid`), упаковка `pyproject.toml`, Docker / Docker Compose. Внешние runtime-зависимости, автотесты и CI в текущем прототипе отсутствуют.

**Содержимое ветки `main`:**
```text
.
├── LICENSE
└── README.md
```

**Содержимое ветки `codex/develop-budget-management-application`:**
```text
.
├── Dockerfile
├── README.md
├── docker-compose.yml
├── pyproject.toml
├── docs/
│   ├── api.md
│   ├── design.md
│   ├── infrastructure.md
│   └── technical.md
└── src/
    └── budget_app/
        ├── __init__.py
        ├── cli.py
        ├── models.py
        ├── services.py
        └── storage.py
```

---

## Ветки и статус разработки

- `main` *(защищённая ветка по умолчанию)* — базовая заготовка (`LICENSE`, `README.md`).
- `codex/develop-budget-management-application` *(защищённая ветка, не влита в `main`)* — открыт Pull Request [#1](https://github.com/svend4/data3/pull/1) («Add Budget Assist DE prototype: docs, CLI and Docker skeleton»). Автоматические тесты и CI в PR не добавлены.
- `grokbot-test-files` *(защищённая ветка)* — служебная тестовая ветка, не относящаяся к коду приложения.

---

## Установка и запуск

В ветке `main` исполняемый код отсутствует. Для запуска CLI-прототипа переключитесь на ветку `codex/develop-budget-management-application`:

```bash
git clone https://github.com/svend4/data3.git
cd data3
git checkout codex/develop-budget-management-application
```

### Локальный запуск (Python >= 3.10)

Установите пакет (как в `Dockerfile`) и используйте консольную команду `budget-assist` или модуль `budget_app.cli`:

```bash
pip install --no-cache-dir -e .

python -m budget_app.cli init --storage data/budget.json
python -m budget_app.cli add-income --storage data/budget.json --amount 1200 --source "Sozialhilfe"
python -m budget_app.cli add-expense --storage data/budget.json --amount 45 --category "Mobilität" --note "Taxi"
python -m budget_app.cli summary --storage data/budget.json
```

*(Аналогично команды можно вызывать через установленный скрипт `budget-assist`, например `budget-assist summary --storage data/budget.json`.)*

### Запуск в Docker / Docker Compose

```bash
docker compose up --build
```

По умолчанию сервис `cli` из `docker-compose.yml` монтирует каталог `./data` в `/app/data` и выполняет `summary --storage data/budget.json`.

---

## Лицензия

Проект распространяется под лицензией **GNU Affero General Public License v3.0 (AGPL-3.0)** — подробности см. в файле [LICENSE](LICENSE).
