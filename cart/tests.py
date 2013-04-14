# coding: utf-8
from django.test import TestCase
from catalogue.factories import BookFactory
from cart.factories import CartFactory


class CartTest(TestCase):
    def test_total_price_when_empty(self):
        cart = CartFactory()
        self.assertEqual(cart.total_price(), 0)

    def test_total_price_when_not_empty(self):
        cart = CartFactory()
        book1 = BookFactory()
        book2 = BookFactory()
        cart.items.create(book=book1, quantity=1)
        cart.items.create(book=book2, quantity=2)
        price = book1.price + book2.price * 2
        self.assertEqual(cart.total_price(), price)

    def test_is_empty_when_empty(self):
        cart = CartFactory()
        self.assertTrue(cart.is_empty())

    def test_is_empty_when_not_empty(self):
        cart = CartFactory()
        cart.items.create(book=BookFactory())
        self.assertFalse(cart.is_empty())


class CartItemTest(TestCase):
    def test_default_quantity(self):
        from .models import CartItem
        cart_item = CartItem(book=BookFactory())
        self.assertEqual(cart_item.quantity, 1)
