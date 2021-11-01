from django.urls import path, include
from . import api_views


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    # path('polls/create/', api_views.PollCreateAPIView.as_view(), name='api_poll_create'),
    # path('polls/', api_views.PollsListAPIView.as_view(), name='api_polls_list'),
    # path('poll/<int:pk>/', api_views.PollDetailAPIView.as_view(), name='api_poll_detail'),
    # path('poll/<int:pk>/update/', api_views.PollUpdateAPIView.as_view(), name='api_poll_update'),
    # path('poll/<int:pk>/delete/', api_views.PollDeleteAPIView.as_view(), name='api_poll_delete'),

    path('polls/', api_views.PollsListCreateAPIView.as_view(), name='api_poll_list_create'),
    path('poll/<int:pk>/', api_views.PollsRetrieveUpdateDestroyAPIView.as_view(), name='api_poll_rud'),
]
