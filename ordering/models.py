# coding: utf-8
from django.db.models import (
    Model,
    Manager,
    CharField,
    DecimalField,
    IntegerField,
    DateTimeField,
    ForeignKey,
    F,
    )

from django.db.models import signals
from django.db import connection
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from catalogue.models import Book


class Address(Model):
    user = ForeignKey(User, related_name='addresses')
    postcode = CharField(u'Почтовый индекс', max_length=6)
    region = CharField(u'Регион', max_length=150)
    city = CharField(u'Город', max_length=150)
    other_information = CharField(u'Улица, дом, квартира', max_length=800)
    receiver_name = CharField(u'Имя получателя', max_length=300)

    def __unicode__(self):
        return '%s, %s, %s; %s; %s' % (self.postcode, self.region, self.city,
            self.other_information, self.receiver_name)


class Order(Model):
    STATES = (
        ('new', u'новый'),
        ('paid', u'оплачен'),
        ('ready', u'готов'),
        ('sent', u'отправлен'),
    )
    STATES_DICT = dict(STATES)

    user = ForeignKey(User, verbose_name=u'Пользователь',
        related_name='orders')
    state = CharField(u'Статус', max_length=10, choices=STATES,
        default='new')
    # address information:
    postcode = CharField(u'Почтовый индекс', max_length=6)
    region = CharField(u'Регион', max_length=150)
    city = CharField(u'Город', max_length=150)
    other_information = CharField(u'Улица, дом, квартира', max_length=800)
    receiver_name = CharField(u'Имя получателя', max_length=300)
    # timestamps
    created_at = DateTimeField(u'Время создания', auto_now_add=True)
    changed_at = DateTimeField(u'Время изменения', auto_now=True)

    def clean(self):
        if self.state_effect() == 'prepare' and not self.is_possible():
            raise ValidationError(u'Невозможно изменить состояние заказа.')

    def state_name(self):
        return self.STATES_DICT[self.state]

    def state_effect(self):
        if self.initial_state in ('new', 'paid') \
        and self.state in ('ready', 'sent'):
            return 'prepare'
        elif self.initial_state in ('ready', 'sent') \
        and self.state in ('new', 'paid'):
            return 'unprepare'

    def total_price(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT sum(quantity * price)
            FROM ordering_orderitem
            WHERE order_id = %s
            """, [self.id])
        return cursor.fetchone()[0] or 0

    def set_address(self, address):
        self.postcode = address.postcode
        self.region = address.region
        self.city = address.city
        self.other_information = address.other_information
        self.receiver_name = address.receiver_name

    def is_possible(self):
        return not self.items.filter(quantity__gt=F('book__quantity')).exists()

    def prepare_books(self):
        for item in self.items.all():
            Book.objects.filter(id=item.book_id).update(
                quantity = F('quantity') - item.quantity)

    def unprepare_books(self):
        for item in self.items.all():
            Book.objects.filter(id=item.book_id).update(
                quantity = F('quantity') + item.quantity)

    def __unicode__(self):
        return u'Заказ №%i' % self.id

    def get_absolute_url(self):
        return '/orders/%i' % self.id

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'


@receiver(signals.post_init, sender=Order)
def after_order_init(sender, instance, **kwargs):
    instance.initial_state = instance.state


@receiver(signals.pre_save, sender=Order)
def before_order_save(sender, instance, **kwargs):
    if instance.state_effect() == 'prepare' and instance.is_possible():
        instance.prepare_books()
    elif instance.state_effect() == 'unprepare':
        instance.unprepare_books()


@receiver(signals.pre_delete, sender=Order)
def before_order_delete(sender, instance, **kwargs):
    if instance.state == 'ready':
        instance.unprepare_books()


class OrderItemManager(Manager):
    def create_from_cart_item(self, cart_item):
        return self.create(
            book=cart_item.book,
            price=cart_item.book.price,
            quantity=cart_item.quantity,
            )


class OrderItem(Model):
    order = ForeignKey(Order, related_name='items')
    book = ForeignKey(Book, related_name='order_items', verbose_name=u'Книга')
    price = DecimalField(u'Цена', max_digits=8, decimal_places=2,
        validators=[MinValueValidator(1)])
    quantity = IntegerField(u'Количество', validators=[MinValueValidator(1)])

    objects = OrderItemManager()

    def admin_book_link(self):
        book = self.book
        return '<a href="/admin/catalogue/book/%i/" target="_blank">%s</a>' % (
            book.id, book.title)

    admin_book_link.allow_tags = True
    admin_book_link.short_description = u'Книга'

    def __unicode__(self):
        return '#%i' % self.id

    class Meta:
        verbose_name = u'Заказанный товар'
        verbose_name_plural = u'Заказанные товары'
