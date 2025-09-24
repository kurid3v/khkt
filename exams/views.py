from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import check_password, make_password
from .models import Exam, ExamProblem, ExamChoice, ExamEnrollment
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
        exam.has_password = bool(exam.password)
        
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

# @login_required
# def enroll_in_exam(request, exam_id):
#     exam = get_object_or_404(Exam, id=exam_id)

#     if request.user == exam.created_by or request.user.is_staff:
#         # Xóa các bản ghi ghi danh khác để đảm bảo duy nhất
#         ExamEnrollment.objects.filter(user=request.user).exclude(exam=exam).delete()
#         ExamEnrollment.objects.get_or_create(exam=exam, user=request.user)
#         return redirect('exam_detail', exam_id=exam.id)
    
#     if exam.password:
#         if request.method == 'POST':
#             password_input = request.POST.get('password', '')
#             if check_password(password_input, exam.password):
#                 # Nếu mật khẩu đúng, xóa các ghi danh cũ và ghi danh mới
#                 ExamEnrollment.objects.filter(user=request.user).exclude(exam=exam).delete()
#                 ExamEnrollment.objects.get_or_create(exam=exam, user=request.user)
#                 return redirect('exam_detail', exam_id=exam.id)
#             else:
#                 error_message = "Mật khẩu không đúng. Vui lòng thử lại."
#                 return render(request, 'exams/exam_not_enrolled.html', {
#                     'exam': exam,
#                     'error_message': error_message,
#                 })
#         else:
#             return render(request, 'exams/exam_not_enrolled.html', {'exam': exam})
    
#     ExamEnrollment.objects.filter(user=request.user).exclude(exam=exam).delete()
#     ExamEnrollment.objects.get_or_create(exam=exam, user=request.user)
#     return redirect('exam_detail', exam_id=exam.id)

@login_required
def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # Thêm dòng này để kiểm tra trạng thái ghi danh
    is_enrolled = ExamEnrollment.objects.filter(exam=exam, user=request.user).exists()
    
    if not is_enrolled:
        return redirect('enroll_in_exam', exam_id=exam.id)

    # Logic hiển thị chi tiết đề thi
    letters = ['A', 'B', 'C', 'D']
    answers = []
    total_score = 0
    difficulty_map = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
        'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12,
    }

    exam_problems = exam.exam_problems.order_by('order')
    for prob in exam_problems:
        if prob.problem and prob.problem.difficulty:
            score = difficulty_map.get(prob.problem.difficulty.lower(), 0)
            total_score += score

        if prob.problem.question_type == 'MCQ':
            correct_answer = prob.problem.correct_answer
            if correct_answer:
                try:
                    answers.append(f"{prob.order}{correct_answer.strip().upper()}")
                except ValueError:
                    continue

    input_path = "/home/tuansangg/multisubject_oj/form.jpg"
    output_path = f"/home/tuansangg/multisubject_oj/media/output_exam_{exam_id}.jpg"
    draw_circles_on_form(answers, input_path, output_path)

    return render(request, 'exams/detail.html', {
        'exam': exam,
        'letters': letters,
        'answer_image': f"/media/output_exam_{exam_id}.jpg",
        'total_score': total_score,
        'is_enrolled': is_enrolled, # Truyền biến này vào template
    })

    exam_problems = exam.exam_problems.order_by('order')
    for prob in exam_problems:
        if prob.problem and prob.problem.difficulty:
            score = difficulty_map.get(prob.problem.difficulty.lower(), 0)
            total_score += score

        if prob.problem.question_type == 'MCQ':
            correct_answer = prob.problem.correct_answer
            if correct_answer:
                try:
                    answers.append(f"{prob.order}{correct_answer.strip().upper()}")
                except ValueError:
                    continue

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
            problem.is_hidden = True
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

# @login_required
# def leave_exam(request, exam_id):
#     exam = get_object_or_404(Exam, id=exam_id)
    
#     # Tìm và xóa bản ghi ExamEnrollment của người dùng
#     enrollment = ExamEnrollment.objects.filter(exam=exam, user=request.user)
    
#     # Chỉ cho phép rời kỳ thi nếu người dùng không phải là người tạo
#     if request.user != exam.created_by:
#         enrollment.delete()
    
#     return redirect('exam_list')

@login_required
def enroll_in_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # 1. Bỏ qua bước kiểm tra mật khẩu cho admin và người tạo đề
    if request.user == exam.created_by or request.user.is_staff:
        ExamEnrollment.objects.get_or_create(exam=exam, user=request.user)
        # Tạo biến session xác thực để không hỏi lại mật khẩu
        request.session[f'exam_{exam_id}_authenticated'] = True
        return redirect('exam_detail', exam_id=exam.id)
    
    # 2. Kiểm tra nếu đã có xác thực trong session, thì bỏ qua mật khẩu
    if request.session.get(f'exam_{exam_id}_authenticated'):
        ExamEnrollment.objects.get_or_create(exam=exam, user=request.user)
        return redirect('exam_detail', exam_id=exam.id)

    # 3. Xử lý logic mật khẩu cho người dùng thông thường
    if exam.password:
        if request.method == 'POST':
            password_input = request.POST.get('password', '')
            if check_password(password_input, exam.password):
                # Lưu trạng thái xác thực vào session
                request.session[f'exam_{exam_id}_authenticated'] = True
                ExamEnrollment.objects.get_or_create(exam=exam, user=request.user)
                return redirect('exam_detail', exam_id=exam.id)
            else:
                error_message = "Mật khẩu không đúng. Vui lòng thử lại."
                return render(request, 'exams/exam_not_enrolled.html', {
                    'exam': exam,
                    'error_message': error_message,
                })
        else:
            return render(request, 'exams/exam_not_enrolled.html', {'exam': exam})
    
    # 4. Nếu không có mật khẩu, ghi danh trực tiếp
    ExamEnrollment.objects.get_or_create(exam=exam, user=request.user)
    return redirect('exam_detail', exam_id=exam.id)

@login_required
def leave_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    enrollment = ExamEnrollment.objects.filter(exam=exam, user=request.user)
    
    # Chỉ cho phép rời kỳ thi nếu người dùng không phải là người tạo
    if request.user != exam.created_by:
        enrollment.delete()
        # Xóa trạng thái xác thực mật khẩu khỏi session
        if f'exam_{exam_id}_authenticated' in request.session:
            del request.session[f'exam_{exam_id}_authenticated']

    return redirect('exam_list')