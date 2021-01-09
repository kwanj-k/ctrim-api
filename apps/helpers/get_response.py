"""Get response."""

# rest_framework
from rest_framework import status

# constants
from apps.constants import ERROR_MESSAGES


def get_seed_response(num, record_type):
    """Gets corresponding seed response"""

    msg = f'No new {record_type} added. ' \
          f'Fetched {record_type} have already been saved.'
    status_code = status.HTTP_200_OK
    if num:
        msg = f'Successfully added {num} {record_type}'
        status_code = status.HTTP_201_CREATED
    return {
        'status': 'success',
        'message': msg
    }, status_code


def get_response(**kwargs):
    """Creates response body"""

    msg_type = kwargs.get('res_type', 'error')
    response = {'status': msg_type}
    if msg_type == 'error':
        error_key = kwargs.get('error_key')
        error = ERROR_MESSAGES.get(error_key)
        format_str = kwargs.get('format_str')
        body = {
            'error': error[0].format(format_str),
            'message': error[1].format(format_str),
        }
    else:
        body = {'data': kwargs.get('data')}
    response.update(body)

    return response
