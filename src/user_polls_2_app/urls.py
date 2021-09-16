from django.urls import path
from user_polls_2_app.views import (PollsListView,
                                    PollDetailView,
                                    CreatePollView,
                                    UpdatePollView,
                                    DeletePollView,
                                    # CreateQuestionView,
                                    CreatePollQuestionWithVariantsView,
                                    PollQuestionDetailView,
                                    UpdatePollQuestionView,
                                    DeletePollQuestionView,)


urlpatterns = [
    path('', PollsListView.as_view(), name='home'),
    path('polls/', PollsListView.as_view(), name='polls_list'),
    path('polls/create/', CreatePollView.as_view(), name='poll_create'),
    path('poll<int:pk>/', PollDetailView.as_view(), name='poll_detail'),
    path('poll<int:pk>/update/', UpdatePollView.as_view(), name='poll_update'),
    path('poll<int:pk>/delete/', DeletePollView.as_view(), name='poll_delete'),
    path('poll<int:pk>/questions/create/', CreatePollQuestionWithVariantsView.as_view(), name='question_create'),
    path('poll<int:pk>/questions/<int:q_id>/', PollQuestionDetailView.as_view(), name='question_detail'),
    path('poll<int:pk>/questions/<int:q_id>/update/', UpdatePollQuestionView.as_view(), name='question_update'),
    path('poll<int:pk>/questions/<int:q_id>/delete/', DeletePollQuestionView.as_view(), name='question_delete'),
]
