from .book import *
from .theka import *



# NATURAL LANGUAGE TOOLKIT
# pip install nltk
import nltk

# Download WordNet data needed for Lemmatization
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


# Download WordNet data needed for Lemmatization
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

try:
    nltk.data.find("corpora/omw-1.4")
except LookupError:
    nltk.download("omw-1.4")

#Download stopwords
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")    