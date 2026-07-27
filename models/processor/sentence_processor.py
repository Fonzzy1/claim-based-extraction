from base_processor import BaseProcessor
from nltk import sent_tokenize

class SentenceProcessor(BaseProcessor):
    def __init__(self, pre_content_size, post_content_size):
        super().__init__(pre_content_size, post_content_size, sent_tokenize)
