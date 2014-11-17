from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin

from haweb.apps.web.views import html
from haweb.apps.web.sitemaps import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', html.home, name='home'),
    url(r'^about-us$', html.about_us, name='about_us'),
    url(r'^contact-us$', html.contact_us, name='contact_us'),
    url(r'^pages/$', html.ContentListView.as_view(), name='content_list'),
    url(r'^pages/(?P<slug>[-\w\d]+)/$', html.ContentDetail.as_view(), name='content'),
    url(r'^faqs/$', html.FAQListView.as_view(), name='faq_list'),
    url(r'^helpful-links/$', html.HelpfulLinkListView.as_view(), name='helpful_link_list'),
    url(r'^careers/$', html.CareerListView.as_view(), name='career_list'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Api
    url(r'^api/v1/', include('haweb.apps.web.urls.api')),
    url(r'^api/v1/docs/', include('rest_framework_swagger.urls')),
    # Seo
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    (r'^robots\.txt$', include('robots.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

