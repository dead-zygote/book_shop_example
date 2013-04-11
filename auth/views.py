# coding: utf-8
from django.shortcuts import (
    render,
    redirect,
    )

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from cart.models import Cart
from .forms import RegistrationForm


def register(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cart.objects.create(user=user)
            password = form.cleaned_data['password1']
            user = auth.authenticate(username=user.username,
                password=password)
            auth.login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'auth/registration.html', { 'form': form })


def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],
            password=request.POST['password'])
        if user and user.is_active:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, u'Вы неправильно ввели логин или пароль.')
    return render(request, 'auth/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
