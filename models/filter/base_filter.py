from models.base_model import (
    DocumentLevel,
    Document,
    ElementLevel,
    DocumentElement,
)
from multiprocessing import Pool


class Filter(DocumentLevel):
    def __init__(self) -> None:
        pass

    def infer(self, document: Document | DocumentElement) -> bool:
        return True

    def train(self, X, y) -> None:
        pass

    def _data_join_func(self, corpus, data):
        corpus.documents = [
            x for i, x in enumerate(corpus.documents) if data[i]
        ]
        return corpus


def make_element_filter(base_filter_cls):
    """
    Dynamically create an ElementFilter class from an existing document-level Filter.
    It overrides `infer` and `_data_join_func` to work on elements.
    """

    class ElementFilter(ElementLevel, base_filter_cls):

        def _data_join_func(self, corpus, data):
            for i, document in enumerate(corpus.documents):
                document.elements = [
                    x for j, x in enumerate(document.elements) if data[i][j]
                ]
            return corpus

    ElementFilter.__name__ = f"Element{base_filter_cls.__name__}"
    return ElementFilter
