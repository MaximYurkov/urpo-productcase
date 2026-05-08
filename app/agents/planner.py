from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from app.tools.skill_loader import load_skill


MODEL_NAME = "qwen2.5:1.5b"


def get_llm():
    return ChatOllama(
        model=MODEL_NAME,
        base_url="http://localhost:11434",
        temperature=0.3,
        num_predict=700,
    )


def run_planner(user_idea: str) -> str:
    llm = get_llm()

    product_vision_skill = load_skill("product_vision_skill")

    system_prompt = f"""
Ты Planner Agent в мультиагентной системе ProductCase AI.

Твоя роль — не писать весь продуктовый кейс, а составить план анализа идеи.

Используй следующий skill:
{product_vision_skill}

Нужно определить:
1. Какие аспекты идеи нужно проанализировать.
2. Какие вопросы нужно проверить.
3. Какие блоки должны быть в финальном отчёте.

Пиши по-русски, структурировано и кратко.
"""

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_idea),
        ]
    )

    return response.content