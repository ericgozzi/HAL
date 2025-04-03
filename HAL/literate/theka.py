
from .book import Book

class Library:

    def __init__(self, books: list[Book]):
        self.books = books 
    
    def __str__(self):
        return f'LIBRARY; {len(self.books)} books'
       

    
    def add_book(self, book: Book):
        self.books.append(book)


    def sort_books_by_topic(self, topic: str):

        sorted_books = {}
        for book in self.books:
            eigenvector = book.read_eigenvector()
            try:
                vector = eigenvector[topic]
            except:
                vector = 0
            sorted_books[book] = vector

        self.books = dict(sorted(sorted_books.items(), key=lambda item: item[1], reverse=True))


    def get_answers_to_question(self, question):

        answer = []

        for i, book in enumerate(self.books.keys()):
            sentences_list = book.get_sentences()

            results = []
            for sentence in sentences_list:
                if all(word in sentence.split() for word in question):
                    results.append(sentence)
            

            if len(results) != 0:
                answer.append(f"{book.author.upper()}, {book.title} \n \n")
                for j, result in enumerate(results):
                    answer.append(f"\t{result} \n ")
                answer.append("---")

        return answer



    def ask_theka(self, topic, question) -> list[list[str]]:
        self.sort_books_by_topic(topic)
        answers = self.get_answers_to_question(question)
        return answers
    
