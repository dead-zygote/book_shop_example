# coding: utf-8
from factory import (
    Factory,
    SubFactory,
    )

from .models import (
    Order,
    OrderItem,
    Address,
    )

from auth.factories import UserFactory
from catalogue.factories import BookFactory

class OrderFactory(Factory):
    FACTORY_FOR = Order

    user = SubFactory(UserFactory)
    postcode = '123456'
    region = 'Example Region'
    city = 'Example City'
    other_information = 'Example Street, 12, 34'
    receiver_name = 'Example Receiver'


class AddressFactory(Factory):
    FACTORY_FOR = Address

    user = SubFactory(UserFactory)
    postcode = '654321'
    region = 'Address Region'
    city = 'Address City'
    other_information = 'Address Street, 45, 56'
    receiver_name = 'Address Owner'


class OrderItemFactory(Factory):
    FACTORY_FOR = OrderItem

    order = SubFactory(OrderFactory)
    book = SubFactory(BookFactory)
    quantity = 1

    def _prepare(self):
        self.price = self.book.price
