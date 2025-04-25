from django.urls import path

from .views import IndexView, AboutView, CatalogView, ContactView


app_name = 'menu'

urlpatterns = [
    path('', IndexView.as_view(), name='index_page'),
    path('about/', AboutView.as_view(), name='about_page'),
    path('catalog/', CatalogView.as_view(), name='catalog_page'),
    path('contact/', ContactView.as_view(), name='contact_page'),
]