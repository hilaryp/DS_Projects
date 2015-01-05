#!/usr/bin/env python
# 
# Practice making a simple web scraper!
# Scrapes the abstract titles from the LSA 2015 schedule
# Print output intended to pipe to a text file

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re

URL = "http://www.linguisticsociety.org/node/3901/schedule"

def get_titles():
    html = urlopen(URL).read()
    soup = BeautifulSoup(html, "lxml")
    titles = [a.string for a in soup.find_all(href=re.compile("abstract"))]
                                            # TODO: try r"abstract" instead
    return titles

if __name__ == '__main__':
    raw = get_titles()
    for x in raw:
        y = x.encode('utf8')
        print y
