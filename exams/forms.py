from django import forms
from .models import Exam
from django.forms.widgets import DateTimeInput
from django.contrib.auth.hashers import make_password

class ExamForm(forms.ModelForm):
    # Thêm trường mật khẩu mới vào form
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-md border-2 border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 px-4 py-2.5',
            'placeholder': 'Để trống nếu không muốn đặt mật khẩu'
        }),
        required=False,  # Cho phép trường này trống
        label="Mật khẩu kỳ thi",
        help_text="Nhập mật khẩu nếu bạn muốn kỳ thi này được bảo vệ."
    )

    class Meta:
        model = Exam
        # Thêm 'password' vào danh sách các trường của form
        fields = ['title', 'description', 'start_time', 'end_time', 'password']
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

    # Ghi đè phương thức save để băm mật khẩu trước khi lưu
    def save(self, commit=True):
        # Lấy bản sao của exam instance nhưng chưa lưu vào DB
        exam = super().save(commit=False)
        
        # Nếu người dùng đã nhập mật khẩu, băm nó
        if self.cleaned_data.get('password'):
            exam.password = make_password(self.cleaned_data['password'])
        else:
            # Nếu không có mật khẩu, đặt trường password là None
            exam.password = None

        if commit:
            exam.save()
        return exam