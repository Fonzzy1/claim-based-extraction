from typing import List
from tqdm import tqdm
import dill
from models.text  import Text
from models.sources import Source

class Corpus:
    """
    A class to manage and process a collection of articles.
    """
    def __init__(self) -> None:
        self.texts: List[Text] = []
    
    def process_all_articles(self, redo: bool = False) -> None:
        """
        Fetch, analyze, and evaluate all articles in the corpus.
        """
        self.fetch_all_objects(redo)
        self.analyze_all_articles(redo)
        self.evaluate_all_claims(redo)

    def fetch_all_objects(self, redo: bool = False) -> None:
        """
        Fetch all texts in the corpus if not already fetched.
        """
        for text in tqdm(self.texts, total=len(self.texts), desc='Fetching Texts'):
                text.fetch(redo)

    def analyze_all_articles(self, redo: bool = False) -> None:
        """
        Analyze all texts in the corpus to extract claims.
        """
        for text in tqdm(self.texts, total=len(self.texts), desc='Analyzing Texts'):
            if not text.fetched:
                raise Exception('Text has not been fetched yet')
            text.analyze_text(redo=redo)

    def evaluate_all_claims(self, redo: bool = False) -> None:
        """
        Evaluate all claims in the corpus.
        """
        for text in tqdm(self.texts, total=len(self.texts), desc='Evaluating Claims'):
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
    def from_strings(cls, texts: List[str]) -> 'Corpus':
        """
        Create a corpus from a list of text strings.
        """
        corpus = cls()
        for text in tqdm(texts, total=len(texts), desc='Creating corpus from texts'):
            text_article = Text(text)
            corpus.texts.append(text_article)
        return corpus

    @classmethod
    def from_sources(cls, sources: List[Source])  -> 'Corpus':


if __name__ == '__main__':
    with open('../urls.txt', 'r') as f:
        urls = f.read().split('\n')
    urls =urls[0:5]
    corpus = corpus.from_urls(urls)
    corpus.process_all_articles()
    corpus.to_pickle('../corpus.pkl')
