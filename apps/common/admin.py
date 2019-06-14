import os
from django.db.models.signals import post_migrate
from apps.users.models import User


def add_initial_super_admin(sender, **kwargs):
    if User.objects.count() == 0:
        print('Creating a superAdmin')
        User.objects.create_superuser(
            username=os.getenv('SUPER_NAME'),
            email=os.getenv('SUPER_EMAIL'),
            password=os.getenv('SUPER_PASS')
        )


post_migrate.connect(add_initial_super_admin)
