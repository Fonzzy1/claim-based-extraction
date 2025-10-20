from models.base_model import BaseModel
from multiprocessing import Pool

class Filter(BaseModel):
    def __init__(self) -> None:
        pass

    def infer(self, string) -> bool:
        return True

    def train(self, X, y) -> None:
        pass
 
    def infer_list(self, ls) -> list[bool]:
        with Pool() as pool:
            return pool.map(self.infer, ls)

    def filter(self, ls) -> list:
        with Pool() as pool:
            keys = pool.map(self.infer, ls)
        return [item for item, key in zip(ls, keys) if key]



