# exams/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('add/', views.add_exam, name='add_exam'),
    path('<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('<int:exam_id>/add-problem/', views.add_exam_problem, name='add_exam_problem'),
    path('problem/<int:problem_id>/submit-mcq/', views.submit_mcq, name='submit_mcq'),
    path('enroll/<int:exam_id>/', views.enroll_in_exam, name='enroll_in_exam'),
    path('exam/<int:exam_id>/leave/', views.leave_exam, name='leave_exam'),
]
