#! docker compose run -it --build back-end python
from models.data_objects.audio import Audio
import yt_dlp
import tempfile
from models.ai_client import Ai


client = Ai()

class Video(Audio):
    def __init__(self, url: str) -> None:
        super().__init__(url)

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
                self.audio = f.read()


if __name__=='__main__':
    self = Video('https://www.skynews.com.au/opinion/outsiders/germany-to-enshrine-climate-neutrality-by-2045-into-its-constitution/video/6ec4eac5cc7bc329b835f26eb809f0eb')
    self.fetch()
    trans = self.transcribe()



