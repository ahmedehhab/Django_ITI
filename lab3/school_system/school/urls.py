from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students-v2', views.StudentViewSet, basename='student-viewset')
router.register(r'subjects-v2', views.SubjectViewSet, basename='subject-viewset')
router.register(r'grades-v2', views.GradeViewSet, basename='grade-viewset')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),  
    path('students/create/', views.create_student, name='create_student'),
    path('students/all/', views.get_all_students, name='get_all_students'),
    path('students/<int:student_id>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('subjects/create/', views.create_subject, name='create_subject'),
    path('subjects/all/', views.get_all_subjects, name='get_all_subjects'),
    path('subjects/<int:subject_id>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('grades/create/', views.create_grade, name='create_grade'),
    path('grades/all/', views.get_all_grades, name='get_all_grades'),
    path('grades/<int:grade_id>/', views.GradeDetailView.as_view(), name='grade_detail'),    
    path('', include(router.urls)),
]

