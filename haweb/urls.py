from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin

from haweb.apps.web.views import html
from haweb.apps.web.sitemaps import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', html.home, name='home'),
    url(r'^about-us$', html.about_us, name='about_us'),
    url(r'^contact-us$', html.contact_us, name='contact_us'),
    url(r'^pages/$', html.ContentListView.as_view(), name='content_list'),
    url(r'^pages/(?P<slug>[-\w\d]+)/$', html.ContentDetail.as_view(), name='content'),
    url(r'^faqs/$', html.FAQListView.as_view(), name='faq_list'),
    url(r'^helpful-links/$', html.HelpfulLinkListView.as_view(), name='helpful_link_list'),
    url(r'^careers/$', html.CareerListView.as_view(), name='career_list'),
    url(r'^resources/$', html.ResourceListView.as_view(), name='resource_list'),
    url(r'^staff/$', html.StaffListView.as_view(), name='staff_list'),
    url(r'^commissioners/$', html.CommissionerListView.as_view(), name='commissioner_list'),
    url(r'^get-directions$', html.get_directions, name='get_directions'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # issues
    url(r'^issues/', include('haweb.apps.issues.urls')),
    # housing
    url(r'^housing/', include('haweb.apps.housing.urls.html')),
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

