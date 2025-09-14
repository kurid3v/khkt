from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

SUBJECT_CHOICES = [
    ('TOAN', 'Toán'),
    ('LY', 'Vật Lý'),
    ('HOA', 'Hóa Học'),
    ('SINH', 'Sinh Học'),
    ('VAN', 'Ngữ Văn'),
    ('ANH', 'Tiếng Anh'),
    ('TIN', 'Tin Học'),
]

QUESTION_TYPE = [
    ('CODE', 'Lập trình'),
    ('MCQ', 'Trắc nghiệm'),
    ('WRIT', 'Tự luận'),
]

DIFFICULTY_LEVELS = [
    ('one', '1'),
    ('two', '2'),
    ('three', '3'),
    ('four', '4'),
    ('five', '5'),
    ('six', '6'),
    ('seven', '7'),
    ('eight', '8'),
    ('nine', '9'),
    ('ten', '10'),
    ('eleven', '11'),
    ('twelve', '12'),
]

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=10, choices=SUBJECT_CHOICES)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE, default='WRIT')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grading_criteria = models.TextField(null=True, blank=True, help_text="Tiêu chí chấm bài (dành cho AI)")
    created_at = models.DateTimeField(default=timezone.now)
    # Thêm trường mới để ẩn/hiện bài tập
    is_hidden = models.BooleanField(default=False)

    choice_a = models.CharField(max_length=255, null=True, blank=True)
    choice_b = models.CharField(max_length=255, null=True, blank=True)
    choice_c = models.CharField(max_length=255, null=True, blank=True)
    choice_d = models.CharField(max_length=255, null=True, blank=True)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        null=True, blank=True,
        help_text="Chỉ áp dụng cho câu hỏi trắc nghiệm"
    )

    def __str__(self):
        return self.title
