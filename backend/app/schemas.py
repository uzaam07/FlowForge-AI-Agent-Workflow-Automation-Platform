from pydantic import BaseModel, EmailStr, Field
from typing import Any, Literal

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class Node(BaseModel):
    id: str = Field(min_length=1, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    type: Literal["trigger", "transform", "condition", "ai_summary", "http_request", "approval", "output"]
    label: str = Field(min_length=1, max_length=100)
    config: dict[str, Any] = Field(default_factory=dict)

class Edge(BaseModel):
    source: str = Field(min_length=1, max_length=80)
    target: str = Field(min_length=1, max_length=80)

class WorkflowDefinition(BaseModel):
    nodes: list[Node] = Field(min_length=1, max_length=30)
    edges: list[Edge] = Field(default_factory=list, max_length=60)

class WorkflowCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    definition: WorkflowDefinition

class WorkflowUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    definition: WorkflowDefinition | None = None

class RunCreate(BaseModel):
    input_data: dict[str, Any] = Field(default_factory=dict)
