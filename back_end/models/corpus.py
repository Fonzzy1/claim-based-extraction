from typing import List
from tqdm import tqdm
import dill
from models.text  import Text
from models.article import Article

class Corpus:
    """
    A class to manage and process a collection of articles.
    """
    def __init__(self) -> None:
        self.articles: List[Text] = []
    
    def process_all_articles(self, redo: bool = False) -> None:
        """
        Fetch, analyze, and evaluate all articles in the corpus.
        """
        self.fetch_all_articles(redo)
        self.analyze_all_articles(redo)
        self.evaluate_all_claims(redo)

    def fetch_all_articles(self, redo: bool = False) -> None:
        """
        Fetch all articles in the corpus if not already fetched.
        """
        for article in tqdm(self.articles, total=len(self.articles), desc='Fetching Articles'):
            if isinstance(article, Article):
                article.fetch_article(redo)

    def analyze_all_articles(self, redo: bool = False) -> None:
        """
        Analyze all articles in the corpus to extract claims.
        """
        for text in tqdm(self.articles, total=len(self.articles), desc='Analyzing Texts'):
            if isinstance(text, Article):
                if not text.fetched:
                    raise Exception('Article has not been fetched yet')
            text.analyze_text(redo=redo)

    def evaluate_all_claims(self, redo: bool = False) -> None:
        """
        Evaluate all claims in the corpus.
        """
        for text in tqdm(self.articles, total=len(self.articles), desc='Evaluating Claims'):
            text.evaluate_all(redo=redo)

    def to_pickle(self, path: str) -> None:
        """
        Serialize the corpus to a file using dill.
        """
        with open(path, 'wb') as f:
            dill.dump(self, f)

    @classmethod
    def from_pickle(cls, filepath: str) -> 'Corpus':
        """
        Load a corpus from a pickle file.
        """
        with open(filepath, 'rb') as f:
            return dill.load(f)

    @classmethod
    def from_urls(cls, urls: List[str]) -> 'Corpus':
        """
        Create a corpus from a list of URLs.
        """
        corpus = cls()
        for url in tqdm(urls, total=len(urls), desc='Creating corpus from URLs'):
            article = Article(url)
            corpus.articles.append(article)
        return corpus

    @classmethod
    def from_texts(cls, texts: List[str]) -> 'Corpus':
        """
        Create a corpus from a list of text strings.
        """
        corpus = cls()
        for text in tqdm(texts, total=len(texts), desc='Creating corpus from texts'):
            text_article = Text(text)
            corpus.articles.append(text_article)
        return corpus

if __name__ == '__main__':
    with open('../urls.txt', 'r') as f:
        urls = f.read().split('\n')
    urls =urls[0:5]
    corpus = corpus.from_urls(urls)
    corpus.process_all_articles()
    corpus.to_pickle('../corpus.pkl')
