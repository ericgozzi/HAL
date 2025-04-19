
import requests

from PIL import Image

from io import BytesIO


def ask_wikipedia(question: str, lang='en', sentences = 2) -> str:
    """
    Queries Wikipedia and returns a summary.

    Parameters:
    - question (str): The search term or question.
    - lang (str): Language of the Wikipedia (default: 'en').
    - sentences (int): Number of sentences to return from the summary.

    Returns:
    - str: Summary of the topic or an error message.
    """

    endpoint = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{question.replace(' ', '_')}"

    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            summary = data.get("extract")
            if summary:
                return ' '.join(summary.split('. ')[:sentences]) + '.'
            else:
                return "No summary available for this topic."
            
        elif response.status_code == 404:
            return "No matching page found."
        
        else:
            return f"Wikipedia API returned status code {response.status_code}."
        
    except Exception as e:
        return f"An error occurred: {e}"
    
