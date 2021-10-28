from django import forms
from user_polls_2_app.models import Poll, PollQuestion, PollAnswer, PollsAssignedToUser, UserAnswer


class PollModelForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'
        widgets = {'date_finish': forms.SelectDateWidget()}


class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = PollQuestion
        fields = ('type', 'text')


class PollAnswerModelForm(forms.ModelForm):
    class Meta:
        model = PollAnswer
        exclude = ('question', )


class BasePollAnswerFormSet(forms.BaseFormSet):
    def clean(self):
        '''
        Adds validation to check that no two field has the same variants.
        '''
        if any(self.errors):
            return

        variants_set = set()
        for form in self.forms:
            if form.cleaned_data:
                variant = form.cleaned_data.get('text')
                if variant:
                    if variant in variants_set:
                        raise forms.ValidationError('Variants must be unique', code='duplicate_variants')
                    variants_set.add(variant)


class PollsAssignedToUserForm(forms.ModelForm):
    class Meta:
        model = PollsAssignedToUser
        fields = '__all__'


# class UserAnswerCreateCheckboxForm(forms.ModelForm):
#     class Meta:
#         model = PollAnswer
#         # fields = ('choice_answer', )
#         fields = ('text',)
#         widgets = {'choice_answer': forms.CheckboxInput()}


# class UserAnswerCreateRadioForm(forms.ModelForm):
#     class Meta:
#         model = PollAnswer
#         # fields = ('choice_answer', )
#         fields = ('text',)
#         widgets = {'choice_answer': forms.RadioSelect()}


class UserAnswerCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.fields_dict = {
            '1': forms.ModelMultipleChoiceField,
            '2': forms.ModelChoiceField,
            '3': forms.CharField
        }
        self.widget_dict = {
            '1': forms.CheckboxSelectMultiple,
            '2': forms.RadioSelect,
            '3': forms.TextInput
        }
        self.custom_initial_params = kwargs.pop('custom_initial_params')
        self.queryset = self.custom_initial_params.get('queryset')
        self.widget_type = self.custom_initial_params.get('question_type')
        super().__init__(*args, **kwargs)
        if self.widget_type == '3':
            self.fields['user_answers'] = self.fields_dict.get(self.widget_type)(
                strip=True,
                widget=self.widget_dict.get(self.widget_type),
            )
        else:
            self.fields['user_answers'] = self.fields_dict.get(self.widget_type)(
                queryset=self.queryset,
                widget=self.widget_dict.get(self.widget_type),
            )


# class UserAnswerCreateTextForm(forms.ModelForm):
#     class Meta:
#         model = PollAnswer
#         # fields = ('text_answer', )
#         fields = ('text', )
#         widgets = {'text_answer': forms.TextInput()}


PollAnswerFormSet = forms.formset_factory(PollAnswerModelForm, formset=BasePollAnswerFormSet)
