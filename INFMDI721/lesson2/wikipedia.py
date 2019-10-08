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
#    paragraphs = soup.find_all("p")
#    paragraphs = soup.select("p a")
    paragraphs = soup.find(id="mw-content-text").select('p a')
    for p in paragraphs:
        x = p.find("a")
        if x:
            link = x.get('href')
            break
            
    if link:
        # build full url
        link = urllib.parse.urljoin('https://en.wikipedia.org/', link)

    return link


def search_urls(url_start, url_stop, max_iter=25):
    """
    Builds the chain of urls.
    """
    urls = []

    flag_remove_first = False
    if 'Special:Random' in url_start:
        flag_remove_first = True

    urls.append(url_start)

    while True:
        # find next link
        link = find_link(urls[-1])
        if not link:
            urls = None
            break

        urls.append(link)
        
        if urls[-1] == url_stop:
            if flag_remove_first:
                urls.pop(0) 
            print("distance between {} and {} is {}".format(urls[0], urls[-1], len(urls)))
            break
        elif len(urls) > max_iter:
            if flag_remove_first:
                urls.pop(0) 
            print("STOP!!! The search {} and {} is too long ({} iter.)!".format(urls[0],
                                                                                url_stop,
                                                                                max_iter))
            break
        elif link in urls[:-1]:
            print("STOP!! We are looping. We pass twice in {}".format(link))
            break
        else:
            continue
                 
    return urls


if __name__ == '__main__':

    url_start = "https://fr.wikipedia.org/wiki/Boulangerie"
    url_stop = "https://fr.wikipedia.org/wiki/Philosophie"
    urls = search_urls(url_start, url_stop)
    
    url_start = "https://en.wikipedia.org/wiki/Mathematics"
    url_stop = "https://en.wikipedia.org/wiki/Philosophy"
    urls = search_urls(url_start, url_stop)

    url_start = "https://en.wikipedia.org/wiki/Molecular_biophysics"
    urls = search_urls(url_start, url_stop)
    #print(urls)

    # Test on random URL
    print("Test on random URLs (/wiki/Special:Random)")
    print("******************************************")
    
    url_start = "https://en.wikipedia.org/wiki/Special:Random"
        
    for i in range(3):
        urls = search_urls(url_start, url_stop)
        
    print("That's All, Folks!")
