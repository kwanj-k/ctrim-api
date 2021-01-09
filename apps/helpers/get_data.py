"""Helper function to query Goauth API."""


from os import getenv
import requests

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from apps.helpers.auth import get_token, decode_token


def get_source_details(request, source, url_suffix=''):
    """Gets metadata required for a specified external api."""

    token = get_token(request._request)
    decoded_token = decode_token(token)
    base_api = getattr(settings, 'GOAUTH_API')
    header = {'Authorization': f'Bearer {token[7:]}'}
    source_mapper = {
        'goauth_users': (base_api + url_suffix, header),
    }
    return source_mapper[source]



def get_data(request, source='goauth', url_suffix='', **kwargs):
    """Get data from external API."""

    url, headers = get_source_details(request, source, url_suffix)

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        data = {
            'status': 'error',
            'error': f'{source}_api_error',
            'message': response.json()
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response.json()


def get_users(request, source='goauth_users'):
    """"Retrieves all users from the Goauth API"""
    
    users = []
    url = f'/users/'
    user_data = get_data(request, source, url)
    users.extend(user_data)
    return users
