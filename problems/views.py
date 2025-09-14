from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .forms import ProblemForm
from .models import Problem
from submissions.models import Submission

def problem_list(request):
    """
    Hiển thị danh sách các bài tập.
    Chỉ hiển thị các bài tập không bị ẩn, trừ khi người dùng là admin.
    """
    query = request.GET.get('q', '')
    problems = Problem.objects.filter(is_hidden=False)

    if request.user.is_authenticated and request.user.is_staff:
        # Admin có thể xem tất cả các bài tập
        problems = Problem.objects.all()

    if query:
        problems = problems.filter(Q(title__icontains=query))

    problems = problems.order_by('?')

    return render(request, 'problems/problem_list.html', {'problems': problems})

def problem_detail(request, pk):
    """
    Hiển thị chi tiết một bài tập.
    Người dùng không phải tác giả chỉ có thể xem nếu bài tập không bị ẩn.
    """
    problem = get_object_or_404(Problem, pk=pk)

    if problem.is_hidden:
        # Nếu bài tập bị ẩn, kiểm tra quyền của người dùng
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Bạn không có quyền xem bài tập này.")
        
        if request.user != problem.author and not request.user.is_staff:
            return HttpResponseForbidden("Bạn không có quyền xem bài tập này.")

    return render(request, 'problems/problem_detail.html', {'problem': problem})

@login_required
def add_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.author = request.user
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

@login_required
def toggle_problem_visibility(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    if request.user != problem.author:
        return HttpResponseForbidden("Bạn không có quyền thực hiện hành động này.")

    problem.is_hidden = not problem.is_hidden
    problem.save()

    return redirect('problem_detail', pk=problem.pk)
