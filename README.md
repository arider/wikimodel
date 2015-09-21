This is a toy project to scrape some wikipedia text and make a simple classifier.

Running setup.sh will install a virtualenv with the packages you need. You can then run parallel_webscrape.py to get the training set of data and use wiki_model.py to classify additional web pages. You'll need to run the scripts from a directory up. Classify a document like this: python wikimodel/classify_document.py -d https://en.wikipedia.org -p /wiki/Q-learning
