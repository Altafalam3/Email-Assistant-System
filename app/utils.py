from joblib import load
import nltk
import string
import re
from typing import Dict
import requests

# Ensure NLTK resources are downloaded
nltk.download("stopwords")
nltk.download("punkt")

# Pre-processing
stop_words = set(nltk.corpus.stopwords.words("english"))
special_chars = set(string.printable) - set(string.ascii_letters) - set(" ")
escaped_chars = [re.escape(c) for c in special_chars]
regex = re.compile(f"({'|'.join(escaped_chars)})")
stemmer = nltk.stem.PorterStemmer()
url_regex = re.compile(r"https?://[^\s]+")

# Load the model
model_path = "models/spam_detection_model.joblib"
try:
    spam_model = load(model_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Model file not found at {model_path}. Ensure the path is correct.")

def preprocess_text(text: str) -> str:
    """
    Pre-process text by performing the following:
    - Convert to lowercase
    - Remove URLs
    - Tokenize
    - Remove stop words
    - Remove non-alphabetic characters
    - Perform stemming
    """
    # Lowercase the text
    text = text.lower()

    # Remove URLs
    text = re.sub(url_regex, " ", text)

    # Tokenization
    tokens = nltk.word_tokenize(text, language='english')

    # Remove stop words
    tokens = [word for word in tokens if word not in stop_words]

    # Remove non-alphabetic characters
    tokens = [word for word in tokens if word.isalpha()]

    # Apply stemming
    tokens = [stemmer.stem(word) for word in tokens]

    return ' '.join(tokens)

def detect_spam(email_text: str) -> Dict[str, bool]:
    """
    Detect if the given email text is spam or not.

    Args:
    - email_input (dict): Dictionary with key 'email_text' containing the email content.

    Returns:
    - dict: Dictionary with key 'is_spam' indicating if the email is spam (True/False).
    """
    # Preprocess the email text
    processed_text = preprocess_text(email_text)

    # Predict using the spam model
    try:
        prediction = spam_model.predict([processed_text])
        print(prediction)
        is_spam = bool(prediction[0])
        return {"is_spam": is_spam, "error":False}
    except Exception as e:
        return {"is_spam": False, "error":True}

# Helper functions
def is_internal_email(sender, user_email):
    """Check if the sender's email belongs to the same organization."""
    sender_domain = sender.split("@")[-1]
    user_domain = user_email.split("@")[-1]
    return sender_domain == user_domain

def search_web_for_context(content):
    """Perform a web search for additional context."""
    response = requests.get(f"https://api.searchengine.com?q={content}")
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

# if __name__=="__main__":
#    email_input = """Congratulations! You've been selected to win a free iPhone 15.
#        Click here to claim your prize."""
#    result = detect_spam(email_input)
#    print(result)