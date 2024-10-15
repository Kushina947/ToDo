from django.db import models


class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    lecture_schedule = models.CharField(max_length=100)

    def __str__(self):
        return self.name