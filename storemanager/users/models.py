from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from common.models import AbstractBase
from common.utils import unique_slug_generator
from django.urls import reverse

class MyUserManager(BaseUserManager):

    def create_user(self,username,email,password=None):
        phash = make_password(password)
        user = self.model(
            username=username,email=email,password=phash
        )
        user.save()
        return user

    def create_superuser(self,username,email,password):
        phash = make_password(password)
        user = self.model(
            username=username,email=email,password=phash
        )
        user.active = True
        user.deleted = False
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=25,unique=True)
    email = models.EmailField(max_length=40,unique=True)
    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    deleted = models.BooleanField(
        default=False,
        help_text='Toogle to prevent actual deletes'
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        app_label = 'users'

class UserProfile(AbstractBase):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(default='',max_length=255)
    slug = models.SlugField(null=True,blank=True)

    def get_absolute_url(self):
        return reverse('details', kwargs={self.user:self.slug})

def s_post_save_receiver(sender,instance,*args, **kwargs):
	if kwargs['created']:
		instance.user_profile = UserProfile.objects.create(user=instance)

def s_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

post_save.connect(s_post_save_receiver, sender=User)
pre_save.connect(s_pre_save_receiver, sender=UserProfile)

