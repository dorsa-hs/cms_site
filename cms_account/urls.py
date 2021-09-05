from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_user, register, log_out, user_account_main_page, edit_user_profile, UserEditView, PasswordsChangeView, password_success

urlpatterns = [
    path('login', login_user),
    path('register', register),
    path('log-out', log_out),
    path('user', user_account_main_page),
    # path('user/edit', edit_user_profile),
    # path('user/edit', edit_profile)
    path('edit_profile', UserEditView.as_view(), name='edit_profile'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='account/change_password.html')),
    path('password/', PasswordsChangeView.as_view()),
    path('password_success', password_success, name='password_success'),
]
