from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from .models import Poll, PollQuestion, PollAnswer
from .serializers import (
    # PollCreateSerializer,
    # PollsListSerializer,
    # PollDetailSerializer,
    # PollUpdateSerializer,
    PollsSerializer,
    PollSerializer,
    QuestionAndOptionsCreateSerializer,
)
from .service import PaginationPolls


class PollsListCreateAPIView(generics.ListCreateAPIView):
    """
        Polls list and create generics.ListCreateAPIView)
    """

    queryset = Poll.objects.all()
    serializer_class = PollsSerializer
    pagination_class = PaginationPolls


class PollsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        Polls retrieve, update and destroy (generics.RetrieveUpdateDestroyAPIView)
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer



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
