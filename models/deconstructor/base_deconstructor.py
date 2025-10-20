from models.base_model import BaseModel
from models.deconstructor.codebook import Label


class BaseDeconstructor(BaseModel):
    def __init__(self) -> None:
        pass

    def infer(self, string) -> Label:
        """
        for a single extracted claim
        """
        return []

    def train(self, X, y) -> None:
        pass

    def infer_list(self, ls_string) -> list[str]:
        with Pool() as pool:
            results = pool.starmap(self.infer, ls_string)
        return results
