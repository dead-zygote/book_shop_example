# coding: utf-8
from functools import wraps
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def require_cart(view):
    @wraps(view)
    def wrapper(request, *args, **kw):
        if request.user.cart.items.exists():
            return view(request, *args, **kw)
        else:
            return redirect(reverse('cart.views.show_cart'))
    return wrapper
