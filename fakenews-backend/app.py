import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Load model and vectorizer from backend directory
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
VECT_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

model = None
vectorizer = None
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECT_PATH)
except Exception as e:
    # Print to stderr so Railway / logs capture the problem
    print(f"Error loading model/vectorizer: {e}", file=sys.stderr)


@app.route('/predict', methods=['POST'])
def predict():
    if model is None or vectorizer is None:
        return jsonify({'error': 'Model not loaded'}), 500
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400
    text = data['text']
    vect = vectorizer.transform([text])
    prediction = model.predict(vect)[0]
    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    # Use PORT from environment for platforms like Railway; default to 5000 for local dev
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port)