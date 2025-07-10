from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code']
        labels = {
            'code': 'Bài làm',
        }

from django import forms

class ImageSubmissionForm(forms.Form):
    image = forms.ImageField(label="Tải ảnh bài làm")
