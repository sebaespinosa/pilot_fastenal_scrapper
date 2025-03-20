from adapters.adapter_webdriver import WebDriverAdapter
from services.service_webdriver import WebScrapingService, create_webdriver

def main():
    driver = create_webdriver()
    adapter = WebDriverAdapter(driver)
    service = WebScrapingService(adapter)

    try:
        page_source = service.scrape_page()
        print(page_source)  # Replace with your processing logic
    finally:
        driver.quit()

if __name__ == "__main__":
    main()