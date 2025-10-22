from models.deconstructor.base_deconstructor import BaseDeconstructor
from models.base_model import (
    Claim,
    ISSUE_TAXONOMY,
    TECH_TAXONOMY,
    Label,
    Corpus,
    DocumentElement,
    Document,
)
import questionary


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
        # Level 2
        flat_issue_options.append(l2)
        issue_backmap[l2] = (l1, l2)


def manual_label_input_flat() -> Label:
    tech_choice = questionary.autocomplete(
        "Select a technology label (any level):", choices=flat_tech_options
    ).ask()

    issue_choice = questionary.autocomplete(
        "Select an issue label (any level):", choices=flat_issue_options
    ).ask()

    sentiment = questionary.autocomplete(
        "Select the sentiment (impact):",
        choices=["Alleviates", "Exacerbates", "Does Not Impact"],
    ).ask()

    # Backfill
    tech_l1, tech_l2, tech_l3 = tech_backmap[tech_choice]
    issue_l1, issue_l2 = issue_backmap[issue_choice]

    return Label(
        tech_level_1=tech_l1,
        tech_level_2=tech_l2,
        tech_level_3=tech_l3,
        issue_level_1=issue_l1,
        issue_level_2=issue_l2,
        sentiment=sentiment,
    )


class LabelingDeconstructor(BaseDeconstructor):
    def infer(self, claim: Claim):
        print("Claim text:\n")
        print(claim.text)
        print("\n--- Label the claim ---\n")
        return manual_label_input_flat()

    def infer_corpus(self, corpus: Corpus):
        return list(map(self.infer_document, corpus.documents))

    def infer_document(self, document: Document):
        return list(map(self.infer_element, document.elements))

    def infer_element(self, element: DocumentElement):
        return list(map(self.infer_claim, element.claims))
