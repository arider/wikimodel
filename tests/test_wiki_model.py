import unittest
from unittest import TestCase
from ..wiki_model import WikiModel
import numpy


class WikiModelTest(TestCase):
    def test_loads_training_data(self):
        wikimodel = WikiModel()
        self.assertIsNotNone(wikimodel.classifier)

    def test_classify_url(self):
        wikimodel = WikiModel()
        domain = "https://en.wikipedia.org"
        url = "/wiki/Q-learning"
        probs = wikimodel.classify_url(domain, url)
        self.assertEqual('/wiki/Category:Machine_learning_algorithms',
                         wikimodel.reverse_label_map[numpy.argmax(probs)])


if __name__ == '__main__':
    unittest.main()
