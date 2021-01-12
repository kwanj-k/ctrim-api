""" Checks for resource existence"""
from rest_framework import status

from apps.helpers.save_serializer import save_serializer


def check_resource(model, model_serializer, pk, request, model_name):
    """
        returns a particular message for when resource exist or not.
    """
    try:
        resource = model.objects.get(pk=pk)
        if request.method == "GET":
            serializer = model_serializer(
                resource, context={'request': request})
            data = {
                'status': 'success',
                'data': serializer.data
            }
            return (data, status.HTTP_200_OK)
        serializer = model_serializer(
            resource, context={'request': request}, data=request.data, partial=True)
        if serializer.is_valid():
            data = save_serializer(serializer)
            return (data, status.HTTP_200_OK)
        data = {
            "status": "error",
            "error": "name is empty",
            "message": "Ensure the name is not empty"
        }
        return (data, status.HTTP_400_BAD_REQUEST)
    except model.DoesNotExist:
        data = {
            'status': 'error',
            'error': '{}_not_found.'.format(model_name),
            'message': 'Ensure the ID passed is of an existing {}.'.format(model_name)
        }
        return (data, status.HTTP_404_NOT_FOUND)


def resource_exists(model, pk):
    """Checks if resource exists."""

    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return False
