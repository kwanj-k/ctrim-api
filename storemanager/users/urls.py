from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupAPIView.as_view(),name='signup'),
    path('login/',views.Login.as_view(),name='login'),
]
