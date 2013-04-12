# coding: utf-8
from django.db.models import (
    Model,
    IntegerField,
    OneToOneField,
    ForeignKey,
    )

from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from catalogue.models import Book
from django.db import connection


class Cart(Model):
    user = OneToOneField(User, null=True)

    @property
    def total_price(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT sum(cart_cartitem.quantity * catalogue_book.price)
            FROM cart_cartitem INNER JOIN catalogue_book
            ON cart_cartitem.book_id = catalogue_book.id
            WHERE cart_cartitem.cart_id = %s
            """, [self.id])
        return cursor.fetchone()[0]


class CartItem(Model):
    cart = ForeignKey(Cart, related_name='items')
    book = ForeignKey(Book, related_name='cart_items')
    quantity = IntegerField(u'Количество', validators=[MinValueValidator(1)])
