import gzip
import simplejson as json

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
from sklearn import cross_validation

from ml_classes import FeatureDictTransformer

def getCategoryModel(X,y):
    """Extract 'categories' data as a list of feature dicts 
    and feed into DictVectorizer"""
    fcol = 'categories'
    # create a list of feature dictionaries for each json entry
    t = FeatureDictTransformer(fcol)
    features = [t.fit_transform(i) for i in X]
    # turn that into a matrix we can regress on
    v = DictVectorizer()
    X_trans = v.fit_transform(features)
    # regression
    regr = LinearRegression()
    #cv = cross_validation.ShuffleSplit(len(y), n_iter=20, test_size=0.2, random_state=42)
    #error = cross_validation.cross_val_score(regr, X_trans, y, cv=cv, 
    ###                                         scoring='mean_squared_error').mean()    
    model = regr.fit(X_trans, y)
    return model, v

def main():
    with gzip.open('./data.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()]
    y = [i['stars'] for i in f]
    model, vectorizer = getCategoryModel(f,y)
    
    # test model on a sample record
    record = {'categories': ['Food', 'Ice Cream & Frozen Yogurt', 'Fast Food', 'Restaurants']}
    t = FeatureDictTransformer('categories')
    test = t.fit_transform(record)
    X_test_trans = vectorizer.transform(test)
    print model.predict(X_test_trans)
    joblib.dump(model, 'CategoryModel.pkl')
    joblib.dump(vectorizer, 'CategoryVectorizer.pkl')

    modelpickle = joblib.load('CategoryModel.pkl')
    print modelpickle.predict(X_test_trans)

if __name__ == '__main__':
    main()
