import string
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

def remove_stopwords(text: str) -> str:

    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))

    try:
        words = word_tokenize(text)
    except LookupError:
        nltk.download('punkt')
        nltk.download('punkt_tab')
        words = word_tokenize(text)
    filtered = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered)



def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans('', '', string.punctuation))



def remove_numbers(text: str) -> str:
    return re.sub(r'\d+', '', text)


def clean_whitespaces(text: str) -> str:
    # Replace multiple spaces, tabs, or newlines with a single space
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()


def transform_text_in_list(text: str) -> list[str]:
    return text.split()


def remove_verbs(text):


    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Perform part-of-speech tagging
    try:
        tagged_tokens = pos_tag(tokens)
    except:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('averaged_perceptron_tagger_eng')
    
    # Filter out verbs (VB, VBD, VBG, VBN, VBP, VBZ)
    no_verbs = [word for word, tag in tagged_tokens if tag[:2] != 'VB']
    
    # Return the result as a string
    return ' '.join(no_verbs)


def remove_adjectives(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Perform part-of-speech tagging
    tagged_tokens = pos_tag(tokens)
    
    # Filter out adjectives (JJ, JJR, JJS)
    no_adjectives = [word for word, tag in tagged_tokens if tag not in ['JJ', 'JJR', 'JJS']]
    
    # Return the result as a string
    return ' '.join(no_adjectives)



def lemmatize_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Initialize the lemmatizer
    lemmatizer = WordNetLemmatizer()
    
    # Lemmatize each token
    try:
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    except:
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('stopwords')
    
    # Return the result as a string
    return ' '.join(lemmatized_tokens)


