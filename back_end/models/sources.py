from typing import List
from tqdm import tqdm
from models.data_objects.article import Article
from models.text import Text

class Source():
    def __init__(self, url):
        self.url = url
        self.objects=[]
        self.object_class = Text

    def get_urls(self):
        pass

    def fetch_all_objects(self, redo: bool = False) -> None:
        """
        Fetch all texts in the corpus if not already fetched.
        """
        for text in tqdm(self.objects, total=len(self.objects), desc='Fetching Texts'):
                text.fetch(redo)

    @classmethod
    def from_urls(cls, urls: List):
        s = cls(None)
        s.objects = [s.object_class(url) for url in urls]
        return s


class AudioSource(Source):
    def __init__(self, url):
        super().__init__(url)


class TextSource(Source):
    def __init__(self, url):
        super().__init__(url)
        self.object_class = Article

class VideoSource(Source):
    def __init__(self, url):
        super().__init__(url)










