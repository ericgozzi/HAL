import streamlit as st
import pandas as pd 

from HAL.literate import *
from HAL.pixels import Color
from HAL.metrika import Graph


def get_connections_of_a_question(theka, question):

    topic = question


    library = Library.from_library_folder(theka)
    answers = library.ask(topic,  question, print_answers=False);


    quotebook = Quotebook(answers)
    text, footnotes, title = quotebook.build_text(create_title=True, n=30)

    narrative = filter_by_places(text)
    narrative = clean_whitespaces(narrative)
    connections = get_connection_of_word(narrative)

    return connections



def build_the_city(library: str, questions: list[str]):

    connectivity = Rule([])

    for q in questions:
        conn = get_connections_of_a_question(library, q)
        connectivity.merge(conn)


    g = Graph()
    g.build_graph_from_rules(connectivity)


    bck_colors = {
        'urbotheka': Color.BLACK,
        'hitchhikers_guide': Color.BLUE

    }

    city = g.draw(show_nodes=False, 
                  label_color=Color.WHITE, 
                  edge_color=Color.WHITE,
                  background_color = bck_colors.get(library, Color.BLACK),
                  label_size=30, 
                  edge_direction=False, 
                  graph_type="KAMADA-KAWAI")

    return city









st.title('ASK HAL')


library = st.selectbox(
    "From which library of books would you like to generate a city?",
    ("urbotheka", "hitchhikers_guide"),
)

questions = st.text_input("Generate a city around: ")


questions = questions.lower()
questions = questions.split(' ')


if st.button("Generate"):
    image = build_the_city(library, questions)
    st.image(image.np_array)


