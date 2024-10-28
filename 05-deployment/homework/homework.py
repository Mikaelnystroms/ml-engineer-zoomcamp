import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)


# Load the model and vectorizer
with open('model1.bin', 'rb') as f_model:
    model = pickle.load(f_model)

with open('dv.bin', 'rb') as f_dv:
    dv = pickle.load(f_dv)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the client data from request
    client = request.get_json()

    # Transform the client data using DictVectorizer
    X = dv.transform([client])

    # Make prediction
    y_pred = model.predict_proba(X)[0, 1]

    # Return prediction as JSON
    result = {
        'subscription_probability': float(y_pred)
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
