# Predict Yelp review scores using a Feature Union

import gzip
import simplejson as json

from sklearn.externals import joblib
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.feature_extraction import DictVectorizer 
from sklearn.grid_search import GridSearchCV

from ml_modeltrans import *


# Combine all the models with a feature union
def getFullModel(X, y):
    pipeline = Pipeline([
            ('features', FeatureUnion([
                # Pipeline for the geographic clustering model
                ("latlong", Pipeline([
                    ('transform', LatLongTransformer(['longitude','latitude'])),
                    ('model', ModelTransformer(KNeighborsRegressor(n_neighbors=90)))
                ])), 
                # Pipeline for category features model
                ("categories", Pipeline([
                    ('features', CategoryDictTransformer()),
                    ('vectorizer', DictVectorizer()),
                    ('estimator', ModelTransformer(LinearRegression()))
                ])),
                # Pipeline for attribute features model
                ("attributes", Pipeline([
                    ('features', AttributeDictTransformer()),
                    ('vectorizer', DictVectorizer()),
                    ('model', ModelTransformer(LinearRegression()))
                ]))
            ], 
            transformer_weights= {'latlong': 0.64899274, 'categories': 0.86715093, 
                                  'attributes': 0.35141275})),
            ('estimator', Ridge(alpha=20))
        ])

    model = pipeline.fit(X,y)
    return model


def main():
    with gzip.open('./data.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()]

    y = [i['stars'] for i in f]

    model = getFullModel(f, y)
    record = {'city': 'De Forest', 'review_count': 3, 'name': 'Chang Jiang Chinese Kitchen', 
              'neighborhoods': [], 'type': 'business', 'business_id': 'RgDg-k9S5YD_BaxMckifkg', 
              'full_address': '631 S Main St\nDe Forest, WI 53532', 'hours': {
              'Monday': {'close': '22:00', 'open': '11:00'}, 
              'Tuesday': {'close': '22:00', 'open': '11:00'}, 
              'Friday': {'close': '22:30', 'open': '11:00'}, 
              'Wednesday': {'close': '22:00', 'open': '11:00'}, 
              'Thursday': {'close': '22:00', 'open': '11:00'}, 
              'Sunday': {'close': '21:00', 'open': '16:00'}, 
              'Saturday': {'close': '22:30', 'open': '11:00'}}, 'state': 'WI', 
              'longitude': -89.3437217, 'latitude': 43.2408748, 
              'attributes': {'Take-out': True, 'Has TV': False, 'Outdoor Seating': False, 
              'Attire': 'casual'}, 'open': True, 'categories': ['Chinese', 'Restaurants']}
    print model.predict([record])
    joblib.dump(model, 'FullModel.pkl')


if __name__ == '__main__':
    main()
