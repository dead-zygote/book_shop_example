# coding: utf-8
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    )

from django.views.decorators.http import require_POST

from auth.decorators import require_login
from .models import Address
from .forms import AddressForm


@require_login
def show_orders(request):
    orders = request.user.orders.all()
    return render(request, 'ordering/orders.html', {'orders': orders})


@require_login
def add_order(request):
    pass


@require_POST
@require_login
def delete_order(request):
    pass


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

