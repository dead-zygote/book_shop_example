# coding: utf-8
from django.contrib.auth.decorators import login_required

def require_login(view):
    return login_required(login_url='/login')(view)
