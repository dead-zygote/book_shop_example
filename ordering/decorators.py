# coding: utf-8
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def require_address(view):
    @wraps(view)
    def wrapper(request, *args, **kw):
        if request.user.addresses.exists():
           return view(request, *args, **kw)
        else:
            messages.info(request, u'Вам нужно указать свой адрес.')
            return redirect(reverse('ordering.views.add_address')) 
    return wrapper
