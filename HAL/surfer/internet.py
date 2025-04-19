import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

from ..pixels import Picture



def crawl_images(query, max_images=5):
    """
    Crawls the web for images based on the query string, returns a list of PIL Image objects,
    and avoids downloading logos (like Google logo).

    Parameters:
    - query (str): The search query string.
    - max_images (int): The maximum number of images to return.

    Returns:
    - list: List of PIL Image objects that were downloaded.
    """
    # Build the URL for image search (using Google search for simplicity here)
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    
    # Send request to Google Images search
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image elements
    image_tags = soup.find_all('img', {'src': True})

    image_urls = [img['src'] for img in image_tags]

    pil_images = []

    for idx, img_url in enumerate(image_urls[:max_images]):
        try:
            # Skip images with "logo" or "google" in the URL
            if "logo" in img_url.lower() or "google" in img_url.lower():
                print(f"Skipping logo image: {img_url}")
                continue

            # Join relative URLs to form full URLs
            full_url = urljoin(search_url, img_url)

            # Request the image content
            img_data = requests.get(full_url).content

            # Convert the image data into a PIL Image object
            img = Image.open(BytesIO(img_data))

            pil_images.append(img)
            print(f"Downloaded image {idx + 1}: {img_url}")

        except Exception as e:
            print(f"Failed to download image {idx + 1}: {e}")


    pictures = [Picture.from_PIL_image(image) for image in pil_images]
    return pictures