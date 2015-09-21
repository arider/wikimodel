import numpy
from wiki_scraper import (
    parse_html_simple,
    crawl_page)
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import os.path
from parallel_webscrape import scrape_wikipedia

PATH = 'wikimodel/'


class WikiModel():

    def __init__(self):
        self.vocabulary = set()
        self.stop_words = set()
        self.english_words = set()
        self.label_map = {}
        self.reverse_label_map = {}
        self.count_data = []
        self.labels = []
        self.vectorizer = None
        self.classifier = None
        self.load_training_data()

    def load_training_data(self):
        # make some dictionaries to preprocess the words
        english_words = set()
        with open(PATH + "american-english.txt") as english_dictionary:
            english_words = set(
                word.strip().lower() for word in english_dictionary)

        stop_words = set()
        with open(PATH + "english_stopwords.txt") as stopwords:
            stop_words = set(word.strip().lower() for word in stopwords)

        self.english_words = english_words
        self.stop_words = stop_words

        if not os.path.isfile(PATH + 'categories.pickle'):
            scrape_wikipedia()

        categories = pickle.load(open(PATH + 'categories.pickle', 'rb'))

        # parse the html, turning it into a list of words
        # and removing stop words and non-dictionary words
        # we'll also collect all of the words so that we can make a map of
        # words to numbers

        all_words = set()
        # the category level
        for k, v in categories.iteritems():
            # the document level
            for inner_k, inner_document in v.iteritems():
                # parse the html to get lists of words per document
                words = parse_html_simple(inner_document)
                parsed = []
                for word in words:
                    if word in english_words and word not in stop_words:
                        all_words.add(word)
                        parsed.append(word)
                categories[k][inner_k] = parsed

        # aggregate all of the documents into one big data set while
        # transforming them into counts
        self.vocabulary = set(all_words)
        self.vectorizer = CountVectorizer(vocabulary=self.vocabulary)

        count_data = []
        string_data = []
        labels = []
        # the category level
        for k, v in categories.iteritems():
            # the document level
            for inner_k, inner_document in v.iteritems():
                # oops, we actually need this in string format
                string_data.append(' '.join(inner_document))
                labels.append(k)

        # transform the string data into count data
        count_data = self.vectorizer.transform(string_data).todense()

        # transform count_data and babels into numpy arrays for easy indexing
        count_data = numpy.array(count_data)
        labels = numpy.array(labels).squeeze()

        # make a map from the string label to a number and vice versa
        self.label_map = {}
        self.reverse_label_map = {}
        i = 0
        for label in sorted(set(labels)):
            self.reverse_label_map[i] = label
            self.label_map[label] = i
            i += 1

        # fit the model
        self.classifier = MultinomialNB()
        self.classifier.fit(count_data, labels)

    def classify_url(self, domain, page, depth=0):
        """
        Classify the documents after crawling them.

        args:
            domain - the domain part of the url
            page - the other part of the url
            depth - how deep to crawl

        returns:
            a list of predicted probabilities for each instance belonging to
            each class
        """
        # get the documents
        documents, _ = crawl_page(domain, page, depth=0)

        # parse the documents
        string_data = []
        for page, doc in documents.iteritems():
            words = parse_html_simple(doc)
            parsed = []
            for word in words:
                if (word in self.english_words
                        and word not in self.stop_words
                        and word in self.vocabulary):
                    parsed.append(word)
            string_data.append(' '.join(parsed))

        count_data = self.vectorizer.transform(string_data)

        # classify the documents
        probs = self.classifier.predict_proba(count_data)
        return probs
