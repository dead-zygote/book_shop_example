from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'book_shop_example.views.home', name='home'),
    # url(r'^book_shop_example/', include('book_shop_example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('catalogue.views',
    url(r'^$', 'show_books'),
    url(r'^books/(\d+)$', 'show_book'),
    url(r'^authors/(\d+)$', 'show_author'),
    url(r'^categories/(\d+)$', 'show_category')
)

urlpatterns += patterns('cart.views',
    url(r'^cart$', 'show_cart_items'),
    url(r'^cart/add', 'add_cart_item'),
)

urlpatterns += patterns('',
    url(r'^orders$', 'ordering.views.show_orders'),
    url(r'^login$', 'auth.views.login'),
    url(r'^logout$', 'auth.views.logout'),
    url(r'^register$', 'auth.views.register'),
    )
