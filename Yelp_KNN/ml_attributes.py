import gzip
import simplejson as json

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
from sklearn import cross_validation

from ml_classes import FlattenDictTransformer

def getAttributeModel(X,y):
    """Extract 'attributes' data as a list of feature dicts 
    and feed into DictVectorizer"""
    toflatten = [i['attributes'] for i in X]
    # create a list of feature dictionaries for each json entry
    t = FlattenDictTransformer()
    features = [t.fit_transform(i) for i in toflatten]
    # turn that into a matrix we can regress on
    v = DictVectorizer()
    X_trans = v.fit_transform(features)
    # regression
    regr = LinearRegression()
    #cv = cross_validation.ShuffleSplit(len(y), n_iter=20, test_size=0.2, random_state=42)
    #error = cross_validation.cross_val_score(regr, X_trans, y, cv=cv, 
    #                                         scoring='mean_squared_error').mean()    
    #print error
    model = regr.fit(X_trans, y)
    return model, v

def main():
    with gzip.open('./data.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()]
    y = [i['stars'] for i in f]
    model, vectorizer = getAttributeModel(f,y)
    
    # test model on a sample record
    #record = {'attributes': {'Take-out': True, 'Has TV': False, 'Outdoor Seating': False,
    #          'Attire': 'casual'}} 
    #t = FlattenDictTransformer()
    #test = t.fit_transform(record['attributes'])
    #X_test_trans = vectorizer.transform(test)
    #print model.predict(X_test_trans)
    joblib.dump(model, 'AttributeModel.pkl')
    joblib.dump(vectorizer, 'AttributeVectorizer.pkl')

    #modelpickle = joblib.load('CategoryModel.pkl')
    #print modelpickle.predict(X_test_trans)

if __name__ == '__main__':
    main()
