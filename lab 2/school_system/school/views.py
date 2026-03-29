from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import EmployeeSignupForm, EmployeeLoginForm, StudentForm, SubjectForm, GradeForm
from .models import Student, Subject, Grade

@login_required
def home(request):
    return render(request, "school/home.html")

@login_required
def students_list(request):
    students = Student.objects.all()
    return render(request, "school/students_list.html", {"students": students})

@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("students_list")
    else:
        form = StudentForm()
    return render(request, "school/student_form.html", {"form": form, "title": "Create Student", "btn_text": "Create"})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("students_list")
    else:
        form = StudentForm(instance=student)
    return render(request, "school/student_form.html", {"form": form, "title": "Edit Student", "btn_text": "Update"})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect("students_list")
    return render(request, "school/confirm_delete.html", {"object": student, "type_name": "Student"})

@login_required
def subjects_list(request):
    subjects = Subject.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        subjects = subjects.filter(Q(name__icontains=search_query) | Q(code__icontains=search_query))
    
    return render(request, "school/subjects_list.html", {"subjects": subjects, "search_query": search_query})

@login_required
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subjects_list")
    else:
        form = SubjectForm()
    return render(request, "school/subject_form.html", {"form": form, "title": "Create Subject", "btn_text": "Create"})

@login_required
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("subjects_list")
    else:
        form = SubjectForm(instance=subject)
    return render(request, "school/subject_form.html", {"form": form, "title": "Edit Subject", "btn_text": "Update"})

@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
        return redirect("subjects_list")
    return render(request, "school/confirm_delete.html", {"object": subject, "type_name": "Subject"})

@login_required
def grades_list(request):
    grades = Grade.objects.select_related("student", "subject").all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        grades = grades.filter(student__name__icontains=search_query)
    
    return render(request, "school/grades_list.html", {"grades": grades, "search_query": search_query})

@login_required
def grade_create(request):
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("grades_list")
    else:
        form = GradeForm()
    return render(request, "school/grade_form.html", {"form": form, "title": "Create Grade", "btn_text": "Create"})

@login_required
def grade_update(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect("grades_list")
    else:
        form = GradeForm(instance=grade)
    return render(request, "school/grade_form.html", {"form": form, "title": "Edit Grade", "btn_text": "Update"})

@login_required
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == "POST":
        grade.delete()
        return redirect("grades_list")
    return render(request, "school/confirm_delete.html", {"object": grade, "type_name": "Grade"})

def signup_view(request):
    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = EmployeeSignupForm()

    return render(request, 'school/auth_form.html', {
        'form': form, 
        'title': 'Create Account', 
        'btn_text': 'Register'
    })

def login_view(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = EmployeeLoginForm(request)

    return render(request, 'school/auth_form.html', {
        'form': form, 
        'title': 'Login', 
        'btn_text': 'Login'
    })

def logout_view(request):
    logout(request)
    return redirect('login')