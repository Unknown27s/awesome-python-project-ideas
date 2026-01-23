# Note: Ebay, Amazon, etc. have strong anti-scraping measures.
# This script is a template for how one would structure such a scraper using BeautifulSoup.
# It may require headers, rotating proxies, or Selenium/Playwright to work reliably.

import requests
from bs4 import BeautifulSoup

def get_ebay_price(url):
    print(f"Scraping: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" 
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch page.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Selectors change frequently on Ebay
        price_tag = soup.find("div", {"class": "x-price-primary"})
        title_tag = soup.find("h1", {"class": "x-item-title__mainTitle"})

        if not price_tag:
            # Fallback for other layouts
            price_tag = soup.find("span", {"id": "prcIsum"})
        
        if price_tag and title_tag:
            price = price_tag.text.strip()
            title = title_tag.text.strip()
            print(f"Product: {title}")
            print(f"Price: {price}")
        else:
            print("Could not find price info. The layout might have changed.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = input("Enter Ebay Product URL: ")
    # Example URL for testing (might be invalid by the time you run): 
    # url = "https://www.ebay.com/itm/1234567890" 
    get_ebay_price(url)
