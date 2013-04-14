# coding: utf-8
from django.test import TestCase
from mock import Mock
from django.core.exceptions import ValidationError

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

    def test_state_effect_when_new(self):
        order = OrderFactory()
        self.assertIsNone(order.state_effect())

    def test_state_effect_when_new_becomes_paid(self):
        order = OrderFactory()
        order.state = 'paid'
        self.assertIsNone(order.state_effect())

    def test_state_effect_when_new_becomes_ready(self):
        order = OrderFactory()
        order.state = 'ready'
        self.assertEqual(order.state_effect(), 'prepare')

    def test_state_effect_when_new_becomes_sent(self):
        order = OrderFactory()
        order.state = 'sent'
        self.assertEqual(order.state_effect(), 'prepare')

    def test_state_effect_when_paid(self):
        order = OrderFactory(state='paid')
        self.assertIsNone(order.state_effect())

    def test_state_effect_when_paid_becomes_new(self):
        order = OrderFactory(state='paid')
        order.state = 'new'
        self.assertIsNone(order.state_effect())

    def test_state_effect_when_paid_becomes_ready(self):
        order = OrderFactory(state='paid')
        order.state = 'ready'
        self.assertEqual(order.state_effect(), 'prepare')

    def test_state_effect_when_paid_becomes_sent(self):
        order = OrderFactory(state='paid')
        order.state = 'sent'
        self.assertEqual(order.state_effect(), 'prepare')

    def test_state_effect_when_ready(self):
        order = OrderFactory(state='ready')
        self.assertIsNone(order.state_effect())

    def test_state_effect_when_ready_becomes_new(self):
        order = OrderFactory(state='ready')
        order.state = 'new'
        self.assertEqual(order.state_effect(), 'unprepare')

    def test_state_effect_when_ready_becomes_paid(self):
        order = OrderFactory(state='ready')
        order.state = 'paid'
        self.assertEqual(order.state_effect(), 'unprepare')

    def test_state_effect_when_ready_becomes_sent(self):
        order = OrderFactory(state='ready')
        order.state = 'sent'
        self.assertIsNone(order.state_effect())

    def test_state_effect_when_sent(self):
        order = OrderFactory(state='sent')
        self.assertIsNone(order.state_effect())

    def test_state_effect_when_sent_becomes_new(self):
        order = OrderFactory(state='sent')
        order.state = 'new'
        self.assertEqual(order.state_effect(), 'unprepare')

    def test_state_effect_when_sent_becomes_paid(self):
        order = OrderFactory(state='sent')
        order.state = 'paid'
        self.assertEqual(order.state_effect(), 'unprepare')

    def test_state_effect_when_sent_becomes_ready(self):
        order = OrderFactory(state='sent')
        order.state = 'ready'
        self.assertIsNone(order.state_effect())

    def test_clean_when_impossible(self):
        order = OrderFactory()
        book = BookFactory(quantity=1)
        order.items.create(book=book, quantity=2, price=book.price)
        order.state = 'ready'
        self.assertRaises(ValidationError, order.clean)

    def test_clean_when_possible(self):
        order = OrderFactory()
        book = BookFactory()
        order.items.create(book=book, quantity=1, price=book.price)
        error_raised = False
        try:
            order.clean()
        except ValidationError:
            error_raised = True
        self.assertFalse(error_raised)

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

    def test_prepare_books_call_when_possible(self):
        order = OrderFactory()
        order.state = 'ready'
        order.is_possible = Mock(return_value=True)
        order.prepare_books = Mock()
        order.save()
        order.prepare_books.assert_called_once_with()

    def test_prepare_books_call_when_impossible(self):
        order = OrderFactory()
        order.state = 'ready'
        order.is_possible = Mock(return_value=False)
        order.prepare_books = Mock()
        order.save()
        self.assertEqual(order.prepare_books.mock_calls, [])

    def test_unprepare_books_call(self):
        order = OrderFactory(state='ready')
        order.state = 'paid'
        order.unprepare_books = Mock()
        order.save()
        order.unprepare_books.assert_called_once_with()

    def test_total_price(self):
        order = OrderFactory()
        book1 = BookFactory()
        book2 = BookFactory()
        order.items.create(book=book1, quantity=2, price=book1.price)
        order.items.create(book=book2, quantity=3, price=book2.price)
        price = book1.price * 2 + book2.price * 3
        self.assertEqual(order.total_price(), price)

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
