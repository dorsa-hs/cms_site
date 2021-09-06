from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm, EditAccountForm, PasswordChangingForm, CreateProfilePageForm, ProfileForm, \
    UserForm, EditProfilePageForm
from .models import UserProfile
from django.contrib.auth import login, get_user_model, authenticate, logout, forms
from django.contrib.auth.models import User
from django.views import generic


# Create your views here
def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        user_name = login_form.cleaned_data.get('user_name')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            login_form.add_error('user_name', 'کاربری با مشخصات وارد شده یافت نشد')

    context = {
        'login_form': login_form
    }
    return render(request, 'account/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    register_form = RegisterForm(request.POST or None)

    if register_form.is_valid():
        user_name = register_form.cleaned_data.get('user_name')
        password = register_form.cleaned_data.get('password')
        email = register_form.cleaned_data.get('email')
        User.objects.create_user(username=user_name, email=email, password=password)
        return redirect('/login')

    context = {
        'register_form': register_form
    }
    return render(request, 'account/register.html', context)


def log_out(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def user_account_main_page(request):
    user_id = request.user.id
    user_profile = UserProfile.objects.get(user_id=user_id)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'account/user_account_main.html', context)


# class ShowProfilePageView(generic.DetailView):
#     model = UserProfile
#     template_name = 'account/user_account_main.html'
#
#     def get_object(self, queryset=User.objects.all()):
#         print(self.kwargs)
#         user_id = self.kwargs.get("id")
#         user = get_object_or_404(User, id=user_id)
#         return user
#
#     def get_context_data(self, **kwargs):
#         print(self.kwargs)
#         context = super(ShowProfilePageView, self).get_context_data(**kwargs)
#         user_id = self.get_object().id
#         user_page = get_object_or_404(UserProfile, id=user_id)
#         context['user_profile'] = user_page
#         return context


class UserEditAccountView(generic.UpdateView):
    form_class = EditAccountForm
    template_name = 'account/edit_account.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    # form_class = forms.PasswordChangeForm
    success_url = reverse_lazy('password_success')
    template_name = 'account/change_password.html'


def password_success(request):
    return render(request, 'account/password_success.html')


@method_decorator(login_required, name='dispatch')
class EditProfilePageView(generic.UpdateView):
    model = UserProfile
    template_name = 'account/edit_profile.html'
    success_url = reverse_lazy('profile')
    fields = ['bio', 'avatar']

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CreateProfilePageView(generic.CreateView):
    model = UserProfile
    form_class = CreateProfilePageForm
    template_name = 'account/create_user_profile_page.html'
    success_url = reverse_lazy('profile')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
