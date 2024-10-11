from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView

class AssignmentView(TemplateView):
    template_name = "assignment/assignment.html"

class Assignment_addView(TemplateView):
    template_name = "assignment/assignment_add.html"
