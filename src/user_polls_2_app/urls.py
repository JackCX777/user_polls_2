from django.urls import path
from user_polls_2_app.views import (PollsListView,
                                    PollDetailView,
                                    CreatePollView,
                                    UpdatePollView,
                                    DeletePollView,
                                    CreatePollQuestionWithVariantsView,
                                    PollQuestionDetailView,
                                    UpdatePollQuestionView,
                                    DeletePollQuestionView,
                                    PollsAssignedToUserListView,
                                    CurrentQuestionRedirectView,
                                    UserAnswerCreateView,
                                    CompletedPollsListView,
                                    PollResultsView,)


urlpatterns = [
    path('', PollsListView.as_view(), name='home'),
    path('polls/create/', CreatePollView.as_view(), name='poll_create'),
    path('polls/', PollsListView.as_view(), name='polls_list'),
    path('poll/<int:pk>/', PollDetailView.as_view(), name='poll_detail'),
    path('poll/<int:pk>/update/', UpdatePollView.as_view(), name='poll_update'),
    path('poll/<int:pk>/delete/', DeletePollView.as_view(), name='poll_delete'),
    path('poll/<int:pk>/question/create/', CreatePollQuestionWithVariantsView.as_view(), name='question_create'),
    path('poll/<int:pk>/question/<int:q_id>/', PollQuestionDetailView.as_view(), name='question_detail'),
    path('poll/<int:pk>/question/<int:q_id>/update/', UpdatePollQuestionView.as_view(), name='question_update'),
    path('poll/<int:pk>/question/<int:q_id>/delete/', DeletePollQuestionView.as_view(), name='question_delete'),
    path('polls/assigned_to_user/', PollsAssignedToUserListView.as_view(), name='polls_assigned_to_user'),
    path('poll/<int:pk>/question/redirect', CurrentQuestionRedirectView.as_view(), name='next_question_redirect'),
    path(
        'poll/<int:pk>/question/<int:q_id>/user_answer_create/',
        UserAnswerCreateView.as_view(),
        name='user_answer_create'
    ),
    path('polls/completed/', CompletedPollsListView.as_view(), name='completed_polls'),
    path('poll/<int:pk>/results', PollResultsView.as_view(), name='poll_results'),
]
