from models.base_model import (
    DocumentLevel,
    Document,
    ElementLevel,
    DocumentElement,
)
from multiprocessing.dummy import Pool as ThreadPool


class Filter(DocumentLevel):
    def __init__(self) -> None:
        pass

    def infer(self, document: Document | DocumentElement) -> bool:
        return True

    def train(self, X, y) -> None:
        pass

    def _get_feature(self, obj):
        return obj.title

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

    class ElementFilter(base_filter_cls):

        def infer_document(self, document: Document):
            with ThreadPool() as pool:
                return pool.map(self.infer_element, document.elements)

        def infer_element(self, element: DocumentElement):
            return self.infer(element)

        def _get_feature(self, obj):
            return obj.text

        def _data_join_func(self, corpus, data):
            for i, document in enumerate(corpus.documents):
                document.elements = [
                    x for j, x in enumerate(document.elements) if data[i][j]
                ]
            return corpus

    ElementFilter.__name__ = f"Element{base_filter_cls.__name__}"
    return ElementFilter
