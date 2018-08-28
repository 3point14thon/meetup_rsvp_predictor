import numpy as np


def neg_rmsle(y, y_pred):
    log_pred = np.log(y_pred + 1)
    log_y = np.log(y + 1)
    return -(np.sum((log_pred-log_y)**2)/len(y))**0.5
