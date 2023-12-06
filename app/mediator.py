import sys, os
from flask import Flask, request, render_template, jsonify

sys.path.insert(0, '../machinelearning')
import classifier

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('developer-home.html')

@app.route('/adminlogin')
def adminLogin():
    return render_template('admin-login.html')

@app.route('/adminhome')
def adminHome():
    return render_template('admin-home.html') 

@app.route('/predict', methods=['POST'])
def predict():
    description = request.json['description']
    predictions = classifier.predict_design_pattern(description)
    return jsonify(predictions)

@app.route('/get-sources')
def get_sources():
    directory = '../crawler_cleanup'
    json_files = [f for f in os.listdir(directory) if f.endswith('.json') and os.path.isfile(os.path.join(directory, f))]
    return jsonify(json_files)

@app.route('/updateLibrary', methods=['POST'])
def updateLibrary():
    description = request.json['description']
    
if __name__ == '__main__':
    app.run(debug=True)
