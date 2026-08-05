from models.classifier.base_classifier import BaseClassifier
from models.base_model import DocumentElement, Corpus, Document, BaseLabelClass
import questionary
from questionary import Choice
from typing import get_args, get_origin, Union, Literal


class LabelingClassifier(BaseClassifier):
    def _with_none_choice(self, choices):
        return [Choice("None", value=None)] + [Choice(str(choice), value=choice) for choice in choices]

    def _extract_literal_values(self, annotation):
        origin = get_origin(annotation)

        if origin is Literal:
            return list(get_args(annotation))

        if origin is Union:
            values = []
            for arg in get_args(annotation):
                if arg is type(None):
                    continue
                values.extend(self._extract_literal_values(arg))
            return values

        return []

    def _get_label_model(self):
        if self.label_class is None:
            raise ValueError("self.label_class is not set")

        if "labels" not in self.label_class.model_fields:
            raise ValueError("self.label_class does not contain a 'labels' field")

        labels_annotation = self.label_class.model_fields["labels"].annotation
        label_args = get_args(labels_annotation)

        if not label_args:
            raise ValueError("Could not extract inner label model from 'labels' field")

        return label_args[0]

    def _get_possible_label_values(self, field_name: str):
        label_model = self._get_label_model()

        if field_name not in label_model.model_fields:
            raise ValueError(f"Field '{field_name}' not found in label model")

        annotation = label_model.model_fields[field_name].annotation
        values = self._extract_literal_values(annotation)

        return sorted(set(values))

    def infer(self, element: DocumentElement):
        print("Sentence:\n")
        print(element.text)
        print("\nContext:\n")
        print("\n".join(element.context) if element.context else "")
        print("\n--- Label element ---\n")

        issue_choices = self._with_none_choice(self._get_possible_label_values("issue"))
        policy_choices = self._with_none_choice(self._get_possible_label_values("policy"))

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
                BaseLabelClass(
                    issue=issue,
                    policy=policy,
                    label=1 if value == "+1" else -1,
                    claim_type="impact" if issue and policy else "signal" if issue else "evaluation",
                )
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

