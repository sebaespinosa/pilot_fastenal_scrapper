import requests
from bs4 import BeautifulSoup

def scrape_fastenal():
    url = "https://www.fastenal.com/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Add scraping logic here
        print("Scraping successful!")
    else:
        print("Failed to retrieve the webpage.")

if __name__ == "__main__":
    scrape_fastenal()