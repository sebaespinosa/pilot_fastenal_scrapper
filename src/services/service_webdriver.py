import os
from dotenv import load_dotenv
from adapters.adapter_webdriver import WebDriverAdapter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Import webdriver-manager

class WebScrapingService:
    def __init__(self, adapter: WebDriverAdapter):
        self.adapter = adapter

    def scrape_page(self):
        load_dotenv()
        url = os.getenv("SCRAPING_URL")
        if not url:
            raise ValueError("SCRAPING_URL is not set in the environment variables.")
        
        page_source = self.adapter.get_page_source(url)
        # Add your scraping logic here (e.g., parsing the page source with BeautifulSoup)
        return page_source

    # Example usage in WebScrapingService
    def scrape_page_async(self):
        load_dotenv()
        url = os.getenv("SCRAPING_URL")
        if not url:
            raise ValueError("SCRAPING_URL is not set in the environment variables.")
        
        # Get the HTML content asynchronously
        html_content = self.adapter.get_page_source_async(url)
        return html_content

# Updated utility function to create a WebDriver instance
def create_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--window-size=1024,800")
    # chrome_options.add_argument("--log-level=3")
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
    service = Service(ChromeDriverManager().install())  # Use webdriver-manager to install the driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver