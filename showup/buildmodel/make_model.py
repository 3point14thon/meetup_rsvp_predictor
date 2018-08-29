import sys
sys.path.append("..")
import pandas as pd
from ..pipeline.meetup_pipeline import random_forest_model, interest
from .clean_data import drop_null_labels
import dill

def create_fit_pickle(X, y, filename):
    with open(filename, 'wb') as f:
        model = random_forest_model.fit(X, y)
        dill.dump(model, f)
        return model

if __name__ == '__main__':
    meetup_df = pd.read_csv('data/data.gzip', compression='gzip')
    X = drop_null_labels(meetup_df)
    y = interest.fit_transform(X)
    create_fit_pickle(X, y, 'showup/website/static/model.pkl')
