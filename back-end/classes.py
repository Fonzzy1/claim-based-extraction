from typing import List
from newspaper import Article as base_article
from newspaper import Config
from tqdm import tqdm
import dill

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

class Article:
    def __init__(self, url):
        self.url = url
        self.fetched = False
        self.analysed = False

    def fetch(self):
        article = base_article(self.url, config=config)
        article.download()
        article.parse()
        
        self.title = article.title
        self.text = article.text
        self.authors = article.authors
        self.publish_date = article.publish_date
        self.fetched = True

class Claim:
    def __init__(self ):
        pass


class Corpus:
    def __init__(self):
        self.articles: List[Article] = []

    def fetch_all(self, redo=False):
        for article in tqdm(self.articles, total=len(self.articles), desc='Fetching Articles'):
            if not article.fetched or redo:
                article.fetch()

    def to_pickle(self, path):
        with open(path, 'wb') as f:
            dill.dump(self, f)  # Corrected: Dump self, not path
    
    @classmethod
    def from_pickle(cls, filepath: str) -> 'Corpus':
        """Create a Corpus instance from a pickle file."""
        with open(filepath, 'rb') as f:
            return dill.load(f)

    @classmethod
    def from_urls(cls, urls: List[str]) -> 'Corpus':
        corpus = cls()
        for url in tqdm(urls, total=len(urls), desc='Creating corpus from urls'):
            article = Article(url)
            corpus.articles.append(article)
        return corpus

if __name__ == '__main__':
    with open('urls.txt', 'r') as f:
        urls = f.read().split('\n')
        corpus = Corpus.from_urls(urls)
        corpus.fetch_all()
        corpus.to_pickle('corpus.pkl')
