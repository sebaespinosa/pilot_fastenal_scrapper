from services.service_webdriver import WebScrapingService, create_webdriver
from adapters.adapter_webdriver import WebDriverAdapter
from models.product import Product

def main():
    driver = create_webdriver()
    adapter = WebDriverAdapter(driver)
    service = WebScrapingService(adapter)

    try:
        # # Scrape the page and get the product name
        # service.scrape_page_async()
        # products = service.get_products()
        
        # for product in products:
        #     service.scrape_single_page(product)
        #     service.get_product_details(product)
        #     print(product)
        
        test_product = Product(product_sku="0546940", product_link="https://www.fastenal.com/product/details/0546940")
        service.scrape_single_page(test_product)
        service.get_product_details(test_product)
        print(test_product)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()