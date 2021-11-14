from datetime import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, renderers
from .models import Poll, PollQuestion, PollAnswer, PollsAssignedToUser, UserAnswer
from .serializers import (
    # PollCreateSerializer,
    # PollsListSerializer,
    # PollDetailSerializer,
    # PollUpdateSerializer,
    # PollsSerializer,
    PollSerializer,
    # QuestionAndOptionsCreateSerializer,
    # QuestionsWithAnswersSerializer,
    # QuestionsSerializer,
    QuestionsListSerializer,
    QuestionDetailSerializer,
    PollRetrieveSerializer,
    PollsAssignedToUserSerializer,
    UserChoiceAnswerSerializer,
    UserTextAnswerSerializer,
)
from .services import PaginationPolls, AvailablePollsMixin
from .mixins import MixedSerializer


class PollViewSet(MixedSerializer, viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    serializer_classes_by_action = {
        # 'list': QuestionsSerializer,
        'retrieve': PollRetrieveSerializer
    }
    # pagination_class = PaginationPolls


class QuestionViewSet(MixedSerializer, viewsets.ModelViewSet):
    queryset = PollQuestion.objects.all()
    serializer_class = QuestionDetailSerializer

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         serializer_class = QuestionsSerializer
    #     elif self.action == 'retrieve':
    #         serializer_class = QuestionsWithAnswersSerializer
    #     return serializer_class

    # Using custom mixin instead if in get_serializer_class()
    serializer_classes_by_action = {
        'list': QuestionsListSerializer,
        # 'retrieve': QuestionsWithAnswersSerializer
    }


class PollsAssignedToUserViewSet(MixedSerializer, AvailablePollsMixin, viewsets.ModelViewSet):
    # queryset = PollsAssignedToUser.objects.filter()
    serializer_class = PollsAssignedToUserSerializer
    serializer_classes_by_action = {}
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.get_personalised_polls()


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()

    def get_question(self):
        return get_object_or_404(PollQuestion, id=self.kwargs.get('q_id'))

    def get_serializer_class(self):
        question = self.get_question()
        if question.type == 3:
            return UserTextAnswerSerializer
        else:
            return UserChoiceAnswerSerializer

    def perform_create(self, serializer):
        serializer.data.update({'question': self.get_question().id})
        if self.request.user.is_authenticated:
            serializer.data.update({'user': self.request.user, 'anonymous_user_id': None})
        else:
            serializer.data.update({'user': None, 'anonymous_user_id': self.request.session.session_key})













# class PollReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


# class PollAndQuestionViewSet(viewsets.ModelViewSet):
#     def list(self, request, *args, **kwargs):
#         queryset = Poll.objects.all()
#         serializer = PollSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         print(request.data)



# class QuestionViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = PollQuestion.objects.all()
#         serializer = QuestionsSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, *args, **kwargs):
#         queryset = PollQuestion.objects.all()
#         question = get_object_or_404(queryset, pk=kwargs.get('pk'))
#         serializer = QuestionsSerializer(question)
#         return Response(serializer.data)


# class CreateQuestionAndOptionsAPIView(generics.CreateAPIView):
#     """
#         Question and options create
#     """
#
#     def get_queryset(self):
#         queryset = PollQuestion.objects.all()
#         return queryset
#
#     def get_serializer_class(self):
#         serializer_class = QuestionAndOptionsCreateSerializer
#         return serializer_class


#####################

# def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)




#####################

# Using generics.ListCreateAPIView and generics.RetrieveUpdateDestroyAPIView


# class PollsListCreateAPIView(generics.ListCreateAPIView):
#     """
#         Polls list and create (generics.ListCreateAPIView)
#     """
#
#     queryset = Poll.objects.all()
#     serializer_class = PollsSerializer
#     pagination_class = PaginationPolls
#
#
# class PollsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """
#         Polls retrieve, update and destroy (generics.RetrieveUpdateDestroyAPIView)
#     """
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


#####################

# Using generics:


# class PollCreateAPIView(generics.CreateAPIView):
#     """
#         Create poll (generics.CreateAPIView)
#     """
#
#     serializer_class = PollCreateSerializer
#
#
# class PollsListAPIView(generics.ListAPIView):
#     """
#         Polls list (generics.ListAPIView)
#     """
#
#     queryset = Poll.objects.all()
#     serializer_class = PollsListSerializer
#     pagination_class = PaginationPolls
#
#
# class PollDetailAPIView(generics.RetrieveAPIView):
#     """
#         Poll detail (generics.RetrieveAPIView)
#     """
#
#     queryset = Poll.objects.all()
#     serializer_class = PollDetailSerializer
#
#
# class PollUpdateAPIView(generics.UpdateAPIView):
#     """
#         Poll update (generics.UpdateAPIView)
#     """
#
#     queryset = Poll.objects.all()
#     partial = True
#     serializer_class = PollUpdateSerializer
#
#
# class PollDeleteAPIView(generics.DestroyAPIView):
#     """
#         Poll delete (generics.DestroyAPIView)
#     """
#
#     queryset = Poll.objects.all()


#####################

# Using APIView:


# class PollCreateAPIView(APIView):
#     '''
#         Create poll (APIView)
#     '''
#
#     @swagger_auto_schema(responses={200: PollCreateSerializer()})
#     def post(self, request, *args, **kwargs):
#         poll = PollCreateSerializer(data=request.data)
#         if poll.is_valid():
#             poll.save()
#         return Response(status=201)


# class PollsListAPIView(APIView):
#     '''
#         Polls list (APIView)
#     '''
#
#     def get(self, request, *args, **kwargs):
#         polls = Poll.objects.all()
#         serializer = PollsListSerializer(polls, many=True)
#         return Response(serializer.data)


# class PollDetailAPIView(APIView):
#     '''
#         Poll detail (APIView)
#     '''
#
#     def get(self, request, *args, **kwargs):
#         poll = Poll.objects.get(id=kwargs.get('pk'))
#         serializer = PollDetailSerializer(poll)
#         return Response(serializer.data)
