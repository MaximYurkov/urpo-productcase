def run_report_writer(
    user_idea: str,
    plan: str,
    market_analysis: str,
    product_analysis: str,
    critic_review: str,
) -> str:
    report = f"""# ProductCase AI Report

## 1. Исходная идея продукта

{user_idea}

---

## 2. План анализа

{plan}

---

## 3. Рыночный и пользовательский анализ

{market_analysis}

---

## 4. Продуктовая проработка

{product_analysis}

---

## 5. Критика и рекомендации

{critic_review}

---

## 6. Итог

ProductCase AI обработал идею через мультиагентный workflow:

1. Planner Agent сформировал план анализа.
2. Market Analyst Agent разобрал аудиторию, проблему, сегменты, конкурентов и риски.
3. Product Manager Agent подготовил JTBD, Lean Canvas, MVP, backlog и roadmap.
4. Critic Agent проверил результат на слабые места и возможные галлюцинации.
5. Report Writer Agent собрал итоговый Markdown-отчёт.

Итоговый отчёт является черновиком продуктового кейса и может быть доработан пользователем вручную.
"""

    return report