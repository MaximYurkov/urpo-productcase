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


def run_market_analyst(user_idea: str, plan: str) -> str:
    llm = get_llm()

    product_vision_skill = load_skill("product_vision_skill")

    system_prompt = f"""
Ты Market Analyst Agent в мультиагентной системе ProductCase AI.

Твоя зона ответственности:
- проблема пользователя;
- целевая аудитория;
- пользовательские сегменты;
- конкуренты;
- рыночные риски.

Используй следующий skill:
{product_vision_skill}

Не пиши Lean Canvas и backlog. Это зона другого агента.
Пиши по-русски, структурировано, без воды.
Если точных данных нет, явно пиши, что это гипотеза.
"""

    user_prompt = f"""
Идея продукта:
{user_idea}

План анализа от Planner Agent:
{plan}

Сделай только рыночный и пользовательский анализ.
"""

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )

    return response.content