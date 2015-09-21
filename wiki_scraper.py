import logging
import requests
from requests.exceptions import ConnectionError
import re
import string
import unicodedata


def remove_punctuation(html):
    """
    With an assist from stack overflow
    """
    return html.translate(string.maketrans("", ""),
                          "[]{}\"';,|.*\?!@#$%^&*()+-=:/\n")


def parse_html_simple(html):
    """
    This function makes some simplifying assumptions, namely that there is
    nothing interesting in script tags, all of the content is >between these<,
    and punctuation isn't interesting. It also doesn't extract anythin in the
    structure of the document. Just words.

    args:
        html - a string of raw html
    returns:
        a list of words
    """
    # some preprocessing
    html = html.lower()
    # exclude text in script tags
    html = re.sub('<script>.*</script>', '', html)
    # remove punctuation
    no_punctuation_html = remove_punctuation(html)

    matches = re.findall(r'>([\w_\s]*)<', no_punctuation_html)
    # separate the words
    words = []
    for match in matches:
        split_words = re.findall(r'\s*([\w_]+)\s*', match)
        words.extend(split_words)

    return words


def crawl_page(domain, url, visited=set(), depth=1, href_match='',
               verbose=True):
    """
    Do a depth first search starting at the given url to the given depth in
    order to get the html of pages and all of the links between pages.

    args:
        url - starting url
        visited - a set of urls to check so that pages are only visited once
        depth - how deep to search
        href_match - a string to look for in href definitions in order to
                     constrain the domain of the search.
        verbose - boolean, print for each call or not
    return:
        a hash of {url: html}
        a hash of {url: set(url, url...)}
    """
    if verbose:
        print domain, url
    documents = {}
    document_edges = {}

    # load the page
    html = ''
    try:
        response = requests.get('{}{}'.format(domain, url))
        if response.status_code == 200:
            html = (unicodedata.normalize('NFKD', response.text)
                    .encode('ascii', 'ignore'))
            html = html.lower()
        else:
            logging.warning("Got status code {} from {}"
                            .format(response.status_code, url))
    except ConnectionError:
            logging.warning("ConnectionError {} {}".format(domain, url))

    # add this document to the hash
    documents[url] = html
    visited.add(url)

    if depth > 0:
        # get the links
        links = re.findall(
            r'href="(' + re.escape(href_match) + '[/:\w\d_\.]+)"', html)

        document_edges[url] = set(links)
        for link in links:
            if link not in visited:
                new_documents, edges = crawl_page(domain, link, visited,
                                                  depth - 1)
                documents = dict(documents.items() + new_documents.items())
                document_edges = dict(document_edges.items() + edges.items())

    return documents, document_edges
