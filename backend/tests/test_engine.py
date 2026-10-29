import pytest
from app.workflow_engine import execute_workflow, validate_definition, WorkflowValidationError

def test_engine_runs_steps():
    d = {"nodes":[{"id":"start","type":"trigger","label":"Start","config":{}},{"id":"ai","type":"ai_summary","label":"Summary","config":{"text":"hello"}},{"id":"end","type":"output","label":"End","config":{}}],"edges":[{"source":"start","target":"ai"},{"source":"ai","target":"end"}]}
    result, steps = execute_workflow(d, {"ticket":"hello"})
    assert result["nodes"]["ai"]["summary"] == "hello"
    assert len(steps) == 3

def test_unknown_edge_rejected():
    d = {"nodes":[{"id":"start","type":"trigger","label":"Start","config":{}}],"edges":[{"source":"start","target":"missing"}]}
    with pytest.raises(WorkflowValidationError): validate_definition(d)
