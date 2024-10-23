from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from accounts.models import CustomUser, User_Assignment
from assignment.models import Assignment
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "base/home.html"

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['user_assignments'] = User_Assignment.objects.filter(user=self.request.user)
        ctx['courses'] = CustomUser.objects.get(id=self.request.user.id).courses.all()
        ctx['user'] = self.request.user
        return ctx
