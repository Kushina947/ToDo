from .form import CustomAuthenticationForm
from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = CustomAuthenticationForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class SignUpView(TemplateView):
    template_name = "registration/sign_up.html"

class CustomLogoutView(LogoutView):
    template_name = "registration/logged_out.html"

class ProfileView(TemplateView):
    template_name = "registration/profile.html"
