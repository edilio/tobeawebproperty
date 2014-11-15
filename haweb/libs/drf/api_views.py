from __future__ import unicode_literals

import warnings

from django.http import Http404
from django.conf import settings

from rest_framework import viewsets, mixins, status, serializers
from rest_framework.response import Response

from .error_responses import ErrorResponse


DEFAULT_LIST_LIMIT = settings.API_SETTINGS.get('DEFAULT_LIST_LIMIT', 30)


def get_offset_limit_params(request, default_limit=DEFAULT_LIST_LIMIT):
    range_errors = []
    offset, limit = 0, default_limit
    try:
        offset = int(request.GET.get('offset', 0))
        if offset < 0:
            raise ValueError
    except ValueError:
        range_errors.append("Invalid value '{0}' for offset. Expected >=0.".format(request.GET.get('offset')))

    try:
        limit = int(request.GET.get('limit', default_limit))
        if limit < 1:
            raise ValueError
    except ValueError:
        range_errors.append("Invalid value '{0}' for limit. Expected >0.".format(request.GET.get('limit')))
    return limit, offset, range_errors


def get_object_list(offset, limit, queryset_or_list):
    return queryset_or_list[offset:(offset+limit)]


class OffsetLimitMixin(object):

    def get_offset_limit_params(self, default_limit=DEFAULT_LIST_LIMIT):
        return get_offset_limit_params(self.request, default_limit)


class JEDListRetrieve(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,
                      OffsetLimitMixin):
    """
    A viewset that provides default `retrieve()` and `list()` actions.
    but the list will contains the way smart bear api should work with limit, offset
    """
    include_total = False

    @staticmethod
    def get_object_not_found_error_response(object_name, object_lookup_key):
        return ErrorResponse(data="{0} with ID '{1}' not found.".format(object_name, object_lookup_key),
                             status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_fields_for_sencha(serializer):
        fields = serializer.get_fields().keys()
        return [{'header': f, 'name': f} for f in fields]

    def generate_list_response(self, query, object_list, serializer, offset, limit):
        """

        :rtype : object
        :param query: The whole query before limiting using offset and limit params
        :param object_list: the result of applying offset and limit to the query
        :param serializer: serialize or serialized_data for some uses
        :param offset:
        :param limit:
        :return: a response object with the data serialized
        """
        object_list_count = len(object_list) if isinstance(object_list, list) else object_list.count()
        serialized_data = serializer.data if isinstance(serializer, serializers.Serializer) else serializer
        json_dict = {
            'success': True,
            'metaData': {
                'root': 'rows',
                'totalProperty': 'totalCount',
                'successProperty': 'success',
                'idProperty': 'id',
                'sortInfo': {
                    "field": 'id',
                    "direction": 'asc'
                },
                'fields': self.get_fields_for_sencha(serializer)
            },
            'rows': serialized_data,
            'totalCount':object_list_count
        }
        return Response(json_dict)

    def list(self, request, *args, **kwargs):
        """
        list all
        limit -- limit
        offset -- offset
        """
        query = self.filter_queryset(self.get_queryset())
        if isinstance(query, ErrorResponse):
            return query
        default_limit = DEFAULT_LIST_LIMIT
        limit, offset, range_errors = self.get_offset_limit_params(default_limit)
        if range_errors:
            return ErrorResponse(data=range_errors)

        self.object_list = get_object_list(offset, limit, query)

        # Default is to allow empty querysets.  This can be altered by setting
        # `.allow_empty = False`, to raise 404 errors on empty querysets.
        if not self.allow_empty and not self.object_list:
            warnings.warn(
                'The `allow_empty` parameter is due to be deprecated. '
                'To use `allow_empty=False` style behavior, You should override '
                '`get_queryset()` and explicitly raise a 404 on empty querysets.',
                PendingDeprecationWarning
            )
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        # the pagination is not supported, use offset and limit
        serializer = self.get_serializer(self.object_list, many=True)
        return self.generate_list_response(query, self.object_list, serializer, offset, limit)


class JEDModelViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     JEDListRetrieve):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    but the list will contains the way smart bear api should work with limit, offset
    """
    pass
