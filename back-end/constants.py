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

3. **Identify the Energy-Producing Infrastructure**: Focus on infrastructure related to energy production methods or technologies pertinent to energy transmission and storage. Look for claims only related to the following, and ignore the rest: {", ".join(all_infrastructure_options)}. 

4. **Identify Claims and Adjectives**: Look for statements with explicit or implicit claims about the identified energy infrastructure. For each claim, determine the single adjective that best captures the essence of the moral judgment, such as "expensive," "beneficial," "harmful," etc. You may include qualifying information with these adjectives, e.g., 'harmful to birds', 'environmentally beneficial', 'emission-reducing'.

5. **Extract and Summarize**: For each identified claim, provide the specific energy infrastructure mentioned and the corresponding adjective representing the moral judgment.

**Additional Tips:**
- **Focus on Subtext**: Look for language suggesting approval or disapproval, such as metaphors, comparisons, or rhetorical questions.
- **Adjective Selection**: Ensure that the selected adjectives reflect both explicit and implicit moral evaluations of the claims.
- **Multiple Claims**: A single piece of infrastructure may have multiple claims associated with it.
- **Implicit Claims**: Many claims may be implicit, where the moral judgment is implied. Be attentive to these subtle expressions.
"""

SYSTEM_EVALUATION = """
**Task Description:**

You are tasked with evaluating a claim that has been made about a peice of energy infrutucure. In this task, you will assess whether the moral judgments highlighted in the text are predominantly along an economic dimension or an externality dimension. Furthermore, you will determine a valence score between -1 and 1 for each judgment, reflecting a spectrum from strong disapproval to strong approval.

**Instructions:**

1. **Review Extracted Claims**: Examine the claims, specifically focusing on the energy infrastructure and corresponding adjectives that represent moral judgments.

2. **Identify Dimensions**: For each claim, determine whether the primary dimension of evaluation is:
   - **Economic**: Concerns related to costs, investments, economic benefits, financial viability, etc.
   - **Externality**: Concerns related to environmental impact, social consequences, health effects, etc.

3. **Assign Valence Score**: Assign a valence score between -1 and 1 to each claim based on the level of approval or disapproval expressed:
   - **-1**: Strong disapproval (e.g., "severely harmful")
   - **0**: Neutral or ambivalent (e.g., "unremarkable")
   - **+1**: Strong approval (e.g., "highly beneficial")


**Additional Tips:**
- **Combine Perspectives**: If a claim touches on both dimensions, prioritize the one with a stronger emphasis.
- **Subjectivity Awareness**: Recognize that these evaluations rely on interpretation; aim to provide interpretations that capture the prevailing sentiment.
"""
