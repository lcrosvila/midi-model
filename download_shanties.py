import os
import requests
from bs4 import BeautifulSoup
import wget
import zipfile

# Function to fetch HTML content from a URL
def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch HTML content from {url}")
        return None

# Function to extract and download .mid links from HTML
def download_mid_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)
    mid_links = []

    for link in links:
        href = link.get('href')
        if href.endswith('.midi'):
            mid_links.append(href)
    os.makedirs('shanties', exist_ok=True)

    # Download .mid files
    for mid_link in mid_links:
        file_url = '/'.join(base_url.split('/')[:-1]) +'/'+ '/'.join(mid_link.split('/')[-2:])
        if 'music' in os.path.basename(mid_link):
            continue
        file_name = os.path.join('shanties', os.path.basename(mid_link))
        print(f"Downloading {file_name} from {file_url}")
        wget.download(file_url, file_name)
        print(f"{file_name} downloaded successfully.")

def create_zip_archive():
    with zipfile.ZipFile('shanties.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk('shanties'):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), 'shanties'))

if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/20774/20774-h/20774-h.htm"  # Replace with the URL of the HTML page you want to scan
    base_url = "https://www.gutenberg.org/files/20774/20774-h/20774-h.htm"  # Replace with the base URL if relative links are used

    html_content = fetch_html(url)
    if html_content:
        download_mid_links(html_content, base_url)
        # create_zip_archive()