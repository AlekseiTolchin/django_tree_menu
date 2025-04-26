from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'menu/index.html'


class AboutView(TemplateView):
    template_name = 'menu/about.html'


class CatalogView(TemplateView):
    template_name = 'menu/catalog.html'


class ContactView(TemplateView):
    template_name = 'menu/contact.html'


class PhonesView(TemplateView):
    template_name = 'menu/phones.html'


class TvsView(TemplateView):
    template_name = 'menu/tvs.html'
