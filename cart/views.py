# coding: utf-8
from django.views.decorators.http import require_POST
from django.contrib import messages
from auth.decorators import require_login

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    )

from django.db.models import F
from catalogue.models import Book

from .models import CartItem
from .forms import CartItemForm


@require_login
def show_cart(request):
    cart_items = request.user.cart.items.all().select_related('book')
    return render(request, 'cart/cart.html', {'cart_items': cart_items})


@require_POST
@require_login
def add_cart_item(request):
    cart = request.user.cart
    cart_item = CartItem(cart=cart)
    form = CartItemForm(request.POST, instance=cart_item)
    if form.is_valid():
        book = form.cleaned_data['book']
        quantity = form.cleaned_data['quantity']
        updated = cart.items.filter(book=book).update(
            quantity = F('quantity') + quantity)
        if updated == 0:
            form.save()
        messages.info(request,
            u'Книга "%s" добавлена в корзину.' % book.title)
    return redirect(show_cart)


@require_POST
@require_login
def delete_cart_item(request, item_id):
    item = get_object_or_404(CartItem, cart=request.user.cart, id=item_id)
    book = item.book
    item.delete()
    messages.info(request, u'Книга "%s" удалена из корзины.' % book.title)
    return redirect(show_cart)


@require_POST
@require_login
def empty_cart(request):
    request.user.cart.items.all().delete()
    messages.info(request, u'Корзина была очищена.')
    return redirect(show_cart)
