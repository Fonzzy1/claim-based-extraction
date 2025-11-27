from models.filter.base_filter import Filter
from pydantic import BaseModel as PydanticBase

from openai import OpenAI


class InitialFilterResponse(PydanticBase):
    is_included: bool
    more_info_needed: bool


class FilterResponse(PydanticBase):
    is_included: bool


class TwoStepGenerativeFilter(Filter):
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
            response_format=InitialFilterResponse,
        )
        response = completion.choices[0].message.parsed
        if response.more_info_needed:
            completion = self.client.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.query},
                    {"role": "user", "content": document.title},
                    {"role": "assistant", "content": "more_info_needed"},
                    {"role": "user", "content": document.text},
                ],
                response_format=FilterResponse,
            )
            response = completion.choices[0].message.parsed

        return response.is_included
