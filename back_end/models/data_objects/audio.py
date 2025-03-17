from models.text import Text
from models.data_objects.audio import Audio
import yt_dlp
import tempfile
from models.ai_client import Ai

client = Ai()

class Audio(Text):
    def __init__(self, url: str) -> None:
        self.url= url 
        self.fetched = False
        self.audio = None

    def transcribe(self):
        self.text = client.transcribe_audio_object(self.audio)['text']
