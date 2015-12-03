import unittest
from rocchio import RocchioSuggester


class TestRocchio(unittest.TestCase):
    def test_rocchio(self):
        suggester = RocchioSuggester(numResults = 30, numTop = 20, numBottom = 20, weightInitial = 1., weightTop = 1., weightBottom = 1.)
        termsDict = suggester.suggest_terms('baseball')
        print termsDict
        print suggester.__class__.__name__
        self.assertTrue(isinstance(termsDict, dict))
        self.assertIn('yahoo', termsDict.keys())

if __name__ == '__main__':
    unittest.main()
