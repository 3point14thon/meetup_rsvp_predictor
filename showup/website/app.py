from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
import pandas as pd
import dill
import meetup_pipeline

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/submit", methods=["POST"])
def submit():
    user_data = pd.DataFrame(request.json, index=[0])
    user_data['waitlist_count'] = 0
    prediction = predict(user_data)[0]
    return jsonify({'prediction': prediction})

def predict(text_input):
    X = text_input
    with open('static/model.pkl', 'rb') as f:
        model = dill.load(f)
    return model.predict(X)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
