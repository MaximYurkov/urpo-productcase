# C4 Component Diagram

```mermaid
flowchart TB
    main["main.py<br/>точка входа"]

    graph["graph.py<br/>LangGraph workflow"]

    planner["Planner Agent"]
    market["Market Analyst Agent"]
    product["Product Manager Agent"]
    critic["Critic Agent"]
    writer["Report Writer Agent"]

    skill_loader["skill_loader.py"]
    memory_tool["memory_tool.py"]
    observability["observability_tool.py"]

    skills["skills/*.md"]
    db["memory.db"]
    log_file["run_logs.jsonl"]
    report["Markdown reports"]

    main --> graph

    graph --> planner
    graph --> market
    graph --> product
    graph --> critic
    graph --> writer

    planner --> skill_loader
    market --> skill_loader
    product --> skill_loader
    critic --> skill_loader
    writer --> skill_loader

    skill_loader --> skills

    graph --> observability
    observability --> log_file

    main --> memory_tool
    memory_tool --> db

    main --> report
```