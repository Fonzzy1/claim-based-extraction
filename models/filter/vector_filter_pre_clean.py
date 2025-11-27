from models.filter.vector_filter import VectorFilter
import numpy as np
from openai import OpenAI


class CleanStringVectorFilter(VectorFilter):

    def _get_feature(self, obj):
        text = obj.title
        for string in self.rm_strings:
            text = text.replace(string, "")
        return text.lower()

    def __init__(
        self,
        model: str,
        endpoint: str,
        query_strings: list[str],
        rm_strings: list[str],
        threshold: float = 0.8,
    ):
        """
        model: str, embedding model name e.g. "text-embedding-3-small"
        endpoint: str, OpenAI API endpoint (can be left default if using openai library)
        query_strings: list of str, the queries to compare against
        threshold: float, similarity threshold between 0 and 1
        rm_strings: list of strings to remove from the docuemt
        """
        self.model = model
        self.endpoint = endpoint
        self.query_strings = query_strings
        self.threshold = threshold
        self.client = OpenAI(base_url=endpoint)
        self.query_embeddings = self._get_embeddings(query_strings)
        self.rm_strings = rm_strings
