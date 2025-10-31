import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the index page
index_url = "https://www.clarelibrary.ie/eolas/coclare/history/kr_evictions/kr_evictions_extracts.htm"

# Folder to save extracts
output_folder = "kilrush_evictions_extracts"
os.makedirs(output_folder, exist_ok=True)

# Fetch index page
response = requests.get(index_url)
response.raise_for_status()

# Parse index page for links
soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a", href=True)

# Filter relevant links (only .htm pages under kr_evictions)
extract_links = [
    urljoin(index_url, link["href"]) 
    for link in links 
    if "kr_evictions" in link["href"] and link["href"].endswith(".htm")
]

print(f"Found {len(extract_links)} extracts. Downloading...")

# Download each extract page
for link in extract_links:
    filename = link.split("/")[-1]
    save_path = os.path.join(output_folder, filename)

    page_resp = requests.get(link)
    page_resp.raise_for_status()

    with open(save_path, "w", encoding="utf-8") as file:
        file.write(page_resp.text)
    
    print(f"Saved: {filename}")

print("\nDownload complete. You can now upload the folder for DOCX compilation.")
