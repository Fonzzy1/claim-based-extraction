from models.filter.base_filter import Filter
import numpy as np
from openai import OpenAI

class VectorFilter(Filter):
    def __init__(self, model: str, endpoint: str, query_strings: list[str],
                 threshold: float = 0.8):
        """
        model: str, embedding model name e.g. "text-embedding-3-small"
        endpoint: str, OpenAI API endpoint (can be left default if using openai library)
        query_strings: list of str, the queries to compare against
        threshold: float, similarity threshold between 0 and 1
        """
        self.model = model
        self.endpoint = endpoint
        self.query_strings = query_strings
        self.threshold = threshold
        self.query_embeddings = self._get_embeddings(query_strings)
        self.client = OpenAI()

    def _get_embeddings(self, texts):
        """
        Get embeddings from OpenAI API.
        Returns: list of numpy arrays
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [np.array(e['embedding']) for e in response['data']]

    def _cosine_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def infer(self, document) -> bool:
        """
        Compute embedding of the document text and compare with query embeddings.
        Returns True if any similarity exceeds the threshold.
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=document.text
        )
        doc_embedding = np.array(response['data'][0]['embedding'])

        for query_emb in self.query_embeddings:
            if self._cosine_similarity(doc_embedding, query_emb) >= self.threshold:
                return True
        return False
