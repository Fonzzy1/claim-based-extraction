from models.text import Text
import yt_dlp
import io


class Video(Text):
    def __init__(self, url: str) -> None:
        self.url= url 

    def fetch(self, redo=False):
        if not self.fetched or redo:
                buffer = io.BytesIO()
                ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': '-',
                        'quiet': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                    }],
                        'progress_hooks': [lambda d: buffer.write(d.get('data',
                                                                        b'')) 
                                       if d['status'] == 'finished' else None]
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                buffer.seek(0)

self = Video('https://www.skynews.com.au/opinion/outsiders/musk-derangement-syndrome-sky-news-host-examines-backlash-against-doge/video/cb38bcd37d4f202b1a256d62fbf16c9b')



