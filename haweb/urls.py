from django.conf.urls import patterns, include, url

from haweb.apps.web import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'haweb.apps.web.views.home', name='home'),
   url(r'^pages/$', views.ContentListView.as_view(), name='content_list'),
    url(r'^pages/(?P<slug>[-\w\d]+)/$', views.ContentDetail.as_view(), name='content'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
