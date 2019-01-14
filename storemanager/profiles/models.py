from django.db import models
from django.urls import reverse
from common.models import AbstractBase
from users.models import User
from django.db.models.signals import post_save
# Create your models here.


class UserProfile(AbstractBase):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profiles')
    bio = models.CharField(default='',max_length=255)
    slug = models.SlugField(null=True,blank=True)


    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse('details', kwargs={self.user:self.slug})


def s_post_save_receiver(sender,instance,*args, **kwargs):
	if kwargs['created']:
		instance.user_profile = UserProfile.objects.create(user=instance)

post_save.connect(s_post_save_receiver, sender=User)
