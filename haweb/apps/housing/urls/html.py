from django.conf.urls import patterns, url

urlpatterns = patterns(
    'haweb.apps.housing.views',
    url(r'^$', 'html.import_view', name='import_view'),
)

