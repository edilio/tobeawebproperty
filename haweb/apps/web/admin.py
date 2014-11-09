from django.contrib import admin
from .models import FAQ, HelpfulLink

admin.site.register([FAQ, HelpfulLink])
