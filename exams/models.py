from django.db import models
from django.conf import settings
from problems.models import Problem

class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    problems = models.ManyToManyField(
        "problems.Problem",
        through="exams.ExamProblem",
        related_name="exams"
    )

    def __str__(self):
        return self.title


class ExamProblem(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="exam_problems")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, blank=True)
    problem_type = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.problem:
            return f"{self.exam.title} - {self.problem.title}"
        return f"{self.exam.title} - [Chưa có Problem]"


class ExamChoice(models.Model):
    problem = models.ForeignKey(ExamProblem, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
