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

def construct_label_class(issues: dict, policies: dict) -> type:
    """
    Construct a label class with issue and policy fields constrained by the
    provided issue and policy values.

    The returned class subclasses BaseLabelClass and defines two optional
    annotated attributes:

    - issue: limited to one of the values contained in issues
    - policy: limited to one of the values contained in policies

    Args:
        issues: A mapping whose values are iterables of issue labels.
        policies: A mapping whose values are iterables of policy labels.

    Returns:
        A dynamically created subclass of BaseLabelClass with typed issue and
        policy attributes.
    """

    issue_values = tuple(chain.from_iterable(issues.values()))
    policy_values = tuple(chain.from_iterable(policies.values()))

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
    def __init__(self, issues, policies) -> None:
        self.issues = issues
        self.policies = policies
        self.label_class = construct_label_class(issues, policies)

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


