# coding: utf-8
from factory import (
    Factory,
    SubFactory,
    )

from auth.factories import UserFactory
from .models import Cart


class CartFactory(Factory):
    FACTORY_FOR = Cart

    user = SubFactory(UserFactory)
