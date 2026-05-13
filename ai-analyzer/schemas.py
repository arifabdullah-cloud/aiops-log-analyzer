from pydantic import BaseModel, Field
from typing import List, Literal


class AnalyzeRequest(BaseModel):
    logs: str = Field(..., min_length=10)


class AnalyzeResponse(BaseModel):
    summary: str
    severity: Literal["low", "medium", "high", "critical"]
    probable_cause: str
    affected_component: str
    recommended_actions: List[str]
