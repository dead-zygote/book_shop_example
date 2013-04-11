from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('catalogue.views',
    url(r'^$', 'show_books'),
    url(r'^books/(\d+)$', 'show_book'),
    url(r'^authors/(\d+)$', 'show_author'),
    url(r'^categories/(\d+)$', 'show_category')
    )

urlpatterns += patterns('cart.views',
    url(r'^cart$', 'show_cart'),
    url(r'^cart_items/add$', 'add_cart_item'),
    url(r'^cart_items/(\d+)/delete$', 'delete_cart_item'),
    url(r'^cart/empty$', 'empty_cart'),
    )

urlpatterns += patterns('ordering.views',
    url(r'^orders$', 'show_orders', name='orders'),
    url(r'^orders/add$', 'add_order', name='order'),
    url(r'^orders/delete$', 'delete_order', name='delete_order'),
    url(r'^addresses$', 'show_addresses', name='addresses'),
    url(r'^addresses/add$', 'add_address', name='add_address'),
    url(r'^addresses/(\d+)/change$', 'change_address', name='change_address'),
    url(r'^addresses/(\d+)/delete$', 'delete_address', name='delete_address'),
    )

urlpatterns += patterns('auth.views',
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^register$', 'register'),
    )

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    )