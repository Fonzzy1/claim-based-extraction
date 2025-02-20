from models.ai_client import Ai
from typing import List
from models.claim import ClaimList
from constants import SYSTEM_EXTRACTOR

# OpenAI client initialization
client: Ai = Ai()

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
            claimlist = client.structured_complete(
                messages=[
                    {"role": "system", "content": SYSTEM_EXTRACTOR},
                    {"role": "user", "content": self.text},
                ],
                structure=ClaimList,
            )

            self.claims = claimlist.claims
            self.analyzed = True

