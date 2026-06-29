"""Compiled LangGraph workflow for productivity AI features."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from backend.langgraph.nodes import (
    analyze_overdue_tasks,
    classify_tasks,
    generate_summary,
    plan_tomorrow,
)
from backend.langgraph.state import ProductivityGraphState

try:
    from langgraph.graph import END, START, StateGraph
except ImportError:  # pragma: no cover - keeps local dev usable before install
    END = "__end__"
    START = "__start__"
    StateGraph = None


class FallbackCompiledGraph:
    """Small sequential fallback used only when langgraph is unavailable."""

    def invoke(self, state: ProductivityGraphState) -> ProductivityGraphState:
        """Run nodes in the same order as the real graph."""
        result: ProductivityGraphState = dict(state)
        for node in (classify_tasks, analyze_overdue_tasks, generate_summary, plan_tomorrow):
            result.update(node(result))
        return result


def compile_productivity_graph() -> Any:
    """Compile the productivity StateGraph."""
    if StateGraph is None:
        return FallbackCompiledGraph()

    graph = StateGraph(ProductivityGraphState)
    graph.add_node("classify_tasks", classify_tasks)
    graph.add_node("analyze_overdue_tasks", analyze_overdue_tasks)
    graph.add_node("generate_summary", generate_summary)
    graph.add_node("plan_tomorrow", plan_tomorrow)

    graph.add_edge(START, "classify_tasks")
    graph.add_edge("classify_tasks", "analyze_overdue_tasks")
    graph.add_edge("analyze_overdue_tasks", "generate_summary")
    graph.add_edge("generate_summary", "plan_tomorrow")
    graph.add_edge("plan_tomorrow", END)

    return graph.compile()


@lru_cache(maxsize=1)
def get_productivity_graph() -> Any:
    """Return a singleton compiled productivity graph."""
    return compile_productivity_graph()
