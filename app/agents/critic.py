from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from app.tools.skill_loader import load_skill


MODEL_NAME = "qwen2.5:1.5b"


def get_llm():
    return ChatOllama(
        model=MODEL_NAME,
        base_url="http://localhost:11434",
        temperature=0.2,
        num_predict=500,
    )


def run_critic(user_idea: str, plan: str, market_analysis: str, product_analysis: str) -> str:
    llm = get_llm()

    critic_skill = load_skill("critic_skill")

    system_prompt = f"""
Ты Critic Agent в мультиагентной системе ProductCase AI.

Твоя задача — проверить работу других агентов.

Используй следующий skill:
{critic_skill}

Проверь:
1. Есть ли логические слабости.
2. Есть ли слишком общие утверждения.
3. Есть ли риск галлюцинаций.
4. Чего не хватает для продуктового кейса.
5. Какие улучшения нужны.

Пиши честно и конкретно. Не переписывай весь кейс.
"""

    user_prompt = f"""
Идея продукта:
{user_idea}

План:
{plan}

Рыночный анализ:
{market_analysis}

Продуктовый анализ:
{product_analysis}

Проверь результат.
"""

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )

    return response.content