from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms


CustomUserModel = get_user_model()


class CustomUserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = CustomUserModel
        fields = '__all__'
