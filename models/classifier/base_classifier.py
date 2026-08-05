from models.base_model import (
    DocumentLevel,
    ElementLevel,
    DocumentElement,
    BaseLabelClass
)
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from itertools import chain


from pydantic import BaseModel as TypingBaseModel
from typing import List, Literal, Optional
from enum import Enum
import pandas as pd

def construct_label_class(issues, policies) -> type:
    def _values(x):
        if isinstance(x, dict):
            return tuple(x.keys()) + tuple(chain.from_iterable(x.values()))
        return tuple(x)

    issue_values = _values(issues)
    policy_values = _values(policies)

    IssueLiteral = Literal.__getitem__(issue_values)
    PolicyLiteral = Literal.__getitem__(policy_values)

    class LabelClass(BaseLabelClass):
        issue: Optional[IssueLiteral] = None
        policy: Optional[PolicyLiteral] = None

    class ReturnClass(TypingBaseModel):
        labels: List[LabelClass]

    return ReturnClass
# Define a Pydantic model for a list of strings output
class BaseClassifier(ElementLevel):
    def __init__(self) -> None:
        self.label_class = None

    def infer(self, element: DocumentElement):
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


