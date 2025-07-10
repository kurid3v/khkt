from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exam
from .forms import ExamForm

def exam_list(request):
    exams = Exam.objects.all().order_by('-created_at')
    return render(request, 'exams/list.html', {'exams': exams})

@login_required
def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'exams/add_exam.html', {'form': form})


def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    return render(request, 'exams/detail.html', {
        'exam': exam
    })