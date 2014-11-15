from __future__ import unicode_literals
from types import DictType, ListType, StringTypes

from rest_framework import status
from rest_framework.response import Response


class ErrorResponseException(Exception):
    pass


class ErrorResponse(Response):
    """
    A HttpResponse that indicates an error
    """
    def __init__(self, *args, **kwargs):
        if 'status' not in kwargs:
            kwargs['status'] = status.HTTP_400_BAD_REQUEST

        error_code = kwargs.get('error_code', kwargs.get('status'))
        data = kwargs.get('data', '')
        if isinstance(data, StringTypes):
            kwargs['data'] = ErrorResponse.assemble_response([ErrorResponse.assemble_message(error_code, data)])
        elif isinstance(data, DictType):
            if len(data) == 0:
                raise ErrorResponseException('Error in dictionary format cannot be empty')
            kwargs['data'] = ErrorResponse.assemble_response([ErrorResponse.dict_to_message(error_code, data)])
        elif isinstance(data, ListType):
            if len(data) == 0:
                raise ErrorResponseException('Error in list format cannot be empty')
            errors = []
            for data_item in data:
                if isinstance(data_item, StringTypes):
                    errors.append(ErrorResponse.assemble_message(error_code, data_item))
                else:
                    errors.append(ErrorResponse.dict_to_message(error_code, data_item))
            kwargs['data'] = ErrorResponse.assemble_response(errors)
        else:
            kwargs['data'] = ErrorResponse.assemble_response([ErrorResponse.assemble_message(error_code, '{0}'.format(data))])
        super(ErrorResponse, self).__init__(*args, **kwargs)

    @staticmethod
    def assemble_message(code, message):
        return {'message': message, 'code': code}

    @staticmethod
    def assemble_response(messages):
        return {'errors': messages}

    @staticmethod
    def list_to_str(data):
        if isinstance(data, ListType):
            return ', '.join(data)
        return data

    @staticmethod
    def dict_to_message(default_error_code, data):
        # no error data, pass it through as none
        if len(data) == 0:
            return None
        if 'message' in data and 'code' in data:
            return data
        # put it in a format that we need
        message = ', '.join("'{0}': '{1}'".format(key, ErrorResponse.list_to_str(data[key])) for key in data)
        return ErrorResponse.assemble_message(default_error_code, message)
