from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exam
from .forms import ExamForm
from django.http import HttpResponseForbidden
from .problem_forms import ExamProblemForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from .models import Exam, ExamProblem, ExamChoice  # ✅ thêm ExamProblem, ExamChoice
from django.shortcuts import render, get_object_or_404
from .models import Exam
from .draw_answers import draw_circles_on_form
from PIL import Image, ImageDraw
import os
#from .utils.answer_sheet import draw_answer_sheet
#from .views import draw_answer_sheet as draw_circles_on_form

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
    letters = ['A', 'B', 'C', 'D']

    # Lấy danh sách đáp án đúng từ các bài trắc nghiệm
    answers = []
    exam_problems = exam.exam_problems.order_by('order')  # Đảm bảo đúng thứ tự
    for prob in exam_problems:
        if prob.problem_type == 'multiple_choice':
            correct = prob.choices.filter(is_correct=True).first()
            if correct:
                try:
                    index = letters.index(correct.text.strip())
                    answers.append(f"{prob.order}{letters[index]}")
                except ValueError:
                    continue  # Nếu đáp án không phải A/B/C/D thì bỏ qua
    print("Answers:", answers)
    # Vẽ ảnh tô
    input_path = "/home/tuansangg/multisubject_oj/form.jpg"
    output_path = f"/home/tuansangg/multisubject_oj/media/output_exam_{exam_id}.jpg"
    draw_circles_on_form(answers, input_path, output_path)

    # Trả về template
    return render(request, 'exams/detail.html', {
        'exam': exam,
        'letters': letters,
        'answer_image': f"/media/output_exam_{exam_id}.jpg"
    })


@login_required
def add_exam_problem(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if exam.created_by != request.user:
        return HttpResponseForbidden("Bạn không có quyền thêm bài tập vào đề này.")

    if request.method == 'POST':
        form = ExamProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.exam = exam
            problem.save()

            if problem.problem_type == 'multiple_choice':
                # Duyệt qua A → D
                for label in ['A', 'B', 'C', 'D']:
                    choice_text = request.POST.get(f'choice_{label}', '').strip()
                    is_correct = request.POST.get(f'correct_{label}') == 'on'

                    if choice_text:  # nếu có nhập nội dung
                        ExamChoice.objects.create(
                            problem=problem,
                            text=choice_text,
                            is_correct=is_correct
                        )

            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = ExamProblemForm()

    return render(request, 'exams/add_exam_problem.html', {'form': form, 'exam': exam})


@require_POST
@login_required
def submit_mcq(request, problem_id):
    problem = get_object_or_404(ExamProblem, id=problem_id)

    if problem.problem_type != 'multiple_choice':
        return HttpResponseForbidden("Bài tập này không phải dạng trắc nghiệm.")

    selected_choice_id = request.POST.get('answer')
    if not selected_choice_id:
        # ✅ Redirect về lại exam kèm thông báo lỗi bằng messages (nếu cần)
        return redirect('exam_detail', exam_id=problem.exam.id)

    selected_choice = get_object_or_404(ExamChoice, id=selected_choice_id)

    # TODO: Lưu kết quả nếu cần

    return redirect('exam_detail', exam_id=problem.exam.id)

def draw_answer_sheet(exam_id, answers):
    # Đường dẫn ảnh gốc (phiếu trắng)
    base_image_path = "/home/tuansangg/multisubject_oj/form.jpg"
    image = Image.open(base_image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Điểm gốc 1A
    x0, y0 = 267, 1286
    dx = 98  # khoảng cách giữa A/B/C/D
    dy = 60  # khoảng cách giữa các câu

    # Tô tròn tại mỗi đáp án đã chọn
    for ans in answers:
        try:
            q_num = int(ans[:-1])  # ví dụ "3C" -> 3
            letter = ans[-1]       # "C"
            col = ['A', 'B', 'C', 'D'].index(letter)
            cx = x0 + col * dx
            cy = y0 + (q_num - 1) * dy
            r = 10  # bán kính ~0.5cm
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill='black')
        except:
            continue

    # Lưu ảnh kết quả
    output_path = f"/home/tuansangg/multisubject_oj/media/output_exam_{exam_id}.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)

    return f"/media/output_exam_{exam_id}.jpg"