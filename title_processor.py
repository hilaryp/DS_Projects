#!/usr/bin/env python
# 

"""Process a list of talk titles (scraped from LSA schedule using
practice_scraper.py) to get stem frequency & most frequent wordform"""

from nltk import word_tokenize, SnowballStemmer
from collections import defaultdict, Counter
from functools import partial
from operator import itemgetter
import sys
import codecs
import unicodecsv

stemmer = SnowballStemmer("english")
STOPWORDS = ['A', 'ALL', 'AM', 'AN', 'AND', 'ARE', 'AS', 
              'AT', 'BE', 'BEEN', 'BOTH', 'BUT', 'BY', 'CAN', 
              'COULD', 'CUZ', 'DID', 'DO', 'DOES', 'DOWN', 'EACH', 'FOR', 
              'FROM', 'HAD', 'HAS', 'HAVE', 'HE', 'HER', 'HERE', 'HIS', 
              'I', 'IF', 'IN', 'IS', 'IT', 'ITS', 'LIKE', 'MAY', 'ME', 
              'MIGHT', 'MUST', 'MY', 'NO', 'NOR', 'OF', 'ON', 'ONE', 'OR', 
              'OUR', 'OUT', 'ROUND', 'SHALL', 'SHE', 'SHOULD', 'SINCE', 
              'SO', 'SOME', 'SUCH', 'THAN', 'THAT', 'THE', 'THEIR', 'THEM', 
              'THESE', 'THEY', 'THIS', 'THOSE', 'THROUGH', 'TILL', 'TO', 
              'TOO', 'UP', 'US', 'WAS', 'WE', 'WERE', 'WHAT', 'WHEN', 
              'WHO', 'WHOM', 'WHOSE', 'WHY', 'WILL', 'WITH', 'WOULD', 
              'YEAH', 'YOU', 'YOUR', '?', '!', ".", ',', '-', '"', "'", 
              ':', '', '(', ')', '&', '``', '[', ']']

def get_stem_freqs(titles):
    """Return most common word form and frequency for each stem in file""" 
    # Initialize word_by_stem {STEM : {wordform : freq}} 
    dd = partial(defaultdict, int)
    word_by_stem = defaultdict(dd)
    # Initialize {STEM : freq}
    stem_freq = Counter()
    # Tokenize words
    words = get_words(titles)
    # Stem each word and update counts
    for word in words:
        stem = stemmer.stem(word).upper()
        if stem not in STOPWORDS:
            word_by_stem[stem][word] += 1
            stem_freq[stem] += 1

    # Find the most frequent form of each stem, {STEM : wordform}
    stem_word = {stem : max(dct.iteritems(), key=itemgetter(1))[0] 
                 for (stem,dct) in word_by_stem.iteritems()}
    
    # Create dict of {wordform : freq} pairs
    freq = {val : stem_freq[key] for (key,val) in stem_word.iteritems()}
    return freq

def get_words(titles):
    """Tokenize title file & return list of words"""
    words = word_tokenize(titles)
    # Clean up chars tokenizing didn't catch
    words = [w.strip("'-") for w in words]
    return words

def main():
    try:
        in_path = sys.argv[1]
        out_path = sys.argv[2]
    except IndexError:
        print >> sys.stderr, "Usage: title_processor input_path output_path"
        exit(1)
    
    # Open input file
    with codecs.open(in_path, 'r', encoding='utf-8') as f:
        titles = f.read()
    
    # Turn it into word frequencies
    freqs = get_stem_freqs(titles)

    # Write output csv
    with open(out_path, 'w') as csvfile:
        writer = unicodecsv.writer(csvfile, encoding='utf-8')
        writer.writerow(('word', 'count'))
        for key, count in freqs.iteritems():
            writer.writerow((key, count))           

if __name__ == '__main__':
    main()
