from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_user, register, log_out, user_account_main_page, UserEditAccountView, PasswordsChangeView, \
    password_success, CreateProfilePageView, EditProfilePageView

urlpatterns = [
    path('login', login_user),
    path('register', register),
    path('log-out', log_out),
    path('profile', user_account_main_page, name='profile'),
    path('edit_account', UserEditAccountView.as_view(), name='edit_account'),
    path('edit_profile', EditProfilePageView.as_view(), name='edit_profile'),
    path('create-profile', CreateProfilePageView.as_view(), name='create_profile'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='account/change_password.html')),
    path('password/', PasswordsChangeView.as_view()),
    path('password_success', password_success, name='password_success'),
]
