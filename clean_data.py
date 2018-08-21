import pandas as pd
import numpy as np
import datetime as dt

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
    return df

def create_columns(df):
    df['month'] = df['local_date'].dt.month

    return df
