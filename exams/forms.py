from django import forms
from .models import Exam
from django.forms.widgets import DateTimeInput

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_time': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }
