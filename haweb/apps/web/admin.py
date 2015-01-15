from django.contrib import admin
# from django import forms
# from django.db import models
from django.db import utils
from django.db.models.loading import get_model

from .models import (FAQ,
                     HelpfulLink,
                     Career,
                     ResourceCategory,
                     ResourceForm,
                     Organization,
                     Menu,
                     CarouselInfo,
                     Content,
                     # WorkOrder
)


class TinymceAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/vendor/tinymce/tinymce.min.js',
            'js/vendor/tinymce/textareas.js',
        )

@admin.register(FAQ)
class FAQAdmin(TinymceAdmin):
    list_display = ('index', 'question', 'short_answer')
    search_fields = ('question', 'answer')


@admin.register(HelpfulLink)
class HelpfulLinkAdmin(TinymceAdmin):
    list_display = ('index', 'title', 'url', 'short_description')
    search_fields = ('title', 'description')


@admin.register(Career)
class CareerAdmin(TinymceAdmin):
    list_display = ('index', 'title', 'short_description')
    search_fields = ('title', 'description')
    list_display_links = ('index', 'title')


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('index', 'name')


@admin.register(ResourceForm)
class ResourceFormAdmin(TinymceAdmin):
    list_display = ('index', 'name', 'short_description', 'visible', 'category')
    list_filter = ('visible', 'category')
    search_fields = ('name', 'description')


class CarouselInfoInline(admin.StackedInline):
    model = CarouselInfo
    extra = 3


@admin.register(Organization)
class OrganizationAdmin(TinymceAdmin):
    list_display = ('name', 'address', 'city_state_zip', 'selected_theme', 'lat', 'lng')

    inlines = [CarouselInfoInline]

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('index', 'name', 'link', 'parent', 'how_many_children')
    list_display_links = ('index', 'name', )


@admin.register(Content)
class ContentAdmin(TinymceAdmin):
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

# @admin.register(WorkOrder)
# class WorkOrderAdmin(admin.ModelAdmin):
#     list_display = ('work_order_no', 'priority', 'scheduled', )


def insert_default_user_groups():
    Group = get_model('auth', 'Group')
    try:
        if not Group.objects.exists():
            Group.objects.create(name='Displayable Users')
            Group.objects.create(name='Commissioners')
    except:
        pass


insert_default_user_groups()