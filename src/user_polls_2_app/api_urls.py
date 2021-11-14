from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views


router = DefaultRouter()
# router.register(r'poll-read', api_views.PollReadOnlyViewSet)
# router.register(r'polls', api_views.PollViewSet)
# router.register(r'polls', api_views.PollAndQuestionViewSet, basename='pollssss')
# router.register(r'questions', api_views.QuestionViewSet)

polls_list = {
    'get': 'list',
    'post': 'create'
}

poll_detail = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
}


question_list = {
    'get': 'list',
    'post': 'create'
}

question_detail = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
}

urlpatterns = [
    # path('auth/', include('rest_framework.urls')),

    path('', include(router.urls)),
    path('polls/', api_views.PollViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('polls/<int:pk>/', api_views.PollViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # path('questions/', api_views.QuestionViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('poll/<int:pk>/question/create/', api_views.QuestionViewSet.as_view({'post': 'create'})),
    path('questions/', api_views.QuestionViewSet.as_view({'post': 'create'})),
    # path('poll/<int:pk>/question/<int:q_id>/', api_views.QuestionViewSet.as_view({
    path('questions/<int:pk>/', api_views.QuestionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('polls/assigned_to_user/', api_views.PollsAssignedToUserViewSet.as_view({'get': 'list'})),
    path('poll/<int:pk>/question/<int:q_id>/user_answers/',
         api_views.UserAnswerViewSet.as_view({'post': 'create'})
         ),

    # path('polls/', api_views.PollAndQuestionViewSet.as_view(polls_list), name='polls-list'),
    # path('polls/<int:pk>/', api_views.PollAndQuestionViewSet.as_view(polls_detail), name='polls-detail'),
    # path('questions', api_views.QuestionViewSet.as_view({'get': 'list'})),
    # path('question/<int:pk>/', api_views.QuestionViewSet.as_view({'get': 'retrieve'})),

    # Using generics.ListCreateAPIView and generics.RetrieveUpdateDestroyAPIView
    # path('polls/', api_views.PollsListCreateAPIView.as_view(), name='api_poll_list_create'),
    # path('poll/<int:pk>/', api_views.PollsRetrieveUpdateDestroyAPIView.as_view(), name='api_poll_rud'),

    # Using APIView or generics
    # path('polls/create/', api_views.PollCreateAPIView.as_view(), name='api_poll_create'),
    # path('polls/', api_views.PollsListAPIView.as_view(), name='api_polls_list'),
    # path('poll/<int:pk>/', api_views.PollDetailAPIView.as_view(), name='api_poll_detail'),
    # path('poll/<int:pk>/update/', api_views.PollUpdateAPIView.as_view(), name='api_poll_update'),
    # path('poll/<int:pk>/delete/', api_views.PollDeleteAPIView.as_view(), name='api_poll_delete'),
]
