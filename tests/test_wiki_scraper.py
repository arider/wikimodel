import unittest
from unittest import TestCase
from ..wiki_scraper import (
    parse_html_simple,
    remove_punctuation,
    crawl_page)


class CrawlPageTest(TestCase):
    """
    commented out so we don't cause too much load on people's networks
    """
    def test(self):
        pass

#    def test_wikipedia(self):
#        domain = "https://en.wikipedia.org"
#        url = "/wiki/Rare_disease"
#
#        documents, edges = crawl_page(domain, url, href_match='/wiki/', depth=1)
#        self.assertGreater(len(documents.keys()), 10)


#    def test_simple_page(self):
#        domain = "http://www.york.ac.uk/teaching/cws/wws/"
#        url = "webpage1.html"
#
#        documents, edges = crawl_page(domain, url, href_match='', depth=2)
#
#        self.assertEqual(3, len(documents.keys()))
#        self.assertItemsEqual(['webpage2.html', 'webpage1.html'], edges.keys())


class ParseHtmlSimpleTest(TestCase):
    def test(self):
        html = """
            <p>A <b>logistic function</b> or <b>logistic curve</b> is a
            common "S" shape (<a href="/wiki/Sigmoid_function" title="Sigmoid
            function">sigmoid curve</a>), with equation:</p>
            <dl>
        """
        expected = ['a',
                    'logistic',
                    'function',
                    'or',
                    'logistic',
                    'curve',
                    'is',
                    'a',
                    'common',
                    's',
                    'shape',
                    'sigmoid',
                    'curve',
                    'with',
                    'equation']
        result = parse_html_simple(html)

        self.assertItemsEqual(expected, result)

    def test_removes_script(self):
        html = """
            <script>window.RLQ = window.RLQ || []; window.RLQ.push( function () {}</script>
            """
        self.assertEqual([], parse_html_simple(html))


class RemovePunctuationTest(TestCase):
    def test(self):
        test_string = '[.?;,\'"()\\-it{}|! worked@#$%^&*+/'
        result = remove_punctuation(test_string)
        self.assertEqual(result, "it worked")

    def test_leaves_tags(self):
        test_string = '<a href title="stuff">some text</a></br>'
        result = remove_punctuation(test_string)
        self.assertEqual(result, '<a href titlestuff>some text<a><br>')

        
class GetPageWordsTest(TestCase):
    def test(self):
        url = 'https://en.wikipedia.org/wiki/Logistic_function'
        self.assertIsNotNone(get_page_words(url, parse_html_simple))


if __name__ == '__main__':
    unittest.main()
