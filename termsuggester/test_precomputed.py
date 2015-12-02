from unittest import TestCase

from precomputed import PrecomputedClusterSuggester, PrecomputedSuggester


class TestPrecomputed(TestCase):
    def test_mi(self):
        suggest = PrecomputedSuggester().suggest_terms
        print_sugg = suggest('print.jpg')
        self.assertIn('printing', print_sugg)
        for k, v in print_sugg.items():
            self.assertTrue(isinstance(k, basestring))
            self.assertTrue(isinstance(v, float))
            self.assertGreater(v, 0)

    def test_cluster(self):
        suggest = PrecomputedClusterSuggester().suggest_terms
        self.assertTrue(isinstance(suggest('baseball'), dict))
        terms = [term for term in suggest('baseball')]
        self.assertIn('ticket', terms)

        terms = [term for term in suggest('import')]
        self.assertIn('export', terms)
        self.assertIn('import', terms)
