from services.service_webdriver import WebScrapingService, create_webdriver
from adapters.adapter_webdriver import WebDriverAdapter

def main():
    driver = create_webdriver()
    adapter = WebDriverAdapter(driver)
    service = WebScrapingService(adapter)

    try:
        # Scrape the page and get the product name
        service.scrape_page_async()
        service.get_products()
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()