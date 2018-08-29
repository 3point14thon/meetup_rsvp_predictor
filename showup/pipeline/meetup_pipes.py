#import dill
import numpy as np
import pandas as pd
import operator
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, LabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from glm.glm import GLM
from glm.families import Poisson

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

class EncodeFeature(BaseEstimator, TransformerMixin):
    def __init__(self, dummy_names):
        self.dummy_names = dummy_names

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        dummy_arr = np.array(self.dummy_names).reshape(1, -1)
        dummy_mat = np.repeat(dummy_arr, len(X), axis=0)
        return np.array(X).reshape(-1, 1) == dummy_mat

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

class intercept(BaseEstimator, TransformerMixin):

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        return np.ones(len(X)).reshape(-1, 1)

class RFRWrapper(RandomForestRegressor):
    def transform(self, X):
        return self

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self

class PoissonRegression(GLM):

    def __init__(self):
        super(PoissonRegression, self).__init__(Poisson())

    def transform(self, X):
        return self

    def fit_transform(self, X, y):
        self.fit(X, y, alpha=0.5)
        return self

    def get_params(self):
        return (self.family, self.alpha)
