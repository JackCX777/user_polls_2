from django import forms
from user_polls_2_app.models import Poll, PollQuestion, PollAnswer


class PollModelForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'


class QuestionModelForm(forms.ModelForm):
    prefix = 'poll_question'

    class Meta:
        model = PollQuestion
        # fields = ('type', 'text')
        exclude = ('poll', )


class PollAnswerModelForm(forms.ModelForm):
    prefix = 'poll_answer'

    class Meta:
        model = PollAnswer
        # fields = '__all__'
        exclude = ('question', )


class BasePollAnswerFormSet(forms.BaseFormSet):
    def clean(self):
        '''
        Adds validation to check that no two field has the same variants.
        '''
        if any(self.errors):
            return

        variants_set = set()
        # duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                variant = form.cleaned_data.get('text')
                print('variant', variant, type(variant))
                if variant:
                    if variant in variants_set:
                        print(variant, 'in set!!')
                        # ???
                        raise forms.ValidationError('Variants must be unique', code='duplicate_variants')
                    variants_set.add(variant)


PollAnswerFormSet = forms.formset_factory(PollAnswerModelForm, formset=BasePollAnswerFormSet)
