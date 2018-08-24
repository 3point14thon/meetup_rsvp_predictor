from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
import dill


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/submit", methods=["POST"])
def submit():
    user_data = request.json
    text_input = user_data['text_input']
    prediction = predict(text_input)
    return jsonify({'prediction': prediction})

def predict(text_input):
    X = [text_input]
    with open('static/model.pkl', 'rb') as f:
        model = dill.load(f)
    return model.predict(X)[0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
