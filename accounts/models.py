from django.db import models
from django.contrib.auth.models import AbstractUser
from assignment.models import Assignment
from lecture.models import Course


class CustomUser(AbstractUser):
    icon = models.ImageField(upload_to='icon/', null=True, blank=True, default='images/default_icon.png')
    courses = models.ManyToManyField(Course, related_name='students', blank=True)
    first_name = None
    last_name = None

    def __str__(self):
        return self.username

class User_Assignment(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user_assignment', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='user_assignment', on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
