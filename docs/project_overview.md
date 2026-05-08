# ProductCase AI — техническое описание

## Назначение

ProductCase AI — учебная мультиагентная LLM-система для анализа продуктовой идеи и генерации черновика продуктового кейса.

Пользователь вводит описание идеи, система прогоняет его через несколько агентов и сохраняет результат в Markdown-отчёт.

## Входные данные

Текстовое описание продуктовой идеи.

Пример:

AI-сервис для автоматического подбора рекламных креативов для малого бизнеса.

## Выходные данные

Система сохраняет результат в папку `reports/`:

- `generated_report.md` — последний отчёт;
- `report_<trace_id>.md` — отдельный отчёт конкретного запуска.

Также сохраняются:

- логи в `logs/run_logs.jsonl`;
- история запусков в `app/memory/memory.db`;
- результаты evals в `evals/eval_results.json`.

## Агенты

В системе используется 5 агентов:

1. `Planner Agent` — формирует план анализа идеи.
2. `Market Analyst Agent` — анализирует аудиторию, проблему, сегменты, конкурентов и риски.
3. `Product Manager Agent` — формирует JTBD, Lean Canvas, MVP, backlog и roadmap.
4. `Critic Agent` — проверяет результат на слабые места, общие формулировки и возможные галлюцинации.
5. `Report Writer Agent` — собирает итоговый Markdown-отчёт.

## Архитектура workflow

Общий flow:

User Input → Planner Agent → Market Analyst Agent → Product Manager Agent → Critic Agent → Report Writer Agent → Markdown Report

Workflow реализован через `LangGraph`.

## Стек

- Python
- LangGraph
- LangChain Ollama
- Ollama
- qwen2.5:1.5b
- Docker Compose
- SQLite
- Markdown skills
- JSONL logs

## Структура проекта

- `app/main.py` — точка входа.
- `app/graph.py` — LangGraph workflow.
- `app/agents/` — агенты.
- `app/skills/` — skill-файлы для агентов.
- `app/tools/` — memory, observability, skill loader.
- `app/memory/` — SQLite-память.
- `evals/` — тест-кейсы и eval-скрипт.
- `reports/` — итоговые отчёты.
- `logs/` — логи запусков.
- `docs/` — техническая документация.

## Запуск

Запустить Ollama:

`docker compose up -d`

Запустить систему:

`python -m app.main`

Запустить evals:

`python -m evals.run_evals`

## Ограничения MVP

- Используется лёгкая локальная модель `qwen2.5:1.5b`.
- Качество текста может быть нестабильным.
- Рыночные выводы являются гипотезами, так как веб-поиск не подключён.
- Observability реализована через локальные JSONL-логи.
- Память реализована через SQLite.