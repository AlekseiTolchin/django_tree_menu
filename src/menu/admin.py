from django.contrib import admin
from .models import Menu, MenuItem


@admin.register(Menu)
class AdminMenu(admin.ModelAdmin):
    pass


@admin.register(MenuItem)
class AdminMenuItem(admin.ModelAdmin):
    pass
