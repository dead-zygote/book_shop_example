# coding: utf-8
from django.forms import ModelForm
from .models import CartItem


class CartItemForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ('book', 'quantity')
