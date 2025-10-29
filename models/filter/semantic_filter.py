from models.filter.vector_filter import VectorFilter
import numpy as np
from openai import OpenAI


class SemanticFilter(VectorFilter):
    def __init__(
        self,
        model: str,
        endpoint: str,
        data_file: str,
        threshold: float = 0.8,
    ):
        self.model = model
        self.endpoint = endpoint
        self.data_file = data_file
        self.threshold = threshold
        self.client = OpenAI(base_url=endpoint)
        self.data = np.loadtxt(self.data_file, delimiter=",")
        self.centrepoint = np.sum(self.data, axis=0)

    def infer(self, document) -> bool:
        """
        Compute embedding of the document text and compare with query embeddings.
        Returns True if any similarity exceeds the threshold.
        """
        response = self.client.embeddings.create(
            model=self.model, input=document.text
        )
        doc_embedding = np.array(response.data[0].embedding)

        return (
            self._cosine_similarity(doc_embedding, self.centrepoint)
            >= self.threshold
        )
