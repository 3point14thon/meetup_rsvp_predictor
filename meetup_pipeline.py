import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer, Binarizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from meetup_pipes import FeatureSelector, MapFeature, CustomBinarizer, FillWith

name_tfidf = Pipeline([
    ('select_name', FeatureSelector('name')),
    ('fillnans', FillWith('')),
    ('tfidf', TfidfVectorizer())
    ])

desc_tfidf = Pipeline([
    ('select_name', FeatureSelector('plain_text_no_images_description')),
    ('fillnans', FillWith('')),
    ('replace_new_line', MapFeature(lambda x: x.replace('\n', ' '))),
    ('tfidf', TfidfVectorizer())
    ])

visibility = Pipeline([
    ('select_visibility', FeatureSelector('visibility', True)),
    ('binarize', CustomBinarizer())
    ])

has_waitlist = Pipeline([
    ('select_waitlist_count', FeatureSelector('waitlist_count', True)),
    ('binarize', Binarizer(0)),
    ('name', MapFeature(lambda x: pd.Series(x.reshape(-1), name='has_waitlist')))
    ])

rsvp_waitlist_union = FeatureUnion([
    ('yes_rsvp_count', FeatureSelector('yes_rsvp_count', True)),
    ('waitlist_count', FeatureSelector('waitlist_count', True))
    ])

interest = Pipeline([
    ('rsvp_waitlist', rsvp_waitlist_union),
    ('sum_cols', MapFeature(lambda x: np.sum(x, axis=1)))
    ])


#meetup_feature_union = FeatureUnion([
#    ('visibility', visibility),
#    ('name_tfidf', name_tfidf),
#    ('desc_tfidf', desc_tfidf)
#    ])
