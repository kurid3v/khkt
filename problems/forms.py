from django import forms
from .models import Problem

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'title',
            'description',
            'subject',
            'question_type',
            'difficulty',
            'grading_criteria',
            'choice_a',
            'choice_b',
            'choice_c',
            'choice_d',
            'correct_answer',
        ]
        labels = {
            'title': 'Tiêu Đề',
            'description': 'Nội Dung',
            'subject': 'Môn',
            'question_type': 'Loại',
            'difficulty': 'Lớp', 
            'grading_criteria': 'Tiêu chí chấm',
            'choice_a': 'Lựa chọn A',
            'choice_b': 'Lựa chọn B',
            'choice_c': 'Lựa chọn C',
            'choice_d': 'Lựa chọn D',
            'correct_answer': 'Đáp án đúng',
        }
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'grading_criteria': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'choice_a': forms.TextInput(attrs={'class': 'form-control'}),
            'choice_b': forms.TextInput(attrs={'class': 'form-control'}),
            'choice_c': forms.TextInput(attrs={'class': 'form-control'}),
            'choice_d': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_answer': forms.Select(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], 
                                         attrs={'class': 'form-control'}),
        }
