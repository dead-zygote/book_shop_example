# coding: utf-8
from django.test import TestCase

from catalogue.factories import BookFactory
from catalogue.models import Book

from .factories import (
    AddressFactory,
    OrderFactory,
    )

from .models import Order


class OrderTest(TestCase):
    def test_default_state(self):
        order = Order()
        self.assertEqual(order.state, 'new')

    def test_is_possible_when_possible(self):
        order = OrderFactory()
        book = BookFactory()
        order.items.create(book=book, quantity=1, price=book.price)
        self.assertTrue(order.is_possible())

    def test_is_possible_when_impossible(self):
        order = OrderFactory()
        book = BookFactory(quantity=1)
        order.items.create(book=book, quantity=2, price=book.price)
        self.assertFalse(order.is_possible())

    def test_prepare_books(self):
        order = OrderFactory()
        book1_quantity, order_item1_quantity = 5, 2
        book1 = BookFactory(quantity=book1_quantity)
        order.items.create(book=book1, quantity=order_item1_quantity,
            price=book1.price)
        book2_quantity, order_item2_quantity = 6, 3
        book2 = BookFactory(quantity=book2_quantity)
        order.items.create(book=book2, quantity=order_item2_quantity,
            price=book2.price)
        order.prepare_books()
        book1 = Book.objects.get(pk=book1.pk)
        book2 = Book.objects.get(pk=book2.pk)
        self.assertEqual(book1.quantity,
            book1_quantity - order_item1_quantity)
        self.assertEqual(book2.quantity,
            book2_quantity - order_item2_quantity,)

    def test_unprepare_books(self):
        order = OrderFactory()
        book1_quantity, order_item1_quantity = 3, 4
        book1 = BookFactory(quantity=book1_quantity)
        order.items.create(book=book1, quantity=order_item1_quantity,
            price=book1.price)
        book2_quantity, order_item2_quantity = 9, 2
        book2 = BookFactory(quantity=book2_quantity)
        order.items.create(book=book2, quantity=order_item2_quantity,
            price=book2.price)
        order.unprepare_books()
        book1 = Book.objects.get(pk=book1.pk)
        book2 = Book.objects.get(pk=book2.pk)
        self.assertEqual(book1.quantity,
            book1_quantity + order_item1_quantity)
        self.assertEqual(book2.quantity,
            book2_quantity + order_item2_quantity)


    def _makeOrderWithAddress(self):
        order = Order()
        address = AddressFactory.build()
        order.set_address(address)
        return order, address

    def test_postcode_after_set_address(self):
        order, address = self._makeOrderWithAddress()
        self.assertEqual(order.postcode, address.postcode)

    def test_region_after_set_address(self):
        order, address = self._makeOrderWithAddress()
        self.assertEqual(order.region, address.region)

    def test_city_after_set_address(self):
        order, address = self._makeOrderWithAddress()
        self.assertEqual(order.city, address.city)

    def test_other_information_after_set_address(self):
        order, address = self._makeOrderWithAddress()
        self.assertEqual(order.other_information, address.other_information)

    def test_receiver_name_after_set_address(self):
        order, address = self._makeOrderWithAddress()
        self.assertEqual(order.receiver_name, address.receiver_name)
