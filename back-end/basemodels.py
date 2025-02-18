from pydantic import BaseModel, Field, field_validator
from constants import INFRASTRUCTURE
from typing import Literal, List

# Ensure INFRASTRUCTURE is a dictionary of lists for this to work correctly
all_infrastructure_options = [item for sublist in INFRASTRUCTURE.values() for item in sublist]

class Claim(BaseModel):
    type: Literal['explicit', 'implicit']
    quote: str
    infrastructure: str = Field(..., description="One of: " + ", ".join(all_infrastructure_options))
    judgment: str
    evidence: List[str]
    reasoning: str
    
    @field_validator('infrastructure')
    def validate_infrastructure(cls, value):
        if value not in all_infrastructure_options:
            raise ValueError(f'infrastructure must be one of {all_infrastructure_options}')
        return value


class ClaimList(BaseModel):
  claims: list[Claim]

class Evaluation(BaseModel):

