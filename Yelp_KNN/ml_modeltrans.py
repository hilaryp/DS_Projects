# modified transformer classes for pipeline

import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin


class LatLongTransformer(BaseEstimator, TransformerMixin):
    """Pull out required columns (passed in a list) from input data."""
    def __init__(self,cols):
        self.cols = cols

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None): 
        X_trans = pd.DataFrame(X, columns=self.cols)
        return X_trans.values


class CategoryDictTransformer(BaseEstimator, TransformerMixin):
    """Pull out category column and return list of feature dicts."""
    def __init__(self):
        pass
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        features = []
        for i in X:
            keys = i['categories']
            row = {k: 1 for k in keys}
            features.append(row)
        return features


class AttributeDictTransformer(BaseEstimator, TransformerMixin):
    """Flatten nested dicts for use in DictVectorizer."""
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def flatten(self, X, y=None, parent_key='', sep='_'):
        flattened = []
        if not X:
            return {}
        for k,v in X.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                flattened.extend(self.flatten(X=v, parent_key=new_key, sep=sep).items())
            else:
                if isinstance(v, str):
                    full_key = new_key + sep + v
                    flattened.append((full_key, 1))
                else:
                    new_v = 1 if v else 0
                    flattened.append((new_key, new_v))
        return dict(flattened)

    def transform(self, X, y=None):
        toflatten = [i['attributes'] for i in X]
        features = [self.flatten(i) for i in toflatten]
        return features


class ModelTransformer(BaseEstimator, TransformerMixin):
    """
    Wrap model in a transformer. 
    
    Only the last step of a pipeline can be a model. Return a data frame
    of model predictions, which can act as input for a feature union.
    """
    def __init__(self, model):
        self.model = model

    def fit(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)
        return self

    def transform(self, X, **transform_params):
        return pd.DataFrame(self.model.predict(X))
