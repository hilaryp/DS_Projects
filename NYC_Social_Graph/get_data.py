# Get data for graph.py miniproject

import re
import codecs
import urllib2
import pickle
from datetime import datetime
from itertools import combinations

from nltk import word_tokenize, pos_tag
from bs4 import BeautifulSoup

from decorators import retry

URL_BASE = 'http://www.newyorksocialdiary.com/party-pictures?page='
# append from 0-24 pages to this base to get all the pages
REFDATE = datetime(2014, 12, 01, 0, 0)
STOPWORDS = re.compile('(Mayor)|(Dr\.)|(Dr\s)|(Mrs\.)|(Mr\.)|(RN)|(Lieutenant)\
			|(Colonel)|(Jr\.)|(friend)|(Chair\w?\s)|(Commissioner)\
			|(Lady)|(Ambassador)|(CEO NYU Langone)|(dean)|(MD)\
			|(UALC board member)|(UALC board president)\
			|(Honorees?)|(Co-Founder)|(Patrick McMullan)\
			|(Mia Matheson)|(Neil Rasmus)|(Jori Klein)')
STOPTITLES = ['MAYOR', 'DR.', 'MRS.', 'MR.', 'RN', 'JR.', 'MD', 'CEO', 'MCMULLAN',
              'NEW', 'SPECIAL', 'EXECUTIVE', 'DIRECTOR']

def get_pages():
	"""Get list of party pages to scrape"""
	print 'Getting pages...'
	pages = [] 
	# open url, read utf-8 encoding, soupify
	for i in xrange(0, 25):
		url = URL_BASE + str(i)
		req = urllib2.urlopen(url)
		content = unicode(req.read(), 'utf-8')
		soup = BeautifulSoup(content, "lxml")
		# pull out links and their date
		links = soup.select('span.views-field-title a')
		dates = soup.select('span.views-field-created span.field-content')
		llist = [x['href'] for x in links]
		dlist = [datetime.strptime(x.text, '%A, %B %d, %Y') for x in dates]
		#final list of links, keep just links after 12/1/14
		for date, link in zip(dlist, llist):
			if date < REFDATE:
				pages.append('http://www.newyorksocialdiary.com' + link)
	return pages

@retry(urllib2.HTTPError, tries=4, delay=3, backoff=2)
def retry_url(url):
	return urllib2.urlopen(url)

def get_captions(urls):
	"""Scrape each url, return list of captions"""
	print 'Getting captions...'
	caps = []
	pages = []
	for page in urls:
		req = retry_url(page)
		content = unicode(req.read(), 'utf-8')
		soup = BeautifulSoup(content, "lxml")
		newcaptions = soup.select('div.photocaption') 
		oldcaptions = soup.select('font[size=1]')
		allcaptions = newcaptions + oldcaptions
		captions = [x.text for x in allcaptions]
		for x in captions:
			if len(x) < 250:	
				caps.append(x)
		if captions:
			pages.append(page)
	return caps, pages

"""
def process_captions(captions):
	""Clean up captions and return list of tuples for edges""
	print 'Cleaning up the captions...'
	names = []
	# build a list (captions)  of lists (names)
	for caption in captions:
		if 'Photographs by' in caption:
			continue
		stripped = re.sub(STOPWORDS,'', caption)
		splits = re.split(',|and\s|\swith', stripped)
		if all(len(x) < 25 for x in splits):
			names.append(splits)
	cleaned = [[name.strip() for name in row if ' ' in name.strip()] 
		    for row in names]
	# create tuples with all possible combinations of names
	# filter out empty strings resulting from 'and' split
	# this also implicitly filters out singleton captions
	connections = [[i for i in combinations(row, 2) if '' not in i] 
			for row in cleaned]
	# flatten list of lists & return for pickling
	result = [item for sublist in connections for item in sublist]
	return result
"""

def process_captions(captions):
    """Clean up captions and return list of tuples for edges"""
    print 'Cleaning up the captions...'
    cooccurrences = []
    for caption in captions:
        names = []
        partial_name = []
        tokens = word_tokenize(caption.strip())
        for (token, tag) in pos_tag(tokens):
            if tag in ("NNP", "NNPS"):
                token = token.upper()
                if token in STOPTITLES:
                    continue
                partial_name.append(token)
            elif len(partial_name) > 1:
                names.append(" ".join(partial_name))
                partial_name = []
            # else we have no names in the `partial_name` buffer
            else:
                partial_name = []
        if len(partial_name) > 1:
            names.append(" ".join(partial_name))
        # else too short
        if len(names) > 1:
            # save all pairs
            cooccurrences.extend(combinations(names, 2))
        #print caption 
        #print partial_name
        #print names
    return cooccurrences

def main():
	# Get list of pages to scrape
#	pages = get_pages()
#	outpage = open('page_links.pkl', 'wb')
#	pickle.dump(pages, outpage)
#	outpage.close()
	# Scrape captions from those pages
#	captions,scraped = get_captions(pages)
#	outcap = open('captions_raw.pkl', 'wb')
#	pickle.dump(captions, outcap)
#	outcap.close()
#	outscrape = open('scraped_pages.pkl', 'wb')
#	pickle.dump(scraped, outscrape)
#	outscrape.close()
	# Clean up the captions
        with open('captions_raw.pkl', 'rb') as infile:
            captions = pickle.load(infile)
	cleaned = process_captions(captions)
	print 'Writing out the data...'
	# write data out to a pickle 
	output = open('connection_tuples.pkl', 'wb')
	pickle.dump(cleaned, output)
	output.close()

if __name__ == '__main__':
	main()
