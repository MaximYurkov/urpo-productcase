# C4 Container Diagram

```mermaid
flowchart TB
    user[User]
    cli[CLI Application]
    graph[LangGraph Workflow]
    agents[Agents]
    skills[Markdown Skills]
    tools[Tools]
    ollama[Ollama Container]
    reports[Reports]
    memory[SQLite Database]
    logs[JSONL Logs]

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