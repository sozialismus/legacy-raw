import requests
from bs4 import BeautifulSoup
import time

def get_page(url):
    """
    Fetches the page content for the given URL and returns a BeautifulSoup object.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error if the request failed
        # UTF-8
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_text(soup):
    """
    Removes script and style elements from the soup and returns cleaned plain text.
    """
    if soup is None:
        return ""
    # Remove unwanted tags
    for tag in soup(["script", "style"]):
        tag.decompose()
    # Extract text and clean up extra whitespace
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def scrape_urls(urls):
    """
    Iterates over a list of URLs, scrapes each one, and returns the combined plain text.
    """
    extracted_texts = []
    for url in urls:
        print(f"Scraping {url} ...")
        soup = get_page(url)
        page_text = extract_text(soup)
        # Append the URL and its content, separated by a clear divider
        extracted_texts.append(f"URL: {url}\n{'='*80}\n{page_text}\n{'-'*80}\n")
        time.sleep(1)  # Respectful delay between requests
    return "\n".join(extracted_texts)

if __name__ == "__main__":
    # Define a list of specific URLs to scrape.
    # Modify or extend this list as needed.
    urls_to_scrape = [
        "https://www.attalus.org/info/alexander.html",
        "https://www.attalus.org/greek/alexander1a.html",
        "https://www.attalus.org/greek/alexander1b.html",
        "https://www.attalus.org/greek/alexander1c.html",
        "https://www.attalus.org/greek/alexander1d.html",
        "https://www.attalus.org/greek/alexander1e.html",
        "https://www.attalus.org/greek/alexander2a.html",
        "https://www.attalus.org/greek/alexander2b.html",
        "https://www.attalus.org/greek/alexander2c.html",
        "https://www.attalus.org/greek/alexander3a.html",
        "https://www.attalus.org/greek/alexander3b.html",
        "https://www.attalus.org/greek/alexander3c.html",
        "https://www.attalus.org/greek/alexander3d.html", # Add additional URLs as needed.
    ]
    
    # Scrape the URLs and combine the extracted text.
    final_text = scrape_urls(urls_to_scrape)
    
    # Save the output to a plain-text file.
    with open("dat/greek/raw_data/attalus/alexander.txt", "w", encoding="utf-8") as file:
        file.write(final_text)
        
    os.makedirs("dat/greek/raw_data/attalus", exist_ok=True)
    
    print("Scraping complete. The extracted text has been saved to 'alexander.txt'.")
