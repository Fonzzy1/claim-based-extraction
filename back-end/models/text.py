
from typing import List
import json
from models import ClaimList
from constants import SYSTEM_EXTRACTOR

# OpenAI client initialization
client: OpenAI = OpenAI()

class Text:
    """
    A class representing text content for analysis.
    """
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.analyzed: bool = False
        self.claims: List[Claim] = []

    def analyze_text(self, redo: bool = False) -> None:
        """
        Analyze the text to extract claims using OpenAI's service.
        """
        if not self.analyzed or redo:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": SYSTEM_EXTRACTOR},
                    {"role": "user", "content": self.text},
                ],
                response_format=ClaimList,
            )

            claimlist: ClaimList = completion.choices[0].message.parsed
            self.claims = claimlist.claims
            self.analyzed = True

