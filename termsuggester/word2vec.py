from gensim.models import Word2Vec
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class Word2VecSuggester():
    def __init__(self, modelfile):
        try:
            self.model = Word2Vec.load(modelfile)
            logger.info('Load Word2Vec model "{}"'.format(modelfile))
        except IOError:
            logger.warn('Unable to load Word2Vec model "{}"'.format(modelfile))
            logger.warn('Was the train_word2vec script run?')
            self.model = None

    def suggest_terms(self, query_word):
        # TODO: make the number of terms returned a parameter of the function
        if self.model is not None:
            results = self.model.most_similar(positive=[query_word],
                                              negative=[], topn=10)
            suggestions = {}
            for word, weight in results:
                suggestions[word] = weight
            return suggestions
        else:
            return {}
