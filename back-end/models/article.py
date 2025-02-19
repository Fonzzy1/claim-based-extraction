from typing import List, Optional
from newspaper import Article as BaseArticle
from newspaper import Config
from models import Text

# User agent configuration for newspaper
user_agent: str = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
config: Config = Config()
config.browser_user_agent = user_agent

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
