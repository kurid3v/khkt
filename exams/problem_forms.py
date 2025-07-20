# forms.py
from django import forms
from .models import ExamProblem, ExamChoice

class ExamProblemForm(forms.ModelForm):
    class Meta:
        model = ExamProblem
        fields = ['question_text', 'problem_type']

class ExamChoiceForm(forms.ModelForm):
    class Meta:
        model = ExamChoice
        fields = ['text', 'is_correct']
