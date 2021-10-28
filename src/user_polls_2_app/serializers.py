from rest_framework import serializers
from .models import Poll


class PollCreateSerializer(serializers.ModelSerializer):
    '''
        Create poll
    '''

    class Meta:
        model = Poll
        fields = '__all__'


class PollsListSerializer(serializers.ModelSerializer):
    '''
        Polls list
    '''

    class Meta:
        model = Poll
        fields = ('name', )


class PollDetailSerializer(serializers.ModelSerializer):
    '''
        Poll detail
    '''

    class Meta:
        model = Poll
        fields = '__all__'
