import os
from django.db.models.signals import post_migrate
from django.contrib import admin

from apps.users.models import User


class BaseAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(BaseAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['created_by'].initial = request.user
        return form

def add_initial_super_admin(sender, **kwargs):
    if User.objects.count() == 0:
        print('Creating a superAdmin')
        User.objects.create_superuser(
            username=os.getenv('SUPER_NAME'),
            email=os.getenv('SUPER_EMAIL'),
            password=os.getenv('SUPER_PASS')
        )


post_migrate.connect(add_initial_super_admin)
