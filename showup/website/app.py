from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import dill
from ..pipeline.meetup_pipes import (FeatureSelector, MapFeature,
                                     CustomBinarizer, FillWith, RFRWrapper)
from ..pipeline.meetup_pipeline import random_forest_model, meetup_union, visibility

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/submit", methods=["POST"])
def submit():
     user_data = pd.DataFrame(request.json, index=[0])
     prediction = predict(user_data)
     return jsonify({'prediction': prediction})

def predict(text_input):
    X = text_input
    with open('showup/website/static/model.pkl', 'rb') as f:
        model = dill.load(f)
    #prediction = model.predict(X)[0]
    trees = model.named_steps['model'].estimators_
    predictions = np.zeros(len(trees))
    for i, tree in enumerate(trees):
        predictions[i] += (tree.predict(model.named_steps['meetup_features'].transform(X)))
    lower_bound = np.sort(predictions)[int(len(predictions)*0.05)]
    lower_bound = int(round(log_to_people(lower_bound)))
    upper_bound = np.sort(predictions)[int(len(predictions)*0.95)]
    upper_bound = int(round(log_to_people(upper_bound)))
    return str(lower_bound) + ' - ' + str(upper_bound)

def log_to_people(x):
    return np.e**x - 1

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
