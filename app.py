from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
import pickle
import pandas as pd
import os

app = Flask(__name__, static_folder='static') # Important for static files
CORS(app)

DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true" # Set to false in production
PORT = int(os.environ.get("PORT", 5000))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_SCIENCE_DIR = os.path.join(BASE_DIR, 'data_science')
FILE_NAME_PROCESSOR = os.path.join(DATA_SCIENCE_DIR, 'customer_segmentation_preprocessor.sav')
FILENAME_MODEL = os.path.join(DATA_SCIENCE_DIR, 'customer_segmentation_model.sav')
FILENAME_DATA = os.path.join(DATA_SCIENCE_DIR, 'customer_data_with_clusters.csv')

try:
    kmeans = pickle.load(open(FILENAME_MODEL, 'rb'))
    preprocessor = pickle.load(open(FILE_NAME_PROCESSOR, 'rb'))
    cluster_means = pd.read_csv(FILENAME_DATA)
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