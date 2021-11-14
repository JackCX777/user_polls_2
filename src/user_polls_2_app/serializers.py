from rest_framework import serializers
from django.db import IntegrityError, transaction
from .models import Poll, PollQuestion, PollAnswer, PollsAssignedToUser, UserAnswer

# from rest_framework.utils import model_meta


class AnswersSerializer(serializers.ModelSerializer):
    """
    Answers serializer
    """

    class Meta:
        model = PollAnswer
        fields = ('text', )


class QuestionsListSerializer(serializers.ModelSerializer):
    """
    Questions list serializer
    """
    poll = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = PollQuestion
        fields = ('id', 'poll', 'type', 'text', )


class QuestionDetailSerializer(serializers.ModelSerializer):
    """
    Questions serializer
    """
    answer_variants = AnswersSerializer(many=True)

    class Meta:
        model = PollQuestion
        fields = ('poll', 'type', 'text', 'answer_variants', )

    def create(self, validated_data):
        answers = validated_data.pop('answer_variants')
        instance = PollQuestion.objects.create(**validated_data)

        for answer in answers:
            answer['question'] = instance
            PollAnswer.objects.create(**answer)

        return instance

    def update(self, instance, validated_data):
        answers = validated_data.pop('answer_variants')

        # instance.poll = validated_data.get('poll', instance.poll)
        instance.type = validated_data.get('type', instance.type)
        instance.text = validated_data.get('text', instance.text)

        new_answers_list = []
        for index, answer in enumerate(answers):
            new_answers_list.append(PollAnswer(question=instance, text=answer.get('text'), _order=index))
        try:
            with transaction.atomic():
                PollAnswer.objects.filter(question_id=instance.id).delete()
                PollAnswer.objects.bulk_create(new_answers_list)
        # If transaction failed
        except IntegrityError:
            print('There was an error saving answer options')

        return instance


class PollSerializer(serializers.ModelSerializer):
    """
    Poll list, create, update or destroy serializer
    """

    class Meta:
        model = Poll
        fields = '__all__'


class PollRetrieveSerializer(serializers.ModelSerializer):
    """
    Poll retrieve serializer
    """
    questions = QuestionsListSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'name', 'description', 'date_start', 'date_finish', 'is_active', 'questions', )


class PollsAssignedToUserSerializer(serializers.ModelSerializer):
    """
    Polls assigned to users serializer
    """
    poll = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = PollsAssignedToUser
        fields = ('poll', )


class UserChoiceAnswerSerializer(serializers.ModelSerializer):
    """
    User choice answers serializer
    """
    question = QuestionDetailSerializer(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ('question', 'choice_answer', )


class UserTextAnswerSerializer(serializers.ModelSerializer):
    """
    User text answers serializer
    """
    question = QuestionDetailSerializer(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ('text_answer', )





# class QuestionsSerializer(serializers.ModelSerializer):
#     """
#         Questions serializer
#     """
#     poll = serializers.SlugRelatedField(slug_field='name', read_only=True)
#
#     class Meta:
#         model = PollQuestion
#         fields = ('poll', 'type', 'text', )
#         # fields = '__all__'





# class QuestionsSerializer(serializers.ModelSerializer):
#     """
#         Questions list serializer
#     """
#     poll = serializers.SlugRelatedField(slug_field='name', read_only=True)
#
#     class Meta:
#         model = PollQuestion
#         fields = ('poll', 'type', 'text', )




#
#
# class PollsSerializer(serializers.ModelSerializer):
#     """
#         Polls list or create serializer
#     """
#
#     class Meta:
#         model = Poll
#         fields = '__all__'
#
#
# class OptionCreateSerializer(serializers.ModelSerializer):
#     """
#         Create option
#     """
#
#     class Meta:
#         model = PollAnswer
#         fields = ('text', )
#
#
# class QuestionAndOptionsCreateSerializer(serializers.ModelSerializer):
#     """
#         Create Question with options
#     """
#
#     answer_variants = OptionCreateSerializer(many=True)
#
#     class Meta:
#         model = PollQuestion
#         fields = '__all__'



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