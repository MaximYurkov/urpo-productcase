# ProductCase AI

ProductCase AI — учебная мультиагентная LLM-система для анализа продуктовой идеи и подготовки черновика продуктового кейса.

Пользователь вводит идею продукта, система прогоняет её через несколько агентов и сохраняет результат в Markdown-отчёт.

## Что делает система

Система помогает получить черновик продуктового кейса:

- анализ идеи;
- проблема пользователя;
- целевая аудитория;
- JTBD;
- Lean Canvas;
- MVP;
- backlog;
- roadmap;
- риски;
- критика результата.

## Агенты

В системе используется 5 агентов:

1. Planner Agent — составляет план анализа идеи.
2. Market Analyst Agent — анализирует аудиторию, проблему, сегменты, конкурентов и риски.
3. Product Manager Agent — формирует JTBD, Lean Canvas, MVP, backlog и roadmap.
4. Critic Agent — проверяет результат на слабые места и возможные галлюцинации.
5. Report Writer Agent — собирает итоговый Markdown-отчёт.

Workflow:

User Input → Planner → Market Analyst → Product Manager → Critic → Report Writer → Report

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

## Установка

Создать виртуальное окружение:

python -m venv .venv

Активировать окружение:

.\.venv\Scripts\Activate.ps1

Установить зависимости:

pip install -r requirements.txt

## Запуск Ollama

Запустить Ollama через Docker Compose:

docker compose up -d

Проверить контейнер:

docker ps

Скачать модель, если её ещё нет:

docker exec -it urpo-ollama ollama pull qwen2.5:1.5b

## Запуск системы

python -m app.main

После запуска нужно ввести описание продуктовой идеи.

Пример:

AI-сервис для автоматического подбора рекламных креативов для малого бизнеса.

## Результаты

После запуска создаются/обновляются файлы:

- reports/generated_report.md — последний отчёт;
- reports/report_<trace_id>.md — отдельный отчёт запуска;
- logs/run_logs.jsonl — логи выполнения;
- app/memory/memory.db — SQLite-память запусков.

## Evals

Запуск evals:

python -m evals.run_evals

Результаты сохраняются в:

evals/eval_results.json

## Структура проекта

app/ — код приложения  
app/agents/ — агенты  
app/skills/ — markdown skills  
app/tools/ — memory, logs, skill loader  
app/memory/ — SQLite memory  
evals/ — eval test cases and runner  
reports/ — generated reports  
logs/ — JSONL logs  
docs/ — technical docs  

## Ограничения MVP

- используется лёгкая локальная модель qwen2.5:1.5b;
- качество текста может быть нестабильным;
- веб-поиск не подключён;
- рыночный анализ является гипотезой;
- observability реализована через локальные JSONL-логи;
- память реализована через SQLite.