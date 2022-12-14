from rest_framework.response import Response
from django.http import QueryDict
from user.utils import EncodeDecodeToken
from user.models import User
from rest_framework import status


class InsertionError(Exception):
    """ my custom exception class """


class AlreadyPresentException(Exception):
    """ my custom exception class """


def verify_token(function):
    """
    For verifying user
    :param function:
    :return:
    """

    def wrapper(self, request, id=None):
        if 'HTTP_AUTHORIZATION' not in request.META:
            response = Response({'message': 'Token not provided in the header'})
            response.status_code = 400
            return response
        token = request.META['HTTP_AUTHORIZATION']
        user_id = EncodeDecodeToken.decode_token(token)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        if not User.objects.filter(id=user_id.get("user_id"), is_verified=True):
            response = Response({'message': 'User Does not exist or Not Verified'})
            response.status_code = 404
            return response
        request.data.update({'user_id': user_id.get("user_id")})
        if id is None:
            return function(self, request)
        else:
            return function(self, request, id)

    return wrapper


def is_superuser(function):
    """
    for checking user is super user or not
    :param function:
    :return: Response
    """

    def wrapper(self, request, id=None):
        user = User.objects.filter(id=request.data.get("user_id"), is_superuser=True)

        if not user:
            return Response(
                {
                    "message": "Only Admin and  Superuser Have the Access"
                }, status=status.HTTP_401_UNAUTHORIZED
            )
        if id is None:
            return function(self, request)
        else:
            return function(self, request, id)

    return wrapper
