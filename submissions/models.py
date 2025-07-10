from django.db import models
from django.contrib.auth import get_user_model
from problems.models import Problem
from django.conf import settings

User = get_user_model()

class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
