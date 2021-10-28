from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms


# CustomUserModel = get_user_model()


class CustomUserLoginForm(auth_forms.AuthenticationForm):
    pass


class CustomUserCreationForm(auth_forms.UserCreationForm):
    # class Meta(auth_forms.UserCreationForm.Meta):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'contact',)


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'contact', 'date_joined', 'last_login')


class CustomUserChangePasswordForm(auth_forms.PasswordChangeForm):
    pass
