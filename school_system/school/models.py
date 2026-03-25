from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    image = models.ImageField(upload_to="students/")

    def __str__(self):
        return self.name


class Feedback(models.Model):
    email = models.EmailField()
    message = models.TextField()
    date_added = models.DateField()

    def __str__(self):
        return self.email