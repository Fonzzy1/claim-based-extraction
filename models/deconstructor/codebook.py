from pydantic import BaseModel, model_validator, ValidationError
from typing import Optional, Literal

TECH_TAXONOMY = {
    "Renewable Energy": {
        "Solar Power": {
            "Small Scale Solar",
            "Large Scale Solar",
            "Concentrated Solar",
        },
        "Wind Power": {"Offshore Wind", "Onshore Wind"},
        "Hydro Power": {"Small Scale Hydro", "Large Scale Hydro"},
    },
    "Fossil Fuels": {
        "Coal": {"Brown Coal", "Black Coal", "Peat"},
        "Gas": {"Conventional Gas", "Non-Conventional Gas"},
        "Oil": {"Oil"},
    },
    "Non-Viable Alternatives": {
        "Biomass": {"Waste Fermentation", "Farmed Biomass", "BioFuels"},
        "Nuclear": {"Large Scale Fission", "Small Modular Fission", "Fusion"},
        "CCS": {"post-combustion", "pre-combustion", "Direct Air Capture"},
        "Ocean Energy": {"Wave", "Tidal", "Thermal"},
        "Geothermal": {"Geothermal Energy"},
    },
    "Storage and Transportation": {
        "Long-Term Storage": {
            "Gravity Storage",
            "Pumped Hydro Storage",
            "Compressed Air Energy Storage (CAES)",
            "Large-Scale Batteries",
            "Hydrogen Storage",
        },
        "Peaking Supply": {
            "Battery Energy Storage Systems (BESS)",
            "Home Battery",
            "Flywheels",
            "Thermal Storage",
        },
        "Transport": {
            "Electrical Transmission Lines",
            "Gas Pipelines",
            "Hydrogen Pipelines",
            "Oil Pipelines",
        },
    },
}

ISSUE_TAXONOMY = {
    "Economic": {
        "Affordability / Cost",
        "Jobs & Industry",
        "Innovation & Growth",
        "Opportunity Cost",
    },
    "Security": {
        "Reliability",
        "Infrastructure Resilience",
        "Resource Scarcity",
        "Resource Control",
        "Achievability",
    },
    "Green / Environmental Sustainability": {
        "Climate Change",
        "Ecology",
        "Natural Beauty",
    },
    "Justice": {"Fairness", "Consent", "Health Impacts"},
    "National Standing": {
        "International Obligations",
        "Keeping up internationally",
    },
}

# --- Literals

Impact = Literal["Alleviates", "Exacerbates", "Does Not Impact"]
tech_level_1 = []
tech_level_2 = []
tech_level_3 = []
for k, v in TECH_TAXONOMY.items():
    tech_level_1.append(k)
    for k2, v2 in v.items():
        tech_level_2.append(k2)
        for k3 in v2:
            tech_level_3.append(k3)

TechLevel1 = Literal.__getitem__(tuple(tech_level_1))
TechLevel2 = Literal.__getitem__(tuple(tech_level_2))
TechLevel3 = Literal.__getitem__(tuple(tech_level_3))

issue_level_1 = []
issue_level_2 = []
for k, v in ISSUE_TAXONOMY.items():
    issue_level_1.append(k)
    for k2 in v:
        issue_level_2.append(k2)

IssueLevel1 = Literal.__getitem__(tuple(issue_level_1))
IssueLevel2 = Literal.__getitem__(tuple(issue_level_2))

# --- Main Model with validation ---


class Label(BaseModel):
    tech_level_1: TechLevel1
    tech_level_2: Optional[TechLevel2] = (
        None  # Will validate later as Enum dynamically
    )
    tech_level_3: Optional[TechLevel3] = None

    issue_level_1: IssueLevel1
    issue_level_2: Optional[IssueLevel2] = None

    sentiment: Impact

    @model_validator(mode="after")
    @classmethod
    def check_tech_hierarchy(cls, values):
        lvl1 = values.tech_level_1
        lvl2 = values.tech_level_2
        lvl3 = values.tech_level_3

        errors = []

        # Check level 2 is valid under level 1
        if lvl2:
            if lvl1 not in TECH_TAXONOMY or lvl2 not in TECH_TAXONOMY[lvl1]:
                errors.append(
                    ErrorWrapper(
                        ValueError(
                            f"tech_level_2 '{lvl2}' is not a valid child of tech_level_1 '{lvl1}'"
                        ),
                        loc="tech_level_2"
                    )
                )

        # Check level 3 is valid under level 2 of level 1
        if lvl3:
            if not lvl2 or lvl1 not in TECH_TAXONOMY or lvl2 not in TECH_TAXONOMY[lvl1]:
                errors.append(
                    ErrorWrapper(
                        ValueError(
                            f"Cannot validate tech_level_3 '{lvl3}' without a valid tech_level_2 '{lvl2}' under tech_level_1 '{lvl1}'"
                        ),
                        loc="tech_level_3"
                    )
                )
            elif lvl3 not in TECH_TAXONOMY[lvl1][lvl2]:
                errors.append(
                    ErrorWrapper(
                        ValueError(
                            f"tech_level_3 '{lvl3}' is not a valid child of tech_level_2 '{lvl2}' under tech_level_1 '{lvl1}'"
                        ),
                        loc="tech_level_3"
                    )
                )

        if errors:
            raise ValidationError(errors, cls)

        return values

    @model_validator(mode="after")
    @classmethod
    def check_issue_hierarchy(cls, values):
        lvl1 = values.issue_level_1
        lvl2 = values.issue_level_2

        if lvl2:
            if lvl1 not in ISSUE_TAXONOMY or lvl2 not in ISSUE_TAXONOMY[lvl1]:
                raise ValidationError(
                    [
                        ErrorWrapper(
                            ValueError(
                                f"issue_level_2 '{lvl2}' is not a valid child of issue_level_1 '{lvl1}'"
                            ),
                            loc="issue_level_2"
                        )
                    ],
                    cls,
                )

        return values
