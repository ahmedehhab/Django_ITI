from django.shortcuts import render, redirect
from .models import Student, Feedback


def home(request):
    return render(request, "school/home.html")


def students(request):

    if request.method == "POST":
        name = request.POST['name']
        age = request.POST['age']
        email = request.POST['email']
        image = request.FILES['image']

        Student.objects.create(
            name=name,
            age=age,
            email=email,
            image=image
        )

        return redirect("students")

    return render(request, "school/students.html")


def students_list(request):
    students = Student.objects.all()
    return render(request, "school/students_list.html",
                  {"students": students})


def delete_students(request):
    Student.objects.all().delete()
    return redirect("students")


def contact(request):

    if request.method == "POST":
        email = request.POST['email']
        message = request.POST['message']
        date = request.POST['date']

        Feedback.objects.create(
            email=email,
            message=message,
            date_added=date
        )

        return redirect("contact")

    return render(request, "school/contact.html")