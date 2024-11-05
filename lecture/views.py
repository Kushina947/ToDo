from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Course
from .forms import CourseForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class Lecture_addView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "lecture/lecture_add.html"
    success_url = reverse_lazy('lecture_list')

    def form_valid(self, form):
        return super().form_valid(form)


class LectureView(ListView): 
    model = Course
    template_name = "lecture/lecture.html"
    context_object_name = 'courses'