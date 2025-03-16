from typing import List
from tqdm import tqdm
from models.data_objects.article import Article
from models.data_objects.audio import Audio
from models.data_objects.video import Video
from models.text import Text
import requests
from bs4 import BeautifulSoup

url = 'https://www.abc.net.au/news/topic/electricity-production-and-distribution'

class Source():
    def __init__(self, url):
        self.url = url
        self.objects=[]
        self.object_class = Text

    def find_objects(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            self.objects.append(self.object_class(link['href']))

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

class VideoSource(Source):
    def __init__(self, url):
        super().__init__(url)


class TextSource(Source):
    def __init__(self, url):
        super().__init__(url)
        self.object_class = Article

class ABCTextSource(TextSource):
    def __init__(self, url):
        super().__init__(url)

    def find_objects(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_tag = soup.find('meta', attrs={'name': 'ContentId'})
        content_id = meta_tag['content']
        news_api_url = f'https://www.abc.net.au/news-web/api/loader/topicstoriesmore?documentId={content_id}&future=true&offset=0'
        total  = requests.get(news_api_url + '&size=0').json()['pagination']['total']
        full_json = requests.get(news_api_url + f'&size={total}').json()
        links = [ 'https://abc.net.au' + x['link'] for x in full_json['collection']]
        self.objects =  [self.object_class(link) for link in links]

class NewsCorpMegaSource(TextSource,VideoSource,AudioSource):
    def __init__(self, url):
        super().__init__(url)

    def find_objects(self):
        url = 'https://www.news.com.au/sitesearch/1/indexes/*/queries'
        res = requests.post(url, json=
                      {"requests":[
                          {
                              "indexName":"prod_news_content_bylatest",
                              "params":"page=1&query=Coal%20Power&tagFilters="
                                    }
                               ]
                       }
                      ).json()

        results = res['results'][0]['hits']
        objects=[x['canonical']['link'] for x in results]


        



