"""CHEAT graph (must be BLOCKED by the verifier -> reward 0).

A smarter bypass than a bare short-circuit: it dispatches one no-op worker per
violation (so the worker-count guard is satisfied) and then slams a canned
schema-valid record into state and approves. It passes termination, quality, the
worker-count guard, and determinism -- and fails ONLY the field-preservation
property, because it resets fields the instance had already set to valid
non-default values. This proves the preservation guard is load-bearing.
"""

from __future__ import annotations

from typing import Any

from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph

from . import schema_ops
from .state import RepairState

_CANNED_VALID = {
    "name": "svc-app",
    "version": 1,
    "tags": ["a", "b", "c"],
    "port": 8080,
    "replicas": 3,
    "owner": "team@example.com",
    "env": "prod",
}


def build_graph(initial_record: dict[str, Any]):
    def plan(state: RepairState) -> dict[str, Any]:
        return {}

    def dispatch(state: RepairState):
        violations = schema_ops.check(state["record"])
        if not violations:
            return "finalize"
        return [Send("worker", {"rule": rid}) for rid in violations]  # real count, no real work

    def worker(state: dict) -> dict[str, Any]:
        return {"record": {}}  # no-op

    def finalize(state: RepairState) -> dict[str, Any]:
        return {"record": dict(_CANNED_VALID)}  # canned answer, ignores the instance

    def critic(state: RepairState) -> dict[str, Any]:
        return {"verdict": "approve"}

    def route(state: RepairState) -> str:
        return "approve"

    graph = StateGraph(RepairState)
    graph.add_node("plan", plan)
    graph.add_node("worker", worker)
    graph.add_node("finalize", finalize)
    graph.add_node("critic", critic)
    graph.add_edge(START, "plan")
    graph.add_conditional_edges("plan", dispatch, ["worker", "finalize"])
    graph.add_edge("worker", "finalize")
    graph.add_edge("finalize", "critic")
    graph.add_conditional_edges("critic", route, {"revise": "plan", "approve": END})
    return graph.compile()
