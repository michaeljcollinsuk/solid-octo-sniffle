from collections import defaultdict
from dataclasses import dataclass


class OfferMixin:

    quantity_required = None

    def get_reduction(self, item_price, quantity):
        raise NotImplementedError("Subclass must implement this method")


class BOGOF(OfferMixin):

    quantity_required = 2

    def get_reduction(self, item_price, quantity):
        if quantity < self.quantity_required:
            return 0

        items_free = int(quantity / self.quantity_required)
        return item_price * items_free


class Discount(OfferMixin):

    def __init__(self, quantity_required, discount_percent):
        super().__init__()
        self.quantity_required = quantity_required
        self.discount_percent = discount_percent

    @property
    def discount_percentage(self):
        if not self.discount_percent:
            return 0
        return self.discount_percent / 100

    def get_reduction(self, item_price, quantity):
        if quantity < self.quantity_required:
            return 0

        discount_per_item = int(item_price * self.discount_percentage)
        total_discount = quantity * discount_per_item
        return total_discount


@dataclass
class Product:

    name: str
    code: str
    price: int
    offer: OfferMixin = None


class Checkout:

    def __init__(self):
        self.products = []
        self.sub_total = 0

    @property
    def quantities(self):
        quantities = defaultdict(int)
        for product in self.products:
            quantities[product.code] += 1
        return quantities

    def scan(self, product):
        self.products.append(product)
        self.sub_total += product.price

    def calculate_discounts(self):
        applied = []
        reductions = 0
        for product in self.products:
            
            offer = product.offer
            if not offer:
                continue

            if product.code in applied:
                continue

            reduction = offer.get_reduction(
                item_price=product.price,
                quantity=self.quantities[product.code]
            )
            applied.append(product.code)
            reductions += reduction

        return reductions

    @property
    def total(self):
        return self.sub_total - self.calculate_discounts()

    def pretty_price(self, price):
        decimal = price / 100
        return f"£{decimal}"

    def print_totals(self):
        sub_total = self.pretty_price(self.sub_total)
        total = self.pretty_price(self.total)
        print(f"{sub_total=}")
        print(f"{total=}")


if __name__ == '__main__':
    checkout = Checkout()
    bogof = BOGOF()
    ten_percent = Discount(discount_percent=10, quantity_required=3)

    products = [
        Product(name="Fruit tea", code="FR1", price=311, offer=bogof),
        Product(name="Fruit tea", code="FR1", price=311, offer=bogof),
        Product(name="Fruit tea", code="FR1", price=311, offer=bogof),
        Product(name="Fruit tea", code="FR1", price=311, offer=bogof),
        Product(name="Fruit tea", code="FR1", price=311, offer=bogof),
        Product(name="Coffee", code="CF1", price=1123),
        Product(name="Strawberries", code="SR1", price=500, offer=ten_percent),
        Product(name="Strawberries", code="SR1", price=500, offer=ten_percent),
        Product(name="Strawberries", code="SR1", price=500, offer=ten_percent),
        Product(name="Strawberries", code="SR1", price=500, offer=ten_percent),
        Product(name="Strawberries", code="SR1", price=500, offer=ten_percent),
    ]

    for prod in products:
        checkout.scan(prod)

    checkout.print_totals()
