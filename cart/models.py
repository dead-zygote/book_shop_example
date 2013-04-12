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


class Cart(Model):
    user = OneToOneField(User, null=True)

    def total_price(self):
        items = self.items.select_related('book') \
            .only('quantity', 'book__price')
        return sum(item.book.price * item.quantity for item in items)


class CartItem(Model):
    cart = ForeignKey(Cart, related_name='items')
    book = ForeignKey(Book, related_name='cart_items')
    quantity = IntegerField(u'Количество', validators=[MinValueValidator(1)])
