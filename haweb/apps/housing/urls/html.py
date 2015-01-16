from django.conf.urls import patterns, url

urlpatterns = patterns(
    'haweb.apps.housing.views',
    url(r'^$', 'import_view', name='import_view'),
)

