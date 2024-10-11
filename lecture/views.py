from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView

class LectureView(TemplateView):
    template_name = "lecture.html"

