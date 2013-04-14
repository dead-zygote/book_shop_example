"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .models import Book
from .factories import BookFactory

class BookTest(TestCase):
    def test_objects_for_sale(self):
        book1 = BookFactory()
        book2 = BookFactory()
        book3 = BookFactory(for_sale=False)
        self.assertEqual(Book.objects.for_sale.count(), 2)

    def test_quantity_values(self):
        book = BookFactory.build(quantity=3)
        values = list(book.quantity_values())
        self.assertEqual(values, [1, 2, 3])
