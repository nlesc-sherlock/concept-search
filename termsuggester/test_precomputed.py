from unittest import TestCase

from precomputed import PrecomputedSuggester


class TestPrecomputed(TestCase):
    def test_precomputed(self):
        suggest = PrecomputedSuggester().suggest_terms
        terms = [term for term, _ in suggest('baseball')]
        self.assertIn('ticket', terms)

        terms = [term for term, _ in suggest('import')]
        self.assertIn('export', terms)
        self.assertIn('import', terms)
