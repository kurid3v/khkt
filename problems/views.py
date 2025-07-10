from django.shortcuts import render, get_object_or_404
from .models import Problem
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProblemForm
from submissions.models import Submission
from django.db.models import Q
import base64
import requests
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from submissions.forms import ImageSubmissionForm 
from submissions.api import grade_with_ai
from submissions.models import Submission
from problems.models import Problem

# def problem_list(request):
#     query = request.GET.get('q', '')
#     problems = Problem.objects.all()
#     if query:
#         problems = problems.filter(Q(title__icontains=query))
#     return render(request, 'problems/problem_list.html', {'problems': problems})

def problem_list(request):
    query = request.GET.get('q', '')
    problems = Problem.objects.all()

    if query:
        problems = problems.filter(Q(title__icontains=query))

    problems = problems.order_by('?')  # 🔀 Xếp ngẫu nhiên

    return render(request, 'problems/problem_list.html', {'problems': problems})

def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return render(request, 'problems/problem_detail.html', {'problem': problem})

@login_required
def add_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.author = request.user  # 🔥 GÁN TÁC GIẢ TỪ USER ĐĂNG NHẬP
            problem.save()
            return redirect('problem_list')
    else:
        form = ProblemForm()

    return render(request, 'problems/add_problem.html', {'form': form})


@login_required
def submissions_by_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.user == problem.author or request.user.is_staff:
        submissions = Submission.objects.filter(problem=problem).select_related('user')
    else:
        submissions = Submission.objects.filter(problem=problem, user=request.user)

    return render(request, 'submissions/list.html', {
        'submissions': submissions,
        'problem': problem,
    })
