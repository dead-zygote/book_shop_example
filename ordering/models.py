# coding: utf-8
from django.db.models import (
    Model,
    CharField,
    DecimalField,
    IntegerField,
    DateTimeField,
    ForeignKey,
    )

from django.db.models import signals
from django.dispatch import receiver
from django.core.validators import MinValueValidator
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

    def state_name(self):
        return dict(self.STATES)[self.state]

    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())

    def set_address(self, address):
        self.postcode = address.postcode
        self.region = address.region
        self.city = address.city
        self.other_information = address.other_information
        self.receiver_name = address.receiver_name

    def is_possible(self):
        if self.state in ['new', 'paid']:
            items = self.items.all().select_related('book') \
                .only('quantity', 'book__quantity')
            # TODO: попробовать обойтись запросом
            for item in items:
                if item.quantity > item.book.quantity:
                    return False
        return True

    def prepare_books(self):
        for item in self.items.all().select_related('book'):
            book = item.book
            book.quantity -= item.quantity
            book.save()

    def unprepare_books(self):
        for item in self.items.all():
            book = item.book
            book.quantity += item.quantity
            book.save()

    def __unicode__(self):
        return u'Заказ №%i' % self.id

    def get_absolute_url(self):
        return '/order/%i' % self.id

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'


@receiver(signals.post_init, sender=Order)
def after_order_init(sender, instance, **kwargs):
    instance.initial_state = instance.state


@receiver(signals.pre_save, sender=Order)
def before_order_save(sender, instance, **kwargs):
    if instance.initial_state in ('new', 'paid') \
    and instance.state in ('ready', 'sent'):
        if instance.is_possible():
            instance.prepare_books()
        else:
            instance.state = instance.initial_state
    elif instance.initial_state in ('ready', 'sent') \
    and instance.state in ('new', 'paid'):
        instance.unprepare_books()


@receiver(signals.pre_delete, sender=Order)
def before_order_delete(sender, instance, **kwargs):
    if instance.state == 'ready':
        instance.unprepare_books()
    

class OrderItem(Model):
    order = ForeignKey(Order, related_name='items')
    book = ForeignKey(Book, related_name='order_items', verbose_name=u'Книга')
    price = DecimalField(u'Цена', max_digits=8, decimal_places=2,
        validators=[MinValueValidator(1)])
    quantity = IntegerField(u'Количество', validators=[MinValueValidator(1)])

    def admin_book_link(self):
        book = self.book
        return '<a href="/admin/shop/book/%i/" target="_blank">%s</a>' % (
            book.id, book.title)

    admin_book_link.allow_tags = True
    admin_book_link.short_description = u'Книга'

    def __unicode__(self):
        return '#%i' % self.id

    class Meta:
        verbose_name = u'Заказанный товар'
        verbose_name_plural = u'Заказанные товары'
