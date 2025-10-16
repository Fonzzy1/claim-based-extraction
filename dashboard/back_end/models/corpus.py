#! docker compose run -it --build back-end python
from typing import List
from tqdm import tqdm
import dill
from models.text  import Text
from models.sources import Source, TextSource


class Corpus:
    """
    A class to manage and process a collection of articles.
    """
    def __init__(self) -> None:
        self.texts: List[Text] = []
        self.sources = []
    
    def process_all_texts(self, redo: bool = False) -> None:
        """
        Fetch, analyze, and evaluate all articles in the corpus.
        """
        self.analyze_all_texts(redo)
        self.evaluate_all_claims(redo)

    def analyze_all_texts(self, redo: bool = False) -> None:
        """
        Analyze all texts in the corpus to extract claims.
        """
        for text in tqdm(self.texts, total=len(self.texts), desc='Analyzing Texts'):
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
    def from_sources(cls, sources: List[Source])  -> 'Corpus':
        corpus = cls()
        corpus.sources = sources
        corpus.texts = [obj for source in sources for obj in
                        source.objects.values()]
        return corpus


if __name__ == '__main__':
    import pandas as pd
    from models.sources import ABCTextSource
    from tqdm import tqdm

    df = pd.read_csv('urls.csv')
    df = df[(df['News Source']=='ABC News Australia') & (df['MediaType']=='Text')]
    sources = [[ABCTextSource(x) for x in df.Source][0]]
    _ = [ source.find_objects() for source in tqdm(sources,total=len(sources)) ]
    _ = [ source.fetch_all_objects() for source in sources ]
    corpus = Corpus.from_sources(sources)
    corpus.process_all_texts()
    corpus.to_pickle('corpus.pkl')







