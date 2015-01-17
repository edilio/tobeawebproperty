from django.conf.urls import patterns
from rest_framework import routers

from ..views import api as views

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'cities', views.CityViewSet)
router.register(r'zip-codes', views.ZipCodeViewSet)
router.register(r'tenants', views.TenantViewSet)
router.register(r'contracts', views.ContractViewSet)
router.register(r'units', views.UnitViewSet)

urlpatterns = patterns('haweb.apps.housing',
    # Examples:

)

urlpatterns += router.urls

