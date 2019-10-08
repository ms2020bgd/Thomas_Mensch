"""
This code computes the "distance" between 2 urls: url_start and url_stop
"""

import requests
from bs4 import BeautifulSoup
import urllib


def find_link(url):
    """
    Returns the first wikipedia link found in the current page
    """
    link = None

    content = requests.get(url)
    soup = BeautifulSoup(content.text, features="html.parser")
    
    #  Select text paragraphs
    paragraphs = soup.select("p")
    for p in paragraphs:
        x = p.find("a")
        if x:
            link = x.get('href')
            break
            
    if link:
        # build full url
        link = urllib.parse.urljoin('https://en.wikipedia.org/', link)

    return link


def do_next(url_history, url_stop, max_iter=25):
    """
    Checks is the search needs to continue. Returns an enum.
    """
    status = False
    
    if url_history[-1] == url_stop:
        # print("Got it!")
        status =  False
    elif len(url_history) > max_iter:
        # print("The search is too long, STOP!")
        status = False
    elif url_history[-1] in url_history[:-1]:
        # print("We are looping, STOP!")
        status = False
    else:
#        print("We continue to investigate!")
        status =  True

    return status

def search_urls(url_start, url_stop):
    """
    Builds the chain of urls.
    """
    urls = []

    urls.append(url_start)
    # print("start = {}".format(urls[0]))

    while do_next(urls, url_stop):
        link = find_link(urls[-1])
        if not link:
            urls = None
            break

        urls.append(link)
    
    return urls


if __name__ == '__main__':

    url_start = "https://en.wikipedia.org/wiki/Mathematics"
    url_stop = "https://en.wikipedia.org/wiki/Philosophy"

    urls = search_urls(url_start, url_stop)
    print("distance between {} and {} is {}".format(urls[0], urls[-1], len(urls)))
    print(urls)

    url_start = "https://en.wikipedia.org/wiki/Molecular_biophysics"
#    url_start = "https://fr.wikipedia.org/wiki/Paris"

    urls = search_urls(url_start, url_stop)
    print("distance between {} and {} is {}".format(urls[0], urls[-1], len(urls)))

    print(urls)

    # Test on random URL
    print("Test on random URL (/wiki/Special:Random)")
    print("*****************************************")
    
    url_start = "https://en.wikipedia.org/wiki/Special:Random"
        
    for i in range(3):
        urls = search_urls(url_start, url_stop)
        # print(urls)
        if urls:
            print("distance between {} and {} is {}".format(urls[1], urls[-1], len(urls) - 1))
        
    print("That's All, Folks!")
