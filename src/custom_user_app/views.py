from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.views import
from custom_user_app.forms import CustomUserCreationForm


# class CustomUserCreationView