# coding: utf-8
from factory import (
    Factory,
    Sequence,
    )

from django.contrib.auth.models import User


class UserFactory(Factory):
    FACTORY_FOR = User

    username = Sequence(lambda n: 'user%s' % n)
    email = Sequence(lambda n: 'user%s@example.com' % n)
