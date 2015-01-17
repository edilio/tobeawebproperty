from haweb.apps.core.models import (City, ZipCode, Tenant, Contract, Unit)

from ..serializers import (CitySerializer,
                           ZipCodeSerializer,
                           TenantSerializer,
                           ContractSerializer,
                           UnitSerializer)

from haweb.libs.drf.api_views import JEDListRetrieve, JEDModelViewSet


class CityViewSet(JEDModelViewSet):
    model = City
    serializer_class = CitySerializer


class ZipCodeViewSet(JEDModelViewSet):
    model = ZipCode
    serializer_class = ZipCodeSerializer


class TenantViewSet(JEDModelViewSet):
    model = Tenant
    serializer_class = TenantSerializer


class ContractViewSet(JEDModelViewSet):
    model = Contract
    serializer_class = ContractSerializer


class UnitViewSet(JEDModelViewSet):
    model = Unit
    serializer_class = UnitSerializer