from django.contrib import admin
from .models import FAQ, HelpfulLink, Career


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('index', 'question', 'short_answer')
    search_fields = ('question', 'answer')


@admin.register(HelpfulLink)
class HelpfulLinkAdmin(admin.ModelAdmin):
    list_display = ('index', 'title', 'url', 'short_description')
    search_fields = ('title', 'description')


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('index', 'title', 'short_description')
    search_fields = ('title', 'description')