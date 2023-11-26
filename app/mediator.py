from flask import Flask, request, render_template, jsonify
import classifier

app = Flask(__name__, template_folder = '../pages')

@app.route('/')
def index():
    return render_template('developer_home.html')

@app.route('/mediator', methods=['POST'])
def predict():
    description = request.jason['description']
    predictions = classifier.predict_design_pattern(description)
    return jsonify(predictions)


if __name__ == '__main__':
    app.run(debug=True)
