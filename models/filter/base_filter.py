from models.base_model import DocumentLevel, Document
from multiprocessing import Pool


class Filter(DocumentLevel):
    def __init__(self) -> None:
        pass

    def infer(self, string) -> bool:
        return True

    def train(self, X, y) -> None:
        pass

    def infer_document(self, document: Document) -> bool:
        return self.infer(document.text)

    def _data_join_func(self, corpus, data):
        corpus.documents = [
            x for i, x in enumerate(corpus.documents) if data[i]
        ]
        return corpus
