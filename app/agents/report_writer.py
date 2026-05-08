from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from app.tools.skill_loader import load_skill


MODEL_NAME = "qwen2.5:1.5b"


def get_llm():
    return ChatOllama(
        model=MODEL_NAME,
        base_url="http://localhost:11434",
        temperature=0.3,
        num_predict=900,
    )


def run_report_writer(
    user_idea: str,
    plan: str,
    market_analysis: str,
    product_analysis: str,
    critic_review: str,
) -> str:
    llm = get_llm()

    product_vision_skill = load_skill("product_vision_skill")
    jtbd_skill = load_skill("jtbd_skill")
    lean_canvas_skill = load_skill("lean_canvas_skill")
    backlog_skill = load_skill("backlog_skill")
    critic_skill = load_skill("critic_skill")

    system_prompt = f"""
Ты Report Writer Agent в мультиагентной системе ProductCase AI.

Твоя задача — собрать финальный Markdown-отчёт из результатов других агентов.
Отчёт должен быть полезным, но не слишком длинным.
Пиши компактно: 1-3 абзаца или 3-5 пунктов на каждый раздел.

Используй эти skills как правила оформления и проверки:

{product_vision_skill}

{jtbd_skill}

{lean_canvas_skill}

{backlog_skill}

{critic_skill}

Структура отчёта:
# ProductCase AI Report

## 1. Идея продукта
## 2. Проблема пользователя
## 3. Целевая аудитория
## 4. User Persona
## 5. JTBD
## 6. Конкуренты
## 7. Lean Canvas
## 8. MVP
## 9. Backlog
## 10. Roadmap
## 11. Риски
## 12. Критика и улучшения

Пиши по-русски. Форматируй как Markdown.
"""

    user_prompt = f"""
Идея пользователя:
{user_idea}

План:
{plan}

Рыночный анализ:
{market_analysis}

Продуктовый анализ:
{product_analysis}

Критика:
{critic_review}

Собери итоговый отчёт.
"""

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )

    return response.content