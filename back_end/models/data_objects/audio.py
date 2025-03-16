from models.text import Text

class Audio(Text):
    def __init__(self, url: str) -> None:
        self.url= url 
