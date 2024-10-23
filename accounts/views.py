from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView

class LoginView(TemplateView):
    template_name = "registration/login.html"

class SignUpView(TemplateView):
    template_name = "registration/sign_up.html"

class LogoutView(RedirectView):
    template_name = "registration/logged_out.html"

class ProfileView(TemplateView):
    template_name = "registration/profile.html"
