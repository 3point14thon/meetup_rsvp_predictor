import numpy as np
from sklearn.model_selection import KFold

def neg_rmsle(y, y_pred):
    log_pred = np.log(y_pred + 1)
    log_y = np.log(y + 1)
    return -(np.sum((log_pred-log_y)**2)/len(y))**0.5

def cv_score(model, X, y, metric, splits=3, random_state=None, shuffle=False):
    kf = KFold(splits, shuffle, random_state)
    score = []
    for i_train, i_test in kf.split(X):
        X_train = X[i_train]
        X_test= X[i_test]
        y_train = y[i_train]
        y_test = y[i_test]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score.append(metric(y_test, y_pred))
    return score
