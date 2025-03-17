#! docker compose run -it --build back-end python
from models.text import Text
from models.ai_client import Ai
import requests

client = Ai()

class Audio(Text):
    def __init__(self, url: str) -> None:
        self.url= url 
        self.fetched = False
        self.audio = None

    def fetch(self, redo= False):
        if not self.fetched or redo:
            res = requests.get(self.url)
            self.audio = res.content
            self.fetched = True

    def transcribe(self):
        self.text = client.transcribe_audio_object(self.audio)['text']

if __name__=='__main__':
    self = Audio('https://cdn.theconversation.com/audio/1566/nimbin-mixdownfinalllll.mp3')
    self.fetch()
    self.transcribe()

