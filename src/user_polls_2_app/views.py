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
    paginate_by = 5
    template_name = 'user_polls_2_app/polls_list.html'


class PollDetailView(DetailView):
    model = Poll
    template_name = 'user_polls_2_app/poll_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        question_queryset = self.object.questions.all()
        context['question_list'] = question_queryset
        return context


class CreatePollView(CreateView):
    queryset = Poll.objects.all()
    template_name = 'user_polls_2_app/poll_create.html'
    form_class = PollModelForm

    def get_success_url(self):
        return reverse('question_create', kwargs={'pk': self.object.id})


class UpdatePollView(UpdateView):
    queryset = Poll.objects.all()
    form_class = PollModelForm
    template_name = 'user_polls_2_app/poll_update.html'


class DeletePollView(DeleteView):
    queryset = Poll.objects.all()
    success_url = reverse_lazy('polls_list')
    template_name = 'user_polls_2_app/poll_delete.html'


class CreatePollQuestionWithVariantsView(View):
    question_form_class = QuestionModelForm
    answer_formset_class = PollAnswerFormSet
    context = {}
    template_name = 'user_polls_2_app/question_create.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.context['pk'] = pk
        # poll_object = Poll.objects.get(id=pk)
        poll_object = get_object_or_404(Poll, id=pk)
        self.context['poll_object'] = poll_object
        question_form = self.question_form_class(prefix='question')
        self.context['question_form'] = question_form
        answer_formset = self.answer_formset_class(prefix='answer')
        self.context['answer_formset'] = answer_formset
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.context['pk'] = pk
        poll_object = get_object_or_404(Poll, id=pk)
        self.context['poll_object'] = poll_object
        question_form_instance = self.question_form_class(request.POST, prefix='question')
        answer_formset = self.answer_formset_class(request.POST, prefix='answer')
        if question_form_instance.is_valid():
            poll_question_object = question_form_instance.save(commit=False)
            poll_question_object.poll_id = pk
            poll_question_object.save()
            if poll_question_object.type == '3':
                return redirect(to=reverse('poll_detail', kwargs={'pk': pk}))
            elif answer_formset.is_valid():
                new_answers_list = []
                for answer_form in answer_formset:
                    print(pk)
                    print('!!!!!', answer_form.prefix, answer_form.cleaned_data)
                    variant = answer_form.cleaned_data.get('text')
                    if variant:
                        new_answers_list.append(PollAnswer(question=poll_question_object, text=variant))
                    # try:
                    #     PollAnswer.objects.bulk_create(new_answers_list)
                    # except IntegrityError:
                    #     messages.error(request, 'There was an error saving answer options')
                    for new_answer_object in new_answers_list:
                        new_answer_object.save()
                    # new_answer_objects = PollAnswer.objects.bulk_create(new_answers_list)
            else:
                answer_formset = self.answer_formset_class(prefix='answer')
        else:
            question_form_instance = self.question_form_class(prefix='question')
        return redirect(to=reverse('poll_detail', kwargs={'pk': pk}))


class PollQuestionDetailView(DetailView):
    model = PollQuestion
    pk_url_kwarg = 'q_id'
    template_name = 'user_polls_2_app/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PollQuestionDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['pk'] = pk
        q_id = self.kwargs.get('q_id')
        context['q_id'] = q_id
        answer_variants = self.object.answer_variants.all()
        context['answer_variants'] = answer_variants
        return context


class UpdatePollQuestionView(View):
    question_form_class = QuestionModelForm
    answer_formset_class = PollAnswerFormSet
    context = {}
    template_name = 'user_polls_2_app/question_update.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.context['pk'] = pk
        q_id = self.kwargs.get('q_id')
        self.context['q_id'] = q_id
        question_object = get_object_or_404(PollQuestion, id=q_id)
        self.context['question_object'] = question_object
        question_data = {'type': question_object.type, 'text': question_object.text}
        question_form = self.question_form_class(initial=question_data, prefix='question')
        self.context['question_form'] = question_form
        answers_object_list = PollAnswer.objects.filter(question=question_object)
        answers_data = [{'text': answer.text} for answer in answers_object_list]
        answer_formset = self.answer_formset_class(initial=answers_data, prefix='answer')
        self.context['answer_formset'] = answer_formset
        return render(request=request, template_name=self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        q_id = self.kwargs.get('q_id')
        question_object = get_object_or_404(PollQuestion, id=q_id)
        question_data = {'type': question_object.type, 'text': question_object.text}
        answers_object_list = PollAnswer.objects.filter(question=question_object)
        answers_data = [{'text': answer.text} for answer in answers_object_list]
        question_form_instance = self.question_form_class(request.POST, prefix='question')
        answer_formset = self.answer_formset_class(request.POST, prefix='answer')
        if question_form_instance.is_valid():
            question_object.type = question_form_instance.cleaned_data.get('type')
            question_object.text = question_form_instance.cleaned_data.get('text')
            question_object.save()
            if question_object.type == '3':
                return redirect(to=reverse('question_detail', kwargs={'pk': pk, 'q_id': q_id}))
            elif answer_formset.is_valid():
                new_answers_list = []
                for answer_form in answer_formset:
                    variant = answer_form.cleaned_data.get('text')
                    if variant:
                        new_answers_list.append(PollAnswer(question=question_object, text=variant))
                try:
                    with transaction.atomic():
                        PollAnswer.objects.filter(question=question_object).delete()
                        PollAnswer.objects.bulk_create(new_answers_list)
                        # for new_answer_object in new_answers_list:
                        #     new_answer_object.save()
                # If transaction failed
                except IntegrityError:
                    messages.error(request, 'There was an error saving answer options')
                    question_form = self.question_form_class(initial=question_data, prefix='question')
                    answer_formset = self.answer_formset_class(initial=answers_data, prefix='answer')
        else:
            question_form = self.question_form_class(initial=question_data, prefix='question')
            answer_formset = self.answer_formset_class(initial=answers_data, prefix='answer')
        return redirect(to=reverse('question_detail', kwargs={'pk': pk, 'q_id': q_id}))


class DeletePollQuestionView(DeleteView):
    model = PollQuestion
    pk_url_kwarg = 'q_id'
    template_name = 'user_polls_2_app/question_delete.html'

    def get_success_url(self):
        return reverse('poll_detail', kwargs={'pk': self.kwargs.get('pk')})
