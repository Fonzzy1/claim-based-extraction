from models.base_model import BaseModel
from multiprocessing import Pool
from pydantic import BaseModel as TypingBaseModel
from typing import List


class BaseExtractor(BaseModel):
    def __init__(self) -> None:
        pass

    def infer(self, string, context) -> list[str]:
        return []

    def train(self, X, y) -> None:
        pass

    def infer_document(self, ls_string, ls_context) -> list[str]:
        with Pool() as pool:
            per_split_results = pool.starmap(
                self.infer, zip(ls_string, ls_context)
            )
        return [item for sublist in per_split_results for item in sublist]

    def infer_list(self, ls_processed_documents) -> list[list[str]]:
        out = []
        for ls_string, ls_context in ls_processed_documents:
            out.append(self.infer_document(ls_string, ls_context))
        return out


class Processor(BaseModel):
    def __init__(self, context_size, sentence_splitting_function) -> None:
        self.context_size = context_size
        self.sentence_splitting_function = sentence_splitting_function

    def transform(self, string: str) -> tuple[list[str], list[list[str]]]:
        """
        take in a single document and splits in into their sentences, paired
        with their context windows
        """
        sentences = self.sentence_splitting_function(string)
        contexts = []

        for i in range(len(sentences)):
            # Determine start and end indexes for context window
            start = max(0, i - self.context_size)
            end = min(len(sentences), i + self.context_size + 1)

            # Extract context sentences excluding the current sentence itself
            context = sentences[start:i] + sentences[i + 1 : end]
            contexts.append(context)

        return sentences, contexts

    def transform_list(
        self, string_list: list[str]
    ) -> list[tuple[list[str], list[list[str]]]]:
        """
        take in many documents and splits in into their sentences, paired
        with their context windows
        Will return a list the same lengr of the input, each with
        """
        with Pool() as pool:
            # Map the transform function across all input strings in parallel
            results = pool.map(self.transform, string_list)
        return results


# Define a Pydantic model for a list of strings output
class ExtractionOutput(TypingBaseModel):
    result: List[str]
