# Contains custom classes used to solve ml.py

import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin


# city model
class MeansEstimator(BaseEstimator, RegressorMixin):
    """Create a baseline estimator which predicts the mean value of the city."""
    def __init__(self):
        pass

    def fit(self, X, y):
        # Use groupby and mean to get average rating in each city
        groups = X.groupby('city')
        self.means = groups.mean()
        return self

    def predict(self, X):
        try:
            city = X['city']
            prediction = float(self.means.loc[city])
        # In case the city isn't in the training data:
        except KeyError:
            prediction = 3.0
        return prediction


class ColumnSelectTransformer(BaseEstimator, TransformerMixin):
    """Pull out required columns (passed in a list) from input data."""
    def __init__(self, cols):
        self.cols = cols

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_trans = pd.DataFrame(X, columns=self.cols)
        return X_trans


class FeatureDictTransformer(BaseEstimator, TransformerMixin):
    """Pull out required columns (passed in a list) from input data."""
    def __init__(self, col):
        self.col = col

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        keys = X[self.col]
        features = {k: 1 for k in keys}
        return features


class FlattenDictTransformer(BaseEstimator, TransformerMixin):
    """Flatten nested dicts for use in DictVectorizer."""
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, parent_key='', sep='_'):
        if not X:
            return {}
        flattened = []
        for k, v in X.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                flattened.extend(self.transform(X=v, parent_key=new_key, sep=sep).items())
            else:
                if isinstance(v, str):
                    full_key = new_key + sep + v
                    flattened.append((full_key, 1))
                else:
                    new_v = 1 if v else 0
                    flattened.append((new_key, new_v))
        return dict(flattened)
