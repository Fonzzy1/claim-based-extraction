#! docker compose run -it --build back-end python
from models.text import Text
import yt_dlp
import tempfile
from io import BytesIO
import yt_dlp
import speech_recognition as sr


class Video(Text):
    def __init__(self, url: str) -> None:
        self.url= url 
        self.fetched = False

    def fetch(self, redo=False):
        if not self.fetched or redo:
            tmp_file = tempfile.mktemp()[1]
            ydl_opts = {
                    'format':'ba',
                    'outtmpl': tmp_file,
                    'quiet': False,
                    }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.url)

            with open(tmp_file,'rb') as f:
                self.audio_data = f.read()

    def transcribe(self):
        # Initialize recognizer
        recognizer = sr.Recognizer()

        # Load the audio data into an AudioFile instance using BytesIO
        with sr.AudioFile(BytesIO(self.audio_data)) as source:
            audio = recognizer.record(source)

        # Using Google's free service to transcribe
        try:
            return recognizer.recognize_google(audio)

        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google; {e}"

self = Video('https://www.skynews.com.au/opinion/outsiders/germany-to-enshrine-climate-neutrality-by-2045-into-its-constitution/video/6ec4eac5cc7bc329b835f26eb809f0eb')
self.fetch()
trans = self.transcribe()



