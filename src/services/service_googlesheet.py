import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from adapters.adapter_sheet import SheetAdapter
from models.product import Product

class GoogleSheetService(SheetAdapter):
    def __init__(self, credentials_file: str, sheet_name: str):
        """
        Initializes the GoogleSheetService with the credentials file and sheet name.
        """
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        self.client = gspread.authorize(credentials)
        self.sheet = self.client.open(sheet_name).sheet1

    def add_product_row(self, product: Product):
        """
        Adds a new row to the Google Sheet with product details.
        """
        current_date = datetime.now().strftime("%m/%d/%Y")
        row = [
            product.product_sku,
            product.product_name,
            product.product_current_price,
            product.product_description,
            product.product_manufacturer,
            product.product_metal_type,
            current_date
        ]
        self.sheet.append_row(row)