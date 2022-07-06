from django import forms
from .models import Question,Answer,Tags

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title','text','tags')

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)


class TagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ('tag_word',)