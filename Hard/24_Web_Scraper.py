import requests
from bs4 import BeautifulSoup

def scrape_website(url, tag, class_name=None):
    try:
        print(f"Scraping {url} for tag <{tag}>...")
        response = requests.get(url)
        response.raise_for_status() # Check for bad status

        soup = BeautifulSoup(response.text, 'html.parser')
        
        if class_name:
            elements = soup.find_all(tag, class_=class_name)
        else:
            elements = soup.find_all(tag)
        
        print(f"Found {len(elements)} elements:")
        print("-" * 20)
        
        for i, element in enumerate(elements[:20]): # storage limit
            print(f"{i+1}: {element.get_text().strip()}")
            if element.name == 'a':
                print(f"   Link: {element.get('href')}")
            print("-" * 10)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = input("Enter the URL to scrape (include http://): ")
    tag = input("Enter the HTML tag to find (e.g. h1, a, p, div): ")
    class_name = input("Enter a class name to filter by (optional, press Enter to skip): ")
    
    if not class_name:
        class_name = None
        
    scrape_website(url, tag, class_name)
