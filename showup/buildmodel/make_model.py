from ..pipeline.meetup_pipeline import meetup_model
import dill

def create_fit_pickle(X, y, filename):
    with open(filename, 'wb') as f:
        model = meetup_model.fit(X, y)
        dill.dump(model, f)
        return model

if __name__ == '__main__':
    create_fit_pickle(X, y, '../website/static/model.pkl')
