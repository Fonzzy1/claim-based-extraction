from models.deconstructor.codebook import Label
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Claim:
    text: str
    deconstruction: Optional[Label] = None


@dataclass
class DocumentElement:
    text: str
    context: List[str] = field(default_factory=list)
    claims: Optional[List[Claim]] = None


@dataclass
class Document:
    id: int
    text: str
    elements: Optional[List[DocumentElement]] = None


@dataclass
class Corpus:
    documents: List[Document]
