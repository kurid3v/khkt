from django.urls import path
from . import views
from .views import submit_solution, submission_list, view_result, submissions_by_problem, problem_ranking, update_submission_score

urlpatterns = [
    path('', submission_list, name='submission_list'),
    path('submit/<int:problem_id>/', submit_solution, name='submit_solution'),
    path('result/<int:submission_id>/', view_result, name='view_result'),
    path('problem/<int:problem_id>/', submissions_by_problem, name='submissions_by_problem'),
    path('ranking/<int:problem_id>/', problem_ranking, name='problem_ranking'),
    path('<int:submission_id>/update_score/', update_submission_score, name='update_submission_score'),
]
