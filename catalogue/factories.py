# coding: utf-8
from factory import (
    Factory,
    Sequence,
    )

from .models import Book


class BookFactory(Factory):
    FACTORY_FOR = Book

    title = Sequence(lambda n: 'Book %s' % n)
    price = 14.56
    for_sale = True
    quantity = 10
