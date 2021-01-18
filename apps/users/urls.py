from django.urls import path
from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import seed_users


app_name = "authentication"

seed_users = seed_users.SeedUsersViewSet.as_view({
    'get': 'get_users',
    'post': 'seed_users',
})

urlpatterns = format_suffix_patterns([
    url(r'^users/seed/$', seed_users, name='seed-users'),
    url(r'^users/goauth_api/$', seed_users, name='goauth-users'),
])
