from pathlib import Path

from app.graph import build_graph


def save_report(report_text: str):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    report_path = reports_dir / "generated_report.md"
    report_path.write_text(report_text, encoding="utf-8")

    return report_path


def main():
    print("ProductCase AI запущен")
    print("Мультиагентная система для подготовки продуктового кейса")
    print()

    user_idea = input("Введите идею продукта: ")

    graph = build_graph()

    initial_state = {
        "user_idea": user_idea,
        "plan": "",
        "market_analysis": "",
        "product_analysis": "",
        "critic_review": "",
        "final_report": "",
    }

    result = graph.invoke(initial_state)

    report_path = save_report(result["final_report"])

    print()
    print("Готово")
    print(f"Финальный отчёт сохранён в файл: {report_path}")


if __name__ == "__main__":
    main()