"""Checks status of backend api."""


from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

class ApiStatusViewSet(ViewSet):
    """Status api viewset."""

    renderer_classes = (JSONRenderer,)

    def get_status(self, request):
        """
        Get the status of the API.

        If its successful, response payload with:
            - status: 200
            - data
        """
        data = {
            "status": "success",
            "message": "API works as expected."
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request):
        """
        Get welcome message.

        If its successful, response payload with:
            - status code: 200
            - message
        """
        data = {
            "status": "success",
            "message": "Welcome to the Ctrim API."
                       " For the API's  documentation, visit /api/docs/"
        }
        return Response(data, status=status.HTTP_200_OK)
