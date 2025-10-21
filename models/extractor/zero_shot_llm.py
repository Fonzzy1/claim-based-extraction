from typing import List
from openai import OpenAI
from models.extractor.base_extractor import BaseExtractor, ExtractionOutput


class ZeroShotExtractor(BaseExtractor):
    def __init__(
        self,
        model_key: str,
        endpoint: str,
        system_prompt: str,
        message_prompt_format_string: str,
    ):
        self.model_key = model_key
        self.endpoint = endpoint
        self.system_prompt = system_prompt
        self.message_prompt_format_string = message_prompt_format_string
        self.client = OpenAI()

    def infer(self, string: str, context: list[str]) -> ExtractionOutput:
        # Format the prompt string with context
        formatted_message = self.message_prompt_format_string.format(
            string=string, context="\n".join(context)
        )

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": formatted_message},
        ]

        # Define the expected JSON schema for structured output

        response = self.client.chat.completions.parse(
            model=self.model_key,
            messages=messages,
            response_format=ExtractionOutput,  # or "json" depending on SDK
        )

        # Parse the structured output using Pydantic
        # The content should be a dict with a "result" key holding list[str]
        content = response.choices[0].message.parsed
        return content
