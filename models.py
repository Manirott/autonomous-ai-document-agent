from typing import List, Optional
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    request: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Natural language request for the AI agent"
    )


class Task(BaseModel):
    id: int
    name: str
    status: str = "Pending"
    output: Optional[str] = None


class ExecutionStep(BaseModel):
    step: str
    status: str
    details: Optional[str] = None


class AgentResponse(BaseModel):
    status: str
    message: str
    document_type: Optional[str] = None
    document_path: Optional[str] = None
    assumptions: List[str] = []
    tasks: List[Task] = []
    execution_trace: List[ExecutionStep] = []