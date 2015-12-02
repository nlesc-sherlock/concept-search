from unittest import TestCase

from precomputed import PrecomputedClusterSuggester


class TestPrecomputed(TestCase):
    def test_precomputed(self):
        suggest = PrecomputedClusterSuggester().suggest_terms
        self.assertTrue(isinstance(suggest('baseball'), dict))
        terms = [term for term in suggest('baseball')]
        self.assertIn('ticket', terms)

        terms = [term for term in suggest('import')]
        self.assertIn('export', terms)
        self.assertIn('import', terms)
