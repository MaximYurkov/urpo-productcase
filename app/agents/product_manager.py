from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from app.tools.skill_loader import load_skill


MODEL_NAME = "gemma2:2b"


def get_llm():
    return ChatOllama(
        model=MODEL_NAME,
        base_url="http://localhost:11434",
        temperature=0.3,
        num_predict=700,
    )


def run_product_manager(user_idea: str, plan: str, market_analysis: str) -> str:
    llm = get_llm()

    jtbd_skill = load_skill("jtbd_skill")
    lean_canvas_skill = load_skill("lean_canvas_skill")
    backlog_skill = load_skill("backlog_skill")

    system_prompt = f"""
Ты Product Manager Agent в мультиагентной системе ProductCase AI.

Твоя зона ответственности:
- продуктовая ценность;
- JTBD;
- Lean Canvas;
- MVP;
- backlog;
- roadmap.

Используй эти skills:

{jtbd_skill}

{lean_canvas_skill}

{backlog_skill}

Не делай общий отчёт. Не повторяй всё подряд.
Опирайся на анализ Market Analyst Agent.
Пиши по-русски, структурировано.
"""

    user_prompt = f"""
Идея продукта:
{user_idea}

План:
{plan}

Рыночный анализ:
{market_analysis}

Сформируй продуктовую часть кейса.
"""

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )

    return response.content