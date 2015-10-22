from unittest import TestCase

from nmf import NMFSuggester


# Point this to data.
basedir = ''


class NMFTests(TestCase):
    def test_NMF(self):
        nmf = NMFSuggester(basedir=basedir)
        sugg = nmf.suggest_terms('ticket')
        self.assertIn('baseball', sugg)
        self.assertIn('game', sugg)
