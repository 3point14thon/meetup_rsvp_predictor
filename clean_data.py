import pandas as pd
import numpy as np
import datetime as dt
from ast import literal_eval

def drop_unnecessary(df):
    df = df.drop(['status',
                  'updated',
                  'time',
                  'created',
                  'local_date',
                  'local_time'
                  'id'], axis=1)
    return df

def one_hotify(series, dummy_names):
    dummy_names = np.array(dummy_names).reshape(1, -1)
    dummy_mat = np.repeat(dummy_names, len(series), axis=0)
    return np.array(series).reshape(27, 1) == dummy_mat

def convert_types(df):
    df['local_date'] = pd.to_datetime(df['local_date'])
    basic_set['visibility'] = basic_set['visibility'].map({'public': 0,
                                                           'public_limited': 1})
    return df

def create_columns(df):
    df['month'] = df['local_date'].dt.month
    basic_set['has_waitlist'] = np.where(basic_set['waitlist_count'] > 0, 1, 0)
    return df

def reform_columns(df, col_name):
    df[col_name] = meetup_data[col_name].map(lambda x: literal_eval(x))
    return df

def drop_null_labels(df):
    return df[~df['yes_rsvp_count'].isnull()]

def fill_nulls(df):
    #nulls are either blank descriptions or descriptions I don't have access to
    df['plain_text_no_images_description'] = \
                               df['plain_text_no_images_description'].fillna('')
    df['description'] = df['description'].fillna('')
    return df
