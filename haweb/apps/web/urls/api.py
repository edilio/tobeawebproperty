from django.conf.urls import patterns
from rest_framework import routers

from ..views import api as views

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'careers', views.CareerViewSet)
router.register(r'resource-forms', views.ResourceFormViewSet)
router.register(r'faqs', views.FAQViewSet)
router.register(r'helpful-links', views.HelpfulLinkViewSet)
router.register(r'contents', views.ContentViewSet)

urlpatterns = patterns('haweb.apps.web',
    # Examples:

)

urlpatterns += router.urls
