import requests
import xml.etree.ElementTree as ET
import os


from extract_data import read_save_text, create_name, clean_name

def fetch_sitemap_urls(sitemap_index_url):
    """Fetches sitemap URLs from the sitemap index."""
    response = requests.get(sitemap_index_url)
    response.raise_for_status()  # will raise error if status != 200
    root = ET.fromstring(response.content)
    return root

def fetch_sitemap_content(root_value, site_namespace):
    """Fetches sitemap content from the sitemap index."""
    sitemaps = [loc.text for loc in root_value.findall("ns:sitemap/ns:loc", site_namespace)]
    return sitemaps

def initialize_urls_dict(sitemap_url_list):
    """Initializes a dictionary to hold URLs for each sitemap."""
    URLs_dict = {sitemap_url: [] for sitemap_url in sitemap_url_list}
    return URLs_dict

def is_arabic_url(url):
    '''check if the URL is an Arabic URL'''
    if "/ar/" in url:
        return True
    return False


def fetch_post_urls(sitemap_url_list, site_namespace):
    """Fetches post URLs from the sitemap URLs."""
    URLs_dict = initialize_urls_dict(sitemap_url_list)
    for sitemap_url in sitemap_url_list:
        root = fetch_sitemap_urls(sitemap_url)
        for url in root.findall("ns:url", site_namespace):
            page_url = url.find("ns:loc", site_namespace).text
            if not is_arabic_url(page_url):
                URLs_dict[sitemap_url].append(page_url)
    return URLs_dict

def create_folder_name(sitemap_name):
    """create a folder name from the sitemap name."""
    name = create_name(sitemap_name,-1)
    return clean_name(name)



def create_folder(folder_name, root="scraped_data"):
    """Creates a folder if it does not exist."""
    full_path = os.path.join(root, folder_name)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return True


def scrape_and_save_text(dict_of_urls):
    """ loop over each sitemap then scrape data from each URL and
    save it to a file under the sitemap name."""
    for sitemap, urls in dict_of_urls.items():
        folder_name = create_folder_name(sitemap)
        if create_folder(folder_name):
            for url in urls:
                read_save_text(url, folder_name)

def is_redundant_url(dict_of_urls):
    """Check if the urls in the sitemap are redundant."""
    urls_set = set()
    count = 0
    for urls in dict_of_urls.values():
        for url in urls:
            if url in urls_set:
                count += 1
            else:
                urls_set.add(url)
    if count > 0:
        return True
    return False

if __name__ == "__main__":

    # URL of the sitemap index
    post_sitemap_index_url = "https://digico.solutions/sitemap_index.xml"

    # XML has a namespace, so we need to handle it
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # extract <loc> elements
    root = fetch_sitemap_urls(post_sitemap_index_url)
    sitemap_urls = fetch_sitemap_content(root, namespace)
    print(sitemap_urls)

    # Fetch post URLs from each sitemap
    pages_urls_dict = fetch_post_urls(sitemap_urls, namespace)

    print(is_redundant_url(pages_urls_dict))

    scrape_and_save_text(pages_urls_dict)

