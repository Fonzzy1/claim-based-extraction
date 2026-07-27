from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool
import dill
import os
import os
import io
from io import BytesIO
from multiprocessing.dummy import Pool as ThreadPool
from typing import Literal, Optional, List, Union
from pydantic import BaseModel as PyBaseModel, model_validator
from dataclasses import dataclass, field
from tqdm.contrib.concurrent import thread_map

class BaseModel:
    def save_to_file(self, filepath):
        if os.path.exists(filepath):
            raise FileExistsError("File already exists")
        with open(filepath, "wb") as f:
            dill.dump(self, f)
    @classmethod
    def load_from_file(cls, filepath):
        with open(filepath, "rb") as f:
            obj = dill.load(f)
        return obj

@dataclass
class DocumentElement:
    text: str
    context: List[str] = field(default_factory=list)
    claims: Optional[List] = None



from dataclasses import dataclass
from typing import Literal, Optional

ClaimType = Literal["signal", "evaluation", "impact"]
Label = Literal[1, -1]

class BaseLabelClass(PyBaseModel):
    issue: Optional[str] = None
    policy: Optional[str] = None
    label: Label
    claim_type: ClaimType

    @model_validator(mode="after")
    def validate_claim(self):
        if self.claim_type == "signal":
            if self.issue is None or self.policy is not None:
                raise ValueError("signal requires issue only")
        elif self.claim_type == "evaluation":
            if self.policy is None or self.issue is not None:
                raise ValueError("evaluation requires policy only")
        elif self.claim_type == "impact":
            if self.issue is None or self.policy is None:
                raise ValueError("impact requires both issue and policy")
        return self



@dataclass
class Document:
    id: int
    text: str
    title: Optional[str]
    elements: Optional[List[DocumentElement]] = None

@dataclass
class Corpus(BaseModel):
    documents: List[Document]

    @classmethod
    def from_file_of_strings(cls, file_path: str) -> "Corpus":
        with open(file_path, "r", encoding="utf-8") as f:
            docs = [
                Document(id=i, text=line.rstrip("\n"), title=None)
                for i, line in enumerate(f)
                if line.strip()
            ]
        return cls(documents=docs)


class DocumentLevel(BaseModel):
    """
    Base class for things that run inferance on documents
    """

    def infer_corpus(self, corpus: Corpus):
        with ThreadPool() as pool:
            return thread_map(self.infer_document, corpus.documents)

    def infer_document(self, document: Document):
        return self.infer(document)

    def transform(self, corpus: Corpus) -> Corpus:
        data = self.infer_corpus(corpus)
        return self._data_join_func(corpus, data)

    def _data_join_func(self, corpus, data):
        return corpus


class ElementLevel(DocumentLevel):
    """
    Base class for things that run inferance on Elements
    """

    def infer_document(self, document: Document):
        with ThreadPool() as pool:
            return pool.map(self.infer_element, document.elements)

    def infer_element(self, element: DocumentElement):
        return self.infer(element)


