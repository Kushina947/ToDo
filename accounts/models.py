from django.db import models
from django.contrib.auth.models import AbstractUser
from assignment.models import Assignment
from lecture.models import Course


class CustomUser(AbstractUser):
    icon = models.ImageField(upload_to='icon/', null=True, blank=True)
    courses = models.ManyToManyField(Course, related_name='students', blank=True)

    def __str__(self):
        return self.username

class User_Assignment(models.model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
