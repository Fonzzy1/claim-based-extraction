from models.base_model import BaseModel
from models.deconstructor.codebook import Label
from multiprocessing import Pool


class BaseDeconstructor(BaseModel):
    def __init__(self) -> None:
        pass

    def infer(self, string) -> Label | None:
        """
        for a single extracted claim
        """
        return None

    def train(self, X, y) -> None:
        pass

    def infer_string(self, data):
        for claim in data:
            pass

    def infer_document(self, data: dict) -> list[Label | None]:
        with Pool() as pool:
            results = pool.starmap(self.infer, data["claims"])
        return results

    def infer_dict(self, data: dict) -> list:
        out = []
        for k, v in data.items():
            out.append(self.infer_document(v))
        return out

    def transform(self, data: dict) -> dict:
        inferred = self.infer_dict(data)
        keys = list(data.keys())
        for i in range(len(keys)):
            data[keys[i]]["claims"] = inferred[i]
        return data
