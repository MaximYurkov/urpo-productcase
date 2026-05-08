import json
from datetime import datetime
from pathlib import Path
from time import perf_counter


LOG_PATH = Path("logs/run_logs.jsonl")


def write_log(event: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    event["timestamp"] = datetime.now().isoformat(timespec="seconds")

    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")


def log_run_start(trace_id: str, user_idea: str) -> None:
    write_log(
        {
            "event": "run_start",
            "trace_id": trace_id,
            "user_idea": user_idea,
        }
    )


def log_run_end(trace_id: str, status: str) -> None:
    write_log(
        {
            "event": "run_end",
            "trace_id": trace_id,
            "status": status,
        }
    )


def run_with_observability(trace_id: str, agent_name: str, func, *args, **kwargs):
    started_at = perf_counter()

    write_log(
        {
            "event": "agent_start",
            "trace_id": trace_id,
            "agent_name": agent_name,
        }
    )

    try:
        result = func(*args, **kwargs)
        duration_seconds = round(perf_counter() - started_at, 3)

        write_log(
            {
                "event": "agent_end",
                "trace_id": trace_id,
                "agent_name": agent_name,
                "status": "success",
                "duration_seconds": duration_seconds,
            }
        )

        return result

    except Exception as error:
        duration_seconds = round(perf_counter() - started_at, 3)

        write_log(
            {
                "event": "agent_error",
                "trace_id": trace_id,
                "agent_name": agent_name,
                "status": "error",
                "duration_seconds": duration_seconds,
                "error": str(error),
            }
        )

        raise