from ..models import Career, ResourceForm, FAQ, HelpfulLink, Content, WorkOrder
from ..serializers import (CareerSerializer,
                           ResourceFormSerializer,
                           FAQSerializer,
                           HelpfulLinkSerializer,
                           ContentSerializer,
                           WorkOrderSerializer)

from haweb.libs.drf.api_views import JEDListRetrieve, JEDModelViewSet


class CareerViewSet(JEDListRetrieve):
    model = Career
    serializer_class = CareerSerializer


class ResourceFormViewSet(JEDListRetrieve):
    model = ResourceForm
    serializer_class = ResourceFormSerializer


class FAQViewSet(JEDListRetrieve):
    model = FAQ
    serializer_class = FAQSerializer


class HelpfulLinkViewSet(JEDListRetrieve):
    model = HelpfulLink
    serializer_class = HelpfulLinkSerializer


class ContentViewSet(JEDListRetrieve):
    model = Content
    serializer_class = ContentSerializer


class WorkOrderViewSet(JEDModelViewSet):
    model = WorkOrder
    serializer_class = WorkOrderSerializer