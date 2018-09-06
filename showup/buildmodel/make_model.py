import sys
sys.path.append("..")
import pandas as pd
from sklearn.model_selection import train_test_split
from ..pipeline.meetup_pipeline import random_forest_model, interest
from .clean_data import drop_null_labels
import dill

def create_fit_pickle(X, y, filename):
    '''
    Creates a dill file fitted to the input data using the random_forest_model
    from meetup_pipeline.
    Input:
        X: Data to be used in fitting the model as array.
        y: Labels to be used in fitting the model as array.
        filename: Name of file as string.
    Output:
        model: The fitted random_forest_model.
    '''
    with open(filename, 'wb') as f:
        model = random_forest_model.fit(X, y)
        dill.dump(model, f)
        return model

def get_data():
    '''
    Retrieves a consistant train test split of data from data.gzip.
    Input:
        None
    Output:
        train_test_split of data: (X_train, X_test, y_train, y_test)
    '''
    f = 'data/data.gzip'
    meetup_df = pd.read_csv(f, compression='gzip')
    X = drop_null_labels(meetup_df)
    y = interest.fit_transform(X)
    return train_test_split(X, y, random_state=1969)

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = get_data()
    create_fit_pickle(X_train, y_train, 'showup/website/static/model.pkl')
