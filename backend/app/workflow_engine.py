from collections import defaultdict, deque
from typing import Any
from pydantic import ValidationError
from .schemas import WorkflowDefinition

class WorkflowValidationError(ValueError):
    pass

def validate_definition(raw: dict) -> dict:
    try:
        definition = WorkflowDefinition.model_validate(raw)
    except ValidationError as exc:
        raise WorkflowValidationError("Workflow definition is invalid.") from exc
    ids = [n.id for n in definition.nodes]
    if len(ids) != len(set(ids)):
        raise WorkflowValidationError("Node IDs must be unique.")
    known = set(ids)
    outgoing = defaultdict(list)
    indegree = {node_id: 0 for node_id in ids}
    for edge in definition.edges:
        if edge.source not in known or edge.target not in known:
            raise WorkflowValidationError("Every edge must reference an existing node.")
        if edge.source == edge.target:
            raise WorkflowValidationError("Self-referencing edges are not allowed.")
        outgoing[edge.source].append(edge.target)
        indegree[edge.target] += 1
    queue = deque([node_id for node_id, degree in indegree.items() if degree == 0])
    order = []
    while queue:
        current = queue.popleft()
        order.append(current)
        for target in outgoing[current]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if len(order) != len(ids):
        raise WorkflowValidationError("Workflow must be acyclic (no loops).")
    return {"nodes": [n.model_dump() for n in definition.nodes], "edges": [e.model_dump() for e in definition.edges]}

def _bounded_text(value: Any, limit: int = 4000) -> str:
    import json
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value)[:limit]

def execute_workflow(definition: dict, input_data: dict) -> tuple[dict, list[dict]]:
    definition = validate_definition(definition)
    nodes = {n["id"]: n for n in definition["nodes"]}
    outgoing = defaultdict(list)
    indegree = {node_id: 0 for node_id in nodes}
    for edge in definition["edges"]:
        outgoing[edge["source"]].append(edge["target"])
        indegree[edge["target"]] += 1
    queue = deque([node_id for node_id, degree in indegree.items() if degree == 0])
    outputs, logs = {}, []
    while queue:
        node_id = queue.popleft()
        node = nodes[node_id]
        incoming = [outputs[p] for p in nodes if node_id in outgoing[p] and p in outputs]
        value = incoming[-1] if incoming else input_data
        config = node.get("config") or {}
        kind = node["type"]
        if kind == "trigger":
            output = input_data
        elif kind == "transform":
            output = {"value": _bounded_text(config.get("value", value))}
        elif kind == "condition":
            field = str(config.get("field", ""))[:100]
            output = {"matches": isinstance(value, dict) and value.get(field) == config.get("equals"), "field": field}
        elif kind == "ai_summary":
            output = {"summary": _bounded_text(config.get("text") or value, 500), "mode": "demo-summary"}
        elif kind == "approval":
            output = {"approval_required": True, "status": "awaiting_approval", "message": "Demo approval step; no external action was taken."}
        elif kind == "http_request":
            output = {"status": "disabled", "message": "HTTP nodes are disabled in this secure starter."}
        else:
            output = {"result": value}
        outputs[node_id] = output
        logs.append({"node_id": node_id, "label": node["label"], "type": kind, "status": "completed", "output": output})
        for target in outgoing[node_id]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if len(logs) != len(nodes):
        raise WorkflowValidationError("Workflow could not be fully executed.")
    return {"nodes": outputs}, logs
