from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Course
from .forms import CourseAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from assignment.models import Assignment
from thread.models import Post


class LectureView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "lecture/lecture.html"
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['assignments'] = Assignment.objects.filter(course=self.object)
        ctx['threads'] = Post.objects.filter(course=self.object)
        return ctx