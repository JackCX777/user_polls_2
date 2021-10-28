from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, RedirectView
from django.urls import reverse_lazy, reverse
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.db.models import Q
from django.urls import resolve
from django.db.models import ObjectDoesNotExist
from user_polls_2_app.models import Poll, PollQuestion, PollAnswer, PollsAssignedToUser, UserAnswer
from user_polls_2_app.forms import (PollModelForm,
                                    QuestionModelForm,
                                    PollAnswerFormSet,
                                    UserAnswerCreateForm,)


class SessionRequiredMixin:
    def get(self, request, *args, **kwargs):
        if not self.request.session.session_key:
            self.request.session.create()
            print('session_key now is', self.request.session.session_key)
        return super().get(request, *args, **kwargs)


class PollsListView(SessionRequiredMixin, ListView):
    model = Poll
    paginate_by = 5
    template_name = 'user_polls_2_app/polls_list.html'


class CreatePollView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('user_polls_2_app.add_poll',)
    queryset = Poll.objects.all()
    form_class = PollModelForm
    success_message = 'The poll has been created'
    template_name = 'user_polls_2_app/poll_create.html'

    def update_polls_assigned_to_users(self):
        if self.object.is_active:
            users_set = set()
            for poll_assigned_to_user in PollsAssignedToUser.objects.all():
                users_set.add(poll_assigned_to_user.user)
            users_list = list(users_set)
            new_assigned_polls_list = []
            for poll_user in users_list:
                if not PollsAssignedToUser.objects.filter(Q(poll=self.object) & Q(user=poll_user)).exists():
                    new_assigned_polls_list.append(
                        PollsAssignedToUser(poll=self.object, user=poll_user, is_active=True)
                    )
            PollsAssignedToUser.objects.bulk_create(new_assigned_polls_list)

    def get_success_url(self):
        self.update_polls_assigned_to_users()
        return reverse('question_create', kwargs={'pk': self.object.id})


class PollDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('user_polls_2_app.view_poll', 'user_polls_2_app.view_pollquestion',)
    model = Poll
    template_name = 'user_polls_2_app/poll_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        context['question_list'] = self.object.questions.all()
        return context


class UpdatePollView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('user_polls_2_app.change_poll',)
    queryset = Poll.objects.all()
    form_class = PollModelForm
    success_message = 'The poll has been updated'
    template_name = 'user_polls_2_app/poll_update.html'

    def update_polls_assigned_to_users(self):
        if self.object.is_active:
            users_set = set()
            for poll_assigned_to_user in PollsAssignedToUser.objects.all():
                users_set.add(poll_assigned_to_user.user)
            users_list = list(users_set)
            new_assigned_polls_list = []
            for poll_user in users_list:
                if not PollsAssignedToUser.objects.filter(Q(poll=self.object) & Q(user=poll_user)).exists():
                    new_assigned_polls_list.append(
                        PollsAssignedToUser(poll=self.object, user=poll_user, is_active=True)
                    )
            PollsAssignedToUser.objects.bulk_create(new_assigned_polls_list)
        else:
            PollsAssignedToUser.objects.filter(poll=self.object).delete()

    def get_success_url(self):
        self.update_polls_assigned_to_users()
        return self.object.get_absolute_url()


class DeletePollView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = ('user_polls_2_app.delete_poll',)
    queryset = Poll.objects.all()
    success_url = reverse_lazy('polls_list')
    success_message = 'The poll has been deleted'
    template_name = 'user_polls_2_app/poll_delete.html'


class CreatePollQuestionWithVariantsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('user_polls_2_app.add_pollquestion', 'user_polls_2_app.add_pollanswer',)
    context = {}
    template_name = 'user_polls_2_app/question_create.html'

    def get(self, request, *args, **kwargs):
        self.context['pk'] = self.kwargs.get('pk')
        self.context['poll_object'] = get_object_or_404(Poll, id=self.kwargs.get('pk'))
        self.context['question_form'] = QuestionModelForm(prefix='question')
        self.context['answer_formset'] = PollAnswerFormSet(prefix='answer')
        return render(request, template_name=self.template_name, context=self.context)

    def create_questions(self):
        self.question_object = self.question_form_instance.save(commit=False)
        self.question_object.poll_id = self.kwargs.get('pk')
        self.question_object.save()
        if self.question_object.type != '3':
            return self.create_answers()

    def create_answers(self):
        new_answers_list = []
        for index, answer_form in enumerate(self.answer_formset):
            new_answers_list.append(
                PollAnswer(question=self.question_object, text=answer_form.cleaned_data.get('text'), _order=index)
            )
        PollAnswer.objects.bulk_create(new_answers_list)

    def post(self, request, *args, **kwargs):
        self.context['poll_object'] = get_object_or_404(Poll, id=self.kwargs.get('pk'))
        self.question_form_instance = QuestionModelForm(request.POST, prefix='question')
        self.answer_formset = PollAnswerFormSet(request.POST, prefix='answer')

        if self.question_form_instance.is_valid() and self.answer_formset.is_valid():
            self.create_questions()
        return redirect(to=reverse('poll_detail', kwargs={'pk': self.kwargs.get('pk')}))


class PollQuestionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('user_polls_2_app.view_pollquestion', 'user_polls_2_app.view_pollanswer',)
    model = PollQuestion
    pk_url_kwarg = 'q_id'
    template_name = 'user_polls_2_app/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PollQuestionDetailView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        context['q_id'] = self.kwargs.get('q_id')
        context['answer_variants'] = self.object.answer_variants.all()
        return context


class UpdatePollQuestionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'user_polls_2_app.change_pollquestion',
        'user_polls_2_app.add_pollanswer',
        'user_polls_2_app.change_pollanswer',
    )
    context = {}
    template_name = 'user_polls_2_app/question_update.html'

    def get(self, request, *args, **kwargs):
        self.context['pk'] = self.kwargs.get('pk')
        self.context['q_id'] = self.kwargs.get('q_id')

        self.context['question_object'] = get_object_or_404(PollQuestion, id=self.kwargs.get('q_id'))
        question_data = {
            'type': self.context.get('question_object').type,
            'text': self.context.get('question_object').text
        }
        self.context['question_form'] = QuestionModelForm(initial=question_data, prefix='question')

        answers_object_list = PollAnswer.objects.filter(question=self.context.get('question_object'))
        answers_data = [{'text': answer.text} for answer in answers_object_list]
        self.context['answer_formset'] = PollAnswerFormSet(initial=answers_data, prefix='answer')
        return render(request=request, template_name=self.template_name, context=self.context)

    def update_question(self):
        self.question_object.type = self.question_form_instance.cleaned_data.get('type')
        self.question_object.text = self.question_form_instance.cleaned_data.get('text')
        self.question_object.save()
        if self.question_object.type != '3':
            self.update_answers()

    def update_answers(self):
        new_answers_list = []
        for index, answer_form in enumerate(self.answer_formset):
            new_answers_list.append(
                PollAnswer(question=self.question_object, text=answer_form.cleaned_data.get('text'), _order=index)
            )
        try:
            with transaction.atomic():
                PollAnswer.objects.filter(question=self.question_object).delete()
                PollAnswer.objects.bulk_create(new_answers_list)
        # If transaction failed
        except IntegrityError:
            messages.error(self.request, 'There was an error saving answer options')

    def post(self, request, *args, **kwargs):
        self.question_object = get_object_or_404(PollQuestion, id=self.kwargs.get('q_id'))
        self.question_form_instance = QuestionModelForm(request.POST, prefix='question')
        self.answer_formset = PollAnswerFormSet(request.POST, prefix='answer')

        if self.question_form_instance.is_valid() and self.answer_formset.is_valid():
            self.update_question()
        return redirect(to=reverse('question_detail', kwargs={'pk': self.kwargs.get('pk'),
                                                              'q_id': self.kwargs.get('q_id')}))


class DeletePollQuestionView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('user_polls_2_app.delete_pollquestion',)
    model = PollQuestion
    pk_url_kwarg = 'q_id'
    template_name = 'user_polls_2_app/question_delete.html'

    def get_success_url(self):
        return reverse('poll_detail', kwargs={'pk': self.kwargs.get('pk')})


class PollsAssignedToUserListView(SessionRequiredMixin, ListView):
    template_name = 'user_polls_2_app/polls_assigned_to_user.html'

    def update_polls(self):
        spoilt_polls = Poll.objects.filter(Q(is_active=True) & Q(date_finish__lt=datetime.now()))
        for spoilt_poll in spoilt_polls:
            polls_for_editing = PollsAssignedToUser.objects.filter(poll_id=spoilt_poll.id)
            for poll in polls_for_editing:
                poll.is_active = False
                poll.save()

    def get_polls_for_new_user(self):
        polls = Poll.objects.filter(is_active=True)
        # polls_assigned_to_user_list = []
        if self.request.user.is_authenticated:
            for poll in polls:
                # polls_assigned_to_user_list.append(
                #     PollsAssignedToUser(poll=poll, user=self.request.user, anonymous_user_id=None, is_active=True)
                # )
                # PollsAssignedToUser.objects.bulk_create(polls_assigned_to_user_list)
                # something wrong with bulk create
                p = PollsAssignedToUser(poll=poll, user=self.request.user, anonymous_user_id=None, is_active=True)
                p.save()
            return PollsAssignedToUser.objects.filter(user=self.request.user)
        else:
            for poll in polls:
                # polls_assigned_to_user_list.append(
                #     PollsAssignedToUser(poll=poll, anonymous_user_id=self.request.session.session_key,
                #                         is_active=True)
                # )
                # PollsAssignedToUser.objects.bulk_create(polls_assigned_to_user_list)
                # something wrong with bulk create
                p = PollsAssignedToUser(poll=poll, anonymous_user_id=self.request.session.session_key, is_active=True)
                p.save()
            return PollsAssignedToUser.objects.filter(anonymous_user_id=self.request.session.session_key)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = PollsAssignedToUser.objects.filter(user=self.request.user)
            if not queryset:
                if self.request.user.groups.filter(name='Poll users').exists():
                    queryset = self.get_polls_for_new_user()
                else:
                    messages.error(self.request, 'You are not allowed to take polls')
        else:
            queryset = PollsAssignedToUser.objects.filter(anonymous_user_id=self.request.session.session_key)
            if not queryset:
                queryset = self.get_polls_for_new_user()
        self.update_polls()
        return queryset.filter(is_active=True)


class CurrentQuestionRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        poll = Poll.objects.get(id=self.kwargs.get('pk'))
        poll_question_order = poll.get_pollquestion_order()
        if self.request.user.is_authenticated:
            user_answers_list = list(
                UserAnswer.objects.filter(Q(user=self.request.user) & Q(question__poll_id=self.kwargs.get('pk')))
            )
        else:
            user_answers_list = list(
                UserAnswer.objects.filter(
                    Q(anonymous_user_id=self.request.session.session_key) & Q(question__poll_id=self.kwargs.get('pk'))
                )
            )
        if user_answers_list:
            last_question_id = user_answers_list[-1].question_id
            last_question = PollQuestion.objects.get(id=last_question_id)
            try:
                current_question_id = last_question.get_next_in_order().id
            except ObjectDoesNotExist as e:
                return reverse('polls_assigned_to_user')
        else:
            current_question_id = poll_question_order[0]
        return reverse('user_answer_create', kwargs={'pk': self.kwargs.get('pk'), 'q_id': current_question_id})


class UserAnswerCreateView(SessionRequiredMixin, View):
    context = {}
    template_name = 'user_polls_2_app/user_answer_create.html'

    def get(self, request, *args, **kwargs):
        self.context['poll'] = get_object_or_404(Poll, id=self.kwargs.get('pk'))
        try:
            if self.request.user.is_authenticated:
                self.context['poll_assigned_to_user'] = PollsAssignedToUser.objects.get(
                    poll_id=self.kwargs.get('pk'), user=self.request.user
                )
            else:
                self.context['poll_assigned_to_user'] = PollsAssignedToUser.objects.get(
                    poll_id=self.kwargs.get('pk'), anonymous_user_id=self.request.session.session_key
                )
        except ObjectDoesNotExist as e:
            print(e)
        self.context['question'] = get_object_or_404(PollQuestion, id=self.kwargs.get('q_id'))
        self.context['answers_object_list'] = PollAnswer.objects.filter(question_id=self.kwargs.get('q_id'))
        self.custom_initial_params = {
            'queryset': self.context.get('answers_object_list'),
            'question_type': self.context.get('question').type,
        }
        self.context['form'] = UserAnswerCreateForm(custom_initial_params=self.custom_initial_params)
        return render(request=request, template_name=self.template_name, context=self.context)

    def save_user_answer(self, data):
        if self.custom_initial_params.get('question_type') == '1':
            user_answers_list = []
            for index, answer in enumerate(data.get('user_answers')):
                if self.request.user.is_authenticated:
                    user_answer = UserAnswer(
                        user=self.request.user,
                        anonymous_user_id=None,
                        question_id=self.kwargs.get('q_id'),
                        choice_answer=answer,
                        _order=index
                    )
                else:
                    user_answer = UserAnswer(
                        user=None,
                        anonymous_user_id=self.request.session.session_key,
                        question_id=self.kwargs.get('q_id'),
                        choice_answer=answer,
                        _order=index
                    )
                user_answers_list.append(user_answer)
            UserAnswer.objects.bulk_create(user_answers_list)
        elif self.custom_initial_params.get('question_type') == '2':
            if self.request.user.is_authenticated:
                user_answer = UserAnswer(
                    user=self.request.user,
                    anonymous_user_id=None,
                    question_id=self.kwargs.get('q_id'),
                    choice_answer=data.get('user_answers')
                )
            else:
                user_answer = UserAnswer(
                    user=None,
                    anonymous_user_id=self.request.session.session_key,
                    question_id=self.kwargs.get('q_id'),
                    choice_answer=data.get('user_answers')
                )
            user_answer.save()
        elif self.custom_initial_params.get('question_type') == '3':
            if self.request.user.is_authenticated:
                user_answer = UserAnswer(
                    user=self.request.user,
                    anonymous_user_id=None,
                    question_id=self.kwargs.get('q_id'),
                    text_answer=data.get('user_answers')
                )
            else:
                user_answer = UserAnswer(
                    user=None,
                    anonymous_user_id=self.request.session.session_key,
                    question_id=self.kwargs.get('q_id'),
                    text_answer=data.get('user_answers')
                )
            user_answer.save()

    def post(self, request, *args, **kwargs):
        self.custom_initial_params = {
            'queryset': self.context.get('answers_object_list'),
            'question_type': self.context.get('question').type,
        }
        user_answer_form_instance = UserAnswerCreateForm(request.POST, custom_initial_params=self.custom_initial_params)
        if user_answer_form_instance.is_valid():
            self.save_user_answer(user_answer_form_instance.cleaned_data)
            try:
                next_question_id = self.context.get('question').get_next_in_order().id
            except ObjectDoesNotExist as e:
                self.context.get('poll_assigned_to_user').is_active = False
                self.context.get('poll_assigned_to_user').save()
                return redirect(to=reverse('polls_assigned_to_user'))
            return redirect(
                to=reverse('user_answer_create', kwargs={'pk': self.kwargs.get('pk'), 'q_id': next_question_id})
            )


class CompletedPollsListView(SessionRequiredMixin, ListView):
    template_name = 'user_polls_2_app/completed_polls.html'

    def update_polls(self):
        spoilt_polls = Poll.objects.filter(Q(is_active=True) & Q(date_finish__lt=datetime.now()))
        print('spoilt_polls', spoilt_polls)
        for spoilt_poll in spoilt_polls:
            polls_for_editing = PollsAssignedToUser.objects.filter(poll_id=spoilt_poll.id)
            for poll in polls_for_editing:
                poll.is_active = False
                poll.save()

    def get_queryset(self):
        self.update_polls()
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Poll editors').exists() or self.request.user.is_staff:
                queryset = PollsAssignedToUser.objects.filter(is_active=False).order_by('poll_id').distinct('poll_id')
            else:
                queryset = PollsAssignedToUser.objects.filter(Q(user=self.request.user) & Q(is_active=False))
        else:
            queryset = PollsAssignedToUser.objects.filter(
                Q(anonymous_user_id=self.request.session.session_key) & Q(is_active=False)
            )
        return queryset


class PollResultsView(SessionRequiredMixin, View):
    context = {}
    template_name = 'user_polls_2_app/poll_results.html'

    def get(self, request, *args, **kwargs):
        self.context['poll'] = get_object_or_404(Poll, id=self.kwargs.get('pk'))
        poll_question_order = list(self.context['poll'].get_pollquestion_order())
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Poll editors').exists() or self.request.user.is_staff:
                user_answers = UserAnswer.objects.filter(question_id__in=poll_question_order)
            else:
                user_answers = UserAnswer.objects.filter(
                    Q(question_id__in=poll_question_order) & Q(user=self.request.user)
                )
        else:
            user_answers = UserAnswer.objects.filter(
                Q(question_id__in=poll_question_order) & Q(anonymous_user_id=self.request.session.session_key)
            )
        poll_results = {}
        for user_answer in user_answers:
            if user_answer.user:
                user = user_answer.user
            else:
                user = user_answer.anonymous_user_id
            question = user_answer.question
            if user_answer.choice_answer:
                answer = user_answer.choice_answer
            else:
                answer = user_answer.text_answer

            if user in poll_results:
                if question in poll_results.get(user):
                    poll_results[user][question].append(answer)
                else:
                    poll_results[user].update({question: [answer]})
            else:
                poll_results[user] = {question: [answer]}
        self.context['poll_results'] = poll_results
        return render(request=request, template_name=self.template_name, context=self.context)
