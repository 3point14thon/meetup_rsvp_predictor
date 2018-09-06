import numpy as np
from sklearn.model_selection import KFold

def cv_score(model, X, y, metric, splits=3, random_state=None, shuffle=False):
    '''
    Cross validates the input data with the input labels.
    Input:
        model: The model to be cross validated, must have fit and predict
               methodes.
        X: The data to be used as array.
        y: The labels to be used as array.
        metric: The perfomance metric for evaluation as method.
        splits: Number of splits as int, 3 if not specified.
        random_state: random state as int, None if not specified.
        shuffle: If data should be shuffled or not, as boolean.
    Returns:
        score: The list of scores for the given parameters.
    '''
    kf = KFold(splits, shuffle, random_state)
    score = []
    for i_train, i_test in kf.split(X):
        X_train = X.iloc[i_train]
        X_test= X.iloc[i_test]
        y_train = y[i_train]
        y_test = y[i_test]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score.append(metric(y_test, y_pred))
    return score
