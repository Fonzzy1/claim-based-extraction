from pydantic import BaseModel, Field, field_validator
from typing import Literal, List

INFRASTRUCTURE = {
    'Renewables': [
        "Small Scale Solar", 
        "Large Scale Solar", 
        "Onshore Wind", 
        "Offshore Wind", 
        "Hydroelectric Power", 
        "Biomass"
    ],
    'Fossil Fuels': [
        "Coal Power", 
        "Gas Power", 
        "Oil Power", 
        "Geothermal Power"
    ],
    'Speculative Power Sources': [
        "Nuclear Power", 
        "Tidal Power", 
        "Hydrogen Power", 
        "Wave Power",
        "Emerging Energy Production Technologies"
    ],
    'Energy Storage and Transportation': [
        "Small Scale Battery Storage",
        "Large Scale Battery Storage",
        "Pumped Hydro Storage",
        "Transmission Lines",
        "Smart Grids",
        "Thermal Energy Storage",
    ]
}

# Ensure INFRASTRUCTURE is a dictionary of lists for this to work correctly
all_infrastructure_options = [item for sublist in INFRASTRUCTURE.values() for item in sublist]

# Reverse map
reverse_map = {}
for category, items in INFRASTRUCTURE.items():
    for item in items:
        reverse_map[item] = category


SYSTEM_EXTRACTOR = f"""
**Task Description:**

You are tasked with analyzing a peice of text to identify and extract moral judgments related to energy infrastructure in Australia. Your goal is to find claims that express or imply moral evaluations or judgments and summarize them using a single adjective.

**Instructions:**

1. **Read the Article**: Carefully read the provided text about energy infrastructure in Australia.

2. **Identify the Claims**: Identify all claims made in the article, and note down each quote that relates to these claims.

3. **Identify the Energy-Producing Infrastructure**: Focus on infrastructure related to energy production methods or technologies pertinent to energy transmission and storage. Look for claims related to: {", ".join(all_infrastructure_options)}

4. **Identify Claims and Adjectives**: Look for statements with explicit or implicit claims about the identified energy infrastructure. For each claim, determine the single adjective that best captures the essence of the moral judgment, such as "expensive," "beneficial," "harmful," etc. You may include qualifying information with these adjectives, e.g., 'harmful to birds', 'environmentally beneficial', 'emission-reducing'.

5. **Extract and Summarize**: For each identified claim, provide the specific energy infrastructure mentioned and the corresponding adjective representing the moral judgment.

**Additional Tips:**
- **Focus on Subtext**: Look for language suggesting approval or disapproval, such as metaphors, comparisons, or rhetorical questions.
- **Adjective Selection**: Ensure that the selected adjectives reflect both explicit and implicit moral evaluations of the claims.
- **Multiple Claims**: A single piece of infrastructure may have multiple claims associated with it.
- **Implicit Claims**: Many claims may be implicit, where the moral judgment is implied. Be attentive to these subtle expressions.
"""


class ClaimModel(BaseModel):
    quote: str = Field(..., description="A quote from the article text that makes the claim")
    infrastructure: str = Field(..., description="The infristructure that the claim is being made about. One of: " + ", ".join(all_infrastructure_options))
    judgement: str = Field(..., description="An adjective with or without qualifying information")
    
    @field_validator('infrastructure')
    def validate_infrastructure(cls, value):
        if value not in all_infrastructure_options:
            raise ValueError(f'infrastructure must be one of {all_infrastructure_options}')
        return value


class ClaimList(BaseModel):
  claims: list[ClaimModel]

class EvaluationModel(BaseModel):
    judgment: str = Field(..., description="An evaluative statement or judgment regarding the subject.")
    dimension: Literal['economic', 'externalities']
    valence: float = Field(..., description="A float between -1 and 1 indicating the sentiment of the judgment.")
    
    # Validator to ensure the valence is within the specified range
    @field_validator('valence')
    def valence_must_be_in_range(cls, v):
        if not -1 <= v <= 1:
            raise ValueError('valence must be between -1 and 1')
        return v
