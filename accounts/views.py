from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView

class LoginView(TemplateView):
    template_name = "registration/login.html"

class SignUpView(TemplateView):
    template_name = "registration/sign_up.html"