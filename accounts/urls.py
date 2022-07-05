from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', profile_user, name='dashboard'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset/', password_reset_request, name="password_reset"),
    path('edit_profile/', edit_profile, name='edit-profile')
]