from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Poll(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_start = models.DateField(auto_now_add=True, null=False, blank=False, editable=False)
    date_finish = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('id', 'date_start', )
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('poll_detail', kwargs={'pk': self.pk})


class PollQuestion(models.Model):
    QUESTION_TYPES = (
        ('1', 'CheckBox'),
        ('2', 'Choice'),
        ('3', 'Text')
    )
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=255, blank=False, choices=QUESTION_TYPES)
    text = models.TextField(blank=False)

    class Meta:
        # ordering = ('poll',)
        order_with_respect_to = 'poll'
        verbose_name = 'PollQuestion'
        verbose_name_plural = 'PollQuestions'

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.poll_id, 'q_id': self.pk})


class PollAnswer(models.Model):
    question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE, related_name='answer_variants')
    text = models.CharField(max_length=255, blank=True)

    class Meta:
        # ordering = ('question',)
        order_with_respect_to = 'question'
        verbose_name = 'PollAnswer'
        verbose_name_plural = 'PollAnswers'

    def __str__(self):
        return self.text


class PollsAssignedToUser(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    anonymous_user_id = models.CharField(max_length=255, null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('poll',)
        verbose_name = 'PollsAssignedToUsers'
        verbose_name_plural = 'PollsAssignedToUsers'

    def __str__(self):
        return str(self.poll) + ' assigned to ' + str(self.user)


class UserAnswer(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user_id = models.CharField(max_length=255, null=True, blank=True, default=None)
    question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
    choice_answer = models.ForeignKey(PollAnswer, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(blank=False)

    class Meta:
        # ordering = ('question_id',)
        order_with_respect_to = 'question'
        verbose_name = 'UserAnswer'
        verbose_name_plural = 'UserAnswers'

    def __str__(self):
        if self.text_answer:
            return str(self.text_answer)
        else:
            return str(self.choice_answer)
