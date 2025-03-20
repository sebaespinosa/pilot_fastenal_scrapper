from abc import ABC, abstractmethod
from models.product import Product

class SheetAdapter(ABC):
    @abstractmethod
    def add_product_row(self, product: Product):
        """
        Adds a new row to the sheet with product details.
        """
        pass