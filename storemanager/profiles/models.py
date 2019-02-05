from django.db import models
from common.models import AbstractBase
from django.db.models.signals import post_save

# Third-party imports
from cloudinary.models import CloudinaryField

# Local imports
from users.models import User
from storemanager.settings import AUTH_USER_MODEL


class UserProfile(AbstractBase):
        user = models.OneToOneField(AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='profiles')
        image = CloudinaryField('image', default='')
        bio = models.TextField(null=True, blank=True, max_length=255)

        @property
        def username(self):
                return self.user

        def __str__(self):
                return str(self.user)


def create_profile_post_receiver(sender, instance, *args, **kwargs):
    if kwargs['created']:
        instance.user_profile = UserProfile.objects.create(user=instance)


post_save.connect(create_profile_post_receiver, sender=User)
