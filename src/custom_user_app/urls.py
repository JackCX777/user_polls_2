from django.urls import path
from custom_user_app.views import (CustomUserLoginView,
                                   CustomUserLogoutView,
                                   CustomUserCreationView,
                                   CustomUserUpdateView,
                                   CustomUserPasswordChangeView,
                                   CustomUserPasswordChangeDoneView)


urlpatterns = [
    path('login/', CustomUserLoginView.as_view(), name='user_login'),
    path('logout/', CustomUserLogoutView.as_view(), name='user_logout'),
    path('registration/', CustomUserCreationView.as_view(), name='user_registration'),
    path('profile/<int:profile_id>', CustomUserUpdateView.as_view(), name='user_profile'),
    path('password_change/<int:profile_id>', CustomUserPasswordChangeView.as_view(), name='user_password_change'),
    path('password_change_done/<int:profile_id>', CustomUserPasswordChangeDoneView.as_view(),
         name='password_change_done'),
]
