#! python3

"""
pip install -r back_end/requirements.txt
"""
import sys
import os
sys.path.append(f'{os.getcwd()}/back_end')
from models import Corpus
from models.sources import TextSource

if __name__ == '__main__':
    with open('urls.txt', 'r') as f:
        urls = f.read().split('\n')
    urls =urls[0:5]
    source = TextSource.from_urls(urls)
    source.fetch_all_objects()
    corpus = Corpus.from_sources([source])
    corpus.process_all_texts()
    # corpus.to_pickle('../corpus.pkl')
