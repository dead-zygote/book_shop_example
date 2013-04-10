# coding: utf-8
from django.db.models import (
    Model,
    CharField,
    IntegerField,
    PositiveIntegerField,
    DecimalField,
    TextField,
    ImageField,
    BooleanField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    )

from django.core.validators import MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class Book(Model):
    title = CharField(u'Название', max_length=200)
    isbn = CharField(u'ISBN', max_length=80, blank=True)
    year = IntegerField(u'Год', validators=[MinValueValidator(1)],
        blank=True, null=True)
    pages_count = IntegerField(u'Количество страниц',
        validators=[MinValueValidator(1)], blank=True, null=True)
    printed_copies_count = PositiveIntegerField(u'Тираж',
        blank=True, null=True, validators=[MinValueValidator(1)])
    description = TextField(u'Описание', blank=True)
    price = DecimalField(u'Цена', max_digits=8, decimal_places=2,
        validators=[MinValueValidator(1)])
    quantity = PositiveIntegerField(u'Количество')
    width = IntegerField(u'Ширина', blank=True, null=True,
        validators=[MinValueValidator(1)])
    height = IntegerField(u'Длина', blank=True, null=True,
        validators=[MinValueValidator(1)])
    thickness = IntegerField(u'Толщина', blank=True, null=True,
        validators=[MinValueValidator(1)])
    weight = IntegerField(u'Вес', blank=True, null=True,
        validators=[MinValueValidator(1)])
    for_sale = BooleanField(u'На продажу', default=False)
    image = ImageField(u'Фотография обложки', upload_to='images/books',
        blank=True, max_length=300)
    small_image = ImageSpecField([ResizeToFit(120,120)],
        image_field='image', format='JPEG')
    publisher = ForeignKey('Publisher', verbose_name=u'Издательство',
        related_name='books', blank=True, null=True)
    cover_type = ForeignKey('CoverType', verbose_name=u'Тип обложки',
        related_name='books', blank=True, null=True)
    authors = ManyToManyField('Author', verbose_name=u'Авторы',
        related_name='books', blank=True)
    categories = ManyToManyField('Category', verbose_name=u'Категории',
        related_name='books', blank=True)
    created_at = DateTimeField(u'Время создания', auto_now_add=True)
    changed_at = DateTimeField(u'Время изменения', auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/book/%i' % self.id

    def author_names(self):
        return ', '.join(author.name for author in self.authors.all())

    def quantity_values(self):
        return xrange(1, self.quantity + 1)
    
    author_names.short_description = u'Авторы'

    class Meta:
        verbose_name = u'Книга'
        verbose_name_plural = u'Книги'


class Publisher(Model):
    name = CharField(u'Название', max_length=200, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/publisher/%i' % self.id

    class Meta:
        verbose_name = u'Издательство'
        verbose_name_plural = u'Издательства'


class Author(Model):
    name = CharField(u'Имя', max_length=300)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/authors/%i' % self.id

    class Meta:
        verbose_name = u'Автор'
        verbose_name_plural = u'Авторы'


class Category(Model):
    name = CharField(u'Название', max_length=150, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/category/%i' % self.id

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class CoverType(Model):
    name = CharField(u'Название', max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип обложки'
        verbose_name_plural = u'Типы обложки'
