from rest_framework import serializers
from .models import Poll, PollQuestion, PollAnswer


class PollsSerializer(serializers.ModelSerializer):
    """
        Polls list or create serializer
    """

    class Meta:
        model = Poll
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    """
        Poll retrieve, update or destroy serializer
    """

    class Meta:
        model = Poll
        fields = '__all__'


class OptionCreateSerializer(serializers.ModelSerializer):
    """
        Create option
    """

    class Meta:
        model = PollAnswer
        fields = ('text', )


class QuestionAndOptionsCreateSerializer(serializers.ModelSerializer):
    """
        Create Question with options
    """

    answer_variants = OptionCreateSerializer(many=True)

    class Meta:
        model = PollQuestion
        fields = '__all__'



'''
{
q: '',
type: '',
answers: [
    {
    text: ''
    },
    {
    }
]
}


'''


#####################

# Using APIView or simple generics:


# class PollCreateSerializer(serializers.ModelSerializer):
#     """
#         Create poll
#     """
#
#     class Meta:
#         model = Poll
#         fields = '__all__'
#
#
# class PollsListSerializer(serializers.ModelSerializer):
#     """
#         Polls list
#     """
#
#     class Meta:
#         model = Poll
#         fields = ('name', )
#
#
# class PollDetailSerializer(serializers.ModelSerializer):
#     """
#         Poll detail
#     """
#
#     class Meta:
#         model = Poll
#         fields = '__all__'
#
#
# class PollUpdateSerializer(serializers.ModelSerializer):
#     """
#         Poll update
#     """
#
#     class Meta:
#         model = Poll
#         fields = '__all__'