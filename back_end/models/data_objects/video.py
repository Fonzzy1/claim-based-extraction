from models.text import Text

class Video(Text):
    def __init__(self, url: str) -> None:
        self.url= url 
