from gensim.models import Word2Vec


class Word2VecSuggester():
    def __init__(self, modelfile):
        self.model = Word2Vec.load(modelfile)

    def suggest_terms(self, query_word):
        results = self.model.most_similar(positive=[query_word], negative=[])
        suggestions = {}
        for word, weight in results:
            suggestions[word] = weight
        return suggestions
