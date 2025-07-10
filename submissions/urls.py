from django.urls import path
from . import views
from .views import submit_solution, submission_list, view_result


urlpatterns = [
    path('', submission_list, name='submission_list'),
    path('submit/<int:problem_id>/', submit_solution, name='submit_solution'),
    path('result/<int:submission_id>/', view_result, name='view_result'),  # ✅ Thêm dòng này
    path('problem/<int:problem_id>/', views.submissions_by_problem, name='submissions_by_problem'),
    path('ranking/<int:problem_id>/', views.problem_ranking, name='problem_ranking'),
]
