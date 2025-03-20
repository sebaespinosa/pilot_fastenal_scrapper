import os
from dotenv import load_dotenv
from services.service_webdriver import WebScrapingService, create_webdriver
from services.service_googlesheet import GoogleSheetService
from adapters.adapter_webdriver import WebDriverAdapter
from models.product import Product

# Load environment variables from .env file
load_dotenv()

def main():
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
        test_product = Product(product_sku="921708370", product_link="https://www.fastenal.com/product/details/921708370")
        service.scrape_single_page(test_product)
        service.get_product_details(test_product)
        print(test_product)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()