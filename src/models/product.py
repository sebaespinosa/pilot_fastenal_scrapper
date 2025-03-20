class Product:
    def __init__(self, *, product_name: str = None, product_sku: str = None, product_link: str = None, 
                 product_description: str = None, product_manufacturer: str = None, 
                 product_metal_type: str = None, product_current_price: str = None):
        self.product_name = product_name
        self.product_sku = product_sku
        self.product_link = product_link
        self.product_description = product_description
        self.product_manufacturer = product_manufacturer
        self.product_metal_type = product_metal_type
        self.product_current_price = product_current_price

    def __repr__(self):
        return (f"Product(product_name={self.product_name}, product_sku={self.product_sku}, "
                f"product_link={self.product_link}, product_description={self.product_description}, "
                f"product_manufacturer={self.product_manufacturer}, product_metal_type={self.product_metal_type}, "
                f"product_current_price={self.product_current_price})")