from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('students/', views.students, name="students"),
    path('students/list/', views.students_list, name="students_list"),
    path('students/delete/', views.delete_students, name="delete_students"),
    path('contact/', views.contact, name="contact"),
]