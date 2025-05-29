from pydantic import BaseModel

from s_conformance_score import SConformanceScore

class SConformanceValues(BaseModel):
    case_id: str
    last_activity: str | None
    conformance: SConformanceScore
