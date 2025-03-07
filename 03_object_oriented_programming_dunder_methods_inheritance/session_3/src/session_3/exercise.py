class Product:
    product_name: str
    product_price: float
    def __init__(self, product_name, product_price):
        self.product_name = product_name
        self.product_price = product_price
    def __str__(self):
        return f"The product {self.product_name}, costs {self.product_price:.2f} €"
    def __repr__(self):
        return f"Product: {self.product_name}; Price: {self.product_price:.2f} €;"
class User:
    def __init__(self, userName):
        self.userName = userName
class Store (Product):
    product_stock = int
    def __init__(self, product_name, product_price, product_stock):
        super().__init__(product_name, product_price)
        self.product_stock = product_stock
    def __str__(self):
        return f"The product {self.product_name} costs {self.product_price:.2f} and there's {self.product_stock} units in stock."
    def __repr__(self):
        return f"Product: {self.product_name}; Price: {self.product_price:.2f}; Stock {self.product_stock}."




    