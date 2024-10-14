from flask import Flask
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Initialize the Flask application
application = Flask(__name__)

@application.route('/')
def home():
    return 'Fake News Classifier is running!'

# Model loading
loaded_model = None
with open('basic_classifier.pkl', 'rb') as fid:
    loaded_model = pickle.load(fid)

vectorizer = None
with open('count_vectorizer.pkl', 'rb') as vd:
    vectorizer = pickle.load(vd)

@application.route('/predict')
def predict():
    prediction = loaded_model.predict(vectorizer.transform(['This is fake news']))[0]
    return 'FAKE' if prediction == 1 else 'REAL'

# Start the Flask app
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080)


