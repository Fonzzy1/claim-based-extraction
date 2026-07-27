from models.base_model import (
    DocumentLevel,
    DocumentElement,
    Document
)
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from pydantic import BaseModel as TypingBaseModel
from typing import List, Literal
import pandas as pd

class BaseProcessor(DocumentLevel):
    def __init__(self, pre_context_size, post_context_size, splitting_function) -> None:
        self.pre_context_size = pre_context_size
        self.post_context_size = post_context_size
        self.splitting_function = splitting_function

    def infer(self, document: Document):
        """
        take in a single document and splits in into their sentences, paired
        with their pre-context and post-context windows
        """
        elements = [
                {"text": element}
            for element in self.splitting_function(document.text)
        ]

        for i in range(len(elements)):
            start = max(0, i - self.pre_context_size)
            end = min(len(elements), i + self.post_context_size + 1)

            pre_context = [x["text"] for x in elements[start:i]]
            post_context = [x["text"] for x in elements[i + 1:end]]

            elements[i]["context"] = pre_context + post_context

        return [DocumentElement(**element) for element in elements]

    def _data_join_func(self, corpus, data):
        for doc, res in zip(corpus.documents, data):
            doc.elements = res
        return corpus
