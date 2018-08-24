#import dill
import numpy as np
import pandas as pd
import operator
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, LabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor

class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key, as_numpy=False):
        self.key = key
        self.as_numpy = as_numpy

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X:pd.DataFrame, *args, **kwargs):
        for k in ('as_numpy', ):
            if getattr(self, k):
                if isinstance(X.loc[:, self.key], pd.Series):
                    return X.loc[:, self.key].values.reshape(-1,1)
                return X.loc[:, self.key].values
        return X.loc[:, self.key]

class MapFeature(BaseEstimator, TransformerMixin):
    def __init__(self, f):
        self.f = f

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        return self.f(X)

class CustomBinarizer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None,**fit_params):
        return self
    def transform(self, X):
        return LabelBinarizer().fit(X).transform(X)

class FillWith(BaseEstimator, TransformerMixin):

    def __init__(self, fill_with):
        self.fill_with = fill_with

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        return X.fillna(self.fill_with)

class RFRWrapper(RandomForestRegressor):
    def transform(self, X):
        return self

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self
