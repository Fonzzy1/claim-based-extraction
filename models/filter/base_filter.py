from models.base_model import BaseModel
from models.data_structure import *
from multiprocessing import Pool
import pandas as pd


class Filter(BaseModel):
    def __init__(self) -> None:
        pass

    def infer(self, string) -> bool:
        return True

    def train(self, X, y) -> None:
        pass

    def infer_corpus(self, corpus: Corpus) -> list:
        with Pool() as pool:
            results = pool.map(self.infer, [d.text for d in corpus.documents])
        return results

    def transform(self, corpus: Corpus) -> Corpus:
        keys: dict = self.infer_corpus(corpus)
        corpus.documents = [
            x for i, x in enumerate(corpus.documents) if keys[i]
        ]
        return corpus
