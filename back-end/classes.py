from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Literal
from newspaper import Article as BaseArticle
from newspaper import Config
from tqdm import tqdm
import dill
import json
from constants import SYSTEM_EXTRACTOR, SYSTEM_EVALUATION, all_infrastructure_options
from openai import OpenAI

# OpenAI client initialization
client = OpenAI()

# User agent configuration for newspaper
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

class Text:
    """
    A class that represents text content for analysis.
    """
    def __init__(self, text: str):
        self.text = text
        self.analysed = False
        self.claims = []

    def analyze(self):
        """
        Analyze the text to extract claims using OpenAI's service.
        """
        if not self.analysed:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": SYSTEM_EXTRACTOR},
                    {"role": "user", "content": self.text},
                ],
                response_format=ClaimList,
            )

            claimlist = completion.choices[0].message.parsed
            self.claims = claimlist.claims
            self.analysed = True

class Claim(BaseModel):
    """
    A model for representing a claim extracted from text.
    """
    quote: str = Field(..., description="A quote from the article text that makes the claim")
    infrastructure: str = Field(..., description=f"The infrastructure that the claim is being made about. One of: {', '.join(all_infrastructure_options)}")
    judgement: str = Field(..., description="An adjective with or without qualifying information")
    evaluated: bool = Field(..., description="A field that is always False")

    @field_validator('infrastructure')
    def validate_infrastructure(cls, value):
        if value not in all_infrastructure_options:
            raise ValueError(f'Infrastructure must be one of {all_infrastructure_options}')
        return value

    @field_validator('evaluated')
    def validate_evaluated(cls, value):
        if value != False:
            raise ValueError(f'Evaluated was not set as false')
        return value

    def evaluate(self):
        """
        Analyze the text to extract claims using OpenAI's service.
        """
        if not self.evaluated:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": SYSTEM_EVALUATION},
                    {"role": "user", "content": json.dumps(self.__dict__)},
                ],
                response_format=Evaluation,
            )
            evaluation = completion.choices[0].message.parsed
            self.__dict__ = {
                **self.__dict__,
                **evaluation.__dict__
            }
            self.evaluated = True



class Evaluation(BaseModel):
    """
    A model for evaluating claims based on judgments and sentiments.
    """
    dimension: Literal['economic', 'externalities']
    valence: float = Field(..., description="A float between -1 and 1 indicating the sentiment of the judgment.")

    @field_validator('valence')
    def valence_must_be_in_range(cls, v):
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
    def __init__(self, url: str):
        super().__init__(text=None)
        self.url = url
        self.title = None
        self.authors = []
        self.publish_date = None
        self.fetched = False

    def fetch(self):
        """
        Fetches and parses the article content from the given URL.
        """
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
    def __init__(self):
        self.articles: List[Text] = []

    def fetch_all(self, redo=False):
        """
        Fetch all articles in the corpus if not already fetched.
        """
        for article in tqdm(self.articles, total=len(self.articles), desc='Fetching Articles'):
            if isinstance(article, Article) and (not article.fetched or redo):
                article.fetch()

    def to_pickle(self, path):
        """
        Serialize the corpus to a file using pickle.
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
    urls = [urls[0]]
    corpus = Corpus.from_urls(urls)
    corpus.fetch_all()
    corpus.to_pickle('corpus.pkl')
    self = corpus.articles[0]
    self.analyze()
    self.claims
    claim = self.claims[0]
    claim.evaluate()
    claim.valence
    
