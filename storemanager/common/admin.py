from django.contrib import admin
from django.apps import apps
from django.db.models.signals import post_migrate
from users.models import User

def add_initial_super_admin(sender,**kwargs):
    if User.objects.count() == 0:
        print('Creating a superAdmin')
        User.objects.create_superuser(
            username='kwanj-k',
            email='mwangikwanj@gmail.com',
            password='zeusK1'
        )

post_migrate.connect(add_initial_super_admin)
