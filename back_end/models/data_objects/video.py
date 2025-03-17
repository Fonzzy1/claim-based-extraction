#! docker compose run -it --build back-end python
from models.text import Text
import yt_dlp
import tempfile


class Video(Text):
    def __init__(self, url: str) -> None:
        self.url= url 
        self.fetched = False

    def fetch(self, redo=False):
        if not self.fetched or redo:
            tmp_file = tempfile.mktemp()
            ydl_opts = {
                    'verbose':True,
                    'format': 'bestaudio/best',
                    'outtmpl': f'{tmp_file}.%(ext)s',
                    'postprocessors': [{  # Extract audio using ffmpeg
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }]
                    }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.url)

            with open(f'{tmp_file}.mp3', 'rb') as f:
                self.audio_data = f.read()

    def transcribe(self):
            # Initialize the Whisper model
            model = whisper.load_model("base", device = 'cpu')
            # Load the audio data into a temporary file
            with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
                temp_audio_file.write(self.audio_data)
                temp_audio_file.flush()
                # Transcribe the audio using Whisper
                result = model.transcribe(temp_audio_file.name)
            # Return the transcribed text
            return result['text']

if __name__=='__main__':
    self = Video('https://www.skynews.com.au/opinion/outsiders/germany-to-enshrine-climate-neutrality-by-2045-into-its-constitution/video/6ec4eac5cc7bc329b835f26eb809f0eb')
    self.fetch()
    trans = self.transcribe()



