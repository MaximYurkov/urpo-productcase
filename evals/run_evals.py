import json
from pathlib import Path
from uuid import uuid4

from app.graph import build_graph


TEST_CASES_PATH = Path("evals/test_cases.json")
RESULTS_PATH = Path("evals/eval_results.json")


def load_test_cases() -> list[dict]:
    return json.loads(TEST_CASES_PATH.read_text(encoding="utf-8"))


def calculate_keyword_score(text: str, required_keywords: list[str]) -> dict:
    text_lower = text.lower()

    found_keywords = []
    missing_keywords = []

    for keyword in required_keywords:
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    score = round(len(found_keywords) / len(required_keywords), 2)

    return {
        "score": score,
        "found_keywords": found_keywords,
        "missing_keywords": missing_keywords,
    }


def run_single_eval(test_case: dict) -> dict:
    graph = build_graph()

    initial_state = {
        "trace_id": f"eval-{uuid4()}",
        "user_idea": test_case["idea"],
        "plan": "",
        "market_analysis": "",
        "product_analysis": "",
        "critic_review": "",
        "final_report": "",
    }

    result = graph.invoke(initial_state)

    combined_output = "\n\n".join(
        [
            result["plan"],
            result["market_analysis"],
            result["product_analysis"],
            result["critic_review"],
            result["final_report"],
        ]
    )
    
    keyword_score = calculate_keyword_score(
        text=combined_output,
        required_keywords=test_case["required_keywords"],
    )

    passed = keyword_score["score"] >= 0.5

    return {
        "id": test_case["id"],
        "idea": test_case["idea"],
        "score": keyword_score["score"],
        "passed": passed,
        "found_keywords": keyword_score["found_keywords"],
        "missing_keywords": keyword_score["missing_keywords"],
    }


def main():
    print("Запуск evals для ProductCase AI")
    print()

    test_cases = load_test_cases()
    results = []

    for test_case in test_cases:
        print(f"Eval case: {test_case['id']}")
        result = run_single_eval(test_case)
        results.append(result)

        print(f"Score: {result['score']}")
        print(f"Passed: {result['passed']}")
        print()

    RESULTS_PATH.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Результаты сохранены в {RESULTS_PATH}")


if __name__ == "__main__":
    main()