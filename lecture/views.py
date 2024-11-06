from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Course
from .forms import CourseAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse

class Lecture_addView(LoginRequiredMixin, FormView):
    template_name = "lecture/lecture_add.html"
    form_class = CourseAddForm
    success_url = reverse_lazy('lecture_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        search_code = self.request.GET.get('search_code')
        form.search_courses(search_code)
        return form

    def form_valid(self, form):
        user = self.request.user
        selected_courses = form.cleaned_data['courses']
        user.courses.add(*selected_courses)
        return super().form_valid(form)


class LectureView(ListView):
    model = Course
    template_name = "lecture/lecture.html"
    context_object_name = 'courses'

def get_course_details(request):
    course_ids_str = request.GET.get('course_ids')
    if not course_ids_str:
        return JsonResponse({})

    course_ids = course_ids_str.split(',')
    courses = Course.objects.filter(id__in=course_ids).values()
    course_data = {str(course['id']): course for course in courses}

    return JsonResponse(course_data)

class LectureDetailView(DetailView):
    