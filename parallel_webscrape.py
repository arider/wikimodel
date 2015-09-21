from wiki_scraper import crawl_page
from multiprocessing import Pool

PATH = 'wikimodel/'


def call_scraper(args):
    domain = args[0]
    link = args[1]

    return crawl_page(domain, link, href_match='/wiki/', depth=1)


def scrape(domains, links):
    """
    Scrape the given list of links and pickle the output to a file containing a
    dict of <category, dict of link, document> pairs and a dict of {link,
    set(links)}.

    args:
        domains - list of base urls
        links - list of page paths
    """
    pool = Pool(10)
    results = pool.map(call_scraper, zip(domains, links))
    categories = {}
    link_edges = {}
    for index, result in enumerate(results):
        documents, edges = result
        link_edges = dict(link_edges.items() + edges.items())
        categories[links[index]] = documents

    # save the data so that we don't have
    # to put a bunch of load on wikipedia's servers if we run again.
    import pickle
    pickle.dump(categories, open(PATH + "categories.pickle", "wb"))
    pickle.dump(link_edges, open(PATH + "link_edges.pickle", "wb"))


def scrape_wikipedia():
    links = ['/wiki/Category:Rare_diseases',
             '/wiki/Category:Infectious_diseases',
             '/wiki/Category:Cancer',
             '/wiki/Category:Congenital_disorders',
             '/wiki/Category:Organs',
             '/wiki/Category:Machine_learning_algorithms',
             '/wiki/Category:Medical_devices']
    domains = ['http://en.wikipedia.org'] * len(links)
    scrape(domains, links)


if __name__ == "__main__":
    scrape_wikipedia()
