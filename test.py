from HAL.literate import Quote
from HAL.literate import Quotebook
from HAL.data import export_as_pdf
quotes = Quotebook.from_collection_of_quotes('quotes.txt')

text, footnotes = quotes.build_text_randomly()
print(text)
print()
print("--------------")
print(footnotes)
text = f'{text}\n\n\n-------------\n{footnotes}'

print(text)