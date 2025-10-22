from models.base_model import ClaimLevel, Claim, Label
from multiprocessing import Pool


class BaseDeconstructor(ClaimLevel):
    def __init__(self) -> None:
        pass

    def infer(self, claim: Claim) -> Label | None:
        """
        for a single extracted claim
        """
        return None

    def train(self, X, y) -> None:
        pass

    def _data_join_func(self, corpus, data):
        for i, document in enumerate(corpus.documents):
            for j, element in enumerate(document.elements):
                if len(element.claims):
                    for k, claim in enumerate(element.claims):
                        claim.deconstruction = data[i][j][k]
        return corpus
