# C4 Container Diagram

```mermaid
flowchart TB
    user["Пользователь"]

    cli["CLI Application<br/>app/main.py"]

    graph["LangGraph Workflow<br/>app/graph.py"]

    agents["Agents<br/>app/agents"]

    skills["Markdown Skills<br/>app/skills"]

    tools["Tools<br/>memory / logs / skill loader"]

    ollama["Ollama Container<br/>qwen2.5:1.5b"]

    reports["Reports<br/>reports"]

    memory["SQLite DB<br/>app/memory/memory.db"]

    logs["JSONL Logs<br/>logs/run_logs.jsonl"]

    user --> cli
    cli --> graph
    graph --> agents
    agents --> skills
    agents --> ollama
    graph --> tools
    tools --> memory
    tools --> logs
    cli --> reports
```