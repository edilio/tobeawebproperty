from django.contrib import admin
from django import forms
from django.db import models

from .models import (FAQ,
                     HelpfulLink,
                     Career,
                     ResourceCategory,
                     ResourceForm,
                     Organization,
                     Menu,
                     CarouselInfo,
                     Content)


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

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('index', 'name')


@admin.register(ResourceForm)
class ResourceFormAdmin(admin.ModelAdmin):
    list_display = ('index', 'name', 'short_description', 'visible', 'category')
    list_filter = ('visible', 'category')
    search_fields = ('name', 'description')


class CarouselInfoInline(admin.StackedInline):
    model = CarouselInfo
    extra = 3


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city_state_zip', 'selected_theme')

    inlines = [CarouselInfoInline]

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('index', 'name', 'link', 'parent', 'how_many_children')
    list_display_links = ('index', 'name', )


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_by', 'created_on', 'modified_by', 'modified_on')

    def save_model(self, request, obj, form, change):
        try:
            u = obj.created_by
            obj.modified_by = request.user
        except Exception as E:
            print type(E)
            obj.created_by = request.user
        obj.save()

    # formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class': 'ckeditor'})}, }

    class Media:
        js = (
            'js/vendor/tinymce/tinymce.min.js',
            'js/vendor/tinymce/textareas.js',
        )


