from flask import Flask, request, render_template, jsonify
import pandas as pd
import dill
from ..pipeline.meetup_pipes import (FeatureSelector, MapFeature,
                                     CustomBinarizer, FillWith, RFRWrapper)
from ..pipeline.meetup_pipeline import meetup_model, visibility

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
    return model.predict(X)[0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
