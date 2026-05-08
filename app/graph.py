from typing import TypedDict

from langgraph.graph import StateGraph, END

from app.agents.planner import run_planner
from app.agents.market_analyst import run_market_analyst
from app.agents.product_manager import run_product_manager
from app.agents.critic import run_critic
from app.agents.report_writer import run_report_writer
from app.tools.observability_tool import run_with_observability


class AgentState(TypedDict):
    trace_id: str
    user_idea: str
    plan: str
    market_analysis: str
    product_analysis: str
    critic_review: str
    final_report: str


def planner_node(state: AgentState) -> AgentState:
    print("Planner Agent запущен")

    state["plan"] = run_with_observability(
        state["trace_id"],
        "Planner Agent",
        run_planner,
        state["user_idea"],
    )

    return state


def market_analyst_node(state: AgentState) -> AgentState:
    print("Market Analyst Agent запущен")

    state["market_analysis"] = run_with_observability(
        state["trace_id"],
        "Market Analyst Agent",
        run_market_analyst,
        state["user_idea"],
        state["plan"],
    )

    return state


def product_manager_node(state: AgentState) -> AgentState:
    print("Product Manager Agent запущен")

    state["product_analysis"] = run_with_observability(
        state["trace_id"],
        "Product Manager Agent",
        run_product_manager,
        state["user_idea"],
        state["plan"],
        state["market_analysis"],
    )

    return state


def critic_node(state: AgentState) -> AgentState:
    print("Critic Agent запущен")

    state["critic_review"] = run_with_observability(
        state["trace_id"],
        "Critic Agent",
        run_critic,
        state["user_idea"],
        state["plan"],
        state["market_analysis"],
        state["product_analysis"],
    )

    return state


def report_writer_node(state: AgentState) -> AgentState:
    print("Report Writer Agent запущен")

    state["final_report"] = run_with_observability(
        state["trace_id"],
        "Report Writer Agent",
        run_report_writer,
        state["user_idea"],
        state["plan"],
        state["market_analysis"],
        state["product_analysis"],
        state["critic_review"],
    )

    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("market_analyst", market_analyst_node)
    graph.add_node("product_manager", product_manager_node)
    graph.add_node("critic", critic_node)
    graph.add_node("report_writer", report_writer_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "market_analyst")
    graph.add_edge("market_analyst", "product_manager")
    graph.add_edge("product_manager", "critic")
    graph.add_edge("critic", "report_writer")
    graph.add_edge("report_writer", END)

    return graph.compile()