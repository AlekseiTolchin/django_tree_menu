from django.urls import path

from .views import IndexView, AboutView, CatalogView, ContactView, PhonesView, TvsView


app_name = 'menu'

urlpatterns = [
    path('', IndexView.as_view(), name='index_page'),
    path('about/', AboutView.as_view(), name='about_page'),
    path('catalog/', CatalogView.as_view(), name='catalog_page'),
    path('contacts/', ContactView.as_view(), name='contacts_page'),
    path('catalog/phones', PhonesView.as_view(), name='phones_page'),
    path('catalog/tvs', TvsView.as_view(), name='tvs_page'),
]
