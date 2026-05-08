from pathlib import Path
from uuid import uuid4

from app.graph import build_graph
from app.tools.memory_tool import save_run_to_memory
from app.tools.observability_tool import log_run_start, log_run_end


def save_report(report_text: str, trace_id: str):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    latest_report_path = reports_dir / "generated_report.md"
    unique_report_path = reports_dir / f"report_{trace_id}.md"

    latest_report_path.write_text(report_text, encoding="utf-8")
    unique_report_path.write_text(report_text, encoding="utf-8")

    return latest_report_path, unique_report_path


def main():
    print("ProductCase AI запущен")
    print("Мультиагентная система для подготовки продуктового кейса")
    print()

    user_idea = input("Введите идею продукта: ")
    trace_id = str(uuid4())

    print()
    print(f"Trace ID: {trace_id}")
    print()

    log_run_start(trace_id=trace_id, user_idea=user_idea)

    graph = build_graph()

    initial_state = {
        "trace_id": trace_id,
        "user_idea": user_idea,
        "plan": "",
        "market_analysis": "",
        "product_analysis": "",
        "critic_review": "",
        "final_report": "",
    }

    try:
        result = graph.invoke(initial_state)

        latest_report_path, unique_report_path = save_report(
            report_text=result["final_report"],
            trace_id=result["trace_id"],
            )

        save_run_to_memory(
            trace_id=result["trace_id"],
            user_idea=result["user_idea"],
            plan=result["plan"],
            market_analysis=result["market_analysis"],
            product_analysis=result["product_analysis"],
            critic_review=result["critic_review"],
            final_report=result["final_report"],
        )

        log_run_end(trace_id=trace_id, status="success")

        print()
        print("Готово")
        print(f"Последний отчёт сохранён в файл: {latest_report_path}")
        print(f"Отдельный отчёт запуска сохранён в файл: {unique_report_path}")
        print("Запуск сохранён в SQLite-память: app/memory/memory.db")
        print("Логи сохранены в: logs/run_logs.jsonl")

    except Exception as error:
        log_run_end(trace_id=trace_id, status="error")
        print()
        print("Ошибка во время выполнения:")
        print(error)
        raise


if __name__ == "__main__":
    main()