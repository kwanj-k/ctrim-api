from django.urls import path
from . import views


app_name = "authentication"
urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
]
