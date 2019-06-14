"""ctrim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

# set the title for the API.
schema_view = get_swagger_view(title="Ctrim API")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.stores.urls')),
    path('users/login', include('rest_framework.urls')),
    path('', schema_view),
]
