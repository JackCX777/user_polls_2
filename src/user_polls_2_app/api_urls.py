from django.urls import path, include
from . import api_views


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('polls/create/', api_views.PollCreateAPIView.as_view(), name='api_poll_create'),
    path('polls/', api_views.PollsListAPIView.as_view(), name='api_polls_list'),
    path('poll/<int:pk>/', api_views.PollDetailAPIView.as_view(), name='api_poll_detail'),

    # path('polls/create/test/', api_views.PollCreateView.as_view()),
]
