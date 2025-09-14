from django import forms
from .models import Exam
from django.forms.widgets import DateTimeInput

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-md border-2 border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 px-4 py-2.5',
                'placeholder': 'Nhập tiêu đề đề thi'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-md border-2 border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 px-4 py-2.5',
                'placeholder': 'Nhập mô tả cho đề thi',
                'rows': 4
            }),
            'start_time': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full rounded-md border-2 border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 px-4 py-2.5'
            }),
            'end_time': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full rounded-md border-2 border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 px-4 py-2.5'
            }),
        }
        labels = {
            'title': 'Tiêu đề',
            'description': 'Mô tả',
            'start_time': 'Thời gian bắt đầu',
            'end_time': 'Thời gian kết thúc'
        }
        help_texts = {
            'title': 'Nhập tiêu đề ngắn gọn và dễ hiểu',
            'description': 'Mô tả chi tiết về đề thi, yêu cầu và hướng dẫn cho học sinh',
            'start_time': 'Thời điểm bắt đầu cho phép làm bài',
            'end_time': 'Thời điểm kết thúc, sau thời gian này học sinh không thể nộp bài'
        }
