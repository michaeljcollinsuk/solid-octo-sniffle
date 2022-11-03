# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from collections import defaultdict


class Product:

    def __init__(self, name, code, price, offer=None):
        self.name = name
        self.code = code
        self.price = price
        self.offer = None


class Checkout:

    products = []
    sub_total = 0
    # products = {
    #     "pr1": 1,
    #     "pr2": 2,
    # }

    @property
    def quantities(self):
        quantities = defaultdict(int)
        for product in self.products:
            quantities[product.code] += 1
        return quantities

    @property
    def offers(self):
        return {product.code: product.offer for product in self.products if product.offer}

    def scan(self, product):
        self.products.append(product)
        self.sub_total += product.price

    @property
    def get_total_reductions(self):
        reductions = 0
        for product_code, offer in self.offers.items():
            print(offer)
            reductions -= offer.get_reduction()
        return reductions

    def calculate_total(self):
        return self.sub_total - self.get_total_reductions


class OfferMixin:

    def __init__(self, product, quantity_required):
        self.product = product
        self.quantity_required = quantity_required

    def get_reduction(self, quantity):
        raise NotImplementedError("Subclass must implement this method")


class BOGOF(OfferMixin):

    def get_reduction(self, quantity):
        items_free = int(quantity / self.quantity_required)
        return self.product.price * items_free


class Discount(OfferMixin):

    discount_percent = 10

    @property
    def discount_percentage(self):
        return self.discount_percent / 100

    @property
    def discount_per_item(self):
        return int(self.product.price * self.discount_percentage)

    def get_reduction(self, quantity):
        if quantity < self.quantity_required:
            return 0

        total_discount = quantity * self.discount_per_item
        return total_discount


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    checkout = Checkout()
    tea1 = Product(name="Fruit tea", code="FR1", price=311)
    tea2 = Product(name="Fruit tea", code="FR1", price=311)
    BOGOF(quantity_required=1)
    BOGOF(quantity_required=1)

    checkout.scan(tea1)
    checkout.scan(tea2)
    print(checkout.sub_total)
    print(checkout.calculate_total())



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
