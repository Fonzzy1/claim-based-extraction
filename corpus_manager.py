#! python3

"""
pip install -r back_end/requirements.txt
"""
import sys
import os
sys.path.append(f'{os.getcwd()}/back_end')
from models import Corpus

if __name__ == '__main__':
    with open('urls.txt', 'r') as f:
        urls = f.read().split('\n')
    corpus = Corpus.from_urls(urls)
    corpus.process_all_articles()
    corpus.to_pickle('corpus.pkl')
