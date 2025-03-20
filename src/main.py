import os
from dotenv import load_dotenv
from services.service_webdriver import WebScrapingService, create_webdriver
from services.service_googlesheet import GoogleSheetService
from adapters.adapter_webdriver import WebDriverAdapter
from models.product import Product
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def main():
    # Print the start time
    print(f"Script started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    driver = create_webdriver()
    adapter = WebDriverAdapter(driver)

    # Get variables from .env file
    credentials_file = os.getenv("CREDENTIALS_FILE")
    sheet_name = os.getenv("SHEET_NAME")

    # Initialize GoogleSheetService
    google_sheet_service = GoogleSheetService(
        credentials_file=credentials_file,
        sheet_name=sheet_name
    )

    # Pass the GoogleSheetService (via SheetAdapter) to WebScrapingService
    service = WebScrapingService(adapter, google_sheet_service)

    try:
        # Scrape the page and get the product name
        service.scrape_page_async()
        products = service.get_products()
        
        for product in products:
            service.scrape_single_page(product)
            service.get_product_details(product)
            print(product)

    finally:
        driver.quit()
        # Print the end time
        print(f"Script ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()