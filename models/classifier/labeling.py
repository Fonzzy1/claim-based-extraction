from models.classifier.base_classifier import BaseClassifier
from models.base_model import DocumentElement, Corpus, Document, BaseLabelClass
import questionary
from questionary import Choice
from itertools import chain


class LabelingClassifier(BaseClassifier):
    def _flatten_choices(self, mapping):
        return list(chain.from_iterable(mapping.values()))

    def _with_none_choice(self, choices):
        return [Choice("None", value=None)] + [Choice(str(choice), value=choice) for choice in choices]

    def infer(self, element: DocumentElement):
        print("Sentence:\n")
        print(element.text)
        print("\nContext:\n")
        print("\n".join(element.context) if element.context else "")
        print("\n--- Label element ---\n")

        issue_choices = self._with_none_choice(self._flatten_choices(self.issues))
        policy_choices = self._with_none_choice(self._flatten_choices(self.policies))

        labels = []

        while True:
            is_claim = questionary.confirm(
                "Is there a claim?", default=False
            ).ask()

            if not is_claim:
                break

            issue = questionary.select(
                "Select an issue:",
                choices=issue_choices,
            ).ask()

            policy = questionary.select(
                "Select a policy:",
                choices=policy_choices,
            ).ask()

            if issue is None and policy is None:
                print("\nA claim must have at least an issue or a policy.\n")
                continue

            value = questionary.select(
                "Select a label value:",
                choices=["+1", "-1"],
            ).ask()

            if value is None:
                break
            labels.append(
                    BaseLabelClass(issue = issue, policy = policy, label= 1 if value == "+1" else -1,
                  claim_type='impact' if issue and policy else 'signal' if issue else 'evaluation')

            )

            add_another = questionary.confirm(
                "Add another label for this sentence?", default=False
            ).ask()

            if not add_another:
                break

        return labels

    def infer_corpus(self, corpus: Corpus):
        return list(map(self.infer_document, corpus.documents))

    def infer_document(self, document: Document):
        return list(map(self.infer, document.elements))

