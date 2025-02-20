from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import json
from constants import SYSTEM_EVALUATION, InfrastructureType, Dimension
from models.ai_client import Ai

# OpenAI client initialization
client: Ai = Ai()

class ClaimStruct(BaseModel):
    quote: str = Field(..., description="A quote from the article text that makes the claim")
    infrastructure: InfrastructureType = Field(..., description=f"The infrastructure that the claim is made about")
    judgement: str = Field(..., description="An adjective with or without qualifying information")


# User agent configuration for newspaper
class Claim(ClaimStruct):
    """
    A model representing a claim extracted from text.
    """
    evaluated: bool = False
    dimension: Optional[Dimension] = Field(None, description="A feild tha is always Empty")
    valence: float = 0

    def evaluate_claim(self, redo: bool = False) -> None:
        """
        Evaluate the claim using OpenAI's service.
        """
        if not self.evaluated or redo:
            evaluation: Evaluation = client.structured_complete(
                messages=[
                    {"role": "system", "content": SYSTEM_EVALUATION},
                    {"role": "user", "content": json.dumps({
                        "quote": self.quote,
                        "infrastructure": self.infrastructure.value,  # Access the enum value
                        "judgement": self.judgement
                    })},
                ],
                structure=Evaluation,
            )
            self.dimension = evaluation.dimension
            self.valence = evaluation.valence
            self.evaluated = True

    def __getstate__(self):
           state = self.__dict__.copy()
           # Convert enum to string for serialization
           state['infrastructure'] = state['infrastructure'].value if isinstance(state['infrastructure'], InfrastructureType) else state['infrastructure']
           state['dimension'] = state['dimension'].value if isinstance(state['dimension'], Dimension) else state['dimension']
           return state

    def __setstate__(self, state):
           # Restore enum from string
           if isinstance(state.get('infrastructure'), str):
               state['infrastructure'] = InfrastructureType(state['infrastructure'])
           if isinstance(state.get('dimension'), str):
               state['dimension'] = Dimension(state['dimension'])
           self.__dict__.update(state)


class Evaluation(BaseModel):
    """
    A model evaluating claims based on judgments and sentiments.
    """
    dimension: Dimension
    valence: float = Field(..., description="A float between -1 and 1 indicating the sentiment of the judgment.")

    @field_validator('valence')
    def valence_must_be_in_range(cls, v: float) -> float:
        if not -1 <= v <= 1:
            raise ValueError('Valence must be between -1 and 1')
        return v

class ClaimList(BaseModel):
    """
    A model for holding a list of claims.
    """
    claims: List[ClaimStruct]

    def transform_to_claims(self) -> List[Claim]:
        """
        Convert all ClaimStruct instances in the list to Claim instances.
        """
        return [Claim(**claim_struct.dict()) for claim_struct in self.claims]


