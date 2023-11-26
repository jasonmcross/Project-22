import sys
from flask import Flask, request, render_template, jsonify

sys.path.insert(0, '../machinelearning')
import classifier

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('developer-home.html')


@app.route('/predict', methods=['POST'])
def predict():
    description = request.json['description']
    predictions = classifier.predict_design_pattern(description)
    return jsonify(predictions)


if __name__ == '__main__':
    app.run(debug=True)
