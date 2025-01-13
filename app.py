from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
import pickle
import pandas as pd
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__, template_folder='templates') # Important for static files
CORS(app)

# Get configuration values
DEBUG = config.getboolean('flask', 'debug')
PORT = config.getint('flask', 'port')
HOST = config.get('flask', 'host')

MODEL_PATH = config.get('data_science', 'model_path')
PREPROCESSOR_PATH = config.get('data_science', 'preprocessor_path')
DATA_PATH = config.get('data_science', 'data_path')

try:
    kmeans = pickle.load(open(MODEL_PATH, 'rb'))
    preprocessor = pickle.load(open(PREPROCESSOR_PATH, 'rb'))
    cluster_means = pd.read_csv(DATA_PATH)
    cluster_means = cluster_means.groupby('cluster').mean(numeric_only=True)
    cluster_labels = {}
    sorted_clusters = cluster_means.sort_values('amount_spent').index.tolist()
    cluster_labels[sorted_clusters[0]] = 'Low Income'
    cluster_labels[sorted_clusters[1]] = 'Middle Income'
    cluster_labels[sorted_clusters[2]] = 'High Income'
except FileNotFoundError as e:
    print(f"Error loading resources: {e}")
    exit()

@app.route('/', methods=['GET']) #Serve the html
def index():
    return render_template('index.html', api_url=url_for('predict', _external=True))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_fields = ['area', 'amount_spent', 'tenure', 'qualification']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing fields"}), 400
        try:
            new_data = pd.DataFrame([data])
            processed_new_data = preprocessor.transform(new_data)
            prediction = kmeans.predict(processed_new_data).tolist()
            predicted_label = cluster_labels.get(prediction[0])
            return jsonify({'cluster_label': predicted_label}), 200
        except ValueError as e:
            return jsonify({"error": f"Invalid data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT, host="0.0.0.0") #Important for Render