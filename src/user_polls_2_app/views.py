from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from user_polls_2_app.models import Poll, PollQuestion, PollAnswer
from user_polls_2_app.forms import PollModelForm, QuestionModelForm, PollAnswerModelForm, PollAnswerFormSet
from django.db import IntegrityError, transaction
from django.contrib import messages


class PollsListView(ListView):
    model = Poll
    template_name = 'user_polls_2_app/polls_list.html'
    # paginate_by = 3
    # context_object_name = 'polls'

    def get_queryset(self):
        print(self.kwargs)
        return Poll.objects.all()


class PollDetailView(DetailView):
    model = Poll
    # queryset = Poll.objects.all()
    pk_url_kwarg = 'pk'
    template_name = 'user_polls_2_app/poll_detail.html'

    # def get_queryset(self):
    #     queryset = Poll.objects.get(id=self.kwargs.get('pk'))
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        question_queryset = self.object.questions.all()
        context['question_list'] = question_queryset
        return context


class CreatePollView(CreateView):
    queryset = Poll.objects.all()
    template_name = 'user_polls_2_app/poll_create.html'
    form_class = PollModelForm
    # success_url = reverse_lazy('question_create')

    def get_success_url(self):
        return reverse('question_create', kwargs={'pk': self.object.id})


class UpdatePollView(UpdateView):
    queryset = Poll.objects.all()
    template_name = 'user_polls_2_app/poll_update.html'
    form_class = PollModelForm


class DeletePollView(DeleteView):
    queryset = Poll.objects.all()
    template_name = 'user_polls_2_app/poll_delete.html'
    success_url = reverse_lazy('polls_list')


# class CreateQuestionView(CreateView):
#     model = PollQuestion
#     # queryset = PollQuestion.objects.all()
#     template_name = 'user_polls_2_app/question_create.html'
#     form_class = QuestionModelForm
#     context_object_name = 'poll_question_form'
#     # success_url = reverse_lazy('poll_detail')
#
#     def get_poll_id(self):
#         # return self.kwargs.get('pk')
#         return self.pk_url_kwarg
#
    # def form_valid(self, form):
#         # url_pk = self.kwargs.get('pk')
#         # form.instance.poll_id = url_pk
#         form.instance.poll_id = self.get_poll_id()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         # return reverse('poll_detail', kwargs={'pk': self.kwargs.get('pk')})
#         return reverse('poll_detail', kwargs={'pk': self.get_poll_id()})
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['parent_poll'] = Poll.objects.get(id=self.kwargs.get('pk'))
#         context['parent_poll'] = self.get_poll_id()
#         context['poll_question_form'] = QuestionModelForm()
#         # context['poll_answer_form'] = PollAnswerModelForm(prefix='poll_answer')
#         return context


class CreatePollQuestionWithVariantsView(View):
    question_form_class = QuestionModelForm
    # answer_form_class = PollAnswerModelForm
    answer_formset_class = PollAnswerFormSet
    template_name = 'user_polls_2_app/question_create.html'
    context = {}

    def get_pk_from_url(self):
        return self.kwargs.get('pk')

    def get(self, request, *args, **kwargs):
        self.context['pk'] = self.get_pk_from_url()
        poll_question_form = self.question_form_class(prefix='poll_question')
        self.context['poll_question_form'] = poll_question_form
        # poll_answer_form = self.answer_form_class(prefix='poll_answer')
        # self.context['poll_answer_form'] = poll_answer_form
        poll_answer_formset = self.answer_formset_class(prefix='poll_answer')
        self.context['poll_answer_formset'] = poll_answer_formset
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        self.context['pk'] = self.get_pk_from_url()
        poll_question_form_instance = self.question_form_class(request.POST, prefix='poll_question')
        # poll_answer_form_instance = self.answer_form_class(request.POST, prefix='poll_answer')
        poll_answer_formset = self.answer_formset_class(request.POST, prefix='poll_answer')
        print(poll_answer_formset)
        if poll_question_form_instance.is_valid():
            poll_question_object = poll_question_form_instance.save(commit=False)
            poll_question_object.poll_id = self.context.get('pk')
            poll_question_object.save()
            # if poll_answer_form_instance.is_valid():
            if poll_question_object.type == '3':
                # messages.error(self.request, 'Questions of the text type'
                #                              ' should not have any answer options')
                # return render(request, template_name=self.template_name, context=self.context)
                poll_answer_formset = self.answer_formset_class(prefix='poll_answer')
                poll_question_form_instance = self.question_form_class(prefix='poll_question')
            elif poll_answer_formset.is_valid():
                # poll_answer_object = poll_answer_form_instance.save(commit=False)
                new_answers_list = []
                for answer_form in poll_answer_formset:
                    variant = answer_form.cleaned_data.get('text')
                    print('variant!!', variant)
                    if variant:
                        # print('exist11111111')
                        new_answers_list.append(PollAnswer(question=poll_question_object, text=variant))
                try:
                    # transaction.atomic here only for example
                    with transaction.atomic():
                        print('new_answers_list', new_answers_list)
                        PollAnswer.objects.bulk_create(new_answers_list)
                # If transaction failed
                except IntegrityError:
                    messages.error(self.request, 'There was an error saving answer variants')
                    # return redirect(reverse('poll_detail'))
                    return render(request, template_name=self.template_name, context=self.context)
            else:
                poll_answer_formset = self.answer_formset_class(prefix='poll_answer')
        else:
            poll_question_form_instance = self.question_form_class(prefix='poll_question')
        return redirect(to=reverse('poll_detail', kwargs={'pk': self.context.get('pk')}))


class PollQuestionDetailView(DetailView):
    model = PollQuestion
    pk_url_kwarg = 'q_id'
    template_name = 'user_polls_2_app/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PollQuestionDetailView, self).get_context_data(**kwargs)
        answer_variants = self.object.answer_variants.all()
        # print(answer_variants)
        context['answer_variants'] = answer_variants
        # poll_object = Poll.objects.get(id=self.kwargs.get('pk'))
        poll_object = Poll.objects.get(id=self.object.poll_id)
        print('_____poll_object', poll_object)
        context['poll_object'] = poll_object
        return context


class UpdatePollQuestionView(View):
    question_form_class = QuestionModelForm
    answer_formset_class = PollAnswerFormSet
    template_name = 'user_polls_2_app/question_update.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['pk'] = self.kwargs.get('pk')
        self.context['q_id'] = self.kwargs.get('q_id')
        question_object = PollQuestion.objects.get(id=self.kwargs.get('q_id'))
        question_data = {'type': question_object.type, 'text': question_object.text}
        self.context['question_object'] = question_object
        poll_question_form = self.question_form_class(initial=question_data, prefix='poll_question')
        self.context['poll_question_form'] = poll_question_form
        answers_object_list = PollAnswer.objects.filter(question=question_object)
        answers_data = [{'text': answer.text} for answer in answers_object_list]
        poll_answer_formset = self.answer_formset_class(initial=answers_data, prefix='poll_answer')
        self.context['poll_answer_formset'] = poll_answer_formset
        return render(request=request, template_name=self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        poll_question_form_instance = self.question_form_class(request.POST, prefix='poll_question')
        poll_answer_formset = self.answer_formset_class(request.POST, prefix='poll_answer')
        question_object = PollQuestion.objects.get(id=self.kwargs.get('q_id'))
        answers_object_list = PollAnswer.objects.filter(question=question_object)
        if poll_question_form_instance.is_valid():
            question_object.type = poll_question_form_instance.cleaned_data.get('type')
            question_object.text = poll_question_form_instance.cleaned_data.get('text')
            question_object.save()
            if poll_answer_formset.is_valid():
                new_answers_list = []
                for answer_form in poll_answer_formset:
                    variant = answer_form.cleaned_data.get('text')
                    if variant:
                        if question_object.type == '3':
                            messages.error(self.request, 'Questions of the text type'
                                                         ' should not have any answer options')
                            self.get(request)
                        else:
                            new_answers_list.append(PollAnswer(question=question_object, text=variant))
                try:
                    with transaction.atomic():
                        PollAnswer.objects.filter(question=question_object).delete()
                        PollAnswer.objects.bulk_create(new_answers_list)
                except IntegrityError:
                    messages.error(request, 'There was an error saving answer variants')
                    question_object = PollQuestion.objects.get(id=self.kwargs.get('q_id'))
                    question_data = {'type': question_object.type, 'text': question_object.text}
                    poll_question_form = self.question_form_class(initial=question_data, prefix='poll_question')
                    answers_object_list = PollAnswer.objects.filter(question=question_object)
                    answers_data = [{'text': answer.text} for answer in answers_object_list]
                    poll_answer_formset = self.answer_formset_class(initial=answers_data, prefix='poll_answer')
        else:
            question_object = PollQuestion.objects.get(id=self.kwargs.get('q_id'))
            question_data = {'type': question_object.type, 'text': question_object.text}
            poll_question_form = self.question_form_class(initial=question_data, prefix='poll_question')
            answers_object_list = PollAnswer.objects.filter(question=question_object)
            answers_data = [{'text': answer.text} for answer in answers_object_list]
            poll_answer_formset = self.answer_formset_class(initial=answers_data, prefix='poll_answer')
        return redirect(to=reverse('question_detail', kwargs={'pk': self.kwargs.get('pk'),
                                                              'q_id': self.kwargs.get('q_id')}))


class DeletePollQuestionView(DeleteView):
    model = PollQuestion
    pk_url_kwarg = 'q_id'
    template_name = 'user_polls_2_app/question_delete.html'
    # success_url = reverse_lazy('poll_detail')

    def get_success_url(self):
        return reverse('poll_detail', kwargs={'pk': self.kwargs.get('pk')})
