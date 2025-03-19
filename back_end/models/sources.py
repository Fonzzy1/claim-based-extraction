#! docker compose run -it --build back-end python
from typing import List, Dict
from tqdm import tqdm
from models.data_objects.article import Article
from models.data_objects.audio import Audio
from models.data_objects.video import Video
from models.text import Text
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd


class Source():
    def __init__(self, url):
        self.url = url
        self.objects: Dict[str, Text] = {}
        self.object_class = Text

    def find_objects(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            if link['href'] not in self.objects.keys():
                self.objects[link['href']] = self.object_class(link['href'])

    def fetch_all_objects(self, redo: bool = False) -> None:
        """
        Fetch all texts in the corpus if not already fetched.
        """
        for text in tqdm(self.objects.values(), total=len(self.objects),
                         desc=f'Fetching Texts for {self.url}'):
                text.fetch(redo)

    @classmethod
    def from_urls(cls,site_url, urls: List):
        s = cls(site_url)
        s.objects = {url:s.object_class(url) for url in urls}
        return s


class AudioSource(Source):
    def __init__(self, url):
        super().__init__(url)
        self.object_class = Audio

class VideoSource(Source):
    def __init__(self, url):
        super().__init__(url)
        self.object_class = Video


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
        for link in links:
            if link not in self.objects.keys():
                self.objects[link] = self.object_class(link)


def query_newscorp(query):
    url = 'https://www.heraldsun.com.au/sitesearch/1/indexes/*/queries'

    results = []
     
    i = 0
    nb_pages = 100
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0',
        'Origin': 'https://www.heraldsun.com.au',
        'Cookie': 'nk=gimmeyourdata',  
    }
    while i < nb_pages:
        print(i)
        data = {
            'requests': [{
                'indexName': 'prod_plnn_content_bylatest',
                'params': urllib.parse.urlencode({
                    'page': i,
                    'query': str(query).lower(),
                })
            }]
        }

        response = requests.post(url, headers=headers, json=data, allow_redirects=False)
        results += response.json()['results'][0]['hits']
        nb_pages = response.json()['results'][-1]['nbPages']
        i+=1
    
    links = [
                (x['canonical']['link'] if 'canonical' in x else 
                 x.get(x.get('seoOwner'), {}).get('link'), 
                 x['type'], 
                 x.get('seoOwner')) 
                for x in results
                ]

    return links

if __name__=='__main__':
    links  = query_newscorp('Gas Power')
    df = pd.DataFrame(links, columns = ['url','type','owner'])
    df.groupby(['owner','type']).count()

        
