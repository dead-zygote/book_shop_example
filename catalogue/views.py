# coding: utf-8
from django.shortcuts import (
    render,
    get_object_or_404,
    )

from core.shortcuts import paginate

from .models import (
    Book,
    Author,
    Category,
    Publisher,
    )


def show_book(request, id):
    book = get_object_or_404(Book, id=id, for_sale=True)
    return render(request, 'catalogue/book.html', {
        'book': book,
        })


class BooksView(object):
    def __init__(self, owner_class=None):
        self.owner_class = owner_class

    def __call__(self, request, id=None):
        if self.owner_class:
            owner = get_object_or_404(self.owner_class, id=id)
            books_list = owner.books.for_sale
            heading = owner.name
        else:
            books_list = Book.objects.for_sale
            heading = u'Книги'
        search = request.GET.get('search')
        if search:
            books_list = books_list.search(search)
        order_field = request.GET.get('sort_by')
        if order_field and order_field in (
            'title', 'year', '-title', '-year'):
            books_list = books_list.order_by(order_field)
        books = paginate(books_list, request.GET.get('page'))
        return render(request, 'catalogue/books.html', {
            'books': books,
            'categories': Category.objects.all(),
            'search': search,
            'sort_by': order_field,
            'heading': heading,
            })


show_books = BooksView()
show_author = BooksView(Author)
show_category = BooksView(Category)
show_publisher = BooksView(Publisher)
