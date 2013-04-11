# coding: utf-8
from django.core.management.base import (
    BaseCommand,
    CommandError,
    )

from django.core.files.images import ImageFile
import json
import os

from catalogue.models import (
    Book,
    Author,
    Publisher,
    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('A path to json file with data is required.')
        file_path = args[0]
        if not os.path.exists(file_path):
            raise CommandError('File does not exist.')
        images_dir = os.path.join(os.path.dirname(file_path), 'images')
        if not os.path.exists(images_dir):
            raise CommandError('Images directory does not exist.')
        with open(file_path, 'r') as f:
            data = json.loads(f.read())
        for book_data in data:
            publisher = Publisher.objects.get_or_create(
                name=book_data['publisher'])[0]
            book = Book.objects.create(
                title=book_data['title'],
                isbn=book_data['isbn'],
                publisher=publisher,
                year=book_data['year'],
                pages_count=book_data['pages_count'],
                printed_copies_count=book_data['printed_copies_count'],
                width=book_data['width'],
                height=book_data['height'],
                description=book_data['description'],
                price=book_data['price'],
                quantity=10,
                )
            for author_name in book_data['authors']:
                author = Author.objects.get_or_create(name=author_name)[0]
                book.authors.add(author)
            image_path = os.path.join(images_dir, '%s.jpg' % book.isbn)
            if os.path.exists(image_path):
                with open(image_path) as f:
                    book.image = ImageFile(f)
                    book.save()
            else:
                book.save()
