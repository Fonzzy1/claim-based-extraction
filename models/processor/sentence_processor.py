from models.processor.base_processor import BaseProcessor
from nltk import sent_tokenize

class SentenceProcessor(BaseProcessor):
    def __init__(self, pre_context_size, post_context_size):
        super().__init__(pre_context_size, post_context_size, sent_tokenize)
