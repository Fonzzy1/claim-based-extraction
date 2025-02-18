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
        "Wave Power"
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


SYSTEM_EXTRACTOR = """
**Task Description:**

You are tasked with analyzing a news article to identify and extract both explicit and implicit moral judgments related to energy producing infrastructure in Australia. Your goal is to find claims that express or imply moral evaluations or judgments and summarize them using a single adjective.

**Instructions:**

1. **Read the Article**: Carefully read the provided news article about energy infrastructure in Australia.

2. **Identify the Energy Producing Infrastructure**: The infrastructure will always be an energy production method. You will only find claims related to: Small Scale Solar, Large Scale Solar, Onshore Wind, Offshore Wind, Nuclear Power, Hydro Electric Power, Geothermal Power, Coal Power, Gas Power, Oil Power, Biomass, Tidal Power, Hydrogen Power, and Wave Power. For technologies not on this list, label them as "Emerging Energy Technologies".

3. **identify claims and adjectives**: look for statements that make explicit or implicit claims about the identified energy infrastructure. for each claim, identify the single adjective that best describes the moral judgment of the claim. these adjectives should capture the essence of the evaluation, such as "expensive," "beneficial," "harmful," etc.

4. **Consider Explicit Judgments**: For judgments explicitly stated in the article, a direct quote must be present. Explicit judgments involve clear and direct expressions of moral evaluations within the text.

5. **Consider Implicit Judgments**: Pay attention to the context, tone, and implications of the statements. Look for underlying assumptions or connotations that suggest a moral stance, even if not directly stated. Recognize that implicit judgments do not have direct quotes or clear evidence within the article.

6. **Extract and Summarize**: For each identified claim, provide the specific energy infrastructure mentioned and the corresponding adjective that represents the moral judgment. If a direct quote is not available for an implicit judgment, use an empty string `""` for the quote and an empty list `[]` for the evidence.

7. **Format Your Response**: Use the following JSON format for each claim:

```json
{
  "claims": [
    {
      "type": "[explicit/implicit]",
      "quote": "[exact text from article: String, or '' if not present]",
      "infrastructure": "[One of: Small Scale Solar, Large Scale Solar, Onshore Wind, Offshore Wind, Nuclear Power, Hydro Electric Power, Geothermal Power, Coal Power, Gas Power, Oil Power, Biomass, Tidal Power, Hydrogen Power, Wave Power, Emerging Energy Technologies : String]",
      "judgment": "[single adjective: String]",
      "evidence": "[A list of quotes or contextual elements used to support the claim: List, or [] if not present]",
      "reasoning": "[explanation of how this judgment was inferred: String]"
    }
  ]
}
```

**Example Output:**

```json
{
  "claims": [
    {
      "type": "explicit",
      "quote": "Dutton's nuclear plan will cost Australians millions of dollars.",
      "infrastructure": "Nuclear Power",
      "judgment": "Expensive",
      "evidence": ["Dutton's nuclear plan will cost Australians millions of dollars."],
      "reasoning": "Direct statement of cost implications."
    },
    {
      "type": "implicit",
      "quote": "",
      "infrastructure": "Large Scale Solar",
      "judgment": "Beneficial",
      "evidence": [],
      "reasoning": "The article's positive tone and emphasis on sustainability suggest a beneficial view."
    },
    {
      "type": "implicit",
      "quote": "",
      "infrastructure": "Nuclear Power",
      "judgment": "Dangerous",
      "evidence": [
        "In the event of an incident, residents within a 50km radius must be evacuated within 4 hours.",
        "The facility requires triple-redundant safety systems, costing over $300 million.",
        "Lessons learned from Fukushima show the importance of robust containment structures.",
        "Monthly emergency drills will be mandatory for all staff and local emergency services."
      ],
      "reasoning": "While the article does not explicitly state that nuclear power is dangerous, the extensive focus on safety measures, emergency procedures, and historical accidents implies significant risk."
    }]
}
```

**Additional Tips:**

- **Focus on Subtext**: Look for language that suggests approval or disapproval, such as metaphors, comparisons, or rhetorical questions.
- **Contextual Clues**: Consider the broader context of the article, such as the author's background or the publication's stance, which might influence the implicit judgments.
- **Adjective Selection**: Ensure that the adjectives chosen reflect both the explicit and implicit moral evaluations of the claims.
- **Multiple Claims**: Documents can contain multiple claims about a single piece of infrastructure.
- **Other Infrastructures**: Documents will contain claims about infrastructure that do not fall into one of the categories of 'Energy Producing Infrastructure'. Do not include any claims for infrastructure that does not fall into this category.
"""
