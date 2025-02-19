from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional
from newspaper import Article as BaseArticle
from newspaper import Config
from tqdm import tqdm
import dill
import json
from constants import SYSTEM_EXTRACTOR, SYSTEM_EVALUATION, all_infrastructure_options
from openai import OpenAI

# OpenAI client initialization
client: OpenAI = OpenAI()

# User agent configuration for newspaper
user_agent: str = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
config: Config = Config()
config.browser_user_agent = user_agent

class Text:
    """
    A class representing text content for analysis.
    """
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.analyzed: bool = False
        self.claims: List[Claim] = []

    def analyze_text(self, redo: bool = False) -> None:
        """
        Analyze the text to extract claims using OpenAI's service.
        """
        if not self.analyzed or redo:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": SYSTEM_EXTRACTOR},
                    {"role": "user", "content": self.text},
                ],
                response_format=ClaimList,
            )

            claimlist: ClaimList = completion.choices[0].message.parsed
            self.claims = claimlist.claims
            self.analyzed = True

class Claim(BaseModel):
    """
    A model representing a claim extracted from text.
    """
    quote: str = Field(..., description="A quote from the article text that makes the claim")
    infrastructure: str = Field(..., description=f"The infrastructure that the claim is made about. One of: {', '.join(all_infrastructure_options)}")
    judgement: str = Field(..., description="An adjective with or without qualifying information")
    evaluated: bool = Field(..., description="A field that is always False")

    @field_validator('infrastructure')
    def validate_infrastructure(cls, value: str) -> str:
        if value not in all_infrastructure_options:
            raise ValueError(f'Infrastructure must be one of {all_infrastructure_options}')
        return value

    @field_validator('evaluated')
    def validate_evaluated(cls, value: bool) -> bool:
        if value != False:
            raise ValueError('Evaluated must be set as false')
        return value

    def evaluate_claim(self, redo: bool = False) -> None:
        """
        Evaluate the claim using OpenAI's service.
        """
        if not self.evaluated or redo:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": SYSTEM_EVALUATION},
                    {"role": "user", "content": json.dumps(self.__dict__)},
                ],
                response_format=Evaluation,
            )
            evaluation: Evaluation = completion.choices[0].message.parsed
            self.__dict__.update(evaluation.__dict__)
            self.evaluated = True

class Evaluation(BaseModel):
    """
    A model evaluating claims based on judgments and sentiments.
    """
    dimension: Literal['economic', 'externalities']
    valence: float = Field(..., description="A float between -1 and 1 indicating the sentiment of the judgment.")

    @field_validator('valence')
    def valence_must_be_in_range(cls, v: float) -> float:
        if not -1 <= v <= 1:
            raise ValueError('Valence must be between -1 and 1')
        return v

class ClaimList(BaseModel):
    """
    A model for holding a list of claims.
    """
    claims: List[Claim]

class Article(Text):
    """
    A class to represent an article and its metadata.
    """
    def __init__(self, url: str) -> None:
        super().__init__(text='')
        self.url: str = url
        self.title: Optional[str] = None
        self.authors: List[str] = []
        self.publish_date: Optional[str] = None
        self.fetched: bool = False

    def fetch_article(self, redo: bool = True) -> None:
        """
        Fetch and parse the article content from the given URL.
        """
        if not self.fetched or redo:
            article = BaseArticle(self.url, config=config)
            article.download()
            article.parse()

            self.title = article.title
            self.text = article.text
            self.authors = article.authors
            self.publish_date = article.publish_date
            self.fetched = True

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
            if not text.analyzed:
                raise Exception('Text has not been analyzed yet')
            for claim in text.claims:
                claim.evaluate_claim(redo=redo)

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
    corpus = Corpus.from_urls(urls)
    corpus.process_all_articles()
    corpus.to_pickle('../corpus.pkl')
