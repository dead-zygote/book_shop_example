# coding: utf-8
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    )

from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages

from auth.decorators import require_login
from cart.decorators import require_cart
from .decorators import require_address

from .models import (
    Address,
    Order,
    OrderItem,
    )

from .forms import AddressForm


@require_login
def show_orders(request):
    orders = request.user.orders.all()
    return render(request, 'ordering/orders.html', {'orders': orders})


@require_login
def show_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all().select_related('book')
    return render(request, 'ordering/order.html', {
        'order': order,
        'items': items,
        })


@require_login
@require_address
@require_cart
def add_order(request):
    user = request.user
    if request.method == 'POST':
        try:
            address = user.addresses.get(id=request.POST['address_id'])
        except (DoesNotExist, ValueError):
            address = user.addresses.all()[0]
        posted_cart_item_ids = request.POST.getlist('cart_item_ids')
        cart_item_ids = [item_id for item_id in posted_cart_item_ids
            if item_id.isdigit()]
        cart_items = user.cart.items.filter(id__in=cart_item_ids)
        if cart_items.exists():
            order = Order(user=user)
            order.set_address(address)
            order.save()
            for cart_item in cart_items:
                order.items.create_from_cart_item(cart_item)
            cart_items.delete()
            return redirect(show_orders)
        else:
            messages.error(request, u'Вы не выбрали книги.')
    return render(request, 'ordering/add_order.html', {
        'cart_items': user.cart.items.all(),
        'addresses': user.addresses.all(),
        })


@require_POST
@require_login
def delete_order(request, order_id):
    order = get_object_or_404(Order, user=request.user, id=order_id)
    if order.state == 'new':
        order.delete()
    else:
        messages.info(u'Заказ не может быть удален.')
    return redirect(show_orders)


@require_login
def show_addresses(request):
    addresses = request.user.addresses.all()
    return render(request, 'ordering/addresses.html', {
        'addresses': addresses,
        })


@require_login
def add_address(request):
    if request.method == 'POST':
        address = Address(user=request.user)
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect(show_addresses)
    else:
        form = AddressForm()
    return render(request, 'ordering/add_address.html', {'form': form})


@require_login
def change_address(request, address_id):
    address = get_object_or_404(Address, user=request.user, id=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect(show_addresses)
    else:        
        form = AddressForm(instance=address)
    return render(request, 'ordering/change_address.html', {
        'form': form,
        'address': address
        })


@require_POST
@require_login
def delete_address(request, address_id):
    address = get_object_or_404(Address, user=request.user, id=address_id)
    address.delete()
    return redirect(show_addresses)

