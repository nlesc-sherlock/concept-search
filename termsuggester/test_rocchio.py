import unittest
from rocchio import RocchioSuggester


class TestRocchio(unittest.TestCase):
    def test_rocchio(self):
        suggest = RocchioSuggester().suggest_terms
        termsDict = suggest('baseball')
        print termsDict
        self.assertTrue(isinstance(termsDict, dict))
        self.assertIn('yahoo', termsDict.keys())

if __name__ == '__main__':
    unittest.main()
