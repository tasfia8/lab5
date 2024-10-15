from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

# Initialize the Flask application
application = Flask(__name__)

# Load the pre-trained model and vectorizer
with open('basic_classifier.pkl', 'rb') as fid:
    loaded_model = pickle.load(fid)

with open('count_vectorizer.pkl', 'rb') as vd:
    vectorizer = pickle.load(vd)

@application.route('/')
def home():
    return 'Fake News Classifier is running!'

@application.route('/predict')
def predict():
    try:
        # Get the text to classify from the request
        input_text = request.args.get('text', '')
        if not input_text:
            return jsonify({'error': 'No input text provided'}), 400
        
        # Log the received input
        print(f"Received input: {input_text}")
        
        # Vectorize the input text
        transformed_input = vectorizer.transform([input_text])
        
        # Log the vectorized input for debugging
        print(f"Vectorized input shape: {transformed_input.shape}")
        
        # Predict using the loaded model
        prediction = loaded_model.predict(transformed_input)[0]
        
        # Log the raw prediction value for debugging
        print(f"Raw Prediction Value: {prediction}")
        
        # Map string 'FAKE' to 1, and 'REAL' to 0
        if prediction == 'FAKE':
            result = 1  # FAKE News
        elif prediction == 'REAL':
            result = 0  # REAL News
        else:
            raise ValueError(f"Unexpected prediction value: {prediction}")
        
        print(f"Prediction mapped: {result} (1=FAKE, 0=REAL)")  # Add logging for clarity
        
        return jsonify({'input': input_text, 'prediction': result}), 200

    except Exception as e:
        # Log any errors that occur
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

# Start the Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Get the port from environment variable or use 8080
    application.run(host='0.0.0.0', port=port)
