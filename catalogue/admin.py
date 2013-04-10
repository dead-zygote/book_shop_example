# coding: utf-8
from django.contrib.admin import (
    ModelAdmin,
    StackedInline,
    TabularInline,
    )

from django.contrib import admin

from models import (
    Book,
    Author,
    Publisher,
    Category,
    )


class BookAdmin(ModelAdmin):
    list_display = ('id', 'title', 'isbn', 'year',
        'quantity', 'price', 'for_sale')
    list_display_links = ('title', 'isbn')
    search_fields = ('title', 'isbn')
    list_filter = ('categories', 'for_sale', 'cover_type')
    filter_horizontal = ('authors', 'categories')
    readonly_fields = ('created_at', 'changed_at')

admin.site.register(Book, BookAdmin)


class PublisherAdmin(ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)

admin.site.register(Publisher, PublisherAdmin)


class AuthorAdmin(ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)

admin.site.register(Author, AuthorAdmin)


class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)

admin.site.register(Category, CategoryAdmin)
