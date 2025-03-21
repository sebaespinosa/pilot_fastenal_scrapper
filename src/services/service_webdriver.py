import os
import re
from dotenv import load_dotenv
from adapters.adapter_webdriver import WebDriverAdapter
from adapters.adapter_sheet import SheetAdapter
from models.product import Product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # Import By for locating elements
from webdriver_manager.chrome import ChromeDriverManager  # Import webdriver-manager

class WebScrapingService:
    def __init__(self, adapter: WebDriverAdapter, sheet_adapter: SheetAdapter):
        self.adapter = adapter
        self.sheet_adapter = sheet_adapter

    # def scrape_page(self):
    #     load_dotenv()
    #     url = os.getenv("SCRAPING_URL")
    #     if not url:
    #         raise ValueError("SCRAPING_URL is not set in the environment variables.")
        
    #     page_source = self.adapter.get_page_source(url)
    #     return page_source

    def scrape_page_async(self, PageNumber = 1):
        load_dotenv()
        url = os.getenv("SCRAPING_URL")
        if(PageNumber == 1):
            url += "&page=1&pageSize=48"
        else:
            url += f"&page={PageNumber}&pageSize=48"
        if not url:
            raise ValueError("SCRAPING_URL is not set in the environment variables.")
        
        html_content = self.adapter.get_page_source_async(url)
        return html_content
    
    def close(self):
        self.adapter.quit()
    
    def scrape_single_page(self, product):
        html_content = self.adapter.get_page_source_async(product.product_link)
        return html_content

    def get_products(self):
        """
        Extracts all product details from all pages using pagination.
        """
        try:
            products = []
            scrapping = True
            currentPage = 1

            while scrapping:
                # Find all elements matching the CSS_SELECTOR
                table = self.adapter.driver.find_element(By.CSS_SELECTOR, "table.table.table-sm.feco-product-list-view-table")
                rows = table.find_elements(By.TAG_NAME, "tr")

                for row in rows:
                    tds = row.find_elements(By.TAG_NAME, "td")
                    sku = tds[0].find_element(By.CSS_SELECTOR, "a.default-nav-link.font-weight-normal")
                    link = tds[0].find_element(By.TAG_NAME, "a").get_attribute("href")

                    product = Product(product_sku=sku.text, product_link=link)
                    products.append(product)

                try:
                    # Locate the pagination element
                    pagination = self.adapter.driver.find_element(By.CSS_SELECTOR, "ul.pagination")
                    pages = pagination.find_elements(By.TAG_NAME, "li")

                    # Check if the last two elements have the class "page-item disabled"
                    if "disabled" in pages[-1].get_attribute("class") and "disabled" in pages[-2].get_attribute("class"):
                        scrapping = False
                    else:
                        # Proceed to the next page
                        currentPage += 1
                        self.scrape_page_async(currentPage)
                except Exception as e:
                    print(f"Error handling pagination: {e}")
                    break

            print(f"Products to scrap: {len(products)}")
            return products

        except Exception as e:
            print(f"Error locating product names: {e}")
            return []

    def get_product_details(self, product):
        """
        Extracts product information from a single product page and stores it in the sheet.
        """
        try:
            product.product_name = self.adapter.driver.find_element(By.XPATH, "//h1[@class='font-weight-bolder feco-seo-title ecom-proddetail-title']//span").text
            try:
                product.product_description = self.adapter.driver.find_element(By.XPATH, "//tr[td[@class='font-weight-600' and normalize-space()='Manufacturer Part No.']]/td[2]").text
            except:
                product.product_description = "Not available"
            product.product_manufacturer = self.adapter.driver.find_element(By.XPATH, "//tr[td[@class='font-weight-600' and normalize-space()='Manufacturer']]/td[2]").text
            try:
                product.product_metal_type = self.adapter.driver.find_element(By.XPATH, "//tr[td[@class='font-weight-bold' and normalize-space()='Material']]/td[2]").text
            except:
                product.product_metal_type = "Not available"
            product.product_current_price = self.adapter.driver.find_element(By.XPATH, "//span[@class='font-weight-600' and normalize-space()='Online Price:']/following-sibling::span").text
            
            # Remove everything after a space (including the space) and non-numeric characters
            product.product_current_price = re.sub(r'[$]|[^0-9]+| .*$', '', product.product_current_price)

            # Store product details in the sheet
            self.sheet_adapter.add_product_row(product)
        except Exception as e:
            print(f"Error extracting product details: {e}")
            # Assign default values to attributes except product_sku and product_link
            product.product_name = 0
            product.product_description = 0
            product.product_manufacturer = 0
            product.product_metal_type = 0
            product.product_current_price = 0
            self.sheet_adapter.add_product_row(product)

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