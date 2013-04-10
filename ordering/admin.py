# coding: utf-8
from django.contrib.admin import (
    ModelAdmin,
    StackedInline,
    )

from django.contrib import admin

from models import (
    Order,
    OrderItem,
    )


class OrderItemInline(StackedInline):
    model = OrderItem
    exclude = ('book',)
    readonly_fields = ('admin_book_link', 'price', 'quantity')
    extra = 0
    can_delete = False


class OrderAdmin(ModelAdmin):
    list_display = ('__unicode__', 'total_price', 'state')
    readonly_fields = ('user', 'created_at', 'changed_at')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
