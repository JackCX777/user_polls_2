from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth import views as auth_views
from django import views
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from custom_user_app.forms import (CustomUserLoginForm,
                                   CustomUserCreationForm,
                                   CustomUserProfileForm,
                                   CustomUserChangePasswordForm)


class CustomUserLoginView(auth_views.LoginView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('home')
    template_name = 'custom_user_app/user_login.html'


class CustomUserLogoutView(auth_views.LogoutView):
    next_page = 'user_login'
    template_name = 'custom_user_app/user_logout.html'


class CustomUserCreationView(SuccessMessageMixin, views.generic.CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_login')
    success_message = 'Your profile has been successfully created'
    template_name = 'custom_user_app/user_registration.html'


class CustomUserUpdateView(views.generic.UpdateView):
    model = get_user_model()
    form_class = CustomUserProfileForm
    pk_url_kwarg = 'profile_id'
    template_name = 'custom_user_app/user_profile.html'


class CustomUserPasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    model = get_user_model()
    form_class = CustomUserChangePasswordForm
    pk_url_kwarg = 'profile_id'
    success_message = 'The password has been successfully changed'
    template_name = 'custom_user_app/user_change_password.html'


class CustomUserPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    model = get_user_model()
    pk_url_kwarg = 'profile_id'
    template_name = 'custom_user_app/user_password_change_done.html'
