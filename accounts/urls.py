from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]