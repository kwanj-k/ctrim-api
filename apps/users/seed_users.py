"""Module for interacting with goauth api users endpoint."""

import json
from os import getcwd

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import User
from apps.helpers.get_data import get_users
from apps.users.serializers import UserSerializer
from apps.helpers.get_response import get_seed_response


class SeedUsersViewSet(ViewSet):
    """ API users class."""

    def get_users(self, request):
        """Fetch users from the Goauth API and write to a json file."""

        goauth_users = get_users(request)

        users_file = open(
            f'{getcwd()}/apps/static/goauth_api_users.json', 'w+')

        users = []
        existing_users = User.objects.all().values_list('email', flat=True)
        for user in goauth_users:
            if user.get('Email') in existing_users:
                continue
            user_info = {
                'username': user.get('Nickname'),
                'email': user.get('Email'),
            }
            users.append(user_info)

        users_file.write(json.dumps({'users': users}))

        return Response(
            {
                'status': 'success',
                'message': f'{len(users)} new goauth user(s) fetched'},
            status=status.HTTP_200_OK)

    def seed_users(self, request):
        """Save users to DB from JSON file"""
        try:
            users = open(
                f'{getcwd()}/apps/static/goauth_api_users.json', 'r').read()
            users = json.loads(users)['users']
            user_list = []

            for user in users:
                serializer = UserSerializer(
                    data=user, context={'request': request, 'user': user})
                if serializer.is_valid():
                    serializer.save()
                    user_list.append(user)

                if len(user_list) == 900:
                    not_seeded = [
                        usr for usr in users if usr not in user_list]
                    users_file = open(
                        f'{getcwd()}/apps/static/goauth_api_users.json', 'w+')
                    users_file.write(json.dumps({'users': not_seeded}))

                    return Response({
                        "status": "success",
                        "message": "The seeding limit for a single request has "
                                   "been reached(900). Seed again to continue "
                                   "adding users."
                    }, status=status.HTTP_201_CREATED)

            return Response(*get_seed_response(len(user_list), 'users'))

        except FileNotFoundError:
            return Response({
                "status": "error",
                "error": "users_not_found.",
                "message": "Users file not found. Please retrieve "
                           "Goauth Users first"
            }, status=status.HTTP_400_BAD_REQUEST)
