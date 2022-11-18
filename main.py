from collections import defaultdict
from dataclasses import dataclass


class Offer:

    quantity_required = None

    def get_reduction(self, item_price, quantity):
        raise NotImplementedError("Subclass must implement this method")


class BOGOF(Offer):

    quantity_required = 2

    def get_reduction(self, item_price, quantity):
        if quantity < self.quantity_required:
            return 0

        items_free = int(quantity / self.quantity_required)
        return item_price * items_free


class Discount(Offer):

    def __init__(self, quantity_required, discount_percent):
        super().__init__()
        self.quantity_required = quantity_required
        self.discount_percent = discount_percent

    @property
    def discount_decimal(self):
        if not self.discount_percent:
            return 0
        return self.discount_percent / 100

    def get_reduction(self, item_price, quantity):
        if quantity < self.quantity_required:
            return 0

        discount_per_item = int(item_price * self.discount_decimal)
        total_discount = quantity * discount_per_item
        return total_discount


@dataclass
class Product:

    name: str
    code: str
    price: int
    offer: Offer = None


class Checkout:

    def __init__(self):
        # this would have been better as a defaultdict, allow lookup product
        # by their code
        self.products = []
        self.sub_total = 0

    @property
    def quantities(self):
        quantities = defaultdict(int)
        for product in self.products:
            quantities[product.code] += 1
        return quantities

    @property
    def total(self):
        return self.sub_total - self.calculate_discounts()

    def scan(self, product):
        self.products.append(product)
        self.sub_total += product.price

    def calculate_discounts(self):
        applied = []
        reductions = 0

        # this is inefficient as it goes through duplciate products and checks
        # if they are already applied or not. Would be better to go through
        # distinct products
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
