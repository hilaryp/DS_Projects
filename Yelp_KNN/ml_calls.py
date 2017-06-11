"""
This file:
1. Imports the Yelp data
2. Fits the models
3. Pickles the models for use in ml.py
"""

import gzip
import simplejson as json
import pandas as pd
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline

from ml_classes import MeansEstimator, ColumnSelectTransformer

def getCityModel(X, y):
    cols = ['city', 'stars']
    citymodel = Pipeline([
        ('trans', ColumnSelectTransformer(cols=cols)),
        ('est', MeansEstimator())
    ])
    means = citymodel.fit(X,y)
    #t = ColumnSelectTransformer(cols)
    #X_trans = t.fit_transform(X)
    #m = MeansEstimator()
    #means = citymodel.fit(X, y)
    print citymodel.predict({'city' : 'Phoenix'})
    return means
    
def main():
    with gzip.open('./data.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()]

    city = [i['city'] for i in f]
    stars = [i['stars'] for i in f]
   
    cm = getCityModel(f, stars)
    # joblib.dump(cm, 'citymeans_trans.pkl')
    #print cm.predict(f[-1])

if __name__ == '__main__':
    main()
