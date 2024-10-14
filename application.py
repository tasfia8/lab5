from flask import Flask 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Initialize the Flask application
application = Flask(__name__) 

# Model loading
loaded_model = None
with open('basic_classifier.pkl', 'rb') as fid:
    loaded_model = pickle.load(fid)

vectorizer = None
with open('count_vectorizer.pkl', 'rb') as vd:
    vectorizer = pickle.load(vd)

# Prediction
prediction = loaded_model.predict(vectorizer.transform(['This is fake news']))[0]

# Output will be 'FAKE' if fake, 'REAL' if real
if prediction == 1:
    print("FAKE")
else:
    print("REAL")

# Start the Flask app
if __name__ == '__main__':
    # In this simple example, there is no Flask route to handle requests
    # Just add this line to follow the structure in Figure 12
    application.run()

