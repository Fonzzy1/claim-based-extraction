from models.classifier.base_classifier import BaseClassifier
from models.base_model import DocumentElement, Corpus, Document
import questionary


class LabelingClassifier(BaseClassifier):
    def infer(self, element: DocumentElement):
        print("Document Element Text:\n")
        print(element.text)
        print("\nContext:\n")
        print("\n".join(element.context))
        print("\n--- Extract claims ---\n")

        user_input = questionary.text(
            "Enter one or more claims, separated by commas:"
        ).ask()

        return [Claim(x.strip()) for x in user_input.split(",") if x.strip()]

    def infer_corpus(self, corpus: Corpus):
        return list(map(self.infer_document, corpus.documents))

    def infer_document(self, document: Document):
        return list(map(self.infer_element, document.elements))
