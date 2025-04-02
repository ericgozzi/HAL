import re
from collections import Counter



from ..data import read_file
from ..data import export_json



# NATURAL LANGUAGE TOOLKIT
# pip install nltk
import nltk

# Download WordNet data needed for Lemmatization
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords



import networkx as nx



class Book:

    def __init__(self, author: str, title: str):
        self.author = author.lower()
        self.title = title.lower()


    def __str__(self):
        return f'Book: author: {self.author.upper()}, title: {self.title}'





    def from_author_title_and_content(author: str, title: str, file_content: str):
        raise NotImplementedError
    




    def from_json_file(file_path: str):
        raise NotImplementedError





    def set_content (self, file_path: str) -> None:
        self.content = read_file(file_path)





    def curate_book(self):
        """
        Cleans and refines the book content by removing or replacing specific characters 
        and formatting inconsistencies.

        Args:
            None (Operates on the instance's `self.content` attribute).

        Returns:
            None: The cleaned text is stored back in `self.content`.+

        Replacements:
            - `{`, `}` → replaced with a space.
            - `-` → replaced with a space.
            - `\n`, `\r` → replaced with a space.
            - `" ."` → replaced with `"."` (removes space before periods).
            - `" ,"` → replaced with `","` (removes space before commas).
            - Multiple consecutive spaces → replaced with a single space.

        Example:
            Before:
                self.content = "Hello - world!\nThis is {a} test.\rAnother  example."
            
            After calling `curate_book()`:
                self.content = "Hello world! This is a test. Another example."
        """
        text = self.content
        text = text.replace("}", " ")
        text = text.replace("{", " ")
        text = text.replace("-", " ")
        text = text.replace("\n", " ") 
        text = text.replace(" .", ".")
        text = text.replace(" ,", ",")
        text = text.replace("\r", " ")
        text = re.sub(r'\s+', ' ', text)
        self.content = text





    def get_words(self, store_as_variable=False) -> list:
        
        # Download WordNet data needed for Lemmatization
        nltk.download('wordnet')
        nltk.download('omw-1.4')

        #Download stopwords
        from nltk.corpus import stopwords
        nltk.download('stopwords')
        
        lemmatizer = WordNetLemmatizer()

        all_words = re.findall(r'\b\w+\b', self.text.lower())

        words = []
        stop_words = set(stopwords.words("english"))
        for word in all_words:

            base_form = lemmatizer.lemmatize(word)

            if base_form not in stop_words and len(base_form)>2:
                words.append(base_form) 
        return words
    




    def get_sentences(self) -> list:

        all_sentences = self.text.split(". ")
        sentences = []
        for sentence in all_sentences:
            if len(sentence) > 3:
                sentence = sentence + "."
                sentences.append(sentence)
                
        return sentences
    




    def get_concatenation_of_words(self) -> list[tuple]:
        word_connections = []
        words = self.get_words()

        for i in range(len(words) - 1):
            word_connections.append((words[i], words[i+1]))

        return word_connections
    



    def get_words_count(self):
        words = self.get_words()
        words_count = Counter(words)
        return words_count




    def get_words_graph(self):
        graph = nx.Graph()
        for word1, word2 in self.word_connections:
            graph.add_edge(word1, word2)
        self.eigenvector_centrality = nx.eigenvector_centrality(graph)
        self.add_metadata("eigenvector", self.eigenvector_centrality)


    
    

    def export_as_json(self, file_path):
        data = {
            'author' : self.author,
            'title' : self.title,

            'content' : self.content,

            'words' : self.get_words(),
            'sentences' : self.get_sentences(),

            'words count' : self.get_words_count()
        }
        export_json(data, file_path)

    