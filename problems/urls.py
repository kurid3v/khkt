from django.urls import path
from . import views

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('add/', views.add_problem, name='add_problem'),
    path('<int:pk>/', views.problem_detail, name='problem_detail'),
    path('problem/<int:problem_id>/', views.submissions_by_problem, name='submissions_by_problem'),
    path('<int:pk>/toggle_visibility/', views.toggle_problem_visibility, name='toggle_problem_visibility'),
]
