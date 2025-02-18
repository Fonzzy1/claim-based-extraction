from typing import List
from newspaper import Article as base_article
from newspaper import Config
from tqdm import tqdm
import dill

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent


class Text:
    def __init__(self, text: str):
        self.text = text
        self.analysed = False
        self.claims = []

    def analyze(self):
        if not self.analysed:
            # Perform some kind of text analysis here
            self.analysed = True

class Article(Text):
    def __init__(self, url: str):
        super().__init__(text=None)
        self.url = url
        self.title = None
        self.authors = []
        self.publish_date = None
        self.fetched = False

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
    def __init__(self):
        pass

class Corpus:
    def __init__(self):
        self.articles: List[Text] = []

    def fetch_all(self, redo=False):
        for article in tqdm(self.articles, total=len(self.articles), desc='Fetching Articles'):
            if isinstance(article, Article) and (not article.fetched or redo):
                article.fetch()

    def to_pickle(self, path):
        with open(path, 'wb') as f:
            dill.dump(self, f)
    
    @classmethod
    def from_pickle(cls, filepath: str) -> 'Corpus':
        with open(filepath, 'rb') as f:
            return dill.load(f)

    @classmethod
    def from_urls(cls, urls: List[str]) -> 'Corpus':
        corpus = cls()
        for url in tqdm(urls, total=len(urls), desc='Creating corpus from urls'):
            article = Article(url)
            corpus.articles.append(article)
        return corpus

    @classmethod
    def from_texts(cls, texts: List[str]) -> 'Corpus':
        corpus = cls()
        for text in tqdm(texts, total=len(texts), desc='Creating corpus from texts'):
            text_article = Text(text)
            corpus.articles.append(text_article)
        return corpus

if __name__ == '__main__':
    with open('urls.txt', 'r') as f:
        urls = f.read().split('\n')
        corpus = Corpus.from_urls(urls)
        corpus.fetch_all()
        corpus.to_pickle('corpus.pkl')
