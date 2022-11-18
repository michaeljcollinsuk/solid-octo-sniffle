from collections import defaultdict
from dataclasses import dataclass



class Discount:

    def __init__(self, quantity_required, discount_percent, applies_to):
        self.quantity_required = quantity_required
        self.discount_percent = discount_percent
        self.applies_to_every_n_item = applies_to

    @property
    def discount_decimal(self):
        if not self.discount_percent:
            return 0
        return self.discount_percent / 100

    def get_reduction(self, item_price, quantity):
        if quantity < self.quantity_required:
            return 0

        discount_per_item = int(item_price * self.discount_decimal)
        num_items_to_apply_discount = int(quantity / self.applies_to_every_n_item)
        total_discount = num_items_to_apply_discount * discount_per_item
        return total_discount


@dataclass
class Product:

    name: str
    code: str
    price: int
    offer: Discount = None


class Checkout:

    def __init__(self):
        self.products = defaultdict(list)
        self.sub_total = 0

    @property
    def quantities(self):
        return {code: len(products) for code, products in self.products.items()}

    @property
    def distinct_products(self):
        return [products[0] for products in self.products.values()]

    def scan(self, product):
        self.products[product.code].append(product)
        self.sub_total += product.price

    def calculate_discounts(self):
        reductions = 0
        for product in self.distinct_products:

            offer = product.offer
            if not offer:
                continue

            reduction = offer.get_reduction(
                item_price=product.price,
                quantity=self.quantities[product.code]
            )
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
    bogof = Discount(discount_percent=100, quantity_required=2, applies_to=2)
    ten_percent = Discount(discount_percent=10, quantity_required=3, applies_to=1)

    tea = Product(name="Fruit tea", code="FR1", price=311, offer=bogof)
    strawberries = Product(name="Strawberries", code="SR1", price=500, offer=ten_percent)
    coffee = Product(name="Coffee", code="CF1", price=1123)

    checkout.scan(tea)
    checkout.scan(tea)
    checkout.scan(strawberries)
    checkout.scan(strawberries)
    checkout.scan(strawberries)
    checkout.scan(coffee)

    # total should be:
    # - £3.11 for tea, one item is free (worth £3.11)
    # - £13.50 for strawberries, includes £1.50 discount
    # - £11.23 for coffee, no discount
    # - Total: £27.84
    checkout.print_totals()
