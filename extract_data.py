import bs4, requests
import os
import re

def fetch_response(url):
    """Fetches responce from a given URL."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}: {response.status_code}")
    else:
        return response

def fetch_text_content(url):
    """ Fetches text content from a given URL."""
    response = fetch_response(url)
    if response is None:
        return None
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    if soup.body is None:
        return None
    text = soup.body.get_text('\n ', strip=True)
    return text

def clean_name(filename):
    """ Cleans the filename by removing invalid characters."""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def create_name(url, number):
    """Creates a filename from the URL."""
    if number == -2:
        name = url.split("/")[number]+ ".txt"
    else:
        name = url.split("/")[number]
        name = name.split(".")[0]
    return name

def save_text_to_file(text, url, path, root="scraped_data"):
    """Saves text content to a file."""
    filename = create_name(url,-2)
    # Remove any characters that are not allowed in filenames
    filename = clean_name(filename)
    print(f"Saving to file: {filename}")
    full_path = os.path.join(root, path, filename)
    print(full_path)
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Error saving file {full_path}: {e}")

def read_save_text(url,path):
    """ Reads text from a URL and saves it to a file."""
    text  = fetch_text_content(url)
    save_text_to_file(text, url, path)