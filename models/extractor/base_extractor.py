from models.base_model import BaseModel
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from pydantic import BaseModel as TypingBaseModel
from typing import List
from models.data_structure import *
import pandas as pd


# Define a Pydantic model for a list of strings output
class ExtractionOutput(TypingBaseModel):
    result: List[str]


class BaseExtractor(BaseModel):
    def __init__(self) -> None:
        pass

    def infer(self, string, context) -> ExtractionOutput:
        """
        for a single sentence in a documents, extract all the claims from it
        """
        return []

    def train(self, X, y) -> None:
        pass

    def infer_document(self, data) -> list:
        with ThreadPool() as pool:
            out = pool.starmap(
                self.infer,
                [
                    (string["text"], string["context"])
                    for string in data["strings"]
                ],
            )
        return out

    def infer_dict(self, data: dict) -> list:
        out = []
        for k, v in data.items():
            out.append(self.infer_document(v))
        return out

    def transform(self, data: dict) -> dict:
        inferred = self.infer_dict(data)
        keys = list(data.keys())
        for i, key in enumerate(keys):
            for j, claims in enumerate(inferred):
                data[key]["strings"][j]["claims"] = inferred[i][j]
        return data


class Processor(BaseModel):
    def __init__(self, context_size, sentence_splitting_function) -> None:
        self.context_size = context_size
        self.sentence_splitting_function = sentence_splitting_function

    def infer(self, string: str) -> list[DocumentElement]:
        """
        take in a single document and splits in into their sentences, paired
        with their context windows
        """
        sentences = [
            {"text": sentence}
            for sentence in self.sentence_splitting_function(string)
        ]

        for i in range(len(sentences)):
            start = max(0, i - self.context_size)
            end = min(len(sentences), i + self.context_size + 1)
            context = [x["text"] for x in sentences[start:i] + sentences[i:end]]
            sentences[i]["context"] = context

        
        return [DocumentElement(**element) for element in sentences]

    def transform(self, corpus: Corpus) -> dict:
        """
        take in many documents and splits in into their sentences, paired
        with their context windows
        Will return a list the same length of the input, each with
        """
        with Pool() as pool:
            # Map the transform function across all input strings in parallel
            results = pool.map(self.infer, [d.text for d in corpus.documents])
        for doc, res in zip(corpus.documents, results):
            doc.elements = res
        return data
