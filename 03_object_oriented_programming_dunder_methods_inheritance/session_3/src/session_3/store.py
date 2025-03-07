class Product:
  def __init__(self, name, price):
    self.name = name
    self.price = price

  def __str__(self):
    return f"Product: {self.name} costs ${self.price:.2f}"

  def __repr__(self):
    return f"Product({self.name!r}, {self.price!r})"

class DiscountedProduct(Product):
  def __init__(self, name, price, discount):
    super().__init__(name, price)
    self.discount = discount  # discount in percentage

  def discounted_price(self):
    return self.price * (1 - self.discount / 100)

  def __str__(self):
    return (f"{self.name} - Original: ${self.price:.2f}, "
          f"Discount: {self.discount}%, Now: ${self.discounted_price():.2f}")

class User:
  def __init__(self, username, email):
    self.username = username
    self.email = email

  def __str__(self):
    return f"User: {self.username}, Email: {self.email}"