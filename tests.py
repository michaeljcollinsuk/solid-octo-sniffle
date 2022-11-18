import unittest

from main import Discount, Product, Checkout


class TestTotals(unittest.TestCase):

    def setUp(self) -> None:
        self.bogof = Discount(discount_percent=100, quantity_required=2, applies_to=2)
        self.ten_percent_discount = Discount(discount_percent=10, quantity_required=3, applies_to=1)
        self.checkout = Checkout()

    def test_fruit_tea_buy_one_get_one_free(self):
        """
        Check that when two fruit tea products are scanned, the total is the price of one as the BOGOF offer is applied.
        If a third is added to the basked, the price is increased, but the fourth item is also free
        """
        fruit_tea = Product(name="Fruit tea", code="FR1", price=311, offer=self.bogof)

        self.checkout.scan(fruit_tea)
        self.assertEqual(self.checkout.total, 311)

        # second item should be free
        self.checkout.scan(fruit_tea)
        self.assertEqual(self.checkout.total, 311)

        self.checkout.scan(fruit_tea)
        self.assertEqual(self.checkout.total, 622)

        self.checkout.scan(fruit_tea)
        self.assertEqual(self.checkout.total, 622)

    def test_strawberries_discounted_when_buying_three(self):
        """
        Check that when you buy three or more strawberries, the total is discounted by the correct amount.
        """
        strawberries = Product(name="Strawberries", code="SR1", price=500, offer=self.ten_percent_discount)

        self.checkout.scan(strawberries)
        self.assertEqual(self.checkout.total, 500)

        self.checkout.scan(strawberries)
        self.assertEqual(self.checkout.total, 1000)

        # adding a third item discounts the items
        self.checkout.scan(strawberries)
        self.assertEqual(self.checkout.total, 1350)

        # fourth item should also be discounted
        self.checkout.scan(strawberries)
        self.assertEqual(self.checkout.total, 1800)

    def test_combination_of_products(self):
        """
        Check that when you buying a combination of both products, both discounts are applied to the total
        """
        strawberries = Product(name="Strawberries", code="SR1", price=500, offer=self.ten_percent_discount)
        fruit_tea = Product(name="Fruit tea", code="FR1", price=311, offer=self.bogof)

        self.checkout.scan(fruit_tea)
        self.checkout.scan(fruit_tea)
        self.checkout.scan(strawberries)
        self.checkout.scan(strawberries)
        self.checkout.scan(strawberries)

        self.assertEqual(self.checkout.total, 1661)


if __name__ == '__main__':
    unittest.main()
