from django.db import models
from django.conf import settings

class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ thêm dòng này

    def __str__(self):
        return self.title

class ExamProblem(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_problems')
    question_text = models.TextField()
    problem_type = models.CharField(max_length=20, choices=[('multiple_choice', 'Trắc nghiệm'), ('essay', 'Tự luận')])
    order = models.IntegerField(default=0)

class ExamChoice(models.Model):
    problem = models.ForeignKey(ExamProblem, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
