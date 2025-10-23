from models.deconstructor.base_deconstructor import BaseDeconstructor
from models.base_model import (
    Claim,
    ISSUE_TAXONOMY,
    TECH_TAXONOMY,
    EvaluationLabel,
    IssueDeclarationLabel,
    Label,
    Corpus,
    DocumentElement,
    Document,
)
import questionary


# --- Flatten the taxonomy structures for easy user selection ---
flat_tech_options = []
tech_backmap = {}

for l1, l2s in TECH_TAXONOMY.items():
    # Level 1
    flat_tech_options.append(l1)
    tech_backmap[l1] = (l1, None, None)

    for l2, l3s in l2s.items():
        # Level 2
        flat_tech_options.append(l2)
        tech_backmap[l2] = (l1, l2, None)

        for l3 in l3s:
            # Level 3
            flat_tech_options.append(l3)
            tech_backmap[l3] = (l1, l2, l3)


flat_issue_options = []
issue_backmap = {}

for l1, l2s in ISSUE_TAXONOMY.items():
    # Level 1
    flat_issue_options.append(l1)
    issue_backmap[l1] = (l1, None)

    for l2 in l2s:
        flat_issue_options.append(l2)
        issue_backmap[l2] = (l1, l2)


# --- Manual input flow for either Evaluation or Issue Declaration ---

def manual_label_input_flat() -> Label:
    """Prompt user to create either an EvaluationLabel or IssueDeclarationLabel."""
    label_type = questionary.select(
        "Select the type of label:",
        choices=["Evaluation", "Issue Declaration"],
    ).ask()

    # --- ISSUE declaration (simpler case) ---
    if label_type == "Issue Declaration":
        issue_choice = questionary.autocomplete(
            "Select an issue label (any level):",
            choices=flat_issue_options,
        ).ask()

        issue_l1, issue_l2 = issue_backmap[issue_choice]

        return IssueDeclarationLabel(
            issue_level_1=issue_l1,
            issue_level_2=issue_l2,
        )

    # --- EVALUATION label ---
    tech_choice = questionary.autocomplete(
        "Select a technology label (any level):",
        choices=flat_tech_options,
    ).ask()

    issue_choice = questionary.autocomplete(
        "Select an issue label (any level):",
        choices=flat_issue_options,
    ).ask()

    impact = questionary.autocomplete(
        "Select the impact:",
        choices=["Alleviates", "Exacerbates", "Does Not Impact"],
    ).ask()

    # Backfill taxonomy hierarchy
    tech_l1, tech_l2, tech_l3 = tech_backmap[tech_choice]
    issue_l1, issue_l2 = issue_backmap[issue_choice]

    return EvaluationLabel(
        tech_level_1=tech_l1,
        tech_level_2=tech_l2,
        tech_level_3=tech_l3,
        issue_level_1=issue_l1,
        issue_level_2=issue_l2,
        impact=impact,
    )


# --- Deconstructor class ---

class LabelingDeconstructor(BaseDeconstructor):
    def infer(self, claim: Claim):
        print("Claim text:\n")
        print(claim.text)
        print("\n--- Label the claim ---\n")
        label = manual_label_input_flat()
        print("\nCreated Label:\n", label)
        return label

    def infer_corpus(self, corpus: Corpus):
        return list(map(self.infer_document, corpus.documents))

    def infer_document(self, document: Document):
        return list(map(self.infer_element, document.elements))

    def infer_element(self, element: DocumentElement):
        return list(map(self.infer_claim, element.claims))
