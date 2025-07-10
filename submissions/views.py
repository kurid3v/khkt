from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .forms import SubmissionForm
from .models import Submission
from problems.models import Problem
from .api import grade_with_ai
from django.db.models import Max
import re

@login_required
# def submit_solution(request, problem_id):
#     problem = get_object_or_404(Problem, id=problem_id)

#     if request.method == 'POST':
#         form = SubmissionForm(request.POST)
#         if form.is_valid():
#             submission = form.save(commit=False)
#             submission.user = request.user
#             submission.problem = problem
#             submission.save()
#             return redirect('view_result', submission_id=submission.id)
#     else:
#         form = SubmissionForm()

#     return render(request, 'submissions/submit.html', {
#         'form': form,
#         'problem': problem
#     })
@login_required
def submit_solution(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.method == 'POST':
        code = request.POST.get('answer', '').strip()

        submission = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code
        )

        if problem.question_type == 'MCQ':
            # ✅ Tự động chấm trắc nghiệm (so sánh đáp án)
            correct = problem.correct_answer.strip().upper() if problem.correct_answer else ''
            user_answer = code.upper()

            score = 10 if user_answer == correct else 0
            comment = f"Đáp án đúng là {correct}. Bạn đã chọn {user_answer}."
        else:
            # 🧠 Gọi AI chấm bài tự luận / lập trình
            result_text = grade_with_ai(
                problem_text=problem.description,
                answer=code,
                criteria=problem.grading_criteria
            )


            # Tách điểm từ kết quả
            score_match = re.search(r"Điểm[:\s]+(\d+(?:\.\d+)?)", result_text)
            score = float(score_match.group(1)) if score_match else None
            comment = result_text

        # Lưu kết quả
        submission.score = score
        submission.comment = comment
        submission.save()

        return redirect('view_result', submission_id=submission.id)

    return render(request, 'submissions/submit_form.html', {'problem': problem})

def submission_list(request):
    submissions = Submission.objects.select_related('problem', 'user').order_by('-submitted_at')
    return render(request, 'submissions/list.html', {
        'submissions': submissions
    })


# def submission_list(request):
#     user = request.user

#     if user.is_authenticated:
#         submissions = Submission.objects.filter(
#             Q(user=user) | Q(problem__author=user)
#         ).select_related('problem', 'user')
#     else:
#         submissions = Submission.objects.none()  # Không hiển thị gì nếu chưa đăng nhập

#     return render(request, 'submissions/list.html', {
#         'submissions': submissions
#     })

# def view_result(request, submission_id):
#     submission = get_object_or_404(Submission, id=submission_id)

#     # ❗ Không cần kiểm tra quyền — mọi người đều xem được
#     return render(request, 'submissions/result.html', {
#         'submission': submission
#     })

def view_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if submission.user != request.user and submission.problem.author != request.user:
        return HttpResponseForbidden("Bạn không có quyền xem bài này.")

    return render(request, 'submissions/result.html', {
        'submission': submission
    })



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

def problem_ranking(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    # Lấy điểm cao nhất của mỗi người dùng với đề đó
    top_scores = (
        Submission.objects
        .filter(problem=problem, score__isnull=False)
        .values('user__username')
        .annotate(best_score=Max('score'))
        .order_by('-best_score')
    )

    return render(request, 'submissions/ranking.html', {
        'problem': problem,
        'top_scores': top_scores
    })