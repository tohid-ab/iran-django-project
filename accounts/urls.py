from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', profile_user, name='dashboard'),
    # path(
    #     'reset_password/',
    #     auth_views.PasswordResetView.as_view(success_url=reverse_lazy('password_reset_done')),
    #     name='reset_password'
    # ),
    # path(
    #     'reset_password_sent/',
    #     auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
    #     name='password_reset_done'
    # ),
]