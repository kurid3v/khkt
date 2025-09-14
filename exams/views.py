from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from .models import Exam, ExamProblem, ExamChoice
from .forms import ExamForm
from problems.forms import ProblemForm
from problems.models import Problem
from PIL import Image, ImageDraw
import os
from .draw_answers import draw_circles_on_form

def exam_list(request):
    exams = Exam.objects.all().order_by('-created_at')
    
    difficulty_map = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
        'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12,
    }

    for exam in exams:
        total_score = 0
        exam_problems = exam.exam_problems.all()
        for prob in exam_problems:
            if prob.problem and prob.problem.difficulty:
                score = difficulty_map.get(prob.problem.difficulty.lower(), 0)
                total_score += score
        exam.total_score = total_score
        
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
    letters = ['A', 'B', 'C', 'D']

    # Lấy đáp án đúng và tính tổng điểm
    answers = []
    total_score = 0
    difficulty_map = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
        'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12,
    }

    exam_problems = exam.exam_problems.order_by('order')
    for prob in exam_problems:
        # Tính tổng điểm
        if prob.problem and prob.problem.difficulty:
            score = difficulty_map.get(prob.problem.difficulty.lower(), 0)
            total_score += score

        # Lấy đáp án đúng để vẽ phiếu tô đáp án
        if prob.problem.question_type == 'MCQ':
            correct_answer = prob.problem.correct_answer
            if correct_answer:
                try:
                    answers.append(f"{prob.order}{correct_answer.strip().upper()}")
                except ValueError:
                    continue

    # Vẽ ảnh tô đáp án
    input_path = "/home/tuansangg/multisubject_oj/form.jpg"
    output_path = f"/home/tuansangg/multisubject_oj/media/output_exam_{exam_id}.jpg"
    draw_circles_on_form(answers, input_path, output_path)

    return render(request, 'exams/detail.html', {
        'exam': exam,
        'letters': letters,
        'answer_image': f"/media/output_exam_{exam_id}.jpg",
        'total_score': total_score,
    })

@login_required
def add_exam_problem(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == "POST":
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.author = request.user
            problem.is_hidden = True  # Tự động ẩn bài tập khi được thêm vào đề thi
            problem.save()
            ExamProblem.objects.create(
                exam=exam,
                problem=problem,
                problem_type=problem.question_type,
                order=exam.exam_problems.count() + 1
            )
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = ProblemForm()
    return render(request, 'exams/add_exam_problem.html', {'form': form, 'exam': exam})

@require_POST
@login_required
def submit_mcq(request, problem_id):
    problem = get_object_or_404(ExamProblem, id=problem_id)
    if problem.problem_type != 'multiple_choice':
        return HttpResponseForbidden("Bài tập này không phải dạng trắc nghiệm.")
    selected_choice_id = request.POST.get('answer')
    if selected_choice_id:
        get_object_or_404(ExamChoice, id=selected_choice_id)
    return redirect('exam_detail', exam_id=problem.exam.id)

def draw_answer_sheet(exam_id, answers):
    base_image_path = "/home/tuansangg/multisubject_oj/form.jpg"
    image = Image.open(base_image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    x0, y0 = 267, 1286
    dx, dy = 98, 60
    for ans in answers:
        try:
            q_num = int(ans[:-1])
            letter = ans[-1]
            col = ['A', 'B', 'C', 'D'].index(letter)
            cx = x0 + col * dx
            cy = y0 + (q_num - 1) * dy
            r = 10
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill='black')
        except Exception:
            continue
    output_path = f"/home/tuansangg/multisubject_oj/media/output_exam_{exam_id}.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    return f"/media/output_exam_{exam_id}.jpg"
