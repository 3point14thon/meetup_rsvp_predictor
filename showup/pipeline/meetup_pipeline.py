import sys
sys.path.append("..")
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer, Binarizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from nltk import word_tokenize
from .meetup_pipes import (FeatureSelector, MapFeature, CustomBinarizer, FillWith,
                          EncodeFeature, RFRWrapper)

name_tfidf = Pipeline([
    ('select_name', FeatureSelector('name')),
    ('fillnans', FillWith('')),
    ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.95, min_df=.05))
    ])

desc_tfidf = Pipeline([
    ('select_name', FeatureSelector('plain_text_no_images_description')),
    ('fillnans', FillWith('')),
    ('replace_new_line', MapFeature(lambda x: x.replace('\n', ' '))),
    ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.95, min_df=.05))
    ])

log_word_count = Pipeline([
    ('select_desc', FeatureSelector('plain_text_no_images_description')),
    ('fillnans', FillWith('')),
    ('replace_new_line', MapFeature(lambda x: x.replace('\n', ' '))),
    ('word_count', MapFeature(lambda x: x.map(lambda y: len(word_tokenize(y))))),
    ('log_of_count', MapFeature(lambda x: np.array(np.log(x + 1)).reshape(-1, 1)))
    ])

visibility = Pipeline([
    ('select_visibility', FeatureSelector('visibility')),
    ('binarize', CustomBinarizer())
    ])

hour_of_day = Pipeline([
    ('select_local_time', FeatureSelector('local_time')),
    ('convert_to_datetime', MapFeature(lambda t: pd.to_datetime(t))),
    ('select_day', MapFeature(lambda t: t.dt.hour)),
    ('one_hotify', EncodeFeature(range(24)))
    ])

day_of_week = Pipeline([
    ('select_local_date', FeatureSelector('local_date')),
    ('convert_to_datetime', MapFeature(lambda d: pd.to_datetime(d))),
    ('select_day', MapFeature(lambda d: d.dt.dayofweek)),
    ('one_hotify', EncodeFeature(range(7)))
    ])

month_of_year = Pipeline([
    ('select_local_date', FeatureSelector('local_date')),
    ('convert_to_datetime', MapFeature(lambda d: pd.to_datetime(d))),
    ('select_day', MapFeature(lambda d: d.dt.month)),
    ('one_hotify', EncodeFeature(range(1, 13)))
    ])

rsvp_waitlist_union = FeatureUnion([
    ('yes_rsvp_count', FeatureSelector('yes_rsvp_count', True)),
    ('waitlist_count', FeatureSelector('waitlist_count', True))
    ])

interest = Pipeline([
    ('rsvp_waitlist', rsvp_waitlist_union),
    ('log_sum_cols', MapFeature(lambda x: np.log(np.sum(x, axis=1) + 1)))
    ])

meetup_union = FeatureUnion([
    ('visibility', visibility),
    ('name_tfidf', name_tfidf),
    ('desc_tfidf', desc_tfidf),
    ('hour_of_day', hour_of_day),
    ('day_of_week', day_of_week),
    ('month_of_year', month_of_year),
    ('log_word_count', log_word_count)
    ])

meetup_model = Pipeline([
    ('meetup_features', meetup_union),
    ('model', RFRWrapper(random_state=1969))
    ])
