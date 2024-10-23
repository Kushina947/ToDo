from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView

class ThreadView(TemplateView):
    template_name = "thread.html"