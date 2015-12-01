from __future__ import print_function
import sys
import os
import logging

from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec

logging.basicConfig(level=logging.INFO)

class Word2VecCorpus():
    def __init__(self, basedir):
        self.basedir = basedir

    def __iter__(self):
        for person in os.listdir(self.basedir):
            docs_dir = os.path.join(self.basedir, person, 'all_documents')
            for f in os.listdir(docs_dir):
                text = open(os.path.join(docs_dir, f)).read()
                sentences = sent_tokenize(text)
                for s in sentences:
                    yield [w.lower() for w in word_tokenize(s)]

try:
    basedir, outfile = sys.argv[1:]
except Exception:
    print("usage: %s dir outfile"
          % sys.argv[0], file=sys.stderr)
    sys.exit(1)

model = Word2Vec(Word2VecCorpus(basedir), size=100, window=5, min_count=5,
                 workers=4)
model.save(outfile)
