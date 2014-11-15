from ..models import Career, ResourceForm, FAQ, HelpfulLink, Content
from ..serializers import (CareerSerializer,
                           ResourceFormSerializer,
                           FAQSerializer,
                           HelpfulLinkSerializer,
                           ContentSerializer)

from haweb.libs.drf.api_views import JEDListRetrieve


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