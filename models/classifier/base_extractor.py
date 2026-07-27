from models.base_model import (
    DocumentLevel,
    ElementLevel,
    Claim,
    DocumentElement,
    Document
)
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from pydantic import BaseModel as TypingBaseModel
from typing import List, Literal
import pandas as pd


# Define a Pydantic model for a list of strings output
class BaseExtractor(ElementLevel):
    def __init__(self) -> None:
        pass

    def infer(self, element: DocumentElement) -> List[Claim]:
        """
        for a single sentence in a documents, extract all the claims from it
        """
        return []

    def train(self, X, y) -> None:
        pass

    def _data_join_func(self, corpus, data):
        for i, document in enumerate(corpus.documents):
            for j, element in enumerate(document.elements):
                element.claims = data[i][j]
        return corpus


class Processor(DocumentLevel):
    def __init__(self, context_size, sentence_splitting_function) -> None:
        self.context_size = context_size
        self.sentence_splitting_function = sentence_splitting_function

    def infer(self, document: Document):
        """
        take in a single document and splits in into their sentences, paired
        with their context windows
        """
        sentences = [
            {"text": sentence}
            for sentence in self.sentence_splitting_function(document.text)
        ]

        for i in range(len(sentences)):
            start = max(0, i - self.context_size)
            end = min(len(sentences), i + self.context_size + 1)
            context = [x["text"] for x in sentences[start:i] + sentences[i:end]]
            sentences[i]["context"] = context

        return [DocumentElement(**element) for element in sentences]

    def _data_join_func(self, corpus, data):
        for doc, res in zip(corpus.documents, data):
            doc.elements = res
        return corpus
