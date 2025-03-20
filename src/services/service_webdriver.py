import os
from dotenv import load_dotenv
from adapters.adapter_webdriver import WebDriverAdapter
from models.product import Product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # Import By for locating elements
from webdriver_manager.chrome import ChromeDriverManager  # Import webdriver-manager

class WebScrapingService:
    def __init__(self, adapter: WebDriverAdapter):
        self.adapter = adapter

    # def scrape_page(self):
    #     load_dotenv()
    #     url = os.getenv("SCRAPING_URL")
    #     if not url:
    #         raise ValueError("SCRAPING_URL is not set in the environment variables.")
        
    #     page_source = self.adapter.get_page_source(url)
    #     return page_source

    def scrape_page_async(self):
        load_dotenv()
        url = os.getenv("SCRAPING_URL")
        url += "&page=1&pageSize=48"
        if not url:
            raise ValueError("SCRAPING_URL is not set in the environment variables.")
        
        html_content = self.adapter.get_page_source_async(url)
        return html_content

    def get_products(self):
        """
        Extracts all product names from the page using the provided CSS_SELECTOR.
        """
        try:
            
            products = []
            
            # Find all elements matching the CSS_SELECTOR
            table = self.adapter.driver.find_element(By.CSS_SELECTOR, "table.table.table-sm.feco-product-list-view-table")
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                tds = row.find_elements(By.TAG_NAME, "td")
                sku = tds[0].find_element(By.CSS_SELECTOR, "a.default-nav-link.font-weight-normal")
                link = tds[0].find_element(By.TAG_NAME, "a").get_attribute("href")
                
                product = Product(product_sku=sku.text, product_link=link)
                products.append(product)
                
            print(f"Products SKU: {len(products)}")
                
            
        except Exception as e:
            products = [f"Error locating product names: {e}"]
        return products

# Updated utility function to create a WebDriver instance
def create_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1024,800")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"'
    )
    service = Service(ChromeDriverManager().install())  # Use webdriver-manager to install the driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver