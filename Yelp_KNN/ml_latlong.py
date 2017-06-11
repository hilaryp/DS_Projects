import gzip
import simplejson as json
import pandas as pd
import matplotlib.pylab as plt
from sklearn.externals import joblib
from sklearn import neighbors, cross_validation, grid_search 

from ml_classes import ColumnSelectTransformer
def getLatLongModel(X):
    cols = ['longitude', 'latitude', 'stars']
    t = ColumnSelectTransformer(cols)
    X_trans = t.fit_transform(X)
    y = X_trans.pop('stars')
    # cv = cross_validation.ShuffleSplit(len(y), n_iter=20, test_size=0.2, random_state=42)
    # param_grid = {"n_neighbors": range(5, 100, 5)}
    # neighbors_cv = grid_search.GridSearchCV(neighbors.KNeighborsRegressor(),
    #                                        param_grid=param_grid, cv=cv, 
    #                                        scoring='mean_squared_error')
    neigh= neighbors.KNeighborsRegressor(n_neighbors=90)
    model = neigh.fit(X_trans,y)
    return model

def main():
    with gzip.open('./data.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()]

    model = getLatLongModel(f)
    record = {'latitude': 33.499313, 'longitude': -111.983758}
    print model.predict((record['latitude'],record['longitude']))
    joblib.dump(model, 'LatLongModel.pkl')

if __name__ == '__main__':
    main()
