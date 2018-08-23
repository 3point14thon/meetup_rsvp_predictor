from meetup_pipeline import meetup_model
import dill

def create_fit_pickle(X, y, filename):
    with open(filename, 'wb') as f:
        model = meetup_model.fit(X, y)
        dill.dump(model, f)
        return model
