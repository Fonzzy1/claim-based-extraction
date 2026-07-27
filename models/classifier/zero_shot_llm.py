from typing import List
from openai import OpenAI
from models.classifier.base_classifier import BaseClassifier
from pydantic import BaseModel as PyBaseModel
from models.base_model import DocumentElement, Claim



class ZeroShotClassifier(BaseClassifier):
    def __init__(
            self,
            issues: dict,
            policies: dict, 
            model_key: str,
            endpoint: str,
            system_prompt: str,
            message_prompt_format_string: str,
        ):
            super().__init__(issues, policies)
            self.model_key = model_key
            self.endpoint = endpoint
            self.system_prompt = system_prompt
            self.message_prompt_format_string = message_prompt_format_string
            self.client = OpenAI(base_url=endpoint)

    def infer(self, element: DocumentElement):
        # Format the prompt string with context
        formatted_message = self.message_prompt_format_string.format(
            string=element.text, context="\n".join(element.context)
        )

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": formatted_message},
        ]

        response = self.client.chat.completions.parse(
            model=self.model_key,
            messages=messages,
            response_format=self.label_class,
        )

        # Parse the structured output using Pydantic
        content: List[str] = response.choices[0].message.parsed.extracted_claims
        claim_content = [Claim(x) for x in content]
        return claim_content
