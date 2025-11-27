from models.filter.base_filter import Filter
from pydantic import BaseModel as PydanticBase

from openai import OpenAI


class FilterResponse(PydanticBase):
    is_included: bool


class GenerativeFilter(Filter):
    def __init__(self, model, endpoint, query, temp=0.1) -> None:
        self.model = model
        self.endpoint = endpoint
        self.query = query
        self.temp = temp
        self.client = OpenAI(base_url=endpoint)

    def infer(self, document):
        completion = self.client.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": self.query},
                {"role": "user", "content": self._get_feature(document)},
            ],
            response_format=FilterResponse,
        )
        response = completion.choices[0].message.parsed
        return response.is_included
